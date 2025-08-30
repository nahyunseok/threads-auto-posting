#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Actions용 Threads 자동 게시 스크립트
6시간마다 자동 실행 - 한국 시간 기준 (pytz 없이)
"""

import os
import requests
import google.generativeai as genai
from datetime import datetime, timedelta
import json
import random

# 환경변수에서 설정 가져오기
THREADS_TOKEN = os.environ.get('THREADS_TOKEN')
THREADS_USER_ID = os.environ.get('THREADS_USER_ID') 
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# AI 모델 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_korean_time():
    """한국 시간 가져오기 (UTC + 9시간)"""
    utc_now = datetime.utcnow()
    korean_now = utc_now + timedelta(hours=9)
    return korean_now

def get_current_time_context():
    """한국 시간 기준으로 시간대별 컨텍스트"""
    korean_now = get_korean_time()
    hour = korean_now.hour
    
    print(f"🌏 UTC 시간: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"🇰🇷 한국 시간: {korean_now.strftime('%Y-%m-%d %H:%M:%S KST')}")
    
    if 5 <= hour < 12:
        return "아침", "morning", korean_now
    elif 12 <= hour < 18:
        return "오후", "afternoon", korean_now  
    elif 18 <= hour < 22:
        return "저녁", "evening", korean_now
    else:
        return "밤", "night", korean_now

def generate_trending_content():
    """정보성 콘텐츠 생성 (시간 컨텍스트 제거)"""
    
    # 정보성 주제들
    info_topics = [
        "건강과 웰빙",
        "생활 꿀팁",
        "학습과 자기계발", 
        "경제와 재테크",
        "기술과 디지털",
        "환경과 지속가능성",
        "심리학과 인간관계",
        "요리와 영양"
    ]
    
    topic = random.choice(info_topics)

    prompt = f"""
다음 주제에 대한 유용한 정보를 제공하는 Threads 게시물을 작성하세요: {topic}

【필수 규칙】
✅ 반드시 한국어로 작성
✅ 순수하게 정보만 전달 (팁, 상식, 통계, 연구결과 등)
✅ 2-3개의 관련 해시태그 포함
✅ 150자 이내로 간결하게
✅ 구체적인 수치나 방법 제시

【절대 금지사항】
❌ 시간 언급 금지 (아침, 오후, 저녁, 밤, 오늘, 내일 등)
❌ 요일 언급 금지 (월요일, 주말 등)
❌ 계절 언급 금지 (봄, 여름, 가을, 겨울)
❌ 인사말 금지 (안녕하세요, 좋은 하루 등)
❌ 감정 표현 금지 (기분, 느낌 등)

【좋은 예시】
✅ "물을 하루 8잔 마시면 신진대사가 20% 향상됩니다. 🥤 #건강팁 #물마시기"
✅ "스마트폰 배터리는 20-80% 사이로 충전하면 수명이 2배 늘어납니다. 🔋 #스마트폰팁 #배터리관리"
✅ "연 7% 복리로 10년 투자하면 원금이 2배가 됩니다. 📈 #재테크 #복리효과"

【나쁜 예시】
❌ "좋은 아침입니다! 오늘도 물 많이 드세요"
❌ "월요일 피로를 이기는 방법"
❌ "저녁에 스마트폰 사용 줄이기"

