@echo off

IF NOT EXIST venv (
 "C:\Program Files\Python310\python.exe" -m venv venv
) ELSE (
echo venv folder already exists, skipping creation...
)
call .\venv\Scripts\activate.bat

set PYTHON="venv\Scripts\Python.exe"
echo venv %PYTHON%