@echo off
rem FCB uninstaller — hapus shortcut, PATH, dan folder install.
setlocal
set "INSTDIR=%LOCALAPPDATA%\FCB"
set "NAME=FCB Clipboard"

echo hapus shortcut ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws=New-Object -COM WScript.Shell; foreach ($dir in @([IO.Path]::Combine($ws.SpecialFolders('Desktop'), '%NAME%.lnk'), [IO.Path]::Combine($ws.SpecialFolders('StartMenu'), 'Programs', '%NAME%.lnk'))) { if (Test-Path $dir) { Remove-Item $dir -Force; $dir } }"

echo hapus PATH ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$d='%INSTDIR%'; $p=[Environment]::GetEnvironmentVariable('Path','User'); $parts=$p -split ';' | Where-Object { $_.TrimEnd('\') -ine $d }; [Environment]::SetEnvironmentVariable('Path', ($parts -join ';'), 'User'); '  dibersihkan'"

echo hapus folder + diri sendiri ...
start /b "" cmd /c "ping -n 3 127.0.0.1 >nul & rd /s /q "%INSTDIR%" & echo terhapus"
endlocal
