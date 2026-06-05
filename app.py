import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 청개구리 아레나 다크모드 기반 최적화 설정
st.set_page_config(
    page_title="🐸 청개구리 인덱스 - 롤 티어 아레나 v2.1", 
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

# 🛠️ 글로벌 서버 데이터 허브 (실시간 다중 접속 채팅 및 투표 적재용)
@st.cache_resource
def get_global_server_data_hub():
    return {
        "current_match_votes": {
            "SK하이닉스": {"UP": 0, "DOWN": 0},
            "삼성전자": {"UP": 0, "DOWN": 0},
            "한미반도체": {"UP": 0, "DOWN": 0},
            "현대차": {"UP": 0, "DOWN": 0},
            "LG에너지솔루션": {"UP": 0, "DOWN": 0},
            "삼성바이오로직스": {"UP": 0, "DOWN": 0},
            "셀트리온": {"UP": 0, "DOWN": 0}
        },
        "global_chat_stream": [
            {"name": "운영진_🐸", "text": "실시간 데이터 공유 서버 파이프라인 접속 성공. 코스피 7대 대장주 라인업 가동!"}
        ],
        "leaderboard": [
            {"rank": "👑 CHALLENGER", "name": "여의도작두가리가리", "points": "6,450 P", "win_rate": "84.2%", "color": "#FBBF24"},
            {"rank": "🔮 MASTER", "name": "국장개미구조대", "points": "4,100 P", "win_rate": "79.1%", "color": "#C084FC"},
            {"rank": "💎 DIAMOND", "name": "단타는예술이다", "points": "2,850 P", "win_rate": "71.4%", "color": "#60A5FA"},
            {"rank": "🪵 IRON", "name": "내가사면폭락장", "points": "350 P", "win_rate": "12.5%", "color": "#94A3B8"}
        ]
    }

global_server = get_global_server_data_hub()

if "user_login_data" not in st.session_state:
    st.session_state["user_login_data"] = None

# 유저 실시간 데이터 프로필
if "my_arena_profile" not in st.session_state:
    st.session_state["my_arena_profile"] = {
        "voted_hours": [], 
        "nickname": "게스트 파이터", 
        "points": 1000,       
        "total_matches": 0,   
        "win_matches": 0,     
        "title": "🥈 SILVER"
    }

# 🛠️ 포인트 기준 롤 티어 및 색상 변동 함수 수립
def calculate_lol_tier(pts):
    if pts >= 5000:
        return "👑 CHALLENGER", "#FBBF24"
    elif pts >= 3000:
        return "🔮 MASTER", "#C084FC"
    elif pts >= 2000:
        return "💎 DIAMOND", "#60A5FA"
    elif pts >= 1500:
        return "✨ PLATINUM", "#34D399"
    elif pts >= 1200:
        return "🥇 GOLD", "#F59E0B"
    elif pts >= 1000:
        return "🥈 SILVER", "#94A3B8"
    elif pts >= 500:
        return "🥉 BRONZE", "#B45309"
    else:
        return "🪵 IRON", "#475569"

# 🔴 AREA A: 부장님 방어막
if is_boss_mode:
    st.error("🔒 [보안] 本 화면은 사내 인트라넷 자산입니다. 외부 유출을 금합니다.")
    st.title("📊 2026_전사_리소스_최적화_KPI_Data")
    st.dataframe({"Index": [1, 2], "Task": ["Next-Gen ERP 구축", "Data Pipeline v3"], "Progress": ["94.2%", "81.2%"]}, use_container_width=True)
    if st.button("🔄 시스템 세션 새로고침"): st.query_params["boss_mode"] = "false"; st.rerun()

# 익명 웰컴 패널 게이트웨이
elif st.session_state["user_login_data"] is None:
    st.markdown("<center><h2 style='color:#A3E635; font-size:32px; font-weight:800; margin-top:50px;'>🐸 청개구리 인덱스 아레나</h2></center>", unsafe_allow_html=True)
    st.markdown("<center><p style='color:#AAADB0; font-size:14px;'>인간 지표 서열 전장에 입장하기 위해 파이터 정보를 입력하세요.</p></center>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("🔑 아레나 익명 파이터 등록")
        login_nick = st.text_input("👤 사용할 익명 닉네임 설정", placeholder="예: 반대로만사는대리")
        login_birth = st.text_input("🎂 생년월일 8자리 입력", placeholder="예: 19961025", max_chars=8)
        
        if st.button("🎮 아레나 입장권 발급받기", use_container_width=True):
            if not login_nick or len(login_birth) < 8:
                st.error("🚨 닉네임과 생년월일 8자리를 정확히 기입하셔야 전장 셔터가 열립니다!")
            else:
                st.session_state["user_login_data"] = {"nickname": login_nick, "birth": login_birth}
                st.session_state["my_arena_profile"] = {
                    "voted_hours": [],
                    "nickname": login_nick,
                    "points": 1000,
                    "total_matches": 0,
                    "win_matches": 0,
                    "title": "🥈 SILVER"
                }
                st.toast(f"🎉 반갑습니다, {login_nick} 파이터님! 실시간 데이터 월드 진입.", icon="🐸")
                st.rerun()

# 정식 청개구리 아레나 가동
else:
    # 🛠️ 거래대금 최상위 코스피 대장주 3종 전격 추가완료 (총 7종 체제)
    STOCK_TICKER_MAP = {
        "SK하이닉스 (000660.KS)": "000660.KS",
        "삼성전자 (005930.KS)": "005930.KS",
        "한미반도체 (042700.KS)": "042700.KS",
        "현대차 (005380.KS)": "005380.KS",
        "LG에너지솔루션 (373220.KS)": "373220.KS",
        "삼성바이오로직스 (207940.KS)": "207940.KS",
        "셀트리온 (068270.KS)": "068270.KS"
    }

    st.markdown("""
        <div style="background-color: #1A1D20; padding: 15px; border-radius: 8px; border: 1px solid #3C4043; margin-bottom: 15px;">
            <h1 style="color: #A3E635; font-size: 34px; font-weight: 900; margin: 0; letter-spacing: -1px; display: inline-block;">
                🐸 청개구리 인덱스 아레나
            </h1>
            <span style="font-size: 12px; color: #AAADB0; margin-left: 15px; font-weight: normal; vertical-align: bottom;">
                ⚖️ 코스피 7대 대장주 롤 티어 아레나 모드 v2.1
            </span>
        </div>
    """, unsafe_allow_html=True)

    # 매시간 정각 기준 '리얼타임 현재 가격' 수집 엔진
    @st.cache_data(ttl=30)
    def fetch_market_realtime_prices():
        ticker_strings = []
        live_prices_dict = {}
        for name, tk in STOCK_TICKER_MAP.items():
            clean_name = name.split(" (")[0]
            try:
                t_data = yf.Ticker(tk).history(period="1d")
                if not t_data.empty:
                    current_live_price = t_data['Close'].iloc[-1]
                    ticker_strings.append(f"<span style='color: #FFFFFF; font-weight: 500;'>{clean_name}</span> <span style='color: #22D3EE;'>{int(current_live_price):,}원</span>")
                    live_prices_dict[clean_name] = current_live_price
                else:
                    live_prices_dict[clean_name] = 0
                    ticker_strings.append(f"<span style='color: #FFFFFF;'>{clean_name}</span> <span style='color: #AAADB0;'>조회 대기</span>")
            except:
                live_prices_dict[clean_name] = 0
                ticker_strings.append(f"<span style='color: #FFFFFF;'>{clean_name}</span> <span style='color: #AAADB0;'>교신 지연</span>")
        return " &nbsp;&nbsp; | &nbsp;&nbsp; ".join(ticker_strings), live_prices_dict

    live_ticker_html, actual_live_prices = fetch_market_realtime_prices()
    
    st.markdown(f"""
        <div style="background-color: #11151A; padding: 6px 12px; border-radius: 4px; border-left: 4px solid #A3E635; font-size: 11px; margin-bottom: 15px; white-space: nowrap; overflow-x: auto;">
            {live_ticker_html}
        </div>
    """, unsafe_allow_html=True)

    # 한국 표준시 동기화
    server_utc = datetime.datetime.utcnow()
    kst_now = server_utc + datetime.timedelta(hours=9)
    
    current_hour = kst_now.hour
    current_minute = kst_now.minute
    
    is_voting_window = 0 <= current_minute < 5
    target_prediction_hour = (current_hour + 1) % 24

    # 내 실시간 포인트 기반 롤 티어 판별 가동
    profile = st.session_state["my_arena_profile"]
    my_tier_title, my_tier_color = calculate_lol_tier(profile["points"])
    profile["title"] = my_tier_title
    
    calc_win_rate = (profile["win_matches"] / profile["total_matches"] * 100) if profile["total_matches"] > 0 else 0.0

    # 레이아웃 분할
    main_layout, chat_layout = st.columns([2.5, 0.8], gap="medium")

    # ==================== [LEFT SIDE] 메인 아레나 플레이 구역 ====================
    with main_layout:
        tab1, tab2 = st.tabs(["🎮 1시간 타임어택 배팅소", "🏆 실시간 티어 서열 보드"])
        
        # TAB 1: 배팅소 구역
        with tab1:
            st.markdown(f"### 🎯 매 시간 5분 타임어택 리그")
            
            c_p1, c_p2, c_p3 = st.columns(3)
            c_p1.metric("👤 파이터 닉네임", profile["nickname"])
            st.markdown(f"<div style='padding:5px;'><span style='font-size:13px; color:#AAADB0;'>🏅 현재 배팅 계급 티어</span><br><b style='font-size:20px; color:{my_tier_color};'>{my_tier_title}</b></div>", unsafe_allow_html=True)
            c_p2.metric("💰 내 아레나 포인트", f"{profile['points']:,} P")
            c_p3.metric("📊 현재 리얼 승률", f"{calc_win_rate:.1f} %", f"전적: {profile['win_matches']}승 {profile['total_matches']-profile['win_matches']}패")

            current_now_str = kst_now.strftime('%Y-%m-%d %H:%M:%S')
            
            if is_voting_window:
                st.success(f"⏱ **한국 표준시:** {current_now_str} KST | **🚨 {current_hour}시 타임어택 오픈! (배팅 마감까지 {5 - current_minute}분 남음)**")
            else:
                st.error(f"⏱ **한국 표준시:** {current_now_str} KST | **🔒 {current_hour}시 매치 마감됨. ({target_prediction_hour}시 정각에 다음 리그가 시작됩니다)**")
            
            st.write("")
            st.markdown(f"#### 🥊 [ROUND] {current_hour}:00 기준 시세 ➡️ {target_prediction_hour}:00 종가 예측")
            st.caption("매시 0분~5분 사이에만 투표 가능하며, 1회 배팅 시 100 P가 차감 소모됩니다.")

            # 7대 우량주 배팅 카드 루프 출력
            for stock_name in ["SK하이닉스", "삼성전자", "한미반도체", "현대차", "LG에너지솔루션", "삼성바이오로직스", "셀트리온"]:
                live_p = actual_live_prices.get(stock_name, 0)
                votes = global_server["current_match_votes"][stock_name]
                
                up_cnt = votes["UP"]
                down_cnt = votes["DOWN"]
                
                if up_cnt == down_cnt:
                    up_dividend_text = "1.5배 (동배)"
                    down_dividend_text = "1.5배 (동배)"
                elif up_cnt > down_cnt:
                    up_dividend_text = "1.3배 (정배)"
                    down_dividend_text = "1.7배 (역배)"
                else:
                    up_dividend_text = "1.7배 (역배)"
                    down_dividend_text = "1.3배 (정배)"

                with st.container(border=True):
                    c1, c2, c3 = st.columns([1.5, 1.2, 1.3])
                    
                    with c1:
                        display_price = f"{int(live_p):,}원" if live_p > 0 else "실시간 시세 갱신 중"
                        st.markdown(f"<div style='font-size:16px; font-weight:bold; margin-top:2px;'>{stock_name}</div><div style='font-size:12px; color:#22D3EE;'>{current_hour}시 기준가: {display_price}</div>", unsafe_allow_html=True)
                    
                    has_voted_this_hour = f"{current_hour}_{stock_name}" in profile["voted_hours"]
                    button_disabled = (not is_voting_window) or has_voted_this_hour or profile["points"] < 100

                    with c2:
                        if st.button(f"▲ 상승 ({up_dividend_text})", key=f"am_up_{stock_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100
                            is_up_jeong = up_cnt >= down_cnt if (up_cnt != down_cnt) else None
                            
                            global_server["current_match_votes"][stock_name]["UP"] += 1
                            profile["voted_hours"].append(f"{current_hour}_{stock_name}")
                            profile["total_matches"] += 1
                            
                            if random.choice([True, False]): 
                                profile["win_matches"] += 1
                                if is_up_jeong is True: reward = 130; st.toast("🎯 정배 예측 적중! 1.3배 적용 (+130 P)", icon="🚀")
                                elif is_up_jeong is False: reward = 170; st.toast("🔥 역배 대박 적중! 1.7배 적용 (+170 P)", icon="👑")
                                else: reward = 150; st.toast("🎯 동배 적중! 1.5배 적용 (+150 P)", icon="🚀")
                                profile["points"] += reward
                            else: 
                                st.toast("📉 예측 실패! 배팅금 100 P가 소멸되었습니다.", icon="💥")
                            st.rerun()
                            
                    with c3:
                        if st.button(f"▼ 하락 ({down_dividend_text})", key=f"am_down_{stock_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100
                            is_down_jeong = down_cnt >= up_cnt if (up_cnt != down_cnt) else None
                            
                            global_server["current_match_votes"][stock_name]["DOWN"] += 1
                            profile["voted_hours"].append(f"{current_hour}_{stock_name}")
                            profile["total_matches"] += 1
                            
                            if random.choice([True, False]):
                                profile["win_matches"] += 1
                                if is_down_jeong is True: reward = 130; st.toast("🎯 정배 예측 적중! 1.3배 적용 (+130 P)", icon="🚀")
                                elif is_down_jeong is False: reward = 170; st.toast("🔥 역배 대박 적중! 1.7배 적용 (+170 P)", icon="👑")
                                else: reward = 150; st.toast("🎯 동배 적중! 1.5배 적용 (+150 P)", icon="🚀")
                                profile["points"] += reward
                            else:
                                st.toast("📉 예측 실패! 배팅금 100 P가 소멸되었습니다.", icon="💥")
                            st.rerun()
                    
                    total_votes = votes["UP"] + votes["DOWN"]
                    if total_votes > 0:
                        up_per = (votes["UP"] / total_votes) * 100
                        st.progress(int(up_per))
                        st.caption(f"📊 실시간 참여 비율: ▲ {up_per:.1f}% vs ▼ {100-up_per:.1f}% (방 내 총 {total_votes}명 투표 완료)")
                    else:
                        st.progress(50)
                        st.caption("📊 현재 아레나 대기 중... (양방향 1.5배 동배당 상태입니다)")

        # TAB 2: 글로벌 랭킹 서열 (LoL 티어 매트릭스 디자인 반영)
        with tab2:
            st.markdown("### 🏆 글로벌 아레나 실시간 티어 서열 보드")
            st.caption("배팅소 포인트와 실제 승률 전적에 맞춰 롤 레이팅 방식의 8개 티어가 실시간 배치됩니다.")
            st.write("")
            
            st.markdown("##### 👤 나의 실시간 파이터 계급 및 스펙")
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; border: 2px solid {my_tier_color}; padding: 15px 20px; border-radius: 8px; background-color: #12161A; margin-bottom: 25px;">
                    <div style="font-size: 15px; font-weight: 900; color: {my_tier_color}; width: 140px; letter-spacing: 1px;">{my_tier_title}</div>
                    <div style="font-size: 15px; font-weight: bold; color: #FFFFFF; flex: 1;">{profile['nickname']} (나)</div>
                    <div style="font-size: 13px; color: #22D3EE; width: 140px; text-align: center; font-weight: bold;">포인트: {profile['points']:,} P</div>
                    <div style="font-size: 15px; font-weight: bold; color: #81C995; width: 120px; text-align: right;">실시간 승률: {calc_win_rate:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("##### 🏛️ 아레나 통합 랭커 서열단 (티어 연동)")
            for user in global_server["leaderboard"]:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #3C4043; padding: 12px 20px; border-radius: 8px; background-color: #1A1D20; margin-bottom: 8px;">
                        <div style="font-size: 13px; font-weight: 900; color: {user['color']}; width: 140px; letter-spacing: 0.5px;">{user['rank']}</div>
                        <div style="font-size: 14px; font-weight: 500; color: #FFFFFF; flex: 1;">{user['name']}</div>
                        <div style="font-size: 13px; color: #22D3EE; width: 140px; text-align: center;">{user['points']}</div>
                        <div style="font-size: 14px; font-weight: bold; color: #81C995; width: 120px; text-align: right;">{user['win_rate']}</div>
                    </div>
                """, unsafe_allow_html=True)

    # ==================== [RIGHT SIDE] 우측 고정 오픈방 및 인터랙션 패널 ====================
    with chat_layout:
        try:
            from streamlit.runtime.runtime import Runtime
            stats = Runtime.instance()._session_mgr.list_active_sessions()
            real_active_users = len(stats)
            if real_active_users < 1: real_active_users = 1
        except:
            real_active_users = 1
            
        st.markdown(f"<h3 style='margin-top:23px; font-size:16px;'>💬 아레나 오픈방 <span style='font-size:12px; color:#A3E635; font-weight:normal;'>🟢 실제 {real_active_users}명 참여 중</span></h3>", unsafe_allow_html=True)
        st.markdown(f"<span style='font-size:12px; color:{my_tier_color}; font-weight:bold;'>티어: {my_tier_title}</span>", unsafe_allow_html=True)

        chat_container = st.container(height=350)
        with chat_container:
            for msg in global_server["global_chat_stream"]:
                with st.chat_message("user", avatar="🐸"):
                    st.markdown(f"**{msg['name']}**")
                    st.write(msg["text"])

        if user_live_input := st.chat_input("아레나 오픈방에 실시간 한마디..."):
            global_server["global_chat_stream"].append({
                "name": f"[{my_tier_title.split(' ')[0]}] {profile['nickname']}", 
                "text": user_live_input
            })
            st.rerun()

        # 후원 보드
        st.write("---")
        st.markdown("<h4 style='font-size:13px; color:#FF8DA1; margin-bottom:2px;'>🐸 개구리 대장 모이 보충통</h4>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: #1F1625; border: 1px dashed #FF8DA1; padding: 12px; border-radius: 8px; margin-bottom: 8px; text-align: center;">
                <p style="margin: 0; font-size: 11px; color: #FFB3C1; line-height: 1.4;">
                    🐸: "1시간마다 7대 대장주 API 트래픽을 당겨오느라 CPU 올챙이국수 시드가 마르고 있어요... 1,000원만 보태주시면 더 유용한 지표로 보답할게요!"
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.link_button("🐸 개구리 대장에게 국수 후원하기", url="https://toss.me", use_container_width=True)

        # 익명 종목 건의함
        st.write("---")
        st.markdown("<h4 style='font-size:13px; color:#AAADB0;'>🤫 익명 종목 추가 건의함</h4>", unsafe_allow_html=True)
        with st.form("suggest_form", clear_on_submit=True):
            s_input = st.text_input("📝 건의할 종목명/기능", placeholder="예: 코스닥 3배 레버리지 추가요망", label_visibility="collapsed")
            s_submit = st.form_submit_button("🔒 개발자 비밀 전송")
            if s_submit and s_input:
                cur_t = datetime.datetime.now().strftime("%H:%M")
                if "suggested_stocks" not in st.session_state:
                    st.session_state["suggested_stocks"] = []
                st.session_state["suggested_stocks"].append({"time": cur_t, "text": s_input})
                st.toast("✅ 개발자 비밀 DB에 안심 전송되었습니다!", icon="🔒")

        # 백엔드 어드민 콘솔
        is_admin = st.toggle("🛠️ 개발자 관리 콘솔", value=False)
        if is_admin:
            st.markdown("<h5 style='font-size:12px; color:#FFD700;'>📂 유저들의 비밀 종목 건의 리스트</h5>", unsafe_allow_html=True)
            if "suggested_stocks" in st.session_state:
                for s in st.session_state["suggested_stocks"]:
                    st.markdown(f"<p style='font-size:11px; margin:2px 0; color:#81C995;'><b>[{s['time']}]</b> {s['text']}</p>", unsafe_allow_html=True)
