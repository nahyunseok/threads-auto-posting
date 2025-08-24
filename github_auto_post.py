#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Actions용 Threads 자동 게시 스크립트
6시간마다 자동 실행
"""

import os
import requests
import google.generativeai as genai
from datetime import datetime
import json
import random

# 환경변수에서 설정 가져오기
THREADS_TOKEN = os.environ.get('THREADS_TOKEN')
THREADS_USER_ID = os.environ.get('THREADS_USER_ID') 
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# AI 모델 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_current_time_context():
    """현재 시간대별 컨텍스트"""
    now = datetime.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        return "아침", "morning"
    elif 12 <= hour < 18:
        return "오후", "afternoon"  
    elif 18 <= hour < 22:
        return "저녁", "evening"
    else:
        return "밤", "night"

def generate_trending_content():
    """트렌드 기반 AI 콘텐츠 생성"""
    
    korean_time, english_time = get_current_time_context()
    
    # 다양한 콘텐츠 스타일
    styles = [
        "일상적이고 공감가는",
        "유머러스하고 재미있는", 
        "생각해볼 만한",
        "따뜻하고 감성적인",
        "트렌디하고 현재적인"
    ]
    
    style = random.choice(styles)
    
    prompt = f"""
{korean_time} 시간대에 어울리는 {style} 소셜미디어 게시물을 작성해주세요.

요구사항:
1. 한국어로 작성
2. 자연스럽고 친근한 톤
3. 2-4개의 관련 해시태그 포함
4. 150자 이내
5. {korean_time} 시간대의 분위기 반영
6. 현재 트렌드나 시사점 반영

현재 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시')}
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
        return response.text.strip()
    except Exception as e:
        print(f"AI 콘텐츠 생성 오류: {e}")
        # 백업 콘텐츠
        backup_content = [
            "오늘도 좋은 하루 보내세요! 💪 #일상 #긍정에너지",
            "작은 일상의 행복을 찾아보는 하루 🌟 #소소한행복 #일상",
            "새로운 도전, 새로운 시작! 🚀 #도전 #성장",
            "감사한 마음으로 하루를 마무리 🙏 #감사 #일상공유"
        ]
        return random.choice(backup_content)

def post_to_threads(content):
    """Threads에 콘텐츠 게시"""
    
    try:
        print(f"게시할 콘텐츠: {content[:50]}...")
        
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
            print(f"게시물 생성 실패: {create_response.text}")
            return False
        
        creation_data = create_response.json()
        creation_id = creation_data.get('id')
        
        if not creation_id:
            print("생성 ID를 받지 못했습니다")
            return False
        
        print(f"게시물 생성 완료! ID: {creation_id}")
        
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
            print(f"✅ 게시 성공! Thread ID: {thread_id}")
            return True
        else:
            print(f"게시물 발행 실패: {publish_response.text}")
            return False
            
    except Exception as e:
        print(f"게시 오류: {e}")
        return False

def main():
    """메인 실행 함수"""
    
    print("🤖 Threads 자동 게시 시작")
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 환경변수 확인
    if not all([THREADS_TOKEN, THREADS_USER_ID, GEMINI_API_KEY]):
        print("❌ 필수 환경변수가 설정되지 않았습니다")
        print(f"THREADS_TOKEN: {'✅' if THREADS_TOKEN else '❌'}")
        print(f"THREADS_USER_ID: {'✅' if THREADS_USER_ID else '❌'}")
        print(f"GEMINI_API_KEY: {'✅' if GEMINI_API_KEY else '❌'}")
        return False
    
    # AI 콘텐츠 생성
    print("🧠 AI 콘텐츠 생성 중...")
    content = generate_trending_content()
    print(f"생성된 콘텐츠: {content}")
    
    # Threads에 게시
    print("📱 Threads에 게시 중...")
    success = post_to_threads(content)
    
    if success:
        print("🎉 자동 게시 완료!")
    else:
        print("❌ 게시 실패")
    
    print("="*60)
    return success

if __name__ == "__main__":
    main()
