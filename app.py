import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 청개구리 아레나 다크모드 기반 최적화 설정
st.set_page_config(
    page_title="🐸 청개구리 인덱스 - 실시간 시계 무대 v1.3", 
    page_icon="🐸",
    layout="wide"
)

# 2. ⚡ 부장님 감지 패닉 버튼
js_panic_script = """
<script>
    let lastKeyTime = 0;
    window.parent.document.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            const currentTime = new Date().getTime();
            const keyGap = currentTime - lastKeyTime;
            if (keyGap < 300) {  
                const url = new URL(window.parent.location.href);
                url.searchParams.set('boss_mode', 'true');
                window.parent.location.href = url.href;
            }
            lastKeyTime = currentTime;
        }
    });
</script>
"""
components.html(js_panic_script, height=0, width=0)
is_boss_mode = st.query_params.get("boss_mode", "false") == "true"

# 🛠️ 글로벌 중앙 메모리 DB 수립
@st.cache_resource
def get_global_arena_db():
    return {
        "votes_am": {
            "SK하이닉스": {"UP": 142, "DOWN": 88},
            "삼성전자": {"UP": 95, "DOWN": 234},
            "한미반도체": {"UP": 184, "DOWN": 42},
            "현대차": {"UP": 110, "DOWN": 105}
        },
        "votes_pm": {
            "SK하이닉스": {"UP": 211, "DOWN": 156},
            "삼성전자": {"UP": 145, "DOWN": 312},
            "한미반도체": {"UP": 298, "DOWN": 93},
            "현대차": {"UP": 125, "DOWN": 164}
        },
        "live_fighters": []
    }

global_db = get_global_arena_db()

# 세션 데이터 독립 보안 포맷 설정
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "user", "name": "여의도작두", "text": "오전장 배팅 마감 얼마 안 남았는데 삼전 하방 쏠림 대박이네 ㅋㅋ"}, 
        {"role": "user", "name": "반대로만사는대리", "text": "현대차 상방 배팅 완료했습니다. 다들 반대 포지션 잡으세요."},
        {"role": "user", "name": "국장구조대", "text": "시간 보니까 정확히 12시 넘어야 오후장 배팅 셔터 열리네 로직 정밀함 굿"}
    ]
if "suggested_stocks" not in st.session_state:
    st.session_state["suggested_stocks"] = [
        {"time": "09:15", "text": "국장 테마주(코스닥) 전용 아레나방도 개설 원합니다!"}
    ]
# 🛠️ [2번 피드백 로그인 연동] 최초 진입 시 로그인 체크 세션
if "user_login_data" not in st.session_state:
    st.session_state["user_login_data"] = None

if "my_arena_profile" not in st.session_state:
    st.session_state["my_arena_profile"] = {
        "am_voted": False, 
        "pm_voted": False,
        "nickname": "게스트 파이터", 
        "win_rate": "?? %", 
        "title": "🪵 침수된 나무토막"
    }

# 🔴 AREA A: 부장님 방어막
if is_boss_mode:
    st.error("🔒 [보안] 本 화면은 사내 인트라넷 자산입니다. 외부 유출을 금합니다.")
    st.title("📊 2026_전사_리소스_최적화_KPI_Data")
    st.dataframe({"Index": [1, 2], "Task": ["Next-Gen ERP 구축", "Data Pipeline v3"], "Progress": ["94.2%", "81.2%"]}, use_container_width=True)
    if st.button("🔄 시스템 세션 새로고침"): st.query_params["boss_mode"] = "false"; st.rerun()

