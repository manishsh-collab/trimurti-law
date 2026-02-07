@echo off
REM ============================================================================
REM Legal Case AI - Metadata Extraction System
REM Batch file to automate case extraction with one launch
REM ============================================================================

setlocal enabledelayedexpansion

REM Set working directory to script location
cd /d "%~dp0"

REM Check if Python is available
where py >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python and try again.
    pause
    exit /b 1
)

REM Check command line arguments
if "%1"=="" goto :menu
if /i "%1"=="demo" goto :demo
if /i "%1"=="extract" goto :extract
if /i "%1"=="batch" goto :batch
if /i "%1"=="config" goto :config
if /i "%1"=="load-model" goto :load_model_arg
goto :extract_file

:menu
echo.
echo  +====================================================================+
echo  ^|         LEGAL CASE AI - Metadata Extraction System            ^|
echo  ^|         Enterprise Edition v1.1.0                               ^|
echo  +====================================================================+
echo.
echo  Usage: run.bat [command] [options]
echo.
echo  Commands:
echo    demo              Run demonstration extraction
echo    extract ^<file^>    Extract metadata from a single case file
echo    batch ^<folder^>    Process all .txt files in a folder
echo    load-model        Load a custom trained model (e.g. from Cloud)
echo    config            Show current configuration
echo.
echo  Examples:
echo    run.bat demo
echo    run.bat load-model path/to/model.zip
echo.
echo  Enter command (e.g., 'demo') or press Enter to run demo:
set /p user_cmd=^> 
if "%user_cmd%"=="" goto :demo
if "%user_cmd%"=="demo" goto :demo
if "%user_cmd%"=="load-model" goto :load_model_prompt
call run.bat %user_cmd%
goto :eof

:load_model_prompt
echo.
echo Enter path to model zip or folder:
set /p model_path=^> 
py cli.py set-model "%model_path%"
goto :end

:demo
echo.
echo [INFO] Running demo extraction...
echo.
py cli.py demo
goto :end

:extract
if "%2"=="" (
    echo [ERROR] Please specify a file to extract.
    echo Usage: run.bat extract ^<filename.txt^>
    goto :end
)
echo.
echo [INFO] Extracting metadata from: %2
echo.
py cli.py extract "%2" --show-confidence
goto :end

:extract_file
echo.
echo [INFO] Extracting metadata from: %1
echo.
py cli.py extract "%1" --show-confidence
goto :end

:batch
if "%2"=="" (
    echo [ERROR] Please specify a folder to process.
    echo Usage: run.bat batch ^<folder_path^>
    goto :end
)
echo.
echo [INFO] Batch processing folder: %2
echo.
py cli.py batch "%2" --output processed
goto :end

:config
echo.
echo [INFO] Current configuration:
echo.
py cli.py config
goto :end

:load_model_arg
if "%2"=="" (
    echo [ERROR] Please specify model path.
    echo Usage: run.bat load-model ^<path/to/zip^>
    goto :end
)
py cli.py set-model "%2"
goto :end

:end
echo.
echo [INFO] Process complete.
pause
