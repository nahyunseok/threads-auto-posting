@echo off
chcp 65001 >nul

echo ============================================================
echo       Gemini CLI - Unrestricted Shell Access
echo ============================================================
echo.

REM 모든 명령어 허용 (주의: 보안 위험 있음)
set ALLOWED_COMMANDS=all

echo ⚠️  경고: 모든 Shell 명령어가 허용됩니다
echo    보안에 주의하여 사용하세요
echo.

echo 🚀 Gemini CLI 시작 중...
echo.

REM Gemini CLI 실행
gemini

echo.
echo Gemini CLI가 종료되었습니다.
pause