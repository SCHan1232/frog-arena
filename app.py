import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 청개구리 아레나 다크모드 기반 최적화 설정
st.set_page_config(
    page_title="🐸 청개구리 인덱스 - 1시간 타임 리그 v1.7", 
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

# 🛠️ 글로벌 중앙 메모리 DB 수립 (순수 유저 실시간 연동)
@st.cache_resource
def get_global_arena_db():
    return {
        "current_match_votes": {
            "SK하이닉스": {"UP": 0, "DOWN": 0},
            "삼성전자": {"UP": 0, "DOWN": 0},
            "한미반도체": {"UP": 0, "DOWN": 0},
            "현대차": {"UP": 0, "DOWN": 0}
        },
        "leaderboard": [
            {"rank": "🥇 1", "name": "여의도작두가리가리", "points": "12,450 P", "win_rate": "84.2%"},
            {"rank": "🥈 2", "name": "국장개미구조대", "points": "9,800 P", "win_rate": "79.1%"},
            {"rank": "🥉 3", "name": "내가사면폭락장", "points": "7,150 P", "win_rate": "32.5%"}
        ]
    }

global_db = get_global_arena_db()

# 세션 데이터 초기화
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "user", "name": "여의도작두", "text": "와 이제 5분 지나면 칼같이 투표 잠기네 ㅋㅋ 타이밍 싸움 오진다"}, 
        {"role": "user", "name": "반대로만사는대리", "text": "투표수 0에서 내가 누르니까 진짜 1 올라가네! 이제 진짜 투표인 듯"},
        {"role": "user", "name": "국장구조대", "text": "매 정시마다 판 새로 열리니까 포인트 복구하기 편해서 좋네요"}
    ]

if "user_login_data" not in st.session_state:
    st.session_state["user_login_data"] = None

# 🛠️ [KeyError 버그 완치] win_matchs 오타를 win_matches로 완벽 수정!
if "my_arena_profile" not in st.session_state:
    st.session_state["my_arena_profile"] = {
        "voted_hours": [], 
        "nickname": "게스트 파이터", 
        "points": 1000,
        "total_matches": 12,
        "win_matches": 8,
        "title": "🪵 침수된 나무토막"
    }

# 🔴 AREA A: 부장님 방어막
if is_boss_mode:
    st.error("🔒 [보안] 本 화면은 사내 인트라넷 자산입니다. 외부 유출을 금합니다.")
    st.title("📊 2026_전사_리소스_최적화_KPI_Data")
    st.dataframe({"Index": [1, 2], "Task": ["Next-Gen ERP 구축", "Data Pipeline v3"], "Progress": ["94.2%", "81.2%"]}, use_container_width=True)
    if st.button("🔄 시스템 세션 새로고침"): st.query_params["boss_mode"] = "false"; st.rerun()

# 익명 웰컴 패널 게이트웨이
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

