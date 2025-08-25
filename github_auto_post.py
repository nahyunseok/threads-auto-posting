#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Actions용 Threads 자동 게시 스크립트
6시간마다 자동 실행 - 한국 시간 기준으로 수정
"""

import os
import requests
import google.generativeai as genai
from datetime import datetime
import pytz
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
    """한국 시간 가져오기"""
    korean_tz = pytz.timezone('Asia/Seoul')
    return datetime.now(korean_tz)

def get_current_time_context():
    """한국 시간 기준으로 시간대별 컨텍스트"""
    korean_now = get_korean_time()
    hour = korean_now.hour
    
    print(f"🇰🇷 한국 현재 시간: {korean_now.strftime('%Y-%m-%d %H:%M:%S KST')}")
    
    if 5 <= hour < 12:
        return "아침", "morning", korean_now
    elif 12 <= hour < 18:
        return "오후", "afternoon", korean_now  
    elif 18 <= hour < 22:
        return "저녁", "evening", korean_now
    else:
        return "밤", "night", korean_now

def generate_trending_content():
    """한국 시간 기준 트렌드 콘텐츠 생성"""
    
    korean_time, english_time, current_time = get_current_time_context()
    
    # 다양한 콘텐츠 스타일
    styles = [
        "일상적이고 공감가는",
        "유머러스하고 재미있는", 
        "생각해볼 만한",
        "따뜻하고 감성적인",
        "트렌디하고 현재적인"
    ]
    
    style = random.choice(styles)
    
    # 시간대별 특화 메시지
    time_specific_context = {
        "아침": "상쾌한 아침, 새로운 시작, 모닝 루틴, 출근길",
        "오후": "점심시간, 오후 활력, 짧은 휴식, 업무 중간",
        "저녁": "하루 마무리, 퇴근길, 저녁 시간, 하루 정리",
        "밤": "편안한 밤, 하루 돌아보기, 내일 준비, 야경"
    }
    
    context = time_specific_context.get(korean_time, "일상")
    
    prompt = f"""
한국 시간 {korean_time} ({current_time.strftime('%H시 %M분')})에 어울리는 {style} 소셜미디어 게시물을 작성해주세요.

시간대별 컨텍스트: {context}

요구사항:
1. 한국어로 작성
2. 자연스럽고 친근한 톤
3. 2-4개의 관련 해시태그 포함
4. 150자 이내
5. {korean_time} 시간대의 분위기 완벽 반영
6. 현재 트렌드나 시사점 반영
7. 한국인들이 좋아할 만한 내용

현재 한국 시간: {current_time.strftime('%Y년 %m월 %d일 %H시 %M분')}
요일: {current_time.strftime('%A')}

예시:
- 아침: "좋은 아침! 오늘도 힘찬 하루 시작! ☀️ #굿모닝"
- 오후: "점심 맛있게 드셨나요? 오후도 화이팅! 💪 #런치타임"
- 저녁: "오늘 하루 수고하셨어요~ 맛있는 저녁 되세요! 🍽️ #저녁시간"
- 밤: "하루 마무리 잘 하시고 좋은 꿈 꾸세요 🌙 #굿나잇"
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 300,
                "top_p": 0.8,
                "top_k": 40
            }
        )
        
        generated_content = response.text.strip()
        print(f"🧠 AI 생성 콘텐츠 ({korean_time}): {generated_content[:100]}...")
        return generated_content
        
    except Exception as e:
        print(f"AI 콘텐츠 생성 오류: {e}")
        
        # 시간대별 백업 콘텐츠
        backup_content = {
            "아침": [
                "좋은 아침입니다! 오늘도 화이팅하세요! ☀️ #굿모닝 #좋은하루",
                "상쾌한 아침이네요! 새로운 시작! 💪 #아침 #새시작",
                "모든 분들 좋은 아침! 오늘 하루도 행복하세요! 🌅 #아침인사 #행복"
            ],
            "오후": [
                "즐거운 오후시간! 맛있는 점심 드셨나요? 🍽️ #점심시간 #오후",
                "오후도 활기차게! 남은 하루도 힘내세요! ⚡ #오후활력 #힘내요",
                "따뜻한 오후 햇살처럼 좋은 하루! ☀️ #오후 #햇살"
            ],
            "저녁": [
                "오늘 하루 정말 수고하셨습니다! 🌆 #수고했어요 #저녁",
                "맛있는 저녁시간! 가족과 함께 좋은 시간 되세요! 🍚 #저녁식사 #가족시간",
                "하루 마무리 잘 하시고 편안한 저녁 보내세요! 🌇 #저녁 #휴식"
            ],
            "밤": [
                "오늘도 고생 많으셨어요! 좋은 밤 되세요! 🌙 #굿나잇 #좋은꿈",
                "하루를 돌아보며 감사한 마음으로! ⭐ #하루정리 #감사",
                "편안한 밤, 내일도 좋은 일만! 🌃 #편안한밤 #내일도화이팅"
            ]
        }
        
        return random.choice(backup_content.get(korean_time, backup_content["오후"]))

def post_to_threads(content):
    """Threads에 콘텐츠 게시"""
    
    try:
        print(f"📱 게시할 콘텐츠: {content[:50]}...")
        
        # Step 1: 게시물 생성
        create_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
        create_params = {
            'media_type': 'TEXT',
            'text': content,
            'access_token': THREADS_TOKEN
        }
        
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
    print(f"📝 생성된 콘텐츠: {content}")
    
    # Threads에 게시
    print("📱 Threads에 게시 중...")
    success = post_to_threads(content)
    
    if success:
        print("🎉 자동 게시 완료!")
        print(f"⏰ 다음 실행: {korean_time.strftime('%H시')}부터 6시간 후")
    else:
        print("❌ 게시 실패")
    
    print("="*60)
    return success

if __name__ == "__main__":
    main()
