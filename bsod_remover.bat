@echo off
echo Removing BSOD files...
echo.

rmdir /s /q "C:\Users\Public\bsod"

del /q "%TEMP%\bsod.zip" 2>nul
rmdir /s /q "%TEMP%\bsod-extract" 2>nul

echo.
echo BSOD has been removed.
pause