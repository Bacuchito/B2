@echo off
chcp 65001 >nul
title Corrector DeepSeek (OpenCode Go) - deja esta ventana abierta
cd /d "%~dp0"

rem --- Python: primero el que trae el entorno, si no el del sistema ---
set "PY=C:\Users\sergi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
if not exist "%PY%" set "PY=python"

rem --- Clave: se guarda una vez en tools\.oc_key (no se sube al repo) ---
set "KEYFILE=%~dp0tools\.oc_key"
set "OC_KEY="
if exist "%KEYFILE%" set /p OC_KEY=<"%KEYFILE%"
if not "%OC_KEY%"=="" goto arrancar

echo.
echo Pega tu clave de OpenCode Go (empieza por oc_sk_ ) y pulsa Enter.
echo Solo hace falta la primera vez: se guarda en tools\.oc_key
echo.
set /p OC_KEY=Clave: 
if "%OC_KEY%"=="" goto sin_clave
>"%KEYFILE%" echo %OC_KEY%

:arrancar
echo.
echo ------------------------------------------------------------------
echo  Corrector DeepSeek escuchando en http://127.0.0.1:8787
echo  En la app: Endpoint http://127.0.0.1:8787 . Modelo deepseek-v4.1-flash
echo  CIERRA ESTA VENTANA para parar el proxy.
echo ------------------------------------------------------------------
echo.
"%PY%" "%~dp0tools\go-proxy.py"
echo.
echo El proxy se ha parado.
pause
exit /b 0

:sin_clave
echo No has escrito ninguna clave.
pause
exit /b 1
