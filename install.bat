@echo off
setlocal enabledelayedexpansion

REM ============================
REM  Carlsberg Koprivnica - Setup
REM ============================

REM ---- CONFIG (promijeni po potrebi) ----
set DB_NAME=PROJEKT
set DB_HOST=localhost
set DB_PORT=5432
set DB_ADMIN_USER=postgres

REM OVO je password od postgres usera (tvoj je trenutno 123)
set DB_ADMIN_PASSWORD=123

REM Opcionalno: ako imas seed komandu, postavi na 1
set RUN_SEED=1
set SEED_COMMAND=seed_carlsberg

echo.
echo [1/6] Provjera venv...
if not exist ".venv" (
    echo Kreiram .venv...
    python -m venv .venv
)

echo.
echo [2/6] Aktiviram venv...
call .\.venv\Scripts\activate

echo.
echo [3/6] Instaliram dependencies...
python -m pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt ne postoji! Kreiram minimalno...
    pip install django psycopg[binary]
)
echo.
echo Provjeravam psql...
where psql >nul 2>nul
if errorlevel 1 (
    echo ERROR: psql nije u PATH-u.
    echo Rjesenje: dodaj PostgreSQL bin u PATH (npr. C:\Program Files\PostgreSQL\16\bin)
    echo ili pokreni install.bat iz "x64 Native Tools Command Prompt" gdje je PATH postavljen.
    pause
    exit /b 1
)

echo.
echo [4/6] Kreiram bazu ako ne postoji...
set PGPASSWORD=%DB_ADMIN_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_ADMIN_USER% -tc "SELECT 1 FROM pg_database WHERE datname='%DB_NAME%';" | findstr /c:"1" >nul
if errorlevel 1 (
    echo Baza %DB_NAME% ne postoji. Kreiram...
    psql -h %DB_HOST% -p %DB_PORT% -U %DB_ADMIN_USER% -c "CREATE DATABASE \"%DB_NAME%\";"
) else (
    echo Baza %DB_NAME% vec postoji.
)

echo.
echo [5/6] Migracije...
python manage.py migrate

if "%RUN_SEED%"=="1" (
    echo.
    echo [5.1] Seed demo podataka...
    python manage.py %SEED_COMMAND%
)

echo.
echo [6/6] Pokrecem server...
echo Otvori: http://127.0.0.1:8000/
python manage.py runserver

endlocal
