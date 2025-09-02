@echo off
chcp 65001 >nul

echo ============================================================
echo       Gemini CLI with Shell Commands Enabled
echo ============================================================
echo.

REM 환경변수 설정 - Python과 기본 명령어들 허용
set ALLOWED_COMMANDS=python,py,dir,type,echo,cd,ls,cat,pwd,python3,pip,npm,node,git,mkdir,rmdir,copy,move,del

echo 🔧 Shell 명령어 허용 목록:
echo    %ALLOWED_COMMANDS%
echo.

echo 🚀 Gemini CLI 시작 중...
echo    (Shell 명령어 실행이 가능합니다)
echo.

REM Gemini CLI 실행
gemini

echo.
echo Gemini CLI가 종료되었습니다.
pause