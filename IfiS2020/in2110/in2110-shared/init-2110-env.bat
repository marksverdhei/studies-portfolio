@echo off

set IN2110_PATH=%CD%
setlocal
set IN2110_ENV=in2110-env

if not exist %IN2110_ENV% (
	python -m venv %IN2110_ENV%
)

@echo on
cmd /k "%IN2110_PATH%\%IN2110_ENV%\Scripts\activate.bat & pip install -U pip & pip install -r requirements.txt & pip install -e src & python download-nltk-data.py & deactivate & echo "" & echo IN2110 environment created. & echo Run './in2110-shell.bat' to launch environment."