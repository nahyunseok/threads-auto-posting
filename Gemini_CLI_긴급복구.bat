@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo            Gemini CLI 긴급 복구 스크립트
echo ============================================================
echo.

echo 🔄 1단계: 모든 관련 프로세스 종료 중...
wmic process where "commandline like '%%gemini%%'" delete 2>nul
if %errorlevel%==0 (
    echo ✅ 프로세스 종료 완료
) else (
    echo ⚠️  실행 중인 프로세스가 없거나 이미 종료됨
)
echo.

echo 📦 2단계: 필수 패키지 재설치 중...
echo    - Gemini CLI 설치...
call npm install -g @google/gemini-cli
echo    - Filesystem 서버 설치...
call npm install -g @modelcontextprotocol/server-filesystem@latest
echo    - Shell 서버들 설치...
call npm install -g @mkusaka/mcp-shell-server
call npm install -g shell-command-mcp
echo ✅ 패키지 설치 완료
echo.

echo 🔧 3단계: MCP 서버 구성 중...
echo    - Filesystem 서버 추가...
call gemini mcp add filesystem npx @modelcontextprotocol/server-filesystem "C:\Users\user\Claude-Workspace"
echo    - Shell 서버 (보안 설정) 추가...
set ALLOWED_COMMANDS=python,py,dir,type,echo,cd,ls,cat,pwd,python3,pip,npm,node,git
call gemini mcp add shell-secure npx shell-command-mcp
echo    - Shell 서버 (전체 권한) 추가...
set ALLOWED_COMMANDS=all
call gemini mcp add shell-all npx @mkusaka/mcp-shell-server
echo    - 기타 서버들 추가...
call gemini mcp add context7 npx @upstash/context7-mcp
call gemini mcp add playwright-browser npx @playwright/mcp
call gemini mcp add memory-bank npx @modelcontextprotocol/server-memory
echo ✅ MCP 서버 구성 완료
echo.

echo 📊 4단계: 상태 확인...
call gemini mcp list
echo.

echo ============================================================
echo ✅ 복구 완료!
echo.
echo 📝 다음 단계:
echo    1. 새로운 터미널을 열어주세요
echo    2. 'gemini' 명령어로 실행하거나
echo    3. 'start_gemini_with_shell.bat' 파일을 실행하세요 (권장)
echo    4. API 503 오류가 나오면 1-2분 기다린 후 재시도하세요
echo.
echo 💡 참고사항:
echo    - 올바른 도구명: read_multiple_files (read_many_files 아님)
echo    - Shell 명령어 실행 도구들이 보안 설정과 함께 추가되었습니다
echo    - Python 스크립트 실행이 가능합니다
echo    - 모든 설정이 초기화되었습니다
echo    - start_gemini_with_shell.bat 사용을 권장합니다
echo ============================================================
echo.
pause