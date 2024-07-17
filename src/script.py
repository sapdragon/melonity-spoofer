script = '''
@echo off

:Cleaner
set "steam=$steam"
set "guid=%~dp0"
set "file0=%~dp0"

del /A:H /F /S /Q "%steam%\\ssfn*"
del /F /S /Q "%steam%\\ssfn*"
rmdir /S /Q "%steam%\\appcache"
rmdir /S /Q "%steam%\\userdata"
rmdir /S /Q "%steam%\\logs"
rmdir /S /Q "%steam%\\config"
rmdir /S /Q "%steam%\\steamapps\\common\\dota 2 beta\\game\\core\\cfg"
rmdir /S /Q "%steam%\\steamapps\\common\\dota 2 beta\\game\\core\\config"
rmdir /S /Q "%steam%\\steamapps\\common\\dota 2 beta\\game\\dota\\cfg"
rmdir /S /Q "%USERPROFILE%\\AppData\\Local\\Steam"

reg delete "HKEY_CURRENT_USER\\SOFTWARE\\Valve" /f
reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Valve" /f
reg delete "HKEY_CLASSES_ROOT\\steam" /f
reg delete "HKEY_CLASSES_ROOT\\steamlink" /f
reg delete "HKEY_CURRENT_USER\\SOFTWARE\\Classes\\steam" /f
reg delete "HKEY_CURRENT_USER\\SOFTWARE\\Classes\\steamlink" /f
reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes\\steam" /f
reg delete "HKEY_LOCAL_MACHINE\\SOFTWARE\\Classes\\steamlink" /f
reg delete "HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Services\\EventLog\\Application\\Steam Client Service" /f
reg delete "HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Services\\Steam Client Service" /f
reg delete "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\EventLog\\Application\\Steam Client Service" /f
reg delete "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\Steam Client Service" /f

powershell -executionpolicy bypass -command "[guid]::NewGuid()" > %guid%\\1.txt

1>"%file0%\\2.txt" more +3 "%file0%\\1.txt"
move "%file0%\\2.txt" "%file0%\\1.txt"

set /p text=< %file0%\\1.txt
reg.exe add "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography" /v "MachineGuid" /t REG_SZ /d "%text%" /f
echo %text%
del "%~dp0\\1.txt"

 SETLOCAL ENABLEDELAYEDEXPANSION
 SETLOCAL ENABLEEXTENSIONS

 ::Generate and implement a random MAC address
 FOR /F "tokens=1" %%a IN ('wmic nic where physicaladapter^=true get deviceid ^| findstr [0-9]') DO (
 CALL :MAC
 FOR %%b IN (0 00 000) DO (
 REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002bE10318}\\%%b%%a >NUL 2>NUL && REG ADD HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002bE10318}\\%%b%%a /v NetworkAddress /t REG_SZ /d !MAC!  /f >NUL 2>NUL
 )
 )

 ::Disable power saving mode for network adapters
 FOR /F "tokens=1" %%a IN ('wmic nic where physicaladapter^=true get deviceid ^| findstr [0-9]') DO (
 FOR %%b IN (0 00 000) DO (
 REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002bE10318}\\%%b%%a >NUL 2>NUL && REG ADD HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002bE10318}\\%%b%%a /v PnPCapabilities /t REG_DWORD /d 24 /f >NUL 2>NUL
 )
 )

 ::Reset NIC adapters so the new MAC address is implemented and the power saving mode is disabled.
 FOR /F "tokens=2 delims=, skip=2" %%a IN ('"wmic nic where (netconnectionid like '%%') get netconnectionid,netconnectionstatus /format:csv"') DO (
 netsh interface set interface name="%%a" disable >NUL 2>NUL
 netsh interface set interface name="%%a" enable >NUL 2>NUL
 )

 GOTO :EOF
 :MAC
 ::Generates semi-random value of a length according to the "if !COUNT!"  line, minus one, and from the characters in the GEN variable
 SET COUNT=0
 SET GEN=ABCDEF0123456789
 SET GEN2=26AE
 SET MAC=
 :MACLOOP
 SET /a COUNT+=1
 SET RND=%random%
 ::%%n, where the value of n is the number of characters in the GEN variable minus one.  So if you have 15 characters in GEN, set the number as 14
 SET /A RND=RND%%16
 SET RNDGEN=!GEN:~%RND%,1!
 SET /A RND2=RND%%4
 SET RNDGEN2=!GEN2:~%RND2%,1!
 IF "!COUNT!"  EQU "2" (SET MAC=!MAC!!RNDGEN2!) ELSE (SET MAC=!MAC!!RNDGEN!)
 IF !COUNT!  LEQ 11 GOTO MACLOOP 
echo OK
'''