# 🛠️ [2번 피드백 로그인 모듈 구현] 익명 웰컴 패널 게이트웨이
elif st.session_state["user_login_data"] is None:
    st.markdown("<center><h2 style='color:#A3E635; font-size:32px; font-weight:800; margin-top:50px;'>🐸 청개구리 인덱스 아레나</h2></center>", unsafe_allow_html=True)
    st.markdown("<center><p style='color:#AAADB0; font-size:14px;'>인간 지표 서열 아레나에 입장하기 위해 프로필 정보를 기입하세요.</p></center>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("🔑 아레나 익명 파이터 등록")
        login_nick = st.text_input("👤 사용할 익명 닉네임 설정", placeholder="예: 반대로만사는대리")
        login_birth = st.text_input("🎂 생년월일 8자리 입력 (명리 점괘 매칭용)", placeholder="예: 19961025", max_chars=8)
        
        if st.button("🎮 아레나 입장권 발급받기", use_container_width=True):
            if not login_nick or len(login_birth) < 8:
                st.error("🚨 닉네임과 생년월일 8자리를 정확히 기입하셔야 입장 셔터가 열립니다!")
            else:
                st.session_state["user_login_data"] = {"nickname": login_nick, "birth": login_birth}
                st.session_state["my_arena_profile"]["nickname"] = login_nick
                st.toast(f"🎉 반갑습니다, {login_nick} 파이터님! 아레나 전장에 진입합니다.", icon="🐸")
                st.rerun()

# 🟢 AREA B: 로그인 통과 후 정식 청개구리 아레나 가동
else:
    STOCK_TICKER_MAP = {
        "SK하이닉스 (000660.KS)": "000660.KS",
        "삼성전자 (005930.KS)": "005930.KS",
        "한미반도체 (042700.KS)": "042700.KS",
        "현대차 (005380.KS)": "005380.KS"
    }

    # 🛠️ [1번 피드백 완치] 제목 렌더링 정상화 완료
    st.markdown("""
        <div style="background-color: #1A1D20; padding: 15px; border-radius: 8px; border: 1px solid #3C4043; margin-bottom: 15px;">
            <h1 style="color: #A3E635; font-size: 34px; font-weight: 900; margin: 0; letter-spacing: -1px; display: inline-block;">
                🐸 청개구리 인덱스 아레나
            </h1>
            <span style="font-size: 12px; color: #AAADB0; margin-left: 15px; font-weight: normal; vertical-align: bottom;">
                📊 국장 전용 2비트 타임어택 v1.3
            </span>
        </div>
    """, unsafe_allow_html=True)

    # 🛠️ [3번, 4번 피드백] 실시간 시간 분석 및 실제 어제 종가 크롤링 캐시 함수 수립
    @st.cache_data(ttl=600)
    def fetch_market_terminal_data():
        ticker_strings = []
        yesterday_closes = {}
        for name, tk in STOCK_TICKER_MAP.items():
            try:
                t_data = yf.Ticker(tk).history(period="5d")
                if len(t_data) >= 2:
                    close_today = t_data['Close'].iloc[-1]
                    close_prev = t_data['Close'].iloc[-2]
                    diff_pct = ((close_today - close_prev) / close_prev) * 100
                    arrow = "▲" if diff_pct >= 0 else "▼"
                    color_tag = "#81C995" if diff_pct >= 0 else "#F28B82"
                    clean_name = name.split(" (")[0]
                    ticker_strings.append(f"<span style='color: #FFFFFF; font-weight: 500;'>{clean_name}</span> <span style='color: {color_tag};'>{arrow} {diff_pct:+.1f}%</span>")
                    
                    # 🛠️ 4번 피드백: 종목별 가장 최근 장마감 종가 세팅 보존
                    yesterday_closes[clean_name] = close_prev
            except:
                yesterday_closes[clean_name.split(" (")[0]] = 0
        return " &nbsp;&nbsp; | &nbsp;&nbsp; ".join(ticker_strings), yesterday_closes

    live_ticker_html, actual_yesterday_prices = fetch_market_terminal_data()
    
    st.markdown(f"""
        <div style="background-color: #11151A; padding: 6px 12px; border-radius: 4px; border-left: 4px solid #A3E635; font-size: 11px; margin-bottom: 15px; white-space: nowrap; overflow-x: auto;">
            {live_ticker_html}
        </div>
    """, unsafe_allow_html=True)

    # 🛠️ 3번 피드백: 오전/오후 실시간 타임 커맨더 로직 구축
    now_time = datetime.datetime.now().time()
    am_cutoff_start = datetime.time(0, 0, 0)
    am_cutoff_end = datetime.time(12, 0, 0) # 낮 12시 정각 기준 분할
    
    is_am_match_open = am_cutoff_start <= now_time < am_cutoff_end
    is_pm_match_open = not is_am_match_open

    # 공포탐욕지수 메인 보드
    today_seed_gen = int(datetime.date.today().strftime('%Y%m%d'))
    random.seed(today_seed_gen)
    fg_index = random.randint(25, 82)
    fg_status = "📉 극단적 공포" if fg_index < 40 else "🚀 극단적 탐욕" if fg_index > 65 else "📊 중립 기어"
    fg_color = "#F28B82" if fg_index < 40 else "#81C995" if fg_index > 65 else "#8AB4F8"
    random.seed()

    # 레이아웃 분할
    main_layout, chat_layout = st.columns([2.5, 0.8], gap="medium")

    # ==================== [LEFT SIDE] 메인 아레나 플레이 구역 ====================
    with main_layout:
        tab1, tab2 = st.tabs(["🎮 아레나 타임어택 배팅소", "🏆 글로벌 인간지표 서열"])
        
        # TAB 1: 오전장 / 오후장 실시간 자동 셔터 연동 배팅소
        with tab1:
            st.markdown(f"### ⏱️ 대한민국 국장 타임어택 예측 레이스")
            st.caption(f"파이터명: **{st.session_state['my_arena_profile']['nickname']}** | 생년월일 시드: **{st.session_state['user_login_data']['birth']}**")
            
            # 현재 서버 시간 및 활성화 매치 직관적 안내 배너
            current_now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            st.info(f"⏱️ **현재 동기화 시각:** {current_now_str} | **오전 매치 상태:** {'🟢 활성화' if is_am_match_open else '🔒 마감(종료)'} | **오후 매치 상태:** {'🟢 활성화' if is_pm_match_open else '🔒 마감(대기)'}")
            st.write("")
            
            # 🥊 세션 1: 오전장 배팅 (시간에
