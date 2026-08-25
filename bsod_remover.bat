@echo off

echo Removing BSOD...

set "TARGET=C:\Users\Public\bsod"
set "CLEANUP=%TEMP%\bsod_cleanup.bat"

(
    echo @echo off
    echo timeout /t 1 /nobreak ^>nul
    echo del /q "%%TEMP%%\bsod.zip" 2^>nul
    echo rmdir /s /q "%%TEMP%%\bsod-extract" 2^>nul
    echo rmdir /s /q "%TARGET%"
    echo del /q "%%~f0" 2^>nul
) > "%CLEANUP%"

start "" /b "%CLEANUP%"

exit