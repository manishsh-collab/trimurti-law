@echo off
echo ============================================
echo    OPENING GOOGLE COLAB FOR YOU
echo ============================================
echo.
echo 1. Your browser will open Google Colab
echo 2. Sign in with your Google account if needed
echo 3. Click File -> Upload Notebook
echo 4. Select: Trimurti_LAW_Cloud_Training.ipynb
echo.
start https://colab.research.google.com/#create=true
echo.
echo Opening your file location...
explorer "%~dp0"
echo.
echo The notebook file is: Trimurti_LAW_Cloud_Training.ipynb
echo Just drag and drop it into Colab!
echo.
pause
