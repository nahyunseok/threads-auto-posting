# 📱 Threads 자동 게시 완벽 가이드

## 🎉 시스템 완료 상태
- ✅ **토큰 문제 해결** (2025-08-25)
- ✅ **한국 시간 적용** 완료
- ✅ **모니터링 시스템** 추가
- ✅ **백업 게시 시스템** 구축

## ⏰ 자동 실행 스케줄

### 한국 시간 기준:
- 🌅 **06:00** - 아침 게시
- 🌞 **12:00** - 점심/오후 게시  
- 🌆 **18:00** - 저녁 게시
- 🌙 **00:00** - 밤 게시

### 실행 방식:
- **자동**: GitHub Actions 스케줄러
- **수동**: Actions 탭에서 "Run workflow"

## 🛠️ 문제 해결 가이드

### 1️⃣ "예약됨" 상태가 계속 나올 때

**원인:**
- GitHub Actions 서버가 바쁨
- 다른 워크플로우와 충돌
- 리소스 부족

**해결책:**
```bash
# 1. 몇 분 기다린 후 다시 확인
# 2. 수동으로 "Run workflow" 다시 실행
# 3. 이전 실행 중인 워크플로우 취소 후 재실행
```

### 2️⃣ 게시가 안 될 때

**즉시 확인 방법:**
1. **Actions 탭** → 최근 실행 확인
2. **실패한 워크플로우** 클릭 → 오류 로그 확인
3. **Threads 앱**에서 @gost1227 계정 확인

**자가 진단:**
```bash
# GitHub Actions에서 실행:
python check_status.py
```

**긴급 백업 게시:**
```bash
# GitHub Actions에서 실행:
python emergency_post.py
```

### 3️⃣ 토큰 만료 문제

**증상:**
- `Invalid access token` 오류
- `Session has expired` 메시지

**해결:**
1. 새 토큰 발급 (OAuth 프로세스)
2. GitHub Secrets 업데이트
3. 워크플로우 재실행

## 🔍 모니터링 방법

### 일일 확인 체크리스트:
- [ ] Threads 앱에서 새 게시물 확인
- [ ] GitHub Actions 성공/실패 상태
- [ ] 다음 실행 예정 시간

### 주간 점검:
- [ ] 토큰 유효성 확인
- [ ] 게시물 품질 검토
- [ ] 시스템 로그 확인

## 🆘 긴급 상황 대응

### 게시가 며칠간 안 될 때:

1. **즉시 Actions 탭 확인**
2. **"Run workflow"로 수동 실행**
3. **실패 시 오류 로그 확인**
4. **토큰 재발급 고려**

### 백업 실행 방법:

```bash
# Actions 탭에서 새 워크플로우 생성 후 실행:
name: Emergency Backup
on: workflow_dispatch
jobs:
  emergency:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install deps
        run: pip install requests google-generativeai
      - name: Emergency post
        env:
          THREADS_TOKEN: ${{ secrets.THREADS_TOKEN }}
          THREADS_USER_ID: ${{ secrets.THREADS_USER_ID }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python emergency_post.py
```

## 📊 성능 지표

### 정상 운영 기준:
- ✅ **성공률**: 95% 이상
- ✅ **게시 간격**: 6시간 ± 15분
- ✅ **응답 시간**: 30초 이내
- ✅ **토큰 수명**: 60일

### 알림이 필요한 상황:
- ❌ 12시간 이상 게시 없음
- ❌ 연속 3회 실패
- ❌ 토큰 만료 7일 전

## 🔧 유지보수 팁

### 매월 할 일:
1. **토큰 만료일 확인** (60일 주기)
2. **게시물 품질 검토**
3. **시스템 로그 정리**

### 필요시 업데이트:
- AI 프롬프트 개선
- 게시 시간 조정
- 백업 콘텐츠 업데이트

## 📞 지원 정보

### 자주 발생하는 문제:
1. **pytz 모듈 오류** → 수정 완료 ✅
2. **토큰 만료** → 60일마다 갱신 필요
3. **시간대 문제** → 한국시간 적용 완료 ✅
4. **GitHub Actions 대기** → 정상 현상

### 추가 기능 아이디어:
- 📈 게시물 성과 분석
- 🎯 맞춤형 콘텐츠 생성
- 📱 모바일 알림 연동
- 🤖 더 다양한 AI 모델 활용

---

## ✨ 현재 상태: **완벽 작동 중!**

**마지막 업데이트**: 2025-08-25
**시스템 상태**: 🟢 정상
**다음 점검일**: 2025-09-25 (토큰 갱신 예정)
