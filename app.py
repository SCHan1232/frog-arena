import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 사이버펑크 토토 아레나 다크 테마 설정
st.set_page_config(
    page_title="⚡ 청개구리 인덱스 - 하이퍼 밸런스 v3.5", 
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

# 🛠️ 글로벌 서버 데이터 허브 (실시간 다중 접속 채팅, 투표, 확성기 전광판 연동)
@st.cache_resource
def get_global_server_data_hub():
    return {
        "current_match_votes": {
            "SK하이닉스": {"UP": 0, "DOWN": 0}, "삼성전자": {"UP": 0, "DOWN": 0},
            "한미반도체": {"UP": 0, "DOWN": 0}, "현대차": {"UP": 0, "DOWN": 0},
            "LG에너지솔루션": {"UP": 0, "DOWN": 0}, "삼성바이오로직스": {"UP": 0, "DOWN": 0},
            "셀트리온": {"UP": 0, "DOWN": 0}
        },
        "global_chat_stream": [
            {"name": "<span style='color:#A3E635; font-weight:bold;'>[📢 공지] 운영진_🐸</span>", "text": "⚡ v3.5 아레나 UI 밸런스 패치 완료! 미니 룰렛이 메인 센터 탭으로 전격 재배치되었습니다."}
        ],
        "loudsheet_announcement": None,  
        "burst_match_status": {},          
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
        "voted_hours": {},    
        "processed_hours": [], 
        "nickname": "게스트 파이터", 
        "points": 1000,       
        "total_matches": 0,   
        "win_matches": 0,     
        "title": "🥈 SILVER",
        "active_medal": "🌱 응애 파이터",
        "roulette_count": 0,
        "roulette_date": ""
    }

# 포인트 기준 롤 티어 판별 딕셔너리
def calculate_lol_tier(pts):
    if pts >= 5000: return "👑 CHALLENGER", "#FBBF24"
    elif pts >= 3000: return "🔮 MASTER", "#C084FC"
    elif pts >= 2000: return "💎 DIAMOND", "#60A5FA"
    elif pts >= 1500: return "✨ PLATINUM", "#34D399"
    elif pts >= 1200: return "🥇 GOLD", "#F59E0B"
    elif pts >= 1000: return "🥈 SILVER", "#94A3B8"
    elif pts >= 500: return "🥉 BRONZE", "#B45309"
    else: return "🪵 IRON", "#475569"

def get_earned_medals(profile):
    unlocked = ["🌱 응애 파이터"]
    if profile["win_matches"] >= 5: unlocked.append("🎯 족집게 도사")
    if profile["points"] >= 2000: unlocked.append("🔥 역배의 신")
    if profile["win_matches"] >= 10: unlocked.append("👑 여의도 작두")
    return unlocked

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
            <p style="color: #22D3EE; font-size: 13px; font-weight: bold; letter-spacing: 2px;">레이아웃 최적화 10분 매크로 아레나에 로그인하십시오.</p>
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
                    "voted_hours": {}, "processed_hours": [], "nickname": login_nick,
                    "points": 1000, "total_matches": 0, "win_matches": 0, "title": "🥈 SILVER",
                    "active_medal": "🌱 응애 파이터", "roulette_count": 0, "roulette_date": ""
                }
                st.toast(f"⚡ 3.5 버전 인프라 포트 결합 성공.", icon="⚡")
                st.rerun()

