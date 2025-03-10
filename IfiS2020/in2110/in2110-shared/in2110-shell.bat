@echo off

set IN2110_PATH=%CD%
setlocal
set IN2110_ENV=in2110-env

if exist %IN2110_ENV% (
	cmd /k "%IN2110_PATH%\%IN2110_ENV%\Scripts\activate.bat"
)