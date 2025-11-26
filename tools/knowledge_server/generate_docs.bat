@echo off
REM Generate System Documentation from GitLab

echo =====================================
echo Generating System Documentation
echo =====================================
echo.

cd /d %~dp0\..\..

echo Using virtual environment...
if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe tools\knowledge_server\generate_docs.py --branch master --base-path Trunk/FrontierOM
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup_venv.bat first
    exit /b 1
)

echo.
echo =====================================
echo Documentation generation complete!
echo Output: tools\knowledge_server\docs\
echo =====================================
pause