# 정식 청개구리 아레나 가동
else:
    STOCK_TICKER_MAP = {
        "SK하이닉스": "000660.KS", "삼성전자": "005930.KS", "한미반도체": "042700.KS",
        "현대차": "005380.KS", "LG에너지솔루션": "373220.KS", "삼성바이오로직스": "207940.KS",
        "셀트리온": "068270.KS"
    }

    # 최상단 네온 간판 헤더
    st.markdown("""
        <div style="background: linear-gradient(90deg, #1E1B4B 0%, #0F172A 100%); padding: 20px; border-radius: 12px; border: 2px solid #A3E635; box-shadow: 0 0 20px rgba(163,230,53,0.2); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="color: #A3E635; font-size: 36px; font-weight: 900; margin: 0; letter-spacing: -2px; text-shadow: 0 0 10px rgba(163,230,53,0.4);">
                    ⚡ FROG INDEX ARENA
                </h1>
                <p style="font-size: 11px; color: #38BDF8; margin: 4px 0 0 0; font-weight: bold; letter-spacing: 1px;">⚙ trespassERS REAL-TIME FIXED MACRO v3.5</p>
            </div>
            <div style="background-color: #020617; border: 1px solid #38BDF8; padding: 6px 15px; border-radius: 20px; font-size: 11px; color: #38BDF8; font-weight: bold;">
                📡 센터 패널 삼분할 고속 동기화 작동 중
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 마켓 실시간 데이터 전광판 바
    @st.cache_data(ttl=600)
    def fetch_market_10min_macro_prices():
        ticker_strings = []
        live_prices_dict = {}
        for clean_name, tk in STOCK_TICKER_MAP.items():
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

    live_ticker_html, actual_live_prices = fetch_market_10min_macro_prices()
    
    st.markdown(f"""
        <div style="background-color: #020617; padding: 8px 15px; border-radius: 6px; border: 1px solid #1E293B; font-size: 11px; margin-bottom: 20px; white-space: nowrap; overflow-x: auto;">
            {live_ticker_html}
        </div>
    """, unsafe_allow_html=True)

    # 10분 매크로 타임 연산 기믹 수립
    server_utc = datetime.datetime.utcnow()
    kst_now = server_utc + datetime.timedelta(hours=9)
    current_hour = kst_now.hour; current_minute = kst_now.minute; current_second = kst_now.second
    
    block_start_min = (current_minute // 10) * 10
    next_block_min = block_start_min + 10
    minute_offset = current_minute % 10
    
    is_voting_window = (minute_offset == 0)
    target_display_time = f"{(current_hour + 1) % 24}:00" if next_block_min >= 60 else f"{current_hour}:{next_block_min:02d}"
    macro_match_id = f"{kst_now.strftime('%Y%m%d')}_{current_hour}_{block_start_min}"

    if "last_processed_id" not in st.session_state:
        st.session_state["last_processed_id"] = macro_match_id
    if st.session_state["last_processed_id"] != macro_match_id:
        for s_n in global_server["current_match_votes"]:
            global_server["current_match_votes"][s_n] = {"UP": 0, "DOWN": 0}
        st.session_state["last_processed_id"] = macro_match_id

    if macro_match_id not in global_server["burst_match_status"]:
        global_server["burst_match_status"][macro_match_id] = random.random() < 0.15

    is_this_match_burst = global_server["burst_match_status"][macro_match_id]

    profile = st.session_state["my_arena_profile"]
    prev_block_min = block_start_min - 10 if block_start_min >= 10 else 50
    prev_hour = current_hour if block_start_min >= 10 else (current_hour - 1) % 24
    past_macro_id = f"{kst_now.strftime('%Y%m%d')}_{prev_hour}_{prev_block_min}"

    if "voted_hours" not in profile: profile["voted_hours"] = {}
    if "processed_hours" not in profile: profile["processed_hours"] = []

    # 10분 자동 누적 정산 엔진
    if past_macro_id not in profile["processed_hours"]:
        has_any_settle = False
        was_past_burst = global_server["burst_match_status"].get(past_macro_id, False)
        
        for stock_name in STOCK_TICKER_MAP.keys():
            vote_key = f"{past_macro_id}_{stock_name}"
            if vote_key in profile["voted_hours"]:
                user_bet = profile["voted_hours"][vote_key]
                real_win_dir = random.choice(["UP", "DOWN"]) 
                votes = global_server["current_match_votes"][stock_name]
                is_up_jeong = votes["UP"] >= votes["DOWN"] if (votes["UP"] != votes["DOWN"]) else None

                if user_bet == real_win_dir: 
                    profile["win_matches"] += 1
                    base_reward = 130 if (real_win_dir == "UP" and is_up_jeong) or (real_win_dir == "DOWN" and not is_up_jeong) else 170
                    reward = base_reward * 3 if was_past_burst else base_reward
                    profile["points"] += reward
                    st.toast(f"🎉 [{stock_name}] 적중 성공! +{reward} P 지급.", icon="💰")
                else: 
                    st.toast(f"💸 [{stock_name}] 예측 실패로 시드가 청산되었습니다.", icon="💥")
                has_any_settle = True
        if has_any_settle or minute_offset > 0:
            profile["processed_hours"].append(past_macro_id)

    my_tier_title, my_tier_color = calculate_lol_tier(profile["points"])
    profile["title"] = my_tier_title
    calc_win_rate = (profile["win_matches"] / profile["total_matches"] * 100) if profile["total_matches"] > 0 else 0.0

    if global_server.get("loudsheet_announcement") is not None:
        st.markdown(f"""<div style="background-color: #7F1D1D; border: 2px solid #EF4444; padding: 10px 15px; border-radius: 8px; font-size: 13px; font-weight: bold; color: #FCA5A5; text-align: center; margin-bottom: 15px;">📢 [아레나 선동 무전] {global_server['loudsheet_announcement']}</div>""", unsafe_allow_html=True)

    # 좌우 구조 분할 레이아웃
    main_layout, chat_layout = st.columns([2.3, 1.0], gap="medium")

    # ==================== [LEFT SIDE] 메인 아레나 플레이 구역 ====================
    with main_layout:
        # 🛠️ [요청 피드백 반영] 미니 룰렛이 드디어 메인 아레나 서열판 바로 옆 세 번째 탭으로 안착!
        tab1, tab2, tab3 = st.tabs(["🎮 10분 토토 터미널", "🏆 실시간 아레나 서열판", "🎰 아레나 미니 룰렛"])
        
        # 탭 1: 토토 배팅소
        with tab1:
            current_tag_medal = profile.get("active_medal", "🌱 응애 파이터")
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0B0F19 0%, #030712 100%); border: 2px solid {my_tier_color}; box-shadow: 0 0 15px {my_tier_color}40; padding: 20px; border-radius: 10px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 11px; color: #64748B; font-weight: bold; letter-spacing: 1px;">👤 PILOT PROFILE [훈장 태그: {current_tag_medal}]</span>
                        <h3 style="margin: 3px 0 0 0; color: #FFFFFF; font-size: 22px; font-weight: 800;"><span style='color:#A3E635; font-size:15px;'>[{current_tag_medal}]</span> {profile['nickname']}</h3>
                        <span style="display:inline-block; background-color:{my_tier_color}15; color:{my_tier_color}; padding:2px 10px; border-radius:4px; font-size:11px; font-weight:900; border:1px solid {my_tier_color}50; margin-top:5px;">{my_tier_title}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 11px; color: #64748B; font-weight: bold;">💰 AVAILABLE CREDIT</span>
                        <h2 style="margin: 0; color: #22D3EE; font-size: 24px; font-weight: 900; text-shadow: 0 0 8px rgba(34,211,238,0.3);">{profile['points']:,} P</h2>
                        <span style="font-size:12px; color:#81C995; font-weight:bold;">{profile['win_matches']}승 / {profile['total_matches']}전 (승률: {calc_win_rate:.1f}%)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if is_voting_window:
                if is_this_match_burst:
                    st.markdown(f"""<div style="background: linear-gradient(90deg, #78350F 0%, #B45309 100%); border: 2px solid #F59E0B; padding: 12px 15px; border-radius: 6px; color: #FEF3C7; font-weight: 900; font-size: 14px; margin-bottom: 20px;">💥 [버스트 타임 발동!!!] 정산 보상 무조건 '3배(3.0x)' 지급! 마감 {60 - current_second}초 전!</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="background-color: #064E3B; border: 1px solid #10B981; padding: 12px 15px; border-radius: 6px; color: #34D399; font-weight: bold; font-size: 13.5px; margin-bottom: 20px;">🔓 [OPEN] {block_start_min:02d}분 회차 오픈! (마감까지 {60 - current_second}초!)</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background-color: #7F1D1D; border: 1px solid #EF4444; padding: 12px 15px; border-radius: 6px; color: #FCA5A5; font-weight: bold; font-size: 13.5px; margin-bottom: 20px;">🔒 [LOCKED] 배팅 마감. ({target_display_time} 정시 자동 정산 대기 프로토콜 작동 중)</div>""", unsafe_allow_html=True)
            
            if profile["points"] < 100:
                st.markdown("""<div style="background-color: #1E1B4B; border: 2px dashed #A78BFA; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 20px;"><h4 style="margin: 0; color: #F59E0B; font-weight: 900; font-size: 18px;">🚨 WARNING: 시드 자산 오링 고갈 상태</h4></div>""", unsafe_allow_html=True)
                if st.button("🎡 구조대 룰렛 돌리기 (500원 결제 후 시드 무작위 즉시 구호 복구)", type="primary", use_container_width=True):
                    bonus_p = random.choice([500, 1000, 2500, 5000])
                    profile["points"] += bonus_p; st.rerun()

            st.markdown(f"##### ⚔️ 정시 매크로 리그: {block_start_min:02d}분 시세 ➡️ {target_display_time} 마감 예측")
            
            for stock_name in ["SK하이닉스", "삼성전자", "한미반도체", "현대차", "LG에너지솔루션", "삼성바이오로직스", "셀트리온"]:
                live_p = actual_live_prices.get(stock_name, 0)
                votes = global_server["current_match_votes"][stock_name]
                up_cnt = votes["UP"]; down_cnt = votes["DOWN"]
                up_div = "1.30x" if up_cnt > down_cnt else ("1.70x" if up_cnt < down_cnt else "1.50x")
                down_div = "1.70x" if up_cnt > down_cnt else ("1.30x" if up_cnt < down_cnt else "1.50x")

                unique_macro_user_vote_key = f"{macro_match_id}_{stock_name}"
                has_voted = unique_macro_user_vote_key in profile["voted_hours"]
                button_disabled = (not is_voting_window) or has_voted or profile["points"] < 100

                with st.container():
                    st.markdown(f"""<div style="background-color: #090D16; border-left: 4px solid #22D3EE; padding: 12px; border-radius: 4px; margin-bottom: 10px;"><div style="display: flex; justify-content: space-between; align-items: center;"><div><b>{stock_name}</b> <span style="font-size: 11px; color: #64748B; margin-left: 8px;">기준가: {int(live_p):,}원</span></div><span style="font-size: 11px; color: #22D3EE; font-weight: bold;">⚡ 10-MIN MATCH</span></div></div>""", unsafe_allow_html=True)
                    c_b1, c_b2, c_b3 = st.columns([1.0, 1.0, 1.2])
                    with c_b1:
                        if st.button(f"▲ 상승 ({up_div})", key=f"up_{stock_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100; global_server["current_match_votes"][stock_name]["UP"] += 1; profile["voted_hours"][unique_macro_user_vote_key] = "UP"; profile["total_matches"] += 1; st.rerun()
                    with c_b2:
                        if st.button(f"▼ 하락 ({down_div})", key=f"down_{stock_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100; global_server["current_match_votes"][stock_name]["DOWN"] += 1; profile["voted_hours"][unique_macro_user_vote_key] = "DOWN"; profile["total_matches"] += 1; st.rerun()
                    with c_b3:
                        reverse_disabled = button_disabled or profile["points"] < 300 or (up_cnt == down_cnt)
                        if st.button(f"🔮 인간지표 리버스 (300P)", key=f"rev_{stock_name}", use_container_width=True, disabled=reverse_disabled):
                            profile["points"] -= 300
                            target_dir = "DOWN" if up_cnt > down_cnt else "UP"
                            global_server["current_match_votes"][stock_name][target_dir] += 3; profile["voted_hours"][unique_macro_user_vote_key] = target_dir; profile["total_matches"] += 1; st.rerun()
                    
                    total_votes = votes["UP"] + votes["DOWN"]
                    if total_votes > 0: st.progress(int((votes["UP"] / total_votes) * 100))

        # 탭 2: 실시간 랭킹 보드
        with tab2:
            st.markdown("### 🏆 글로벌 아레나 랭크 디비전 서열")
            for user in global_server["leaderboard"]:
                st.markdown(f"""<div style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #1E293B; padding: 12px 20px; border-radius: 6px; background-color: #090D16; margin-bottom: 6px;"><div style="font-size: 13px; font-weight: 900; color: {user['color']}; width: 130px;">{user['rank']}</div><div style="font-size: 14px; font-weight: 500; color: #FFFFFF; flex: 1;">{user['name']}</div><div style="font-size: 13px; color: #22D3EE; width: 120px; text-align: center; font-weight:bold;">{user['points']}</div><div style="font-size: 13px; color: #81C995; width: 100px; text-align: right; font-weight:bold;">{user['win_rate']}</div></div>""", unsafe_allow_html=True)

        # 🛠️ [이식 성공] '실시간 아레나 서열판' 바로 옆인 센터 3번째 탭으로 미니 룰렛 모듈 강제 강착!
        with tab3:
            st.markdown("### 🎰 아레나 포인트 슬롯 룰렛")
            st.caption("10분 배팅 마감 후 남는 대기 시간을 찢을 미니 오락실! 마이너스 없이 소소한 잭팟을 사냥해 보세요.")
            st.write("")
            
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            if profile.get("roulette_date", "") != today_str:
                profile["roulette_date"] = today_str
                profile["roulette_count"] = 0 
                
            current_done_count = profile.get("roulette_count", 0)
            remained_chances = 5 - current_done_count
            
            c_r1, c_r2 = st.columns([1.0, 2.0])
            with c_r1:
                st.metric("📋 오늘 남은 슬롯 기회", f"{remained_chances} / 5 회")
            with c_r2:
                st.markdown("""
                    **🎁 룰렛 당첨 기댓값 비율 (꽝 배제 복구 구조)**
                    * 💎 **대박 잭팟 스코어:** `+100 P` (확률 10%)
                    * 🔮 **중박 보너스 시드:** `+30 P` (확률 25%)
                    * 🥈 **본전 방어 세이프:** `+10 P` (확률 40%)
                    * 🪵 **낙첨 다음 기회에:** `0 P` (확률 25%)
                """)
            
            st.write("")
            roulette_disabled = remained_chances <= 0 or profile["points"] < 10
            
            if st.button("🎰 10 P 차감 후 즉시 룰렛 스타트", use_container_width=True, disabled=roulette_disabled):
                profile["points"] -= 10
                profile["roulette_count"] += 1
                
                spin_result = random.choices(
                    ["JACKPOT", "BONUS", "SAVE", "BOOM"], 
                    weights=[10, 25, 40, 25], 
                    k=1
                )[0]
                
                if spin_result == "JACKPOT":
                    profile["points"] += 100
                    st.success("👑 [대박!!] 슬롯 3줄 일치 잭팟 폭발! +100 P가 예수금에 충전되었습니다!")
                elif spin_result == "BONUS":
                    profile["points"] += 30
                    st.info("🔮 [중박!] 시뮬레이션 보너스 획득. +30 P가 충전되었습니다.")
                elif spin_result == "SAVE":
                    profile["points"] += 10
                    st.warning("🥈 [본전!] 본전 치기 성공! 차감된 10 P가 고스란히 복구되었습니다.")
                else:
                    st.error("🪵 [꽝!] 아쉽게도 꽝입니다! 10분 정시 리그 배팅으로 복구하세요.")
                    
                st.rerun()
                
            if remained_chances <= 0:
                st.caption("🔒 오늘 배정된 5회의 슬롯 머신 가동이 종료되었습니다. 매일 정각에 자동 초기화됩니다.")

    # ==================== [RIGHT SIDE] 우측 고정 교신방 및 명예 업적 태그 보관소 탭 구역 ====================
    with chat_layout:
        chat_tab, shop_tab = st.tabs(["💬 오픈 교신방", "🏅 명예 훈장 보관소"])
        
        # 탭 1: 대화방
        with chat_tab:
            st.markdown("<p style='font-size:11px; color:#A3E635; margin:0;'>🟢 LIVE CHAT PROTOCOL ACTIVE</p>", unsafe_allow_html=True)
            chat_container = st.container(height=380)
            with chat_container:
                for msg in global_server["global_chat_stream"]:
                    with st.chat_message("user", avatar="⚡"):
                        st.markdown(msg["name"], unsafe_allow_html=True)
                        st.write(msg["text"])

            if user_live_input := st.chat_input("교신 패킷 전송..."):
                my_current_medal = profile.get("active_medal", "🌱 응애 파이터")
                styled_name = f"<b style='color:#F59E0B;'>[{my_current_medal}]</b> <span style='color:{my_tier_color}; font-weight:bold;'>{profile['nickname']}</span>"
                global_server["global_chat_stream"].append({"name": styled_name, "text": user_live_input})
                st.rerun()

        # 탭 2: 훈장 보관소 및 아이템 숍
        with shop_tab:
            st.markdown("### 🏛️ 내 실시간 명예 업적 전시장")
            my_earned_list = get_earned_medals(profile)
            medals_manifest = [
                {"id": "🌱 응애 파이터", "condition": "가입 시 즉시 획득 기본 태그", "style_color": "#94A3B8"},
                {"id": "🎯 족집게 도사", "condition": "누적 5회 이상 예측 적중 시 언락", "style_color": "#34D399"},
                {"id": "🔥 역배의 신", "condition": "실시간 자산 2,000 LP 돌파 시 언락", "style_color": "#60A5FA"},
                {"id": "👑 여의도 작두", "condition": "누적 10회 이상 예측 적중 시 히든 언락", "style_color": "#FBBF24"}
            ]
            for m in medals_manifest:
                with st.container(border=True):
                    if m["id"] in my_earned_list:
                        st.markdown(f"<b style='color:{m['style_color']}; font-size:14px;'>🔓 {m['id']} (획득 성공!)</b>", unsafe_allow_html=True)
                        if profile.get("active_medal", "🌱 응애 파이터") == m["id"]:
                            st.button("🟢 현재 프로필 장착 중", key=f"active_{m['id']}", disabled=True, use_container_width=True)
                        else:
                            if st.button("🏷️ 이 훈장 닉네임 옆에 달기", key=f"wear_{m['id']}", use_container_width=True):
                                profile["active_medal"] = m["id"]; st.rerun()
                    else:
                        st.markdown(f"<b style='color:#475569; font-size:14px;'>🔒 {m['id']} (잠김)</b>", unsafe_allow_html=True)
                        st.caption(f"조건: {m['condition']}")
            
            st.write("---")
            with st.container(border=True):
                st.markdown("**📢 배팅 선동 전광판 확성기**")
                speaker_input = st.text_input("💬 전광판 선동 문구 기입", placeholder="예시: 삼전 상방에 풀배팅 땡겨라", key="txt_speaker", label_visibility="collapsed")
                if st.button("📢 확성기 결제 및 발사 (1,000원)", use_container_width=True):
                    if speaker_input: global_server["loudsheet_announcement"] = f"파이터 [{profile['nickname']}] 의 외침: \"{speaker_input}\""; st.rerun()

        # 후원 보드
        st.write("---")
        st.markdown("<h4 style='font-size:12px; color:#FF8DA1; margin-bottom:2px;'>🐸 개구리 대장 모이 보충통</h4>", unsafe_allow_html=True)
        st.link_button("⚡ 개구리 대장 지원하기 (Toss)", url="https://toss.me", use_container_width=True)
