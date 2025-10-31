"""QA Engine Module - Handles embeddings and question answering"""

from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import torch
from typing import List, Tuple, Dict
import re


class QAEngine:
    """Handles embeddings-based search and question answering"""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", 
                 qa_model: str = "distilbert-base-cased-distilled-squad"):
        """Initialize the QA engine with embedding and QA models"""
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Use a smaller QA model for faster inference
        self.qa_pipeline = pipeline(
            "question-answering",
            model=qa_model,
            device=0 if torch.cuda.is_available() else -1
        )
        
        self.text_chunks = []
        self.embeddings = None
    
    def add_documents(self, chunks: List[str]):
        """Add document chunks and compute their embeddings"""
        self.text_chunks.extend(chunks)
        self._compute_embeddings()
    
    def _compute_embeddings(self):
        """Compute embeddings for all text chunks"""
        self.embeddings = self.embedding_model.encode(
            self.text_chunks,
            convert_to_tensor=True,
            show_progress_bar=True
        )
    
    def search_similar_chunks(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Search for the most similar chunks to a query using embeddings"""
        if len(self.text_chunks) == 0:
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)
        
        # Compute similarity scores
        similarity_scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        
        # Get top-k results
        top_results = torch.topk(similarity_scores, k=min(top_k, len(self.text_chunks)))
        
        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            results.append((self.text_chunks[idx], float(score)))
        
        return results
    
    def answer_question(self, question: str, context: str, max_answer_length: int = 500) -> Dict:
        """Answer a question given a context using QA model"""
        try:
            # Validate context
            if not context or len(context.strip()) < 50:
                return {
                    'answer': 'Insufficient context to answer the question.',
                    'score': 0.0,
                    'start': 0,
                    'end': 0
                }
            
            # Use full context for comprehensive answers (QA model has token limits)
            max_context_length = 2048
            if len(context.split()) > max_context_length:
                context = " ".join(context.split()[:max_context_length])
            
            # Try to get a longer answer first
            try:
                result = self.qa_pipeline(
                    question=question,
                    context=context,
                    max_answer_len=max_answer_length
                )
                
                # Extract the answer
                answer = result['answer'].strip()
                score = float(result['score'])
                
                # If answer is too short or confidence is too low, try to get better answer
                if len(answer.split()) < 20 or score < 0.3:
                    # Try with different parameters for better extraction
                    result = self.qa_pipeline(
                        question=question,
                        context=context,
                        max_answer_len=max_answer_length,
                        top_k=1
                    )
                    answer = result['answer'].strip()
                    score = float(result['score'])
                    
            except Exception as qa_error:
                # If QA pipeline fails, use context-based fallback
                answer = self._generate_fallback_answer(context, question)
                score = 0.5
                result = {'start': 0, 'end': len(answer)}
            
            # Add context-aware enhancement
            enhanced_answer = self._enhance_answer(answer, context, question)
            
            return {
                'answer': enhanced_answer,
                'score': score,
                'start': result.get('start', 0),
                'end': result.get('end', len(enhanced_answer))
            }
        except Exception as e:
            return {
                'answer': 'Unable to generate answer from the provided context.',
                'score': 0.0,
                'start': 0,
                'end': 0,
                'error': str(e)
            }
    
    def _enhance_answer(self, answer: str, context: str, question: str) -> str:
        """Enhance answer with additional context for more detailed response"""
        # If answer is too short or incomplete, expand it significantly
        if len(answer.split()) < 100:
            # Find the answer in context and get surrounding sentences
            if answer in context:
                idx = context.find(answer)
                # Get more context before and after
                start = max(0, idx - 300)
                end = min(len(context), idx + len(answer) + 500)
                expanded = context[start:end].strip()
                
                # Extract multiple sentences for comprehensive answer
                sentences = expanded.split('. ')
                if len(sentences) > 2:
                    # Combine multiple sentences for better answer
                    answer = '. '.join(sentences[:5]) + '.'
                elif len(sentences) > 1:
                    answer = '. '.join(sentences) + '.'
            else:
                # If answer not found in context, use context directly
                # Split into sentences and take first few
                sentences = context.split('. ')
                if len(sentences) > 3:
                    answer = '. '.join(sentences[:4]) + '.'
                else:
                    answer = context
        
        # Ensure answer is substantial (at least 50 words)
        if len(answer.split()) < 50:
            # If still too short, prepend relevant context
            sentences = context.split('. ')
            answer = '. '.join(sentences[:3]) + '. ' + answer
        
        return answer
    
    def _generate_fallback_answer(self, context: str, question: str) -> str:
        """Generate answer using context when QA model fails"""
        # If QA model fails, use the first few sentences from context
        sentences = context.split('. ')
        
        if len(sentences) >= 4:
            # Take first 4 sentences
            answer = '. '.join(sentences[:4]) + '.'
        elif len(sentences) >= 2:
            # Take all available sentences
            answer = '. '.join(sentences) + '.'
        else:
            # Use entire context
            answer = context
        
        return answer
    
    def _is_valid_question(self, question: str) -> bool:
        """Validate if question is meaningful (not just symbols/gibberish)"""
        # Check if question is empty or too short
        if not question or len(question.strip()) < 3:
            return False
        
        # Count alphabetic characters
        alpha_count = sum(1 for c in question if c.isalpha())
        total_chars = len(question.strip())
        
        # At least 50% should be alphabetic characters (words, not symbols)
        if total_chars > 0 and alpha_count / total_chars < 0.5:
            return False
        
        # Check for at least one word (sequence of letters)
        import re
        words = re.findall(r'[a-zA-Z]+', question)
        if len(words) == 0:
            return False
        
        return True
    
    def process_query(self, question: str, top_k: int = 3) -> Dict:
        """
        Process a user query:
        1. Validate question
        2. Search for relevant chunks (max 3)
        3. Combine them as context
        4. Generate detailed answer
        """
        # Validate question first
        if not self._is_valid_question(question):
            return {
                'question': question,
                'answer': 'Please ask a meaningful question with actual words (not just symbols).',
                'relevant_chunks': [],
                'confidence': 0.0
            }
        
        if len(self.text_chunks) == 0:
            return {
                'question': question,
                'answer': 'No documents have been uploaded yet.',
                'relevant_chunks': [],
                'confidence': 0.0
            }
        
        # Limit to maximum 3 sources
        top_k = min(3, top_k)
        
        # Search for relevant chunks
        relevant_chunks = self.search_similar_chunks(question, top_k=top_k)
        
        if not relevant_chunks:
            return {
                'question': question,
                'answer': 'No relevant information found in the documents.',
                'relevant_chunks': [],
                'confidence': 0.0
            }
        
        # Combine top chunks as context for more detailed answer
        context = " ".join([chunk for chunk, _ in relevant_chunks])
        
        # Generate detailed answer
        answer_result = self.answer_question(question, context)
        
        return {
            'question': question,
            'answer': answer_result['answer'],
            'relevant_chunks': [
                {'text': chunk, 'similarity': score}
                for chunk, score in relevant_chunks
            ],
            'confidence': answer_result.get('score', 0.0)
        }
    
    def clear_documents(self):
        """Clear all stored documents and embeddings"""
        self.text_chunks = []
        self.embeddings = None
