@echo off
rem ============================================================
rem  FCB installer (Windows, portable) — tanpa admin.
rem  - Copy client ke %LOCALAPPDATA%\FCB
rem  - Daftarkan ke PATH user (ketik `fcc` dari mana saja*)
rem  - Shortcut Desktop + Start Menu (icon anime)
rem  *terminal baru setelah install. Uninstall: uninstall.bat
rem ============================================================
setlocal
set "SRC=%~dp0"
set "INSTDIR=%LOCALAPPDATA%\FCB"
set "NAME=FCB Clipboard"

echo [1/4] copy file ke %INSTDIR% ...
if not exist "%INSTDIR%" mkdir "%INSTDIR%"
copy /y "%SRC%fcc.py" "%INSTDIR%\" >nul
copy /y "%SRC%fcb.vbs" "%INSTDIR%\" >nul
copy /y "%SRC%icon.ico" "%INSTDIR%\" >nul
copy /y "%SRC%uninstall.bat" "%INSTDIR%\" >nul
if errorlevel 1 exit /b 1

echo [2/4] daftarkan PATH user ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$d='%INSTDIR%'; $p=[Environment]::GetEnvironmentVariable('Path','User'); $parts=$p -split ';' | ForEach-Object { $_.TrimEnd('\') }; if ($parts -icontains $d) { '  sudah ada, skip' } else { [Environment]::SetEnvironmentVariable('Path', ($p.TrimEnd(';') + ';' + $d), 'User'); '  ditambahkan' }"
if errorlevel 1 exit /b 1

echo [3/4] shortcut Desktop + Start Menu ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws=New-Object -COM WScript.Shell; foreach ($dir in @([IO.Path]::Combine($ws.SpecialFolders('Desktop'), '%NAME%.lnk'), [IO.Path]::Combine($ws.SpecialFolders('StartMenu'), 'Programs', '%NAME%.lnk'))) { $s=$ws.CreateShortcut($dir); $s.TargetPath='pythonw'; $s.Arguments='\"%INSTDIR%\fcc.py\"'; $s.WorkingDirectory='%INSTDIR%'; $s.IconLocation='%INSTDIR%\icon.ico'; $s.Save(); $dir }"
if errorlevel 1 exit /b 1

echo [4/4] cek pythonw ...
where pythonw >nul 2>&1
if errorlevel 1 (
  echo   PERINGATAN: pythonw tidak di PATH! Install Python 3.8+ dan
  echo   centang "Add python.exe to PATH" saat install, lalu install ulang.
  exit /b 1
)

echo.
echo SELESAI. Buka terminal BARU lalu ketik:  fcb
echo (ketik `fcb` = fcb.vbs di PATH; atau double-click shortcut Desktop)
endlocal
