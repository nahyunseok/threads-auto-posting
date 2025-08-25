#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
백업 게시 시스템 - GitHub Actions가 실패할 때 사용
"""

import os
import requests
import google.generativeai as genai
from datetime import datetime, timedelta
import random

# 환경변수에서 설정 가져오기
THREADS_TOKEN = os.environ.get('THREADS_TOKEN')
THREADS_USER_ID = os.environ.get('THREADS_USER_ID') 
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

def emergency_post():
    """긴급 백업 게시"""
    
    korean_time = datetime.utcnow() + timedelta(hours=9)
    hour = korean_time.hour
    
    print(f"🚨 긴급 백업 게시 시스템 실행")
    print(f"⏰ 한국 시간: {korean_time.strftime('%Y-%m-%d %H:%M:%S KST')}")
    
    # 시간대별 긴급 콘텐츠
    if 5 <= hour < 12:
        time_period = "아침"
        emergency_contents = [
            "좋은 아침입니다! 새로운 하루를 시작해보아요! ☀️ #굿모닝 #새로운하루 #아침인사",
            "상쾌한 아침이네요! 오늘도 좋은 일만 가득하길! 🌅 #아침 #좋은하루 #화이팅",
            "아침 햇살이 참 좋네요~ 모두 행복한 하루 되세요! 💫 #아침햇살 #행복 #좋은아침"
        ]
    elif 12 <= hour < 18:
        time_period = "오후"
        emergency_contents = [
            "점심 맛있게 드셨나요? 오후도 활기차게! 🍽️ #점심시간 #오후 #활력충전",
            "따뜻한 오후 시간이네요~ 잠깐의 여유를 가져보세요! ☕ #오후시간 #여유 #휴식",
            "오후도 힘내세요! 좋은 일들이 기다리고 있을 거예요! 💪 #오후화이팅 #긍정에너지"
        ]
    elif 18 <= hour < 22:
        time_period = "저녁"
        emergency_contents = [
            "오늘 하루 정말 수고 많으셨어요! 편안한 저녁 되세요! 🌆 #하루수고 #저녁시간 #편안한저녁",
            "저녁노을이 아름다운 시간이네요~ 좋은 저녁 보내세요! 🌅 #저녁노을 #아름다운저녁",
            "하루 마무리 잘 하시고 맛있는 저녁식사 되세요! 🍚 #저녁식사 #하루마무리"
        ]
    else:
        time_period = "밤"
        emergency_contents = [
            "늦은 시간까지 고생 많으셨어요! 좋은 꿈 꾸세요! 🌙 #굿나잇 #좋은꿈 #편안한밤",
            "하루를 돌아보며 감사한 마음으로~ 편안한 밤 되세요! ⭐ #하루감사 #편안한밤",
            "오늘도 수고했어요! 내일도 좋은 일만 가득하길! 🌃 #하루마무리 #내일도화이팅"
        ]
    
    # 랜덤 콘텐츠 선택
    content = random.choice(emergency_contents)
    
    print(f"📝 긴급 콘텐츠 ({time_period}): {content}")
    
    # Threads에 게시
    try:
        # Step 1: 게시물 생성
        create_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
        create_params = {
            'media_type': 'TEXT',
            'text': content + f"\n\n[긴급 백업 시스템 - {korean_time.strftime('%H:%M')}]",
            'access_token': THREADS_TOKEN
        }
        
        create_response = requests.post(create_url, data=create_params, timeout=30)
        
        if create_response.status_code == 200:
            creation_data = create_response.json()
            creation_id = creation_data.get('id')
            
            # Step 2: 게시물 발행
            publish_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads_publish"
            publish_params = {
                'creation_id': creation_id,
                'access_token': THREADS_TOKEN
            }
            
            publish_response = requests.post(publish_url, data=publish_params, timeout=30)
            
            if publish_response.status_code == 200:
                publish_data = publish_response.json()
                thread_id = publish_data.get('id')
                print(f"🎉 긴급 백업 게시 성공! Thread ID: {thread_id}")
                return True
            else:
                print(f"❌ 긴급 발행 실패: {publish_response.text}")
                return False
        else:
            print(f"❌ 긴급 생성 실패: {create_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 긴급 게시 오류: {e}")
        return False

if __name__ == "__main__":
    emergency_post()
