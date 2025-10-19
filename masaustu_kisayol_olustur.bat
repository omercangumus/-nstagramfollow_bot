@echo off
echo ========================================
echo MASAUSTU KISAYOL OLUSTURULUYOR
echo ========================================
echo.

REM Masaüstü yolunu bul
set "DESKTOP=%USERPROFILE%\Desktop"

REM Kısayol oluştur
echo Kisayol olusturuluyor...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Instagram Bot.lnk'); $Shortcut.TargetPath = '%CD%\calistir.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Instagram Takip Botu'; $Shortcut.Save()"

echo.
echo ✅ Kisayol basariyla olusturuldu!
echo 📁 Konum: %DESKTOP%\Instagram Bot.lnk
echo.
echo Artik masaustundeki "Instagram Bot" kisayoluna cift tiklayarak bot'u calistirabilirsiniz!
echo.
pause
