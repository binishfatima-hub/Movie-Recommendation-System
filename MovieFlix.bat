@echo off
title MovieFlix - AI Movie Recommendation System
color 0F

REM Always run from the folder this file sits in, even if launched elsewhere.
cd /d "%~dp0"

echo.
echo  ===================================================
echo    MovieFlix - AI Movie Recommendation System
echo  ===================================================
echo.


REM ---------------------------------------------------------------
REM  1. Find a working Python
REM ---------------------------------------------------------------
set "PY="

python --version >nul 2>&1
if not errorlevel 1 set "PY=python"
if defined PY goto foundpython

py --version >nul 2>&1
if not errorlevel 1 set "PY=py"
if defined PY goto foundpython

goto nopython

:foundpython
for /f "tokens=*" %%v in ('%PY% --version 2^>^&1') do set "PYVER=%%v"
echo  [1/3] Using %PYVER%


REM ---------------------------------------------------------------
REM  2. Make sure the libraries are installed
REM ---------------------------------------------------------------
%PY% -c "import flask, pandas, sklearn" >nul 2>&1
if errorlevel 1 goto installdeps

echo  [2/3] Libraries OK
goto checkdata

:installdeps
echo  [2/3] Installing libraries, this happens only once...
echo.
%PY% -m pip install -r requirements.txt
if errorlevel 1 goto pipfailed
echo.
echo        Libraries installed.


REM ---------------------------------------------------------------
REM  3. Make sure the movie dataset exists
REM ---------------------------------------------------------------
:checkdata
if exist "dataset\movies.csv" goto startapp

echo  [3/3] Movie dataset missing, building it now...
echo        (downloads posters and trailers, needs internet)
echo.
%PY% tools\build_dataset.py
if errorlevel 1 goto buildfailed
goto startapp


REM ---------------------------------------------------------------
REM  Run it
REM ---------------------------------------------------------------
:startapp

REM If something is already listening on 5000, MovieFlix is likely
REM running in another window. Just open the browser instead.
netstat -ano | findstr /R /C:"LISTENING" | findstr /C:":5000 " >nul 2>&1
if not errorlevel 1 goto alreadyrunning

echo  [3/3] Starting server...
echo.
echo  ---------------------------------------------------
echo    The website opens in your browser automatically.
echo    If it does not, go to:  http://127.0.0.1:5000
echo.
echo    Keep this window open while using MovieFlix.
echo    Press CTRL+C here to stop the server.
echo  ---------------------------------------------------
echo.

%PY% app.py

echo.
echo  Server stopped. You can close this window.
goto end


:alreadyrunning
echo  [3/3] MovieFlix is already running in another window.
echo.
echo        Opening http://127.0.0.1:5000 in your browser...
start "" "http://127.0.0.1:5000"
goto end


REM ---------------------------------------------------------------
REM  Error messages
REM ---------------------------------------------------------------
:nopython
echo  ERROR: Python is not installed, or not on your PATH.
echo.
echo  Install it from https://www.python.org/downloads/
echo  and tick "Add Python to PATH" during setup.
goto end

:pipfailed
echo.
echo  ERROR: Could not install the libraries.
echo  Check your internet connection and try again, or run:
echo      pip install -r requirements.txt
goto end

:buildfailed
echo.
echo  ERROR: Could not build the movie dataset.
echo  It needs an internet connection. Try again, or run:
echo      python tools\build_dataset.py
goto end

:end
echo.
pause
