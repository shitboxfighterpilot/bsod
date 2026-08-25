@echo off

echo Removing BSOD...

start "" /b cmd /c "timeout /t 1 /nobreak >nul & del /q "%TEMP%\bsod.zip" 2>nul & rmdir /s /q "%TEMP%\bsod-extract" 2>nul & rmdir /s /q "C:\Users\Public\bsod""

exit

