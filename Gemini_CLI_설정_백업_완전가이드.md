# Gemini CLI 설정 백업 및 복구 완전 가이드

## 📋 목차
1. [설치 및 초기 설정](#설치-및-초기-설정)
2. [MCP 서버 구성](#mcp-서버-구성)  
3. [문제 해결 가이드](#문제-해결-가이드)
4. [백업 및 복구 절차](#백업-및-복구-절차)

---

## 🚀 설치 및 초기 설정

### Gemini CLI 설치
```bash
npm install -g @google/gemini-cli
```

### 버전 확인
```bash
gemini --version
# 출력: 0.2.2
```

---

## 🔧 MCP 서버 구성

### 현재 작동하는 MCP 서버 목록

#### 1. Filesystem 서버 (파일 시스템 접근)
```bash
# 설치
npm install -g @modelcontextprotocol/server-filesystem@latest

# 추가
gemini mcp add filesystem npx @modelcontextprotocol/server-filesystem "C:\Users\user\Claude-Workspace"
```
**사용 가능한 도구:**
- `read_file` - 단일 파일 읽기
- `read_multiple_files` - 다중 파일 읽기 ⭐
- `write_file` - 파일 쓰기
- `list_directory` - 디렉토리 목록
- `search_files` - 파일 검색

#### 2. Shell 명령어 서버 (보안 설정 포함) ⭐
```bash
# 설치
npm install -g @mkusaka/mcp-shell-server
npm install -g shell-command-mcp

# 방법 1: 기본 명령어만 허용 (권장)
set ALLOWED_COMMANDS=python,py,dir,type,echo,cd,ls,cat,pwd,python3,pip,npm,node,git
gemini mcp add shell-secure npx shell-command-mcp

# 방법 2: 모든 명령어 허용 (주의: 보안 위험)
set ALLOWED_COMMANDS=all  
gemini mcp add shell-all npx @mkusaka/mcp-shell-server
```

**⚠️ 중요 사항:**
- Shell 서버는 기본적으로 모든 명령어가 차단됨 (`allowed_commands: (none)`)
- 환경변수 `ALLOWED_COMMANDS`를 반드시 설정해야 함
- Python 스크립트 실행을 위해서는 최소한 `python,py` 명령어 허용 필요

#### 4. Context7 서버
```bash
gemini mcp add context7 npx @upstash/context7-mcp
```

#### 5. Playwright 브라우저 서버
```bash
gemini mcp add playwright-browser npx @playwright/mcp
```

#### 6. Memory Bank 서버
```bash
gemini mcp add memory-bank npx @modelcontextprotocol/server-memory
```

### 완전한 설정 복원 스크립트 (업데이트됨)
```bash
# 1. 모든 MCP 서버 설치
npm install -g @google/gemini-cli
npm install -g @modelcontextprotocol/server-filesystem@latest
npm install -g @mkusaka/mcp-shell-server
npm install -g shell-command-mcp

# 2. MCP 서버 추가 (파일시스템)
gemini mcp add filesystem npx @modelcontextprotocol/server-filesystem "C:\Users\user\Claude-Workspace"

# 3. Shell 서버 추가 (환경변수와 함께)
set ALLOWED_COMMANDS=python,py,dir,type,echo,cd,ls,cat,pwd,python3,pip,npm,node,git
gemini mcp add shell-secure npx shell-command-mcp

set ALLOWED_COMMANDS=all
gemini mcp add shell-all npx @mkusaka/mcp-shell-server

# 4. 기타 서버 추가
gemini mcp add context7 npx @upstash/context7-mcp
gemini mcp add playwright-browser npx @playwright/mcp
gemini mcp add memory-bank npx @modelcontextprotocol/server-memory
```

---

## 🚀 전용 실행 스크립트 (권장)

환경변수 설정의 복잡성을 피하고 안전하게 Gemini CLI를 실행할 수 있는 전용 배치 파일들입니다.

### 1. 안전한 실행 스크립트
**파일:** `start_gemini_with_shell.bat`
```batch
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
```

### 2. 무제한 실행 스크립트 (주의 필요)
**파일:** `start_gemini_unrestricted.bat`
```batch
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
```

### 사용 방법
1. 해당 `.bat` 파일을 더블클릭하여 실행
2. 환경변수가 자동으로 설정됨
3. Gemini CLI가 Shell 명령어와 함께 시작됨
4. Python 스크립트 실행 가능

---

## 🛠️ 문제 해결 가이드

### 자주 발생하는 오류들

#### 1. "Tool not found in registry" 오류
**원인:** MCP 서버 연결 문제 또는 캐시 문제

**해결방법:**
```bash
# 1. 모든 Gemini CLI 프로세스 종료
wmic process where "commandline like '%gemini%' or commandline like '%@google/gemini-cli%'" delete

# 2. MCP 서버 재설치
gemini mcp remove filesystem
npm install -g @modelcontextprotocol/server-filesystem@latest
gemini mcp add filesystem npx @modelcontextprotocol/server-filesystem "C:\Users\user\Claude-Workspace"

# 3. 새로운 터미널에서 gemini 재시작
```

#### 2. "read_many_files tool not found" 오류
**원인:** 잘못된 도구 이름 사용

**해결방법:**
- ❌ `read_many_files` (잘못된 이름)
- ✅ `read_multiple_files` (올바른 이름)

#### 3. API 503 "Service Unavailable" 오류
**원인:** Google Gemini API 서버 과부하

**해결방법:**
```bash
# 1-3분 기다린 후 재시도
gemini

# 또는 다른 모델 사용
gemini -m gemini-1.5-flash
gemini -m gemini-pro
```

#### 4. 파일 접근 권한 오류
**원인:** 잘못된 경로 설정

**해결방법:**
```bash
# 올바른 워크스페이스 경로 설정
gemini mcp remove filesystem
gemini mcp add filesystem npx @modelcontextprotocol/server-filesystem "C:\Users\user\Claude-Workspace"
```

#### 5. Shell 명령어 실행 차단 오류
**원인:** `allowed_commands: (none)` - 모든 Shell 명령어가 차단된 상태

**증상:**
- "실행할 명령어를 허용하지 않습니다" 오류
- `echo` 명령어도 허용되지 않음
- 보안 설정에서 명령어가 없는 것으로 표시

**해결방법:**
```bash
# 1. 기존 shell 서버 제거
gemini mcp remove shell
gemini mcp remove shell-command

# 2. 허용된 명령어와 함께 재설정
set ALLOWED_COMMANDS=python,py,dir,type,echo,cd,ls,cat,pwd,python3,pip,npm,node,git
gemini mcp add shell-secure npx shell-command-mcp

# 3. 모든 명령어 허용 (테스트용)
set ALLOWED_COMMANDS=all
gemini mcp add shell-all npx @mkusaka/mcp-shell-server
```

---

## 💾 백업 및 복구 절차

### MCP 서버 상태 확인
```bash
gemini mcp list
```

**예상 출력:**
```
✓ filesystem: npx @modelcontextprotocol/server-filesystem C:\Users\user\Claude-Workspace (stdio) - Connected
✓ context7: npx @upstash/context7-mcp (stdio) - Connected  
✓ playwright-browser: npx @playwright/mcp (stdio) - Connected
✓ memory-bank: npx @modelcontextprotocol/server-memory (stdio) - Connected
✓ shell: npx @mkusaka/mcp-shell-server (stdio) - Connected
✓ shell-command: npx shell-command-mcp (stdio) - Connected
✗ obsidian-enhanced: 연결 해제 (사용안함)
```

### 완전 초기화 절차
```bash
# 1. 모든 MCP 서버 제거
gemini mcp remove filesystem
gemini mcp remove shell  
gemini mcp remove shell-command
gemini mcp remove context7
gemini mcp remove playwright-browser
gemini mcp remove memory-bank

# 2. Gemini CLI 프로세스 종료
wmic process where "commandline like '%gemini%'" delete

# 3. 위의 "완전한 설정 복원 스크립트" 실행
```

### 긴급 복구 스크립트
```bash
@echo off
echo Gemini CLI 긴급 복구 시작...

echo 1. 모든 관련 프로세스 종료...
wmic process where "commandline like '%%gemini%%'" delete 2>nul

echo 2. 필수 패키지 재설치...
npm install -g @google/gemini-cli
npm install -g @modelcontextprotocol/server-filesystem@latest  
npm install -g @mkusaka/mcp-shell-server
npm install -g shell-command-mcp

echo 3. MCP 서버 구성...
gemini mcp add filesystem npx @modelcontextprotocol/server-filesystem "C:\Users\user\Claude-Workspace"
gemini mcp add shell npx @mkusaka/mcp-shell-server
gemini mcp add shell-command npx shell-command-mcp

echo 4. 상태 확인...
gemini mcp list

echo 복구 완료! 새로운 터미널에서 'gemini'를 실행하세요.
pause
```

---

## 📊 성능 최적화 팁

### 1. 불필요한 MCP 서버 제거
```bash
# obsidian-enhanced 서버는 연결 문제가 있으므로 제거
gemini mcp remove obsidian-enhanced
```

### 2. 정기적인 캐시 정리
```bash
# 주기적으로 실행 (월 1회 권장)
wmic process where "commandline like '%gemini%'" delete
npm cache clean --force
```

### 3. 메모리 사용량 모니터링
```bash
# 메모리 사용량 표시 옵션
gemini --show-memory-usage
```

---

## 🔍 디버깅 도구

### 상세 로그 확인
```bash
gemini -d  # 디버그 모드
```

### 도움말 확인
```bash
gemini --help
gemini mcp --help
```

### 사용 가능한 확장 목록
```bash
gemini -l
```

---

## 📝 주요 명령어 요약

| 명령어 | 설명 |
|--------|------|
| `gemini` | 대화형 모드 시작 |
| `gemini --version` | 버전 확인 |
| `gemini mcp list` | MCP 서버 목록 |
| `gemini mcp add <name> <command>` | MCP 서버 추가 |
| `gemini mcp remove <name>` | MCP 서버 제거 |
| `gemini -m <model>` | 특정 모델 사용 |
| `gemini -d` | 디버그 모드 |

---

## ⚠️ 중요 사항

1. **도구 이름 주의**: `read_many_files` ❌ → `read_multiple_files` ✅
2. **Shell 명령어 보안**: 기본값은 `allowed_commands: (none)` - 반드시 환경변수 설정 필요
3. **워크스페이스 경로**: 반드시 정확한 경로 설정 필요  
4. **권장 실행 방법**: `start_gemini_with_shell.bat` 사용으로 복잡한 설정 회피
5. **API 한도**: 무료 사용량 한도 고려
6. **정기 백업**: 이 설정 파일을 정기적으로 백업
7. **보안**: 민감한 정보가 포함된 디렉토리 접근 주의
8. **무제한 모드 주의**: `ALLOWED_COMMANDS=all` 사용 시 보안 위험 존재

---

## 🔄 업데이트 이력

- **2025-09-02 v1.0**: 초기 문서 작성 및 완전한 설정 가이드 완성
  - Tool Registry 동기화 문제 해결 방법 추가
  - 모든 작동하는 MCP 서버 구성 정리
  
- **2025-09-02 v1.1**: Shell 명령어 보안 설정 완전 해결
  - `allowed_commands: (none)` 문제 해결 방법 추가
  - 환경변수 기반 Shell 서버 구성 가이드 작성
  - 전용 실행 스크립트 (`start_gemini_with_shell.bat`) 추가
  - 무제한 모드 스크립트 (`start_gemini_unrestricted.bat`) 추가
  - Shell 명령어 보안 모범 사례 문서화

---

**📧 문제 발생 시**: 이 가이드의 "문제 해결 가이드" 섹션을 먼저 확인하고, 그래도 해결되지 않으면 Gemini CLI 프로세스를 완전히 종료 후 재시작하세요.