주제 '{topic}'에 대한 게시물:"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.6,  # 더 일관된 출력을 위해 낮춤
                "max_output_tokens": 300,
                "top_p": 0.8,
                "top_k": 40
            }
        )
        
        generated_content = response.text.strip()
        print(f"🧠 AI 생성 콘텐츠: {generated_content}")
        return generated_content
        
    except Exception as e:
        print(f"❌ AI 콘텐츠 생성 오류: {e}")
        
        # 정보성 백업 콘텐츠
        backup_content = [
            "단백질은 체중 1kg당 1.2-2g 섭취하면 근육 유지에 효과적입니다. 💪 #건강정보 #단백질",
            "하루 30분 걷기만 해도 심혈관 질환 위험이 30% 감소합니다. 🚶‍♀️ #건강팁 #운동",
            "스마트폰 화면을 20-20-20 법칙으로 보세요. 20분마다 20초간 6m 거리 보기! 👁️ #눈건강 #디지털디톡스",
            "물가 상승률을 이기려면 연 3% 이상의 수익률이 필요합니다. 📈 #재테크 #인플레이션",
            "잠들기 2시간 전 스마트폰 사용을 줄이면 수면의 질이 40% 개선됩니다. 😴 #수면팁 #건강한생활",
            "매일 5분씩 명상하면 스트레스 호르몬이 23% 감소한다는 연구결과가 있습니다. 🧘‍♀️ #명상 #스트레스관리",
            "냉장고 적정 온도는 1-4℃, 냉동고는 -18℃입니다. 전기료 절약과 식품 보관 모두 OK! ❄️ #생활꿀팁 #절약",
            "기억력을 높이려면 새로운 정보를 3번 반복하고 24시간 후 한번 더 복습하세요. 🧠 #학습법 #기억력"
        ]
        
        selected_content = random.choice(backup_content)
        print(f"🔄 백업 콘텐츠 사용: {selected_content}")
        return selected_content

def post_to_threads(content):
    """Threads에 콘텐츠 게시"""
    
    try:
        print(f"📱 게시할 콘텐츠: {content}")
        
        # Step 1: 게시물 생성
        create_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
        create_params = {
            'media_type': 'TEXT',
            'text': content,
            'access_token': THREADS_TOKEN
        }
        
        print("📝 게시물 생성 중...")
        create_response = requests.post(create_url, data=create_params, timeout=30)
        print(f"생성 응답: {create_response.status_code}")
        
        if create_response.status_code != 200:
            print(f"❌ 게시물 생성 실패: {create_response.text}")
            return False
        
        creation_data = create_response.json()
        creation_id = creation_data.get('id')
        
        if not creation_id:
            print("❌ 생성 ID를 받지 못했습니다")
            return False
        
        print(f"✅ 게시물 생성 완료! ID: {creation_id}")
        
        # Step 2: 게시물 발행
        print("📤 게시물 발행 중...")
        publish_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
        publish_params = {
            'creation_id': creation_id,
            'access_token': THREADS_TOKEN
        }
        
        publish_response = requests.post(publish_url, data=publish_params, timeout=30)
        print(f"발행 응답: {publish_response.status_code}")
        
        if publish_response.status_code == 200:
            publish_data = publish_response.json()
            thread_id = publish_data.get('id')
            print(f"🎉 게시 성공! Thread ID: {thread_id}")
            return True
        else:
            print(f"❌ 게시물 발행 실패: {publish_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 게시 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    
    korean_time = get_korean_time()
    
    print("🤖 Threads 자동 게시 시작 (한국 시간 기준)")
    print(f"🌏 UTC 시간: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"🇰🇷 한국 시간: {korean_time.strftime('%Y-%m-%d %H:%M:%S KST')}")
    print("="*60)
    
    # 환경변수 확인
    if not all([THREADS_TOKEN, THREADS_USER_ID, GEMINI_API_KEY]):
        print("❌ 필수 환경변수가 설정되지 않았습니다")
        print(f"THREADS_TOKEN: {'✅' if THREADS_TOKEN else '❌'}")
        print(f"THREADS_USER_ID: {'✅' if THREADS_USER_ID else '❌'}")
        print(f"GEMINI_API_KEY: {'✅' if GEMINI_API_KEY else '❌'}")
        return False
    
    print("✅ 모든 환경변수 확인 완료")
    
    # AI 콘텐츠 생성 (한국 시간 기준)
    print("🧠 AI 콘텐츠 생성 중 (한국 시간 기준)...")
    content = generate_trending_content()
    
    # Threads에 게시
    print("📱 Threads에 게시 중...")
    success = post_to_threads(content)
    
    if success:
        print("🎉 자동 게시 완료!")
        print(f"⏰ 다음 실행 예정: 6시간 후")
    else:
        print("❌ 게시 실패")
    
    print("="*60)
    return success

if __name__ == "__main__":
    main()