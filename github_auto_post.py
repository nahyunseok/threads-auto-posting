#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Actions용 Threads 자동 게시 스크립트
매일 새벽1시, 오전9시, 오후1시30분, 저녁8시에 자동 실행
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

def get_weekday_style():
    """요일별 글 스타일 (일관된 정체성 유지)"""
    weekday = datetime.now().weekday()
    
    # 요일별 글쓰기 스타일만 변경 (정체성은 고정)
    weekday_moods = {
        0: ["월요병 극복하는", "한 주를 시작하는", "월요일 블루스"],  # 월요일
        1: ["차분하게 일상 공유하는", "화요일의 소소한"],  # 화요일
        2: ["주중 절반을 넘긴", "수요일의 작은 행복"],  # 수요일  
        3: ["주말을 기다리며", "목요일 저녁의"],  # 목요일
        4: ["불금을 맞이하는", "금요일의 설렘"],  # 금요일
        5: ["주말을 즐기는", "토요일의 여유"],  # 토요일
        6: ["주말을 마무리하는", "일요일 저녁의"]  # 일요일
    }
    
    return random.choice(weekday_moods.get(weekday, ["일상을 공유하는"]))

def get_time_based_mood():
    """시간대별 감정과 톤 (대전 거주 30대 남성 관점)"""
    hour = datetime.now().hour
    
    if 5 <= hour < 9:  # 아침
        moods = ["상쾌한", "활기찬", "희망찬", "긍정적인"]
        topics = ["모닝커피", "아침 루틴", "출근길", "대전 아침 날씨", "둔산동 카페"]
    elif 9 <= hour < 12:  # 오전
        moods = ["집중하는", "생산적인", "차분한", "열정적인"]
        topics = ["업무", "대덕연구단지", "일상", "도전", "유성 온천"]
    elif 12 <= hour < 14:  # 점심
        moods = ["편안한", "여유로운", "맛있는", "즐거운"]
        topics = ["점심 메뉴", "성심당", "대전 맛집", "칼국수", "동료와의 시간"]
    elif 14 <= hour < 18:  # 오후
        moods = ["나른한", "잔잔한", "집중력 회복하는", "소소한"]
        topics = ["오후 커피", "스트레칭", "작은 성취", "한밭수목원 산책"]
    elif 18 <= hour < 22:  # 저녁
        moods = ["편안한", "감사한", "따뜻한", "여유로운"]
        topics = ["퇴근", "저녁 시간", "엑스포다리 야경", "갑천 산책", "대전역 주변"]
    else:  # 밤
        moods = ["고요한", "사색적인", "차분한", "감성적인"]
        topics = ["밤의 생각", "내일 준비", "대전의 밤", "휴식"]
    
    return random.choice(moods), random.choice(topics)

def generate_trending_content():
    """트렌드 기반 AI 콘텐츠 생성 (일관된 정체성 + 다양한 스타일)"""
    
    korean_time, english_time = get_current_time_context()
    
    # 고정된 정체성 (이것은 변하지 않음)
    fixed_persona = """
    당신은 대전에 사는 30대 중후반 남성입니다. (1985-1995년생)
    - 거주지: 대전 (둔산동, 유성구 등 대전 지역명 자연스럽게 언급 가능)
    - 성별: 남성
    - 나이: 30대 중후반
    - 특징: 대전 토박이 또는 직장 때문에 대전 거주
    - 대전 맛집, 대전 날씨, 대전 생활 등 자연스럽게 언급
    """
    
    # 요일별 스타일 가져오기
    weekday_style = get_weekday_style()
    
    # 시간대별 감정과 주제 가져오기
    mood, topic = get_time_based_mood()
    
    # 글쓰기 스타일 다양화 (정체성과 무관한 것들)
    writing_styles = [
        "짧고 임팩트 있게",
        "스토리텔링으로 풀어서",
        "질문을 던지며",
        "이모지를 활용해 귀엽게",
        "담백하고 간결하게",
        "유머러스하게",
        "감성적으로"
    ]
    
    selected_style = random.choice(writing_styles)
    
    # 해시태그 스타일도 다양화
    hashtag_styles = [
        "한글 해시태그만",
        "영어 해시태그 섞어서",
        "이모지 해시태그 포함"
    ]
    
    selected_hashtag = random.choice(hashtag_styles)
    
    prompt = f"""
{fixed_persona}

현재 {korean_time} 시간대, {weekday_style} 분위기로 글을 작성해주세요.

[작성 스타일]
- 감정 톤: {mood}
- 주제: {topic}
- 글쓰기 방식: {selected_style}
- 해시태그: {selected_hashtag}

[30대 남성 관심사 반영]
- 일과 워라밸
- 운동과 건강 관리
- 맥주, 커피
- IT/테크 관심
- 가끔 게임
- 대전 지역 정보

요구사항:
1. 한국어로 자연스럽게 작성 (30대 남성 말투)
2. 150자 이내
3. 2-4개의 해시태그
4. {korean_time} 시간대와 요일 분위기 반영
5. 대전 거주 30대 남성 정체성 일관되게 유지
6. 글의 스타일과 톤은 자유롭게 변화
7. 가끔 대전 지역 언급 (자연스럽게)

현재 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시')}
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.8,  # 창의성 높임
                "max_output_tokens": 300,
                "top_p": 0.85,
                "top_k": 45
            }
        )
        
        content = response.text.strip()
        
        # 디버그 정보 출력
        print(f"📊 스타일 정보:")
        print(f"  - 요일 분위기: {weekday_style}")
        print(f"  - 감정/톤: {mood}")
        print(f"  - 주제: {topic}")
        print(f"  - 글쓰기 방식: {selected_style}")
        
        return content
        
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
