#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Threads 자동 게시 상태 확인 및 모니터링
"""

import os
import requests
from datetime import datetime, timedelta
import json

# 환경변수에서 설정 가져오기
THREADS_TOKEN = os.environ.get('THREADS_TOKEN')
THREADS_USER_ID = os.environ.get('THREADS_USER_ID') 

def check_recent_posts():
    """최근 게시물 확인"""
    
    try:
        # 최근 게시물 조회
        url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}/threads"
        params = {
            'fields': 'id,text,timestamp,permalink',
            'limit': 5,
            'access_token': THREADS_TOKEN
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', [])
            
            if posts:
                latest_post = posts[0]
                post_time = datetime.fromisoformat(latest_post['timestamp'].replace('Z', '+00:00'))
                korean_time = post_time + timedelta(hours=9)
                
                print(f"✅ 최근 게시물 발견:")
                print(f"   시간: {korean_time.strftime('%Y-%m-%d %H:%M:%S KST')}")
                print(f"   내용: {latest_post['text'][:50]}...")
                print(f"   링크: {latest_post.get('permalink', 'N/A')}")
                
                # 최근 6시간 이내 게시물인지 확인
                now_korean = datetime.utcnow() + timedelta(hours=9)
                time_diff = now_korean - korean_time
                
                if time_diff.total_seconds() <= 6 * 3600:  # 6시간 이내
                    print(f"🎉 정상 작동 중! (마지막 게시: {time_diff.total_seconds()/3600:.1f}시간 전)")
                    return True
                else:
                    print(f"⚠️ 마지막 게시가 {time_diff.total_seconds()/3600:.1f}시간 전입니다")
                    return False
            else:
                print("❌ 게시물을 찾을 수 없습니다")
                return False
                
        else:
            print(f"❌ API 오류: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 상태 확인 오류: {e}")
        return False

def get_system_status():
    """전체 시스템 상태 체크"""
    
    korean_time = datetime.utcnow() + timedelta(hours=9)
    
    print("🔍 Threads 자동 게시 시스템 상태 점검")
    print(f"⏰ 현재 한국 시간: {korean_time.strftime('%Y-%m-%d %H:%M:%S KST')}")
    print("="*60)
    
    # 1. 환경변수 확인
    print("1️⃣ 환경변수 상태:")
    print(f"   THREADS_TOKEN: {'✅' if THREADS_TOKEN else '❌'}")
    print(f"   THREADS_USER_ID: {'✅' if THREADS_USER_ID else '❌'}")
    print()
    
    # 2. 토큰 유효성 확인
    print("2️⃣ 토큰 유효성 확인:")
    try:
        test_url = f"https://graph.threads.net/v1.0/{THREADS_USER_ID}"
        test_params = {
            'fields': 'id,username',
            'access_token': THREADS_TOKEN
        }
        
        test_response = requests.get(test_url, params=test_params, timeout=30)
        
        if test_response.status_code == 200:
            user_data = test_response.json()
            print(f"   ✅ 토큰 유효 - @{user_data.get('username', 'unknown')}")
        else:
            print(f"   ❌ 토큰 오류: {test_response.status_code}")
            print(f"   응답: {test_response.text}")
            
    except Exception as e:
        print(f"   ❌ 토큰 확인 오류: {e}")
    
    print()
    
    # 3. 최근 게시물 확인
    print("3️⃣ 최근 게시물 상태:")
    is_working = check_recent_posts()
    print()
    
    # 4. 다음 스케줄 예측
    print("4️⃣ 다음 실행 예정 시간:")
    current_hour = korean_time.hour
    
    schedule_hours = [0, 6, 12, 18]  # 한국시간 기준
    next_hours = [h for h in schedule_hours if h > current_hour]
    
    if next_hours:
        next_hour = next_hours[0]
    else:
        next_hour = schedule_hours[0] + 24  # 다음날
    
    next_run = korean_time.replace(hour=next_hour % 24, minute=0, second=0, microsecond=0)
    if next_hour >= 24:
        next_run += timedelta(days=1)
    
    time_until_next = next_run - korean_time
    print(f"   ⏰ 다음 실행: {next_run.strftime('%Y-%m-%d %H:%M KST')}")
    print(f"   🕐 남은 시간: {time_until_next.total_seconds()/3600:.1f}시간")
    print()
    
    # 5. 종합 판정
    print("5️⃣ 시스템 종합 상태:")
    if is_working:
        print("   🎉 정상 작동 중! 모든 시스템이 정상입니다.")
    else:
        print("   ⚠️ 주의 필요! 최근 게시물이 없거나 오래되었습니다.")
        print("   📝 해결 방법:")
        print("      1. GitHub Actions에서 수동으로 'Run workflow' 실행")
        print("      2. 토큰 만료 여부 확인")
        print("      3. 네트워크 연결 상태 확인")
    
    print("="*60)
    return is_working

if __name__ == "__main__":
    get_system_status()
