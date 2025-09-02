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
    """참여형 콘텐츠 생성 (상호작용 중심)"""
    
    # 다양한 콘텐츠 타입들 (참여도 높은 순으로 정렬)
    content_types = [
        {
            "type": "질문형",
            "topics": ["일상 루틴", "선택의 갈등", "취미와 관심사", "학습 방법", "인간관계", "라이프스타일"],
            "weight": 35
        },
        {
            "type": "팁+질문형", 
            "topics": ["건강팁", "생활꿀팁", "학습팁", "재테크", "기술팁", "요리팁"],
            "weight": 25
        },
        {
            "type": "경험공유형",
            "topics": ["실패담", "성공경험", "깨달음", "변화", "도전", "배움"],
            "weight": 20
        },
        {
            "type": "트렌드형",
            "topics": ["최신기술", "유행", "이슈", "화제거리", "뉴스", "문화"],
            "weight": 15
        },
        {
            "type": "정보형",
            "topics": ["통계", "연구결과", "상식", "과학", "건강정보", "경제정보"],
            "weight": 5
        }
    ]
    
    # 가중치에 따라 콘텐츠 타입 선택
    weights = [ct["weight"] for ct in content_types]
    selected_type = random.choices(content_types, weights=weights)[0]
    topic = random.choice(selected_type["topics"])

    prompts = {
        "질문형": f"""
다음 주제로 Threads 팔로워들과 대화를 시작하는 게시물을 작성하세요: {topic}

【필수 규칙】
✅ 반드시 한국어로 작성
✅ 질문으로 끝나야 함 (댓글 유도)
✅ 개인적이고 친근한 톤
✅ 1-2개의 관련 해시태그
✅ 120자 이내로 간결하게

【좋은 예시】
✅ "집중력을 높이기 위해 어떤 방법을 쓰시나요? 저는 25분 집중 + 5분 휴식이 효과적이더라구요! 🧠 #집중력 #생산성"
✅ "돈 관리할 때 가장 어려운 부분이 뭐예요? 저는 용돈기입장 쓰기가 제일 힘들어요 😅 #돈관리"

주제 '{topic}'에 대한 질문형 게시물:""",

        "팁+질문형": f"""
다음 주제로 유용한 팁을 제공하고 경험을 묻는 게시물을 작성하세요: {topic}

【필수 규칙】  
✅ 반드시 한국어로 작성
✅ 팁 제공 + 경험 묻기 조합
✅ 구체적인 방법이나 수치 포함
✅ 2개의 관련 해시태그
✅ 140자 이내

【좋은 예시】
✅ "물 하루 2L 마시기 성공 비법: 1시간마다 알람 설정하기! 여러분만의 물 마시기 꿀팁 있나요? 💧 #건강습관 #물마시기"

주제 '{topic}'에 대한 팁+질문형 게시물:""",

        "경험공유형": f"""
다음 주제로 개인적인 경험을 공유하며 공감을 이끌어내는 게시물을 작성하세요: {topic}

【필수 규칙】
✅ 반드시 한국어로 작성  
✅ 개인적 경험담 포함
✅ 공감할 수 있는 내용
✅ 1-2개의 관련 해시태그
✅ 130자 이내

【좋은 예시】
✅ "새벽 6시 기상 도전 7일차... 첫 3일은 지옥이었지만 지금은 상쾌함이 더 크네요! 여러분도 비슷한 경험 있나요? 🌅 #새벽기상"

주제 '{topic}'에 대한 경험공유형 게시물:""",

        "트렌드형": f"""
다음 주제로 최신 트렌드를 다루며 의견을 묻는 게시물을 작성하세요: {topic}

【필수 규칙】
✅ 반드시 한국어로 작성
✅ 최신성과 화제성 강조  
✅ 의견 묻기로 마무리
✅ 2개의 관련 해시태그
✅ 130자 이내

【좋은 예시】
✅ "ChatGPT가 이제 이미지도 생성한다는데... AI 발전 속도가 정말 무섭네요. 여러분은 어디까지 발전할 거라 생각하세요? 🤖 #AI #기술트렌드"

주제 '{topic}'에 대한 트렌드형 게시물:""",

        "정보형": f"""
다음 주제로 흥미로운 정보를 제공하며 추가 정보를 요청하는 게시물을 작성하세요: {topic}

【필수 규칙】
✅ 반드시 한국어로 작성
✅ 놀라운 사실이나 통계 포함
✅ 추가 정보나 경험 요청으로 마무리
✅ 2개의 관련 해시태그  
✅ 130자 이내

【좋은 예시】
✅ "하루 30분 걷기로 심혈관 질환 위험이 30% 감소한다는 연구결과! 여러분은 어떤 운동을 즐기시나요? 🚶‍♀️ #건강정보 #운동"

주제 '{topic}'에 대한 정보형 게시물:"""
    }
    
    prompt = prompts[selected_type["type"]]

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
        
        # 참여형 백업 콘텐츠 (다양한 타입 혼합)
        backup_content = [
            # 질문형
            "집중력 높이는 나만의 비법이 있나요? 저는 25분 집중 + 5분 휴식이 효과적이더라구요! 🧠 #집중력 #생산성",
            "스트레스 받을 때 어떻게 해소하세요? 저는 산책이 최고인데... 여러분만의 방법 궁금해요! 🚶‍♀️ #스트레스해소",
            "돈 관리할 때 가장 어려운 부분이 뭐예요? 저는 용돈기입장 쓰기가 제일 힘들어요 😅 #돈관리 #재테크",
            
            # 팁+질문형
            "물 하루 2L 마시기 성공 비법: 1시간마다 알람 설정하기! 여러분만의 물 마시기 꿀팁 있나요? 💧 #건강습관 #물마시기",
            "기억력 향상 꿀팁: 새 정보를 3번 반복하고 24시간 후 한번 더! 여러분은 어떤 암기법 쓰세요? 🧠 #학습법 #기억력",
            "배터리 수명 2배 늘리는 법: 20-80% 사이로만 충전하기! 다른 스마트폰 관리 팁 있나요? 🔋 #스마트폰팁 #배터리관리",
            
            # 경험공유형  
            "새벽 6시 기상 도전 7일차... 첫 3일은 지옥이었지만 지금은 상쾌함이 더 크네요! 여러분도 비슷한 경험 있나요? 🌅 #새벽기상",
            "명상 시작한지 한 달... 확실히 마음이 평온해진 느낌이에요. 여러분은 어떤 방식으로 마음 다스리세요? 🧘‍♀️ #명상 #마음챙김",
            
            # 트렌드형
            "AI가 이제 그림도 그린다는데... 기술 발전 속도가 정말 무섭네요. 어디까지 발전할 것 같아요? 🤖 #AI #기술트렌드",
            
            # 정보형
            "하루 30분 걷기로 심혈관 질환 위험 30% 감소! 여러분은 어떤 운동을 즐기시나요? 🚶‍♀️ #건강정보 #운동"
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