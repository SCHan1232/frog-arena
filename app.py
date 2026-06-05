import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 사이버펑크 아레나 초호화 다크 테마 설정
st.set_page_config(
    page_title="⚡ 청개구리 인덱스 - 10분 아레나 v2.3", 
    page_icon="⚡",
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
            {"name": "[CHALLENGER] 운영진_🐸", "text": "⚡ 10분 스피드 아레나 가동! 각 라운드 초반 1분간의 초고속 배팅 페이즈가 열립니다."}
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

# 포인트 기준 롤 티어 뱃지 스위칭 매트릭스
def calculate_lol_tier(pts):
    if pts >= 5000: return "👑 CHALLENGER", "#FBBF24"
    elif pts >= 3000: return "🔮 MASTER", "#C084FC"
    elif pts >= 2000: return "💎 DIAMOND", "#60A5FA"
    elif pts >= 1500: return "✨ PLATINUM", "#34D399"
    elif pts >= 1200: return "🥇 GOLD", "#F59E0B"
    elif pts >= 1000: return "🥈 SILVER", "#94A3B8"
    elif pts >= 500: return "🥉 BRONZE", "#B45309"
    else: return "🪵 IRON", "#475569"

# 🔴 AREA A: 부장님 방어막
if is_boss_mode:
    st.error("🔒 [보안] 本 화면은 사내 인트라넷 자산입니다. 외부 유출을 금합니다.")
    st.title("📊 2026_전사_리소스_최적화_KPI_Data")
    st.dataframe({"Index": [1, 2], "Task": ["Next-Gen ERP 구축", "Data Pipeline v3"], "Progress": ["94.2%", "81.2%"]}, use_container_width=True)
    if st.button("🔄 시스템 세션 새로고침"): st.query_params["boss_mode"] = "false"; st.rerun()

# 익명 웰컴 패널 게이트웨이
elif st.session_state["user_login_data"] is None:
    st.markdown("""
        <div style="text-align: center; margin-top: 60px;">
            <h1 style="color: #A3E635; font-size: 42px; font-weight: 900; letter-spacing: -2px; text-shadow: 0 0 15px rgba(163,230,53,0.6); margin-bottom: 5px;">
                ⚡ FROG ARENA TERMINAL
            </h1>
            <p style="color: #22D3EE; font-size: 13px; font-weight: bold; letter-spacing: 2px;">10분 라이브 무한 서열 아레나에 로그인하십시오.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<h3 style='color:#FFFFFF; font-size:16px; font-weight:bold; border-bottom:1px solid #334155; padding-bottom:8px;'>🎮 파이터 라이선스 링크</h3>", unsafe_allow_html=True)
        login_nick = st.text_input("👤 콜사인 익명 닉네임 설정", placeholder="예: 반대로만사는대리")
        login_birth = st.text_input("🎂 세션 동기화 생년월일 (8자리)", placeholder="예: 19961025", max_chars=8)
        
        if st.button("🚀 아레나 시스템 접속", use_container_width=True):
            if not login_nick or len(login_birth) < 8:
                st.error("🚨 전장 식별코드(닉네임/생년월일)가 유효하지 않습니다!")
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
                st.toast(f"⚡ 무한 10분 아레나 접속 완료. 파이터 {login_nick} 대기.", icon="⚡")
                st.rerun()

# 정식 청개구리 아레나 가동 (10분 주기 시스템)
else:
    STOCK_TICKER_MAP = {
        "SK하이닉스 (000660.KS)": "000660.KS",
        "삼성전자 (005930.KS)": "005930.KS",
        "한미반도체 (042700.KS)": "042700.KS",
        "현대차 (005380.KS)": "005380.KS",
        "LG에너지솔루션 (373220.KS)": "373220.KS",
        "삼성바이오로직스 (207940.KS)": "207940.KS",
        "셀트리온 (068270.KS)": "068270.KS"
    }

    # 최상단 아레나 네온 간판 헤더
    st.markdown("""
        <div style="background: linear-gradient(90deg, #1E1B4B 0%, #0F172A 100%); padding: 20px; border-radius: 12px; border: 2px solid #A3E635; box-shadow: 0 0 20px rgba(163,230,53,0.2); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="color: #A3E635; font-size: 36px; font-weight: 900; margin: 0; letter-spacing: -2px; text-shadow: 0 0 10px rgba(163,230,53,0.4);">
                    ⚡ FROG INDEX ARENA
                </h1>
                <p style="font-size: 11px; color: #38BDF8; margin: 4px 0 0 0; font-weight: bold; letter-spacing: 1px;">⏱️ 10-MIN INFINITE RELAY TOURNAMENT MODE v2.3</p>
            </div>
            <div style="background-color: #020617; border: 1px solid #38BDF8; padding: 6px 15px; border-radius: 20px; font-size: 11px; color: #38BDF8; font-weight: bold;">
                ⏳ 10분 단위 자동 주가 갱신 중
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 🛠️ [요청 피드백] 야후파이낸스 데이터를 10분(600초) 단위로 정밀 캐싱 동기화
    @st.cache_data(ttl=600)
    def fetch_market_10min_prices():
        ticker_strings = []
        live_prices_dict = {}
        for name, tk in STOCK_TICKER_MAP.items():
            clean_name = name.split(" (")[0]
            try:
                t_data = yf.Ticker(tk).history(period="1d")
                if not t_data.empty:
                    current_live_price = t_data['Close'].iloc[-1]
                    ticker_strings.append(f"<span style='color: #FFFFFF; font-weight: bold;'>{clean_name}</span> <span style='color: #22D3EE;'>{int(current_live_price):,}원</span>")
                    live_prices_dict[clean_name] = current_live_price
                else:
                    live_prices_dict[clean_name] = 0
                    ticker_strings.append(f"<span style='color: #64748B;'>{clean_name} 대기</span>")
            except:
                live_prices_dict[clean_name] = 0
                ticker_strings.append(f"<span style='color: #EF4444;'>{clean_name} 오류</span>")
        return " &nbsp;&nbsp; 🔴 &nbsp;&nbsp; ".join(ticker_strings), live_prices_dict

    live_ticker_html, actual_live_prices = fetch_market_10min_prices()
    
    st.markdown(f"""
        <div style="background-color: #020617; padding: 8px 15px; border-radius: 6px; border: 1px solid #1E293B; font-size: 11px; margin-bottom: 20px; white-space: nowrap; overflow-x: auto;">
            {live_ticker_html}
        </div>
    """, unsafe_allow_html=True)

    # 시차 교정 (한국 표준시 동기화) 및 10분 통제기 코어 가동
    server_utc = datetime.datetime.utcnow()
    kst_now = server_utc + datetime.timedelta(hours=9)
    current_hour = kst_now.hour
    current_minute = kst_now.minute
    current_second = kst_now.second
    
    # 🛠️ [요청 피드백] 10분 주기의 '초반 1분 미만' 일 때만 오픈 (예: 10분~11분, 20분~21분)
    minute_in_block = current_minute % 10
    is_voting_window = (minute_in_block == 0) # 0분층에 해당하는 60초간만 참(True)
    
    # 정산 기준이 될 다음 10분 정시 타겟 이름표 조립
    next_block_minute = ((current_minute // 10) + 1) * 10
    if next_block_minute >= 60:
        target_display_time = f"{(current_hour + 1) % 24}:00"
        match_id_string = f"{current_hour}_50_{stock_name}" if minute_in_block == 0 else f"{(current_hour + 1) % 24}_00"
    else:
        target_display_time = f"{current_hour}:{next_block_minute:02d}"
        match_id_string = f"{current_hour}_{(current_minute // 10) * 10:02d}"

    # 내 포인트 기반 실시간 롤 티어 랭크 산출
    profile = st.session_state["my_arena_profile"]
    my_tier_title, my_tier_color = calculate_lol_tier(profile["points"])
    profile["title"] = my_tier_title
    calc_win_rate = (profile["win_matches"] / profile["total_matches"] * 100) if profile["total_matches"] > 0 else 0.0

    # 좌우 구조 분할 레이아웃
    main_layout, chat_layout = st.columns([2.4, 0.9], gap="medium")

    # ==================== [LEFT SIDE] 메인 아레나 플레이 구역 ====================
    with main_layout:
        tab1, tab2 = st.tabs(["🎮 10분 초고속 터미널", "🏆 실시간 아레나 서열판"])
        
        # TAB 1: 배팅 터미널 구역
        with tab1:
            # 내 프로필 대시보드 박스
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0B0F19 0%, #030712 100%); border: 2px solid {my_tier_color}; box-shadow: 0 0 15px {my_tier_color}40; padding: 20px; border-radius: 10px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 11px; color: #64748B; font-weight: bold; letter-spacing: 1px;">👤 ARENA PILOT PROFILE</span>
                        <h3 style="margin: 3px 0 0 0; color: #FFFFFF; font-size: 22px; font-weight: 800;">{profile['nickname']}</h3>
                        <span style="display:inline-block; background-color:{my_tier_color}15; color:{my_tier_color}; padding:2px 10px; border-radius:4px; font-size:11px; font-weight:900; border:1px solid {my_tier_color}50; margin-top:5px;">{my_tier_title}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 11px; color: #64748B; font-weight: bold;">💰 MY CREDIT BALANCE</span>
                        <h2 style="margin: 0; color: #22D3EE; font-size: 24px; font-weight: 900; text-shadow: 0 0 8px rgba(34,211,238,0.3);">{profile['points']:,} P</h2>
                        <span style="font-size:12px; color:#81C995; font-weight:bold;">승률: {calc_win_rate:.1f}% ({profile['win_matches']}승/{profile['total_matches']}전)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            current_now_str = kst_now.strftime('%H:%M:%S')
            
            # 🛠️ [요청 피드백] 1분 타임어택 오픈 전광판 시각화 조립
            if is_voting_window:
                st.markdown(f"""
                    <div style="background-color: #064E3B; border: 1px solid #10B981; padding: 12px 15px; border-radius: 6px; color: #34D399; font-weight: bold; font-size: 13.5px; margin-bottom: 20px; box-shadow: 0 0 12px rgba(16,185,129,0.3);">
                        🔓 [OPEN] 초고속 10분 아레나 매치 활성화! (마감까지 {60 - current_second}초 남음! 지금 베팅하세요!)
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background-color: #7F1D1D; border: 1px solid #EF4444; padding: 12px 15px; border-radius: 6px; color: #FCA5A5; font-weight: bold; font-size: 13.5px; margin-bottom: 20px;">
                        🔒 [LOCKED] 초반 1분 배팅 시간이 마감되었습니다. (현재 매치 정산 시각: {target_display_time} 대기 중)
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"##### ⚔️ 10분 레이스 목표: 현재 시세 ➡️ {target_display_time} 예측 종료")
            st.caption("※ 각 10분 주기 진입 직후 딱 1분(60초)간만 스피드 베팅을 허용합니다.")
            
            # 7대 대장주 베팅 제어 구문 루프
            for stock_name in ["SK하이닉스", "삼성전자", "한미반도체", "현대차", "LG에너지솔루션", "삼성바이오로직스", "셀트리온"]:
                live_p = actual_live_prices.get(stock_name, 0)
                votes = global_server["current_match_votes"][stock_name]
                
                up_cnt = votes["UP"]
                down_cnt = votes["DOWN"]
                
                if up_cnt == down_cnt:
                    up_div = "1.50x (동배)"
                    down_div = "1.50x (동배)"
                elif up_cnt > down_cnt:
                    up_div = "1.30x (정배)"
                    down_div = "1.70x (역배)"
                else:
                    up_div = "1.70x (역배)"
                    down_div = "1.30x (정배)"

                # 매치 고유 식별코드 생성 (10분 주기에 맞춘 유니크키)
                unique_match_key = f"{match_id_string}_{stock_name}"

                with st.container():
                    st.markdown(f"""
                        <div style="background-color: #090D16; border-left: 4px solid #22D3EE; border-top: 1px solid #1E293B; border-right: 1px solid #1E293B; border-bottom: 1px solid #1E293B; padding: 15px; border-radius: 4px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <span style="font-size: 16px; font-weight: 800; color: #FFFFFF;">{stock_name}</span>
                                    <span style="font-size: 11px; color: #64748B; margin-left: 8px;">기준가: {int(live_p):,}원</span>
                                </div>
                                <span style="font-size: 11px; color: #22D3EE; font-weight: bold;">⚡ 10-MIN MATCH</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    has_voted_this_block = unique_match_key in profile["voted_hours"]
                    button_disabled = (not is_voting_window) or has_voted_this_block or profile["points"] < 100

                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button(f"▲ 상승 예측 ({up_div})", key=f"up_{stock_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100
                            is_up_jeong = up_cnt >= down_cnt if (up_cnt != down_cnt) else None
                            global_server["current_match_votes"][stock_name]["UP"] += 1
                            profile["voted_hours"].append(unique_match_key)
                            profile["total_matches"] += 1
                            
                            if random.choice([True, False]): 
                                profile["win_matches"] += 1
                                reward = 130 if is_up_jeong is True else (170 if is_up_jeong is False else 150)
                                profile["points"] += reward
                                st.toast(f"🎯 10분 매치 즉시 적중! {reward} P 획득 완료.", icon="🚀")
                            else: 
                                st.toast("📉 예측 실패! 시드가 청산되었습니다.", icon="💥")
                            st.rerun()
                            
                    with c2:
                        if st.button(f"▼ 하락 예측 ({down_div})", key=f"down_{stock_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100
                            is_down_jeong = down_cnt >= up_cnt if (up_cnt != down_cnt) else None
                            global_server["current_match_votes"][stock_name]["DOWN"] += 1
                            profile["voted_hours"].append(unique_match_key)
                            profile["total_matches"] += 1
                            
                            if random.choice([True, False]):
                                profile["win_matches"] += 1
                                reward = 130 if is_down_jeong is True else (170 if is_down_jeong is False else 150)
                                profile["points"] += reward
                                st.toast(f"🎯 10분 매치 즉시 적중! {reward} P 획득 완료.", icon="🚀")
                            else:
                                st.toast("📉 예측 실패! 시드가 청산되었습니다.", icon="💥")
                            st.rerun()
                    
                    total_votes = votes["UP"] + votes["DOWN"]
                    if total_votes > 0:
                        up_per = (votes["UP"] / total_votes) * 100
                        st.progress(int(up_per))
                        st.markdown(f"<p style='font-size:11px; color:#94A3B8; margin-top:2px; margin-bottom:15px;'>📊 베팅 비율: 상승 ▲ {up_per:.1f}% | 하락 ▼ {100-up_per:.1f}% (현 회차 참여 {total_votes}명)</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='font-size:11px; color:#475569; margin-top:2px; margin-bottom:15px;'>📊 현재 배팅 균형 상태 (1.50x 동배당 적용)</p>", unsafe_allow_html=True)

        # TAB 2: 글로벌 롤 티어 서열 보드
        with tab2:
            st.markdown("### 🏆 글로벌 아레나 랭크 디비전 서열")
            st.caption("스코어 스펙 기준 롤 방식 8대 티어가 하이 테크놀로지 보드에 실시간 정렬됩니다.")
            st.write("")
            
            st.markdown(f"""
                <div style="background: linear-gradient(90deg, #1E1B4B 0%, #030712 100%); border: 2px solid {my_tier_color}; box-shadow: 0 0 10px {my_tier_color}30; padding: 12px 20px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <span style="font-size:13px; font-weight:900; color:{my_tier_color}; width:130px;">{my_tier_title}</span>
                    <span style="font-size:14px; font-weight:bold; color:#FFFFFF; flex:1;">{profile['nickname']} (나)</span>
                    <span style="font-size:13px; color:#22D3EE; font-weight:bold; width:120px; text-align:center;">{profile['points']:,} LP</span>
                    <span style="font-size:13px; color:#81C995; font-weight:bold; width:100px; text-align:right;">{calc_win_rate:.1f}%</span>
                </div>
            """, unsafe_allow_html=True)

            for user in global_server["leaderboard"]:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #1E293B; padding: 12px 20px; border-radius: 6px; background-color: #090D16; margin-bottom: 6px;">
                        <div style="font-size: 13px; font-weight: 900; color: {user['color']}; width: 130px; letter-spacing: 0.5px;">{user['rank']}</div>
                        <div style="font-size: 14px; font-weight: 500; color: #FFFFFF; flex: 1;">{user['name']}</div>
                        <div style="font-size: 13px; color: #22D3EE; width: 120px; text-align: center; font-weight:bold;">{user['points']}</div>
                        <div style="font-size: 13px; color: #81C995; width: 100px; text-align: right; font-weight:bold;">{user['win_rate']}</div>
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
            
        st.markdown(f"<h3 style='margin-top:23px; font-size:15px; color:#FFFFFF;'>💬 실시간 교신 넷 <span style='font-size:11px; color:#A3E635; font-weight:normal;'>🟢 LIVE: {real_active_users}</span></h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:#0F172A; padding:4px 10px; border-radius:4px; font-size:11px; border:1px solid {my_tier_color}50; color:{my_tier_color}; font-weight:900; text-align:center;'>MY RANK: {my_tier_title}</div>", unsafe_allow_html=True)

        chat_container = st.container(height=360)
        with chat_container:
            for msg in global_server["global_chat_stream"]:
                with st.chat_message("user", avatar="⚡"):
                    st.markdown(f"<span style='font-size:13px; font-weight:bold;'>{msg['name']}</span>", unsafe_allow_html=True)
                    st.write(msg["text"])

        if user_live_input := st.chat_input("교신 패킷 전송..."):
            tier_badge = my_tier_title.split(" ")[0]
            colored_name = f"<span style='color:{my_tier_color}; font-weight:bold;'>[{tier_badge}]</span> {profile['nickname']}"
            
            global_server["global_chat_stream"].append({
                "name": colored_name, 
                "text": user_live_input
            })
            st.rerun()

        # 후원 보드
        st.write("---")
        st.markdown("<h4 style='font-size:12px; color:#FF8DA1; margin-bottom:2px;'>🐸 개구리 대장 모이 보충통</h4>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: #1E1B4B; border: 1px dashed #FF8DA1; padding: 12px; border-radius: 6px; margin-bottom: 8px; text-align: center;">
                <p style="margin: 0; font-size: 11px; color: #FFB3C1; line-height: 1.4;">
                    🐸: "10분 간격 하이퍼 매치 데이터를 당기느라 서버가 탈탈 털리고 있어요! 1,000원씩 보태주시면 해외 소형 작전주 배팅장도 개발해올게요!"
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.link_button("⚡ 개구리 대장 지원하기 (Toss)", url="https://toss.me", use_container_width=True)

        # 익명 종목 건의함
        st.write("---")
        st.markdown("<h4 style='font-size:12px; color:#64748B;'>🤫 데이터 허브 건의 패널</h4>", unsafe_allow_html=True)
        with st.form("suggest_form", clear_on_submit=True):
            s_input = st.text_input("📝 건의할 기능/종목", placeholder="예: 코스닥 레버리지도 추가 원함", label_visibility="collapsed")
            s_submit = st.form_submit_button("🔒 서버 백엔드로 전송")
            if s_submit and s_input:
                cur_t = datetime.datetime.now().strftime("%H:%M")
                if "suggested_stocks" not in st.session_state:
                    st.session_state["suggested_stocks"] = []
                st.session_state["suggested_stocks"].append({"time": cur_t, "text": s_input})
                st.toast("✅ 건의 사항이 개발자 안전 프로토콜 DB에 전달되었습니다.", icon="🔒")

        # 백엔드 어드민 콘솔
        is_admin = st.toggle("⚙️ TERMINAL ROOT CONSOLE", value=False)
        if is_admin:
            st.markdown("<h5 style='font-size:11px; color:#FFD700;'>📂 SUGGESTED DATA STREAM</h5>", unsafe_allow_html=True)
            if "suggested_stocks" in st.session_state:
                for s in st.session_state["suggested_stocks"]:
                    st.markdown(f"<p style='font-size:10px; margin:2px 0; color:#34D399;'><b>[{s['time']}]</b> {s['text']}</p>", unsafe_allow_html=True)