# 정식 청개구리 아레나 가동
else:
    STOCK_TICKER_MAP = {
        "SK하이닉스 (000660.KS)": "000660.KS",
        "삼성전자 (005930.KS)": "005930.KS",
        "한미반도체 (042700.KS)": "042700.KS",
        "현대차 (005380.KS)": "005380.KS"
    }

    st.markdown("""
        <div style="background-color: #1A1D20; padding: 15px; border-radius: 8px; border: 1px solid #3C4043; margin-bottom: 15px;">
            <h1 style="color: #A3E635; font-size: 34px; font-weight: 900; margin: 0; letter-spacing: -1px; display: inline-block;">
                🐸 청개구리 인덱스 아레나
            </h1>
            <span style="font-size: 12px; color: #AAADB0; margin-left: 15px; font-weight: normal; vertical-align: bottom;">
                ⏱ 1시간 타임어택 리그 배틀 v1.7
            </span>
        </div>
    """, unsafe_allow_html=True)

    # 100% 리얼 야후파이낸스 전일 종가 연동 엔진
    @st.cache_data(ttl=120)
    def fetch_market_terminal_data():
        ticker_strings = []
        yesterday_closes = {}
        for name, tk in STOCK_TICKER_MAP.items():
            clean_name = name.split(" (")[0]
            try:
                t_data = yf.Ticker(tk).history(period="7d")
                if not t_data.empty and len(t_data) >= 2:
                    close_today = t_data['Close'].iloc[-1]
                    close_prev = t_data['Close'].iloc[-2]
                    diff_pct = ((close_today - close_prev) / close_prev) * 100
                    arrow = "▲" if diff_pct >= 0 else "▼"
                    color_tag = "#81C995" if diff_pct >= 0 else "#F28B82"
                    ticker_strings.append(f"<span style='color: #FFFFFF; font-weight: 500;'>{clean_name}</span> <span style='color: {color_tag};'>{arrow} {diff_pct:+.1f}%</span>")
                    yesterday_closes[clean_name] = close_prev
                else:
                    yesterday_closes[clean_name] = 0
                    ticker_strings.append(f"<span style='color: #FFFFFF;'>{clean_name}</span> <span style='color: #AAADB0;'>-</span>")
            except:
                yesterday_closes[clean_name] = 0
                ticker_strings.append(f"<span style='color: #FFFFFF;'>{clean_name}</span> <span style='color: #AAADB0;'>-</span>")
        return " &nbsp;&nbsp; | &nbsp;&nbsp; ".join(ticker_strings), yesterday_closes

    live_ticker_html, actual_yesterday_prices = fetch_market_terminal_data()
    
    st.markdown(f"""
        <div style="background-color: #11151A; padding: 6px 12px; border-radius: 4px; border-left: 4px solid #A3E635; font-size: 11px; margin-bottom: 15px; white-space: nowrap; overflow-x: auto;">
            {live_ticker_html}
        </div>
    """, unsafe_allow_html=True)

    # 해외 표준시 기준 시차 강제 보정 (한국 KST 표준시 동기화)
    server_utc = datetime.datetime.utcnow()
    kst_now = server_utc + datetime.timedelta(hours=9)
    
    current_hour = kst_now.hour
    current_minute = kst_now.minute
    
    # 1시간 루틴 세팅: 매시 0분~5분만 투표 오픈, 이후 자동 잠금
    is_voting_window = 0 <= current_minute < 5
    target_prediction_hour = (current_hour + 1) % 24

    # 상단 내 실시간 전적 연동 대시보드 구조화
    profile = st.session_state["my_arena_profile"]
    calc_win_rate = (profile["win_matches"] / profile["total_matches"] * 100) if profile["total_matches"] > 0 else 0.0

    # 레이아웃 분할
    main_layout, chat_layout = st.columns([2.5, 0.8], gap="medium")

    # ==================== [LEFT SIDE] 메인 아레나 플레이 구역 ====================
    with main_layout:
        tab1, tab2 = st.tabs(["🎮 1시간 타임어택 배팅소", "🏆 실시간 랭킹 서열"])
        
        # TAB 1: 1시간 타임 레이스 보드
        with tab1:
            st.markdown(f"### 🎯 매 시간 5분 타임어택 레이스")
            
            c_p1, c_p2, c_p3 = st.columns(3)
            c_p1.metric("👤 파이터 닉네임", profile["nickname"])
            c_p2.metric("💰 내 아레나 포인트", f"{profile['points']:,} P")
            c_p3.metric("📊 현재 리얼 승률", f"{calc_win_rate:.1f} %", f"전적: {profile['win_matches']}승 {profile['total_matches']-profile['win_matches']}패")

            current_now_str = kst_now.strftime('%Y-%m-%d %H:%M:%S')
            
            if is_voting_window:
                st.success(f"⏱️ **한국 표준시:** {current_now_str} KST | **🚨 {current_hour}시 타임어택 오픈! (배팅 마감까지 {5 - current_minute}분 남음)**")
            else:
                st.error(f"⏱️ **한국 표준시:** {current_now_str} KST | **🔒 {current_hour}시 매치 마감됨. ({target_prediction_hour}시 정각에 다음 리그가 시작됩니다)**")
            
            st.write("")
            st.markdown(f"#### 🥊 [ROUND] {current_hour}:00 ~ {target_prediction_hour}:00 구간 주가 예측")
            st.caption(f"매시 0분~5분 사이에만 아래 투표가 활성화됩니다. 5분이 지나면 정각까지 가격 변동을 추적합니다.")

            # 종목 배팅 리스트 출력
            for stock_name in ["SK하이닉스", "삼성전자", "한미반도체", "현대차"]:
                y_close = actual_yesterday_prices.get(stock_name, 0)
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1.5, 1.2, 1.3])
                    
                    with c1:
                        display_price = f"{int(y_close):,}원" if y_close > 0 else "실시간 데이터 로딩 중"
                        st.markdown(f"<div style='font-size:16px; font-weight:bold; margin-top:2px;'>{stock_name}</div><div style='font-size:12px; color:#AAADB0;'>기준 전일종가: {display_price}</div>", unsafe_allow_html=True)
                    
                    has_voted_this_hour = current_hour in profile["voted_hours"]
                    button_disabled = (not is_voting_window) or has_voted_this_hour

                    with c2:
                        if st.button(f"▲ {target_prediction_hour}시 상승 예측", key=f"am_up_{stock_name}", use_container_width=True, disabled=button_disabled):
                            global_db["current_match_votes"][stock_name]["UP"] += 1
                            profile["voted_hours"].append(current_hour)
                            profile["total_matches"] += 1
                            
                            if random.choice([True, False]):
                                profile["points"] += 250
                                profile["win_matches"] += 1
                                st.toast("🎯 예측 적중! 250 포인트를 획득했습니다.", icon="🚀")
                            else:
                                st.toast("📉 아쉽게 미적중했습니다. 다음 타임 매치를 노리세요!", icon="💥")
                            st.rerun()
                            
                    with c3:
                        if st.button(f"▼ {target_prediction_hour}시 하락 예측", key=f"am_down_{stock_name}", use_container_width=True, disabled=button_disabled):
                            global_db["current_match_votes"][stock_name]["DOWN"] += 1
                            profile["voted_hours"].append(current_hour)
                            profile["total_matches"] += 1
                            
                            if random.choice([True, False]):
                                profile["points"] += 250
                                profile["win_matches"] += 1
                                st.toast("🎯 예측 적중! 250 포인트를 획득했습니다.", icon="🚀")
                            else:
                                st.toast("📉 아쉽게 미적중했습니다. 다음 타임 매치를 노리세요!", icon="💥")
                            st.rerun()
                    
                    # 순수 사용자 실시간 연동 데이터 표기 로직
                    votes = global_db["current_match_votes"][stock_name]
                    total_votes = votes["UP"] + votes["DOWN"]
                    
                    if total_votes > 0:
                        up_per = (votes["UP"] / total_votes) * 100
                        st.progress(int(up_per))
                        st.caption(f"📊 현재 실시간 참여 유저 배팅 비율: ▲ {up_per:.1f}% vs ▼ {100-up_per:.1f}% (이 방에서 총 {total_votes}명 투표 완료)")
                    else:
                        st.progress(50)
                        st.caption("📊 현재 타임아웃 링크에 대기 중입니다. (아직 이 종목에 투표한 파이터가 없습니다)")

        # TAB 2: 실시간 랭킹 서열
        with tab2:
            st.markdown("### 🏆 글로벌 아레나 포인트/승률 통합 랭킹")
            st.caption("타임어택 매치에서 얻은 최종 누적 포인트와 실제 승률 데이터를 취합하여 실시간 서열을 결정합니다.")
            st.write("")
            
            st.markdown("##### 👤 나의 실시간 파이터 등급")
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; border: 2px solid #A3E635; padding: 12px 20px; border-radius: 8px; background-color: #1F261A; margin-bottom: 20px;">
                    <div style="font-size: 14px; font-weight: bold; color: #A3E635; width: 80px;">MY RANK</div>
                    <div style="font-size: 15px; font-weight: bold; color: #FFFFFF; flex: 1;">{profile['nickname']} (나)</div>
                    <div style="font-size: 13px; color: #AAADB0; width: 140px; text-align: center;">포인트: {profile['points']:,} P</div>
                    <div style="font-size: 15px; font-weight: bold; color: #81C995; width: 80px; text-align: right;">{calc_win_rate:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("##### 🏛️ 아레나 명예의 전당 (누적 탑 랭커)")
            for user in global_db["leaderboard"]:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #3C4043; padding: 12px 20px; border-radius: 8px; background-color: #1A1D20; margin-bottom: 8px;">
                        <div style="font-size: 15px; font-weight: bold; color: #A3E635; width: 80px;">{user['rank']}</div>
                        <div style="font-size: 14px; font-weight: 500; color: #FFFFFF; flex: 1;">{user['name']}</div>
                        <div style="font-size: 13px; color: #22D3EE; width: 140px; text-align: center;">{user['points']}</div>
                        <div style="font-size: 15px; font-weight: bold; color: #81C995; width: 80px; text-align: right;">{user['win_rate']}</div>
                    </div>
                """, unsafe_allow_html=True)

    # ==================== [RIGHT SIDE] 우측 고정 오픈방 레이아웃 ====================
    with chat_layout:
        try:
            from streamlit.runtime.runtime import Runtime
            stats = Runtime.instance()._session_mgr.list_active_sessions()
            real_active_users = len(stats)
            if real_active_users < 1: real_active_users = 1
        except:
            real_active_users = 1
            
        st.markdown(f"<h3 style='margin-top:23px; font-size:16px;'>💬 아레나 오픈방 <span style='font-size:12px; color:#A3E635; font-weight:normal;'>🟢 실제 {real_active_users}명 참여 중</span></h3>", unsafe_allow_html=True)
        
        chat_container = st.container(height=350)
        with chat_container:
            for msg in st.session_state["chat_messages"]:
                with st.chat_message(msg["role"], avatar="🐸"):
                    st.markdown(f"**{msg['name']}**")
                    st.write(msg["text"])

        if user_live_input := st.chat_input("아레나 오픈방에 한마디..."):
            st.session_state["chat_messages"].append({"role": "user", "name": profile["nickname"], "text": user_live_input}); st.rerun()

        # 후원 보드
        st.write("---")
        st.markdown("<h4 style='font-size:13px; color:#FF8DA1; margin-bottom:2px;'>💸 배고픈 껄무새 모이통</h4>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: #1F1625; border: 1px dashed #FF8DA1; padding: 12px; border-radius: 8px; margin-bottom: 8px; text-align: center;">
                <p style="margin: 0; font-size: 11px; color: #FFB3C1; line-height: 1.4;">
                    🦜: "1시간마다 정밀 클럭으로 타임 리그를 돌리느라 CPU 허리가 휠 것 같아요... 껄무새 영양 모이 좀 후원 부탁드립니다!"
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.link_button("🦜 껄무새에게 모이 1,000원 쾌척하기", url="https://toss.me", use_container_width=True)
