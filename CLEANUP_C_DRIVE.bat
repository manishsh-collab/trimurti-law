@echo off
echo ============================================
echo    TRIMURTI LAW - C: DRIVE CLEANUP SCRIPT
echo ============================================
echo.

echo [1/7] Cleaning User Temp folder...
del /q/f/s "%TEMP%\*" 2>nul
rd /s /q "%TEMP%\*" 2>nul

echo [2/7] Cleaning Windows Temp folder...
del /q/f/s "C:\Windows\Temp\*" 2>nul

echo [3/7] Cleaning Python pip cache...
python -m pip cache purge 2>nul

echo [4/7] Cleaning npm cache...
npm cache clean --force 2>nul

echo [5/7] Cleaning Windows Prefetch...
del /q/f "C:\Windows\Prefetch\*" 2>nul

echo [6/7] Cleaning Thumbnail Cache...
del /q/f/s "%LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db" 2>nul

echo [7/7] Emptying Recycle Bin...
PowerShell -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"

echo.
echo ============================================
echo    CLEANUP COMPLETE!
echo ============================================
echo.
echo Additional steps to free more space:
echo 1. Run "cleanmgr" (Disk Cleanup) as Administrator
echo 2. Delete old Windows Update files in Settings ^> System ^> Storage
echo 3. Move your Trimurti LAW project to D: drive
echo.
pause
