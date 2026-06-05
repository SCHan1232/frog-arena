import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 사이버펑크 토토 아레나 다크 테마 설정
st.set_page_config(
    page_title="⚡ 청개구리 인덱스 - 하이퍼 도파민 v3.2", 
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
            {"name": "[CHALLENGER] 운영진_🐸", "text": "⚡ v3.2 하이퍼 도파민 시스템 패치 완료! 인간 지표 역배팅 및 버스트 타임 가동 완료!"}
        ],
        "loudspeaker_announcement": None,  # 📢 선동 확성기 메시지 적재용 전역 스토리지
        "burst_match_status": {},          # 회차별 3배 버스트 활성화 체크 디렉토리
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
        "active_skin": "DEFAULT",  
        "purchased_skins": ["DEFAULT"]
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
            <p style="color: #22D3EE; font-size: 13px; font-weight: bold; letter-spacing: 2px;">수익화 전용 아이템 상점 빌드 완료 터미널에 로그인하십시오.</p>
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
                    "active_skin": "DEFAULT", "purchased_skins": ["DEFAULT"]
                }
                st.toast(f"⚡ 하이퍼 아레나 로딩 완료.", icon="⚡")
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
                <p style="font-size: 11px; color: #38BDF8; margin: 4px 0 0 0; font-weight: bold; letter-spacing: 1px;">⚙️ HYPER MONETIZATION DOpaMINE EDITION v3.2</p>
            </div>
            <div style="background-color: #020617; border: 1px solid #38BDF8; padding: 6px 15px; border-radius: 20px; font-size: 11px; color: #38BDF8; font-weight: bold;">
                📡 무한 정시 10분 매크로 엔진 동기화
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
                    ticker_strings.append(f"<span style='color: #FFFFFF; font-weight: bold;'>{clean_name}</span> <span style='color: #22D3EE; text-shadow: 0 0 5px rgba(34,211,238,0.4);'>{int(current_live_price):,}원</span>")
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

    # 회차 변경에 따른 실시간 투표 카운트 초기화 트리거
    if "last_processed_id" not in st.session_state:
        st.session_state["last_processed_id"] = macro_match_id
    if st.session_state["last_processed_id"] != macro_match_id:
        for s_n in global_server["current_match_votes"]:
            global_server["current_match_votes"][s_n] = {"UP": 0, "DOWN": 0}
        st.session_state["last_processed_id"] = macro_match_id

    # 💥 [재미 기능 1] 10분 버스트 타임 이벤트 주입 (15% 확률 유무 전역 메모리 설정)
    if macro_match_id not in global_server["burst_match_status"]:
        global_server["burst_match_status"][macro_match_id] = random.random() < 0.15

    is_this_match_burst = global_server["burst_match_status"][macro_match_id]

    profile = st.session_state["my_arena_profile"]
    prev_block_min = block_start_min - 10 if block_start_min >= 10 else 50
    prev_hour = current_hour if block_start_min >= 10 else (current_hour - 1) % 24
    past_macro_id = f"{kst_now.strftime('%Y%m%d')}_{prev_hour}_{prev_block_min}"

    if "voted_hours" not in profile: profile["voted_hours"] = {}
    if "processed_hours" not in profile: profile["processed_hours"] = []
    if "purchased_skins" not in profile: profile["purchased_skins"] = ["DEFAULT"]

    # 10분 자동 누적 정산 엔진 (버스트 3배 정산 기믹 스케줄 추가)
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
                    
                    # 버스트 판인 경우 보상 3배 가산 연산
                    reward = base_reward * 3 if was_past_burst else base_reward
                    profile["points"] += reward
                    if was_past_burst:
                        st.toast(f"💥 버스트 타임 3배 잭팟 폭발!! [{stock_name}] 적중! +{reward} LP 지급!", icon="👑")
                    else:
                        st.toast(f"🎉 [{stock_name}] 적중 성공! +{reward} P 지급.", icon="💰")
                else: 
                    st.toast(f"💸 [{stock_name}] 예측 실패로 시드가 청산되었습니다.", icon="💥")
                has_any_settle = True
        if has_any_settle or minute_offset > 0:
            profile["processed_hours"].append(past_macro_id)

    my_tier_title, my_tier_color = calculate_lol_tier(profile["points"])
    profile["title"] = my_tier_title
    calc_win_rate = (profile["win_matches"] / profile["total_matches"] * 100) if profile["total_matches"] > 0 else 0.0

    # 📢 [수익화 기능 1] 전광판 선동 확성기 노출 배너 스케줄러
    if global_server.get("loudspeaker_announcement") is not None:
        st.markdown(f"""
            <div style="background-color: #7F1D1D; border: 2px solid #EF4444; padding: 10px 15px; border-radius: 8px; font-size: 13px; font-weight: bold; color: #FCA5A5; text-align: center; box-shadow: 0 0 15px rgba(239,68,68,0.5); margin-bottom: 15px; animation: pulse 1s infinite;">
                📢 [아레나 긴급 선동 확성기] {global_server['loudspeaker_announcement']}
            </div>
        """, unsafe_allow_html=True)

    # 좌우 구조 분할 레이아웃
    main_layout, chat_layout = st.columns([2.3, 1.0], gap="medium")

    # ==================== [LEFT SIDE] 메인 아레나 플레이 구역 ====================
    with main_layout:
        tab1, tab2 = st.tabs(["🎮 10분 토토 터미널", "🏆 실시간 아레나 서열판"])
        
        with tab1:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0B0F19 0%, #030712 100%); border: 2px solid {my_tier_color}; box-shadow: 0 0 15px {my_tier_color}40; padding: 20px; border-radius: 10px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 11px; color: #64748B; font-weight: bold; letter-spacing: 1px;">👤 CURRENT PILOT PROFILE</span>
                        <h3 style="margin: 3px 0 0 0; color: #FFFFFF; font-size: 22px; font-weight: 800;">{profile['nickname']}</h3>
                        <span style="display:inline-block; background-color:{my_tier_color}15; color:{my_tier_color}; padding:2px 10px; border-radius:4px; font-size:11px; font-weight:900; border:1px solid {my_tier_color}50; margin-top:5px; letter-spacing:1px;">{my_tier_title}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 11px; color: #64748B; font-weight: bold;">💰 AVAILABLE CREDIT</span>
                        <h2 style="margin: 0; color: #22D3EE; font-size: 24px; font-weight: 900; text-shadow: 0 0 8px rgba(34,211,238,0.3);">{profile['points']:,} P</h2>
                        <span style="font-size:12px; color:#81C995; font-weight:bold;">{profile['win_matches']}승 / {profile['total_matches']}전 (승률: {calc_win_rate:.1f}%)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 버스트 타임 활성화 여부 대화창 알림 분기
            if is_voting_window:
                if is_this_match_burst:
                    st.markdown(f"""<div style="background: linear-gradient(90deg, #78350F 0%, #B45309 100%); border: 2px solid #F59E0B; padding: 12px 15px; border-radius: 6px; color: #FEF3C7; font-weight: 900; font-size: 14px; margin-bottom: 20px; box-shadow: 0 0 15px #F59E0B60;">💥 [돌발 이벤트: 버스트 타임 발동!!!] 이번 10분 회차 예측 성공 시 정산 보상 무조건 '3배(3.0x)' 지급! 마감 {60 - current_second}초 전!</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="background-color: #064E3B; border: 1px solid #10B981; padding: 12px 15px; border-radius: 6px; color: #34D399; font-weight: bold; font-size: 13.5px; margin-bottom: 20px;">🔓 [OPEN] {block_start_min:02d}분 회차 오픈! (마감까지 {60 - current_second}초!)</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background-color: #7F1D1D; border: 1px solid #EF4444; padding: 12px 15px; border-radius: 6px; color: #FCA5A5; font-weight: bold; font-size: 13.5px; margin-bottom: 20px;">🔒 [LOCKED] 배팅 마감. ({target_display_time} 정시 자동 정산 대기 프로토콜 작동 중)</div>""", unsafe_allow_html=True)
            
            # 🛠️ [수익화 기능 2] 탕진 개미 전용 '구조대 무한 룰렛' 패널 강제 등판 로직 수립
            if profile["points"] < 100:
                st.markdown("""
                    <div style="background-color: #1E1B4B; border: 2px dashed #A78BFA; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
                        <h4 style="margin: 0; color: #F59E0B; font-weight: 900; font-size: 18px;">🚨 WARNING: 시드 자산 오링 고갈 상태</h4>
                        <p style="font-size: 12px; color: #DDD6FE; margin: 4px 0 12px 0;">배팅을 위한 최소 시드(100 P)가 부족합니다. 구조대 룰렛으로 즉시 충전하세요!</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("🎡 구조대 룰렛 돌리기 (500원 결제 후 최소 500 ~ 최대 10,000 P 지급)", type="primary", use_container_width=True):
                    bonus_p = random.choice([500, 1000, 2500, 5000, 10000])
                    profile["points"] += bonus_p
                    st.toast(f"🎡 룰렛 정산 결과: 잭팟 {bonus_p} P가 즉시 충전되었습니다! 아레나에 복귀하세요.", icon="🎡")
                    st.rerun()

            st.markdown(f"##### ⚔️ 정시 매크로 리그: {block_start_min:02d}분 시세 ➡️ {target_display_time} 마감 예측")
            
            for stock_name in ["SK하이닉스", "삼성전자", "한미반도체", "현대차", "LG에너지솔루션", "삼성바이오로직스", "셀트리온"]:
                live_p = actual_live_prices.get(stock_name, 0)
                votes = global_server["current_match_votes"][stock_name]
                
                up_cnt = votes["UP"]
                down_cnt = votes["DOWN"]
                up_div = "1.30x" if up_cnt > down_cnt else ("1.70x" if up_cnt < down_cnt else "1.50x")
                down_div = "1.70x" if up_cnt > down_cnt else ("1.30x" if up_cnt < down_cnt else "1.50x")

                unique_macro_user_vote_key = f"{macro_match_id}_{stock_name}"

                with st.container():
                    st.markdown(f"""
                        <div style="background-color: #090D16; border-left: 4px solid #22D3EE; padding: 12px; border-radius: 4px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div><b>{stock_name}</b> <span style="font-size: 11px; color: #64748B; margin-left: 8px;">기준가: {int(live_p):,}원</span></div>
                                <span style="font-size: 11px; color: #22D3EE; font-weight: bold;">⚡ 10-MIN MATCH</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    has_voted = unique_macro_user_vote_key in profile["voted_hours"]
                    button_disabled = (not is_voting_window) or has_voted or profile["points"] < 100

                    c_b1, c_b2, c_b3 = st.columns([1.0, 1.0, 1.2])
                    with c_b1:
                        if st.button(f"▲ 상승 ({up_div})", key=f"up_{stock_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100
                            global_server["current_match_votes"][stock_name]["UP"] += 1
                            profile["voted_hours"][unique_macro_user_vote_key] = "UP"
                            profile["total_matches"] += 1; st.rerun()
                    with c_b2:
                        if st.button(f"▼ 하락 ({down_div})", key=f"down_{stock_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100
                            global_server["current_match_votes"][stock_name]["DOWN"] += 1
                            profile["voted_hours"][unique_macro_user_vote_key] = "DOWN"
                            profile["total_matches"] += 1; st.rerun()
                    
                    # 🧙‍♂️ [재미 기능 2] 전 국민 쏠림 반대로 무조건 배팅하는 '인간 지표 리버스 역배팅' 버튼 조립
                    with c_b3:
                        reverse_disabled = button_disabled or profile["points"] < 300 or (up_cnt == down_cnt)
                        if st.button(f"🔮 인간지표 리버스 (300P)", key=f"rev_{stock_name}", use_container_width=True, disabled=reverse_disabled, help="현재 유저 비율이 낮아 배당이 높은 황금 포지션에 자동으로 300 P를 풀배팅합니다."):
                            profile["points"] -= 300
                            target_dir = "DOWN" if up_cnt > down_cnt else "UP"
                            global_server["current_match_votes"][stock_name][target_dir] += 3
                            profile["voted_hours"][unique_macro_user_vote_key] = target_dir
                            profile["total_matches"] += 1
                            st.toast(f"🔮 인간 지표 리버스 버프 가동! 대중과 반대 포지션 [{target_dir}]에 300 P 배팅 완료!", icon="🧙‍♂️")
                            st.rerun()
                    
                    total_votes = votes["UP"] + votes["DOWN"]
                    if total_votes > 0:
                        st.progress(int((votes["UP"] / total_votes) * 100))

        with tab2:
            st.markdown("### 🏆 글로벌 아레나 랭크 디비전 서열")
            for user in global_server["leaderboard"]:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #1E293B; padding: 12px 20px; border-radius: 6px; background-color: #090D16; margin-bottom: 6px;">
                        <div style="font-size: 13px; font-weight: 900; color: {user['color']}; width: 130px;">{user['rank']}</div>
                        <div style="font-size: 14px; font-weight: 500; color: #FFFFFF; flex: 1;">{user['name']}</div>
                        <div style="font-size: 13px; color: #22D3EE; width: 120px; text-align: center; font-weight:bold;">{user['points']}</div>
                        <div style="font-size: 13px; color: #81C995; width: 100px; text-align: right; font-weight:bold;">{user['win_rate']}</div>
                    </div>
                """, unsafe_allow_html=True)

    # ==================== [RIGHT SIDE] 우측 고정 교신방 및 아이템 상점 탭 구역 ====================
    with chat_layout:
        chat_tab, shop_tab = st.tabs(["💬 오픈 교신방", "🐸 명예 네온 상점"])
        
        with chat_tab:
            st.markdown("<p style='font-size:11px; color:#A3E635; margin:0;'>🟢 LIVE CHAT PROTOCOL ACTIVE</p>", unsafe_allow_html=True)
            chat_container = st.container(height=380)
            with chat_container:
                for msg in global_server["global_chat_stream"]:
                    with st.chat_message("user", avatar="⚡"):
                        st.markdown(msg["name"], unsafe_allow_html=True)
                        st.write(msg["text"])

            if user_live_input := st.chat_input("교신 패킷 전송..."):
                tier_badge = my_tier_title.split(" ")[0]
                current_skin = profile.get("active_skin", "DEFAULT")
                
                if current_skin == "GOLD_VIP":
                    styled_name = f"<span style='color:#FBBF24; font-weight:900; text-shadow: 0 0 8px #FBBF24;'>👑 [골드VIP] {profile['nickname']}</span>"
                elif current_skin == "NEON_PULSE":
                    styled_name = f"<span style='color:#22D3EE; font-weight:900; text-shadow: 0 0 10px #22D3EE;'>⚡ [네온펄스] {profile['nickname']}</span>"
                elif current_skin == "HELL_FIRE":
                    styled_name = f"<span style='color:#EF4444; font-weight:900; text-shadow: 0 0 12px #EF4444; background-color:#7F1D1D30; padding:2px 6px; border-radius:3px;'>🔥 [지옥불] {profile['nickname']}</span>"
                else:
                    styled_name = f"<span style='color:{my_tier_color}; font-weight:bold;'>[{tier_badge}] {profile['nickname']}</span>"
                
                global_server["global_chat_stream"].append({"name": styled_name, "text": user_live_input})
                st.rerun()

        # [상점 탭 - 수익화 아이템 대거 업데이트 파트]
        with shop_tab:
            st.markdown("### 🐸 아레나 커스텀 숍")
            st.caption("커피 한 잔 값 후원으로 오픈방의 지배자가 되세요. 후원 즉시 아이템이 지급 및 영구 해금됩니다.")
            st.write("")
            
            # 🛠️ [수익화 기능 3] 선동 확성기권 판매 아이템 상점 라인업 보충 배치
            skins_catalog = [
                {"id": "LOUDSPEAKER", "title": "📢 배팅 선동 확성기 이용권", "desc": "상단 메인 전광판에 내 강력한 배팅 선동 문구 5초간 박제 스케줄", "price_krw": "1,000원", "type": "ITEM"},
                {"id": "GOLD_VIP", "title": "👑 골드 VIP 네임텍", "desc": "닉네임 황금빛 광채 + 전용 타이틀 부여", "price_krw": "3,000원", "type": "SKIN"},
                {"id": "NEON_PULSE", "title": "⚡ 사이버 네온 펄스", "desc": "사이버펑크 민트색 발광 네온 이펙트", "price_krw": "5,000원", "type": "SKIN"},
                {"id": "HELL_FIRE", "title": "🔥 지옥불 커스텀 팩", "desc": "채팅창 닉네임 배경 암적색 화염 박스 버프", "price_krw": "9,900원", "type": "SKIN"}
            ]
            
            for skin in skins_catalog:
                with st.container(border=True):
                    st.markdown(f"**{skin['title']}**")
                    st.markdown(f"<p style='font-size:11px; color:#94A3B8; margin:2px 0;'>{skin['desc']}</p>", unsafe_allow_html=True)
                    
                    owned_skins = profile.get("purchased_skins", ["DEFAULT"])
                    
                    if skin["type"] == "SKIN":
                        if skin["id"] in owned_skins:
                            if profile.get("active_skin", "DEFAULT") == skin["id"]:
                                st.button("✅ 현재 장착 중", key=f"active_{skin['id']}", disabled=True, use_container_width=True)
                            else:
                                if st.button("🔄 스킨 장착하기", key=f"wear_{skin['id']}", use_container_width=True):
                                    profile["active_skin"] = skin["id"]; st.rerun()
                        else:
                            if st.button(f"⚡ 스킨 구매 ({skin['price_krw']})", key=f"buy_{skin['id']}", use_container_width=True):
                                profile["purchased_skins"].append(skin["id"])
                                profile["active_skin"] = skin["id"]; st.rerun()
                    
                    # 📢 확성기 아이템 일회성 소모 과금 폼 작동 파트
                    elif skin["type"] == "ITEM":
                        speaker_input = st.text_input("💬 전광판에 띄울 선동 문구 기입", placeholder="예시: 삼전 상방에 풀배팅 땡겨라 개미들아", key=f"txt_{skin['id']}", label_visibility="collapsed")
                        if st.button(f"📢 확성기 쏘기 ({skin['price_krw']})", key=f"shoot_{skin['id']}", use_container_width=True):
                            if not speaker_input:
                                st.error("🚨 선동 멘트를 적으셔야 전광판 발사가 가능합니다!")
                            else:
                                global_server["loudspeaker_announcement"] = f"파이터 [{profile['nickname']}] 가 속삭입니다: \"{speaker_input}\""
                                st.toast("🎉 전광판 선동 무전 발사 성공!! 유저들의 멘탈을 흔듭니다.", icon="📢")
                                st.rerun()
            
            # 확성기 지우기 클리어 마크 및 기본 스킨 원복 스위치
            if global_server.get("loudspeaker_announcement") is not None:
                if st.button("🗑️ [개발자] 전광판 무전 초기화", use_container_width=True):
                    global_server["loudspeaker_announcement"] = None; st.rerun()

            if profile.get("active_skin", "DEFAULT") != "DEFAULT":
                if st.button("❌ 모든 스킨 해제 (기본형)", use_container_width=True):
                    profile["active_skin"] = "DEFAULT"; st.rerun()

        # 후원 보드
        st.write("---")
        st.markdown("<h4 style='font-size:12px; color:#FF8DA1; margin-bottom:2px;'>🐸 개구리 대장 모이 보충통</h4>", unsafe_allow_html=True)
        st.link_button("⚡ 개구리 대장 지원하기 (Toss)", url="https://toss.me", use_container_width=True)
