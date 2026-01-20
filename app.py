"""
🎯 MBTI 매칭 테스트 v3.0 (최종 상용화 버전)
============================================
✅ 모바일 반응형 최적화
✅ 저작권/초상권 완전 보호
✅ 광고 정책 준수
✅ 개인정보 미수집
✅ 국가별 문화 대응
✅ 리스크 방지 장치

Author: 20년차 수익형 웹앱 전문가
License: MIT
Version: 3.0.0
"""

import streamlit as st
import json
import hashlib
import random
from datetime import datetime
import streamlit.components.v1 as components

# ============================================
# ⚠️ 리스크 방지: 국가 차단 (필요시 활성화)
# ============================================
BLOCKED_COUNTRIES = []  # 예: ["CN", "RU"] - 필요시 추가

# ============================================
# 🎨 페이지 설정
# ============================================
st.set_page_config(
    page_title="🎯 MBTI Match Test",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# 📊 테스트 설정
# ============================================
TEST_CONFIG = {
    "anime": {
        "emoji": "💕", "title": "애니 캐릭터", "title_en": "Anime Character",
        "title_full": {"ko": "나와 어울리는 애니 캐릭터는?", "en": "Which Anime Character Matches You?"},
        "data_file": "data/characters.json",
        "image_type": "robohash", "image_set": "set5",
        "question_type": "relationship"
    },
    "dogs": {
        "emoji": "🐕", "title": "강아지", "title_en": "Dog Breed",
        "title_full": {"ko": "나랑 어울리는 강아지 품종은?", "en": "Which Dog Breed Suits You?"},
        "data_file": "data/dogs.json",
        "image_type": "unsplash",
        "question_type": "pet"
    },
    "cats": {
        "emoji": "🐈", "title": "고양이", "title_en": "Cat Breed",
        "title_full": {"ko": "나랑 어울리는 고양이 품종은?", "en": "Which Cat Breed Suits You?"},
        "data_file": "data/cats.json",
        "image_type": "unsplash",
        "question_type": "pet"
    },
    "cities": {
        "emoji": "🌆", "title": "도시", "title_en": "City",
        "title_full": {"ko": "나랑 어울리는 도시는?", "en": "Which City Suits You?"},
        "data_file": "data/cities.json",
        "image_type": "unsplash",
        "question_type": "place"
    },
    "destinations": {
        "emoji": "🏝️", "title": "여행지", "title_en": "Destination",
        "title_full": {"ko": "나랑 어울리는 여행지는?", "en": "Which Destination Suits You?"},
        "data_file": "data/destinations.json",
        "image_type": "unsplash",
        "question_type": "travel"
    },
    "cars": {
        "emoji": "🚗", "title": "자동차", "title_en": "Car",
        "title_full": {"ko": "나랑 어울리는 자동차는?", "en": "Which Car Suits You?"},
        "data_file": "data/cars.json",
        "image_type": "unsplash",
        "question_type": "car"
    },
    "stars": {
        "emoji": "⭐", "title": "글로벌 스타", "title_en": "Global Star",
        "title_full": {"ko": "나랑 어울리는 글로벌 스타는?", "en": "Which Global Star Matches You?"},
        "data_file": "data/global_stars.json",
        "image_type": "robohash", "image_set": "set5",
        "question_type": "relationship"
    },
    "idols": {
        "emoji": "🎤", "title": "아이돌", "title_en": "K-Pop Idol",
        "title_full": {"ko": "나랑 어울리는 아이돌은?", "en": "Which K-Pop Idol Matches You?"},
        "data_file": "data/idols.json",
        "image_type": "robohash", "image_set": "set5",
        "question_type": "relationship"
    },
    "games": {
        "emoji": "🎮", "title": "게임 캐릭터", "title_en": "Game Character",
        "title_full": {"ko": "나랑 어울리는 게임 캐릭터는?", "en": "Which Game Character Matches You?"},
        "data_file": "data/game_characters.json",
        "image_type": "robohash", "image_set": "set2",
        "question_type": "game"
    },
    "tinipings": {
        "emoji": "🎀", "title": "티니핑", "title_en": "Tiniping",
        "title_full": {"ko": "나는 어떤 캐치티니핑?", "en": "Which Tiniping Are You?"},
        "data_file": "data/tinipings.json",
        "image_type": "robohash", "image_set": "set4",
        "question_type": "character"
    }
}

# ============================================
# 🎯 카테고리별 질문
# ============================================
QUESTIONS = {
    "relationship": {
        "ko": {"q": "어떤 관계?", "o": {"ideal": "💕 이상형", "romance": "💝 연애", "marriage": "💍 결혼", "fan": "⭐ 최애"}},
        "en": {"q": "Relationship?", "o": {"ideal": "💕 Ideal", "romance": "💝 Dating", "marriage": "💍 Marriage", "fan": "⭐ Fave"}}
    },
    "pet": {
        "ko": {"q": "어떤 관계?", "o": {"want": "🏠 키우고싶은", "similar": "🪞 닮은", "soulmate": "💫 소울메이트"}},
        "en": {"q": "What match?", "o": {"want": "🏠 Want", "similar": "🪞 Similar", "soulmate": "💫 Soulmate"}}
    },
    "place": {
        "ko": {"q": "어떤 목적?", "o": {"live": "🏠 거주", "travel": "✈️ 여행", "month": "📅 한달살기"}},
        "en": {"q": "Purpose?", "o": {"live": "🏠 Live", "travel": "✈️ Travel", "month": "📅 Month"}}
    },
    "travel": {
        "ko": {"q": "여행 스타일?", "o": {"healing": "🌴 힐링", "adventure": "🏔️ 모험", "bucket": "⭐ 버킷"}},
        "en": {"q": "Travel style?", "o": {"healing": "🌴 Healing", "adventure": "🏔️ Adventure", "bucket": "⭐ Bucket"}}
    },
    "car": {
        "ko": {"q": "어떤 차?", "o": {"dream": "🌟 드림카", "first": "🔰 첫차", "practical": "💼 실용"}},
        "en": {"q": "What car?", "o": {"dream": "🌟 Dream", "first": "🔰 First", "practical": "💼 Practical"}}
    },
    "game": {
        "ko": {"q": "어떤 캐릭터?", "o": {"play": "🕹️ 플레이", "party": "👥 파티원", "similar": "🪞 닮은"}},
        "en": {"q": "What character?", "o": {"play": "🕹️ Play", "party": "👥 Party", "similar": "🪞 Similar"}}
    },
    "character": {
        "ko": {"q": "어떤 타입?", "o": {"similar": "🪞 닮은", "friend": "👫 친구", "guardian": "🛡️ 수호"}},
        "en": {"q": "What type?", "o": {"similar": "🪞 Similar", "friend": "👫 Friend", "guardian": "🛡️ Guardian"}}
    }
}

# ============================================
# 🌍 다국어 (간소화)
# ============================================
T = {
    "ko": {
        "nick": "닉네임", "nick_ph": "이름",
        "mbti": "MBTI", "gender": "성별", "m": "남", "f": "여",
        "age": "나이대", "pers": "💭 성격 3개",
        "submit": "✨ 결과보기", "result": "{}님 결과",
        "rate": "매칭률", "retry": "🔄 다시",
        "other": "🎁 다른 테스트",
        "ages": ["10대", "20대", "30대", "40대", "50+"],
        "p": {"따뜻한": "따뜻한", "냉정한": "냉정한", "열정적인": "열정적",
              "차분한": "차분한", "활발한": "활발한", "겸손한": "겸손한",
              "배려심많은": "배려심", "독립적인": "독립적",
              "낙천적인": "낙천적", "유머러스한": "유머"},
        "disclaimer": "⚠️ 본 테스트는 오락 목적이며 과학적 근거가 없습니다.",
        "privacy": "🔒 개인정보를 수집·저장하지 않습니다.",
        "copyright": "📷 이미지: Unsplash(CC0) / AI생성(RoboHash)"
    },
    "en": {
        "nick": "Nickname", "nick_ph": "Name",
        "mbti": "MBTI", "gender": "Gender", "m": "M", "f": "F",
        "age": "Age", "pers": "💭 3 Traits",
        "submit": "✨ Results", "result": "{}'s Match",
        "rate": "Match", "retry": "🔄 Retry",
        "other": "🎁 More Tests",
        "ages": ["Teen", "20s", "30s", "40s", "50+"],
        "p": {"따뜻한": "Warm", "냉정한": "Cool", "열정적인": "Passionate",
              "차분한": "Calm", "활발한": "Active", "겸손한": "Humble",
              "배려심많은": "Caring", "독립적인": "Independent",
              "낙천적인": "Optimistic", "유머러스한": "Funny"},
        "disclaimer": "⚠️ This is for entertainment only, not scientifically validated.",
        "privacy": "🔒 We do not collect or store any personal data.",
        "copyright": "📷 Images: Unsplash(CC0) / AI-generated(RoboHash)"
    }
}

def t(k, lang): return T.get(lang, T["en"]).get(k, k)

# ============================================
# 🎨 CSS (모바일 반응형 최적화)
# ============================================
def mobile_css():
    st.markdown("""<style>
    /* 기본 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* 컨테이너 */
    .block-container {
        padding: 1rem 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* 카드 */
    .card {
        background: white;
        border-radius: 16px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* 결과 카드 */
    .result {
        background: white;
        padding: 20px 12px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* 이미지 - 모바일 최적화 */
    .match-img {
        width: min(180px, 45vw);
        height: min(180px, 45vw);
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #667eea;
        margin: 10px auto;
        display: block;
    }
    
    /* 이름 */
    .match-name {
        font-size: clamp(20px, 5vw, 28px);
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
        word-break: keep-all;
    }
    
    /* 시리즈 */
    .match-series {
        color: #888;
        font-size: clamp(11px, 3vw, 14px);
    }
    
    /* 점수 박스 */
    .score-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 15px;
        border-radius: 12px;
        margin: 12px auto;
        max-width: 120px;
    }
    
    .score-num {
        font-size: clamp(36px, 10vw, 48px);
        font-weight: 800;
        color: white;
    }
    
    /* 태그 */
    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        margin: 2px;
        font-size: clamp(10px, 2.5vw, 13px);
    }
    
    /* MBTI 배지 */
    .mbti-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ffd89b, #19547b);
        color: white;
        padding: 5px 15px;
        border-radius: 10px;
        font-weight: 700;
        font-size: clamp(12px, 3vw, 15px);
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        padding: 15px 10px;
        color: rgba(255,255,255,0.75);
        font-size: clamp(9px, 2.2vw, 11px);
        margin-top: 20px;
        line-height: 1.6;
    }
    
    /* 버튼 반응형 */
    .stButton > button {
        font-size: clamp(12px, 3vw, 16px) !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
    }
    
    /* 입력 필드 */
    .stTextInput input, .stSelectbox select {
        font-size: 16px !important; /* iOS 줌 방지 */
    }
    
    /* 체크박스 레이블 */
    .stCheckbox label {
        font-size: clamp(11px, 2.8vw, 14px) !important;
    }
    
    /* 라디오 버튼 */
    .stRadio > div {
        flex-wrap: wrap !important;
        gap: 5px !important;
    }
    
    /* 광고 영역 */
    .ad-container {
        text-align: center;
        padding: 10px;
        margin: 10px 0;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        min-height: 50px;
    }
    
    /* 면책조항 박스 */
    .disclaimer-box {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        font-size: clamp(9px, 2.2vw, 11px);
        color: rgba(255,255,255,0.8);
        text-align: center;
    }
    
    /* 터치 영역 확대 (모바일) */
    @media (max-width: 768px) {
        .stButton > button {
            min-height: 44px !important; /* iOS 권장 터치 영역 */
        }
        .stCheckbox {
            padding: 8px 0 !important;
        }
    }
    
    /* 가로 스크롤 방지 */
    html, body {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    </style>""", unsafe_allow_html=True)

# ============================================
# 🖼️ 이미지 URL (저작권 안전)
# ============================================
def get_img(name, name_en, cfg):
    if cfg.get('image_type') == 'unsplash':
        q = (name_en or name).replace(" ", ",").replace("(", "").replace(")", "")[:50]
        return f"https://source.unsplash.com/300x300/?{q}"
    seed = hashlib.md5(name.encode()).hexdigest()
    s = cfg.get('image_set', 'set5')
    return f"https://robohash.org/{seed}.png?set={s}&size=300x300"

# ============================================
# 📊 MBTI 궁합 (간소화)
# ============================================
COMPAT = {"INTJ":["ENFP"],"INTP":["ENTJ"],"ENTJ":["INTP"],"ENTP":["INFJ"],
          "INFJ":["ENTP"],"INFP":["ENTJ"],"ENFJ":["INFP"],"ENFP":["INFJ"],
          "ISTJ":["ESFP"],"ISFJ":["ESTP"],"ESTJ":["ISFP"],"ESFJ":["ISTP"],
          "ISTP":["ESFJ"],"ISFP":["ESTJ"],"ESTP":["ISFJ"],"ESFP":["ISTJ"]}

def calc(mbti, pers, tgt):
    s = 55
    tm = tgt.get('mbti', 'ENFP')
    if tm in COMPAT.get(mbti, []): s += 25
    elif tm == mbti: s += 12
    else: s += 6
    tp = tgt.get('personality', [])
    s += len(set(pers) & set(tp)) * 7
    return min(99, max(65, s + random.randint(-2, 6)))

def match(data, mbti, pers):
    res = sorted([{**d, 'score': calc(mbti, pers, d)} for d in data], 
                 key=lambda x: x['score'], reverse=True)
    return res[:1] if res else []

# ============================================
# 📂 데이터 로드 (캐싱)
# ============================================
@st.cache_data(ttl=3600)
def load(f, cfg):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for d in data:
                d['image_url'] = get_img(d.get('name',''), d.get('name_en',''), cfg)
            return data
    except: return []

# ============================================
# 💰 광고 (정책 준수)
# ============================================
def ad(lang):
    if st.session_state.get('ad_shown'): return
    
    # 광고 코드 삽입 위치
    ad_html = """
    <div class="ad-container">
        <!-- 
        ═══════════════════════════════════════
        📍 광고 코드 삽입 가이드
        ═══════════════════════════════════════
        
        [한국 트래픽 - AdFit]
        1. https://adfit.kakao.com 가입
        2. 새 광고단위 생성 (320x100 또는 320x50)
        3. 아래 주석 해제 후 코드 교체
        
        <ins class="kakao_ad_area" 
             data-ad-unit="YOUR_UNIT_ID"
             data-ad-width="320" 
             data-ad-height="100">
        </ins>
        <script src="//t1.daumcdn.net/kas/static/ba.min.js" async></script>
        
        [해외 트래픽 - PropellerAds]
        1. https://propellerads.com 가입
        2. 새 채널 생성
        3. 스크립트 코드 삽입
        
        <script src="//YOUR_SCRIPT.js"></script>
        ═══════════════════════════════════════
        -->
        <p style="color:rgba(255,255,255,0.5);font-size:10px;margin:0;">
            Sponsored
        </p>
    </div>
    """
    components.html(ad_html, height=60)
    st.session_state['ad_shown'] = True

# ============================================
# 📤 공유 (간소화)
# ============================================
def share(name, score, title, lang):
    txt = f"My {title} match: {name}! {score}%" if lang=='en' else f"나의 {title}: {name}! {score}%"
    url = "https://your-app.streamlit.app"  # 배포 후 변경
    
    components.html(f"""
    <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0;">
        <a href="https://twitter.com/intent/tweet?text={txt}&url={url}" target="_blank"
           style="padding:8px 16px;background:#1da1f2;color:white;border-radius:8px;
                  text-decoration:none;font-size:13px;font-weight:600;">
            🐦 Tweet
        </a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank"
           style="padding:8px 16px;background:#1877f2;color:white;border-radius:8px;
                  text-decoration:none;font-size:13px;font-weight:600;">
            📘 Share
        </a>
    </div>
    """, height=50)

# ============================================
# 🔄 크로스 프로모션
# ============================================
def promo(cur, lang):
    others = [(k,v) for k,v in TEST_CONFIG.items() if k!=cur]
    feat = random.sample(others, min(5, len(others)))
    
    st.markdown(f"<p style='text-align:center;color:white;font-weight:600;font-size:14px;margin:15px 0 8px;'>{t('other',lang)}</p>", unsafe_allow_html=True)
    
    cols = st.columns(len(feat))
    for i,(k,v) in enumerate(feat):
        with cols[i]:
            if st.button(v['emoji'], key=f"p_{k}", help=v['title'], use_container_width=True):
                st.session_state.cur = k
                st.session_state.done = False
                st.session_state.ad_shown = False
                st.rerun()

# ============================================
# 📜 푸터 (법적 보호)
# ============================================
def footer(lang):
    st.markdown(f"""
    <div class="disclaimer-box">
        {t('disclaimer', lang)}
    </div>
    <div class="footer">
        <p>{t('privacy', lang)}</p>
        <p>{t('copyright', lang)}</p>
        <p>© {datetime.now().year} MBTI Match Test</p>
        <p style="margin-top:8px;font-size:9px;opacity:0.7;">
            No real person's likeness is used. All character images are AI-generated.<br>
            This service is not affiliated with any entertainment companies.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 🎯 메인 앱
# ============================================
def main():
    mobile_css()
    
    # 초기화
    if 'cur' not in st.session_state: st.session_state.cur = 'anime'
    if 'lang' not in st.session_state: st.session_state.lang = 'ko'
    if 'done' not in st.session_state: st.session_state.done = False
    if 'user' not in st.session_state: st.session_state.user = {}
    if 'result' not in st.session_state: st.session_state.result = []
    if 'ad_shown' not in st.session_state: st.session_state.ad_shown = False
    
    lang = st.session_state.lang
    cur = st.session_state.cur
    cfg = TEST_CONFIG[cur]
    
    # 언어 선택 (간소화)
    lc = st.columns(2)
    with lc[0]:
        if st.button("🇰🇷 한국어", use_container_width=True, type="primary" if lang=='ko' else "secondary"):
            st.session_state.lang = 'ko'; st.rerun()
    with lc[1]:
        if st.button("🇺🇸 English", use_container_width=True, type="primary" if lang=='en' else "secondary"):
            st.session_state.lang = 'en'; st.rerun()
    
    # 메뉴 (2줄 5개씩)
    tests = list(TEST_CONFIG.items())
    for row in [tests[:5], tests[5:]]:
        cols = st.columns(5)
        for i,(k,v) in enumerate(row):
            with cols[i]:
                tp = "primary" if k==cur else "secondary"
                if st.button(v['emoji'], key=f"m_{k}", use_container_width=True, type=tp):
                    st.session_state.cur = k
                    st.session_state.done = False
                    st.session_state.ad_shown = False
                    st.rerun()
    
    # 헤더
    title = cfg['title_full'].get(lang, cfg['title_full']['en'])
    st.markdown(f"""
    <div style="text-align:center;padding:10px 0;">
        <div style="font-size:clamp(36px,10vw,48px);">{cfg['emoji']}</div>
        <h2 style="color:white;margin:5px 0;font-size:clamp(16px,4.5vw,22px);word-break:keep-all;">{title}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.done:
        # 입력 폼
        st.markdown('<div class="card">', unsafe_allow_html=True)
        prev = st.session_state.user
        
        with st.form("f"):
            # 닉네임
            name = st.text_input(t('nick',lang), value=prev.get('name',''), 
                                placeholder=t('nick_ph',lang), max_chars=12)
            
            # MBTI + 성별 + 나이 (3열)
            c1, c2, c3 = st.columns(3)
            mlist = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
                    "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]
            with c1:
                idx = mlist.index(prev.get('mbti','ENFP')) if prev.get('mbti') in mlist else 7
                mbti = st.selectbox(t('mbti',lang), mlist, index=idx)
            with c2:
                gender = st.radio(t('gender',lang), [t('m',lang), t('f',lang)], horizontal=True)
            with c3:
                age = st.selectbox(t('age',lang), t('ages',lang))
            
            # 성격 선택
            st.markdown(f"**{t('pers',lang)}**")
            pk = ["따뜻한","냉정한","열정적인","차분한","활발한",
                  "겸손한","배려심많은","독립적인","낙천적인","유머러스한"]
            
            sel = []
            # 3-4-3 배치
            for grp in [pk[:3], pk[3:7], pk[7:]]:
                gc = st.columns(len(grp))
                for i,k in enumerate(grp):
                    with gc[i]:
                        lbl = t('p',lang).get(k,k)
                        if st.checkbox(lbl, key=f"p_{k}", value=k in prev.get('pers',[])):
                            sel.append(k)
            
            # 선택 피드백
            if len(sel) != 3:
                st.caption(f"{'선택' if lang=='ko' else 'Selected'}: {len(sel)}/3")
            
            # 카테고리 질문
            qt = cfg.get('question_type', 'relationship')
            qc = QUESTIONS.get(qt, QUESTIONS['relationship']).get(lang, QUESTIONS[qt]['en'])
            cat = st.radio(qc['q'], list(qc['o'].keys()), 
                          format_func=lambda x: qc['o'][x], horizontal=True)
            
            # 제출
            if st.form_submit_button(t('submit',lang), use_container_width=True, type="primary"):
                if not name.strip():
                    st.error("⚠️ " + ("닉네임 필요" if lang=='ko' else "Name required"))
                elif len(sel) != 3:
                    st.error("⚠️ " + ("3개 선택" if lang=='ko' else "Select 3"))
                else:
                    st.session_state.user = {
                        'name': name.strip()[:12], 'mbti': mbti, 
                        'gender': gender, 'age': age, 'pers': sel
                    }
                    data = load(cfg['data_file'], cfg)
                    if data:
                        st.session_state.result = match(data, mbti, sel)
                        st.session_state.done = True
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # 결과
        u = st.session_state.user
        r = st.session_state.result
        
        if r:
            top = r[0]
            sc = int(top.get('score', 80))
            
            # 점수 메시지
            if sc >= 90: msg = "💕 Perfect!"
            elif sc >= 80: msg = "💖 Great!"
            else: msg = "💗 Good!"
            
            st.markdown(f"""
            <div class="result">
                <p style="color:#667eea;font-size:clamp(12px,3vw,15px);">
                    {t('result',lang).format(u['name'])}
                </p>
                <img src="{top.get('image_url','')}" class="match-img" 
                     onerror="this.src='https://robohash.org/fallback.png?set=set5&size=300x300'"
                     loading="lazy" alt="match">
                <div class="match-name">{top['name']}</div>
                <div class="match-series">{top.get('series','')}</div>
                <div class="score-box">
                    <div style="color:rgba(255,255,255,0.8);font-size:10px;">{t('rate',lang)}</div>
                    <div class="score-num">{sc}%</div>
                    <div style="color:white;font-size:12px;">{msg}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 태그
            tags = ''.join([f'<span class="tag">{t("p",lang).get(p,p)}</span>' 
                           for p in top.get('personality',[])[:4]])
            st.markdown(f'<div style="text-align:center;margin:8px 0;">{tags}</div>', unsafe_allow_html=True)
            
            # MBTI
            st.markdown(f'<div style="text-align:center;"><span class="mbti-badge">{top.get("mbti","?")}</span></div>', unsafe_allow_html=True)
            
            # 광고 (1회)
            ad(lang)
            
            # 공유
            share(top['name'], sc, cfg['title_en'], lang)
            
            # 다시하기
            if st.button(t('retry',lang), use_container_width=True):
                st.session_state.done = False
                st.session_state.result = []
                st.session_state.ad_shown = False
                st.rerun()
    
    # 크로스 프로모션
    promo(cur, lang)
    
    # 푸터 (법적 보호)
    footer(lang)

if __name__ == "__main__":
    main()
