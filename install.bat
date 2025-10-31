@echo off
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install fastapi uvicorn python-multipart pydantic PyPDF2 sentence-transformers transformers torch numpy scikit-learn python-dotenv

echo.
echo Installation complete!
echo.
echo To run the application, use:
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Then open http://localhost:8000 in your browser
pause
