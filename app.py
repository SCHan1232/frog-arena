import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 오피스 완벽 스텔스(사내 ERP 대시보드 룩) 테마 설정
st.set_page_config(
    page_title="📊 [보안] 전사_데이터_파이프라인_모니터링_시스템_v3.0", 
    page_icon="📊",
    layout="wide"
)

# 2. ⚡ 부장님 감지 패닉 버튼 (스페이스바 연타 시 진짜 엑셀 데이터 시트로 강제 튕김)
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
            {"name": "[시스템 아키텍트] 운영파트_봇", "text": "KST 정시 스케줄러 동기화 완료. 각 데이터 인프라 노드 트래픽 예측 시뮬레이션을 개시합니다."}
        ],
        "leaderboard": [
            {"rank": "👑 CHALLENGER", "name": "여의도작두가리가리", "points": "6,450 P", "win_rate": "84.2%", "color": "#475569"},
            {"rank": "🔮 MASTER", "name": "국장개미구조대", "points": "4,100 P", "win_rate": "79.1%", "color": "#475569"},
            {"rank": "💎 DIAMOND", "name": "단타는예술이다", "points": "2,850 P", "win_rate": "71.4%", "color": "#475569"}
        ]
    }

global_server = get_global_server_data_hub()

if "user_login_data" not in st.session_state:
    st.session_state["user_login_data"] = None

# 유저 실시간 데이터 프로필
if "my_arena_profile" not in st.session_state:
    st.session_state["my_arena_profile"] = {
        "voted_hours": [], 
        "nickname": "임시 사원", 
        "points": 1000,       
        "total_matches": 0,   
        "win_matches": 0,     
        "title": "🥈 SILVER"
    }

# 스텔스 모드 전용 직급 환산 테이블 (롤 티어 우회용)
def calculate_stealth_title(pts):
    if pts >= 5000: return "👑 수석 아키텍트 (CHALLENGER)", "#1E3A8A"
    elif pts >= 3000: return "🔮 책임 엔지니어 (MASTER)", "#2563EB"
    elif pts >= 2000: return "💎 선임 분석가 (DIAMOND)", "#3B82F6"
    elif pts >= 1500: return "✨ 전임 기획자 (PLATINUM)", "#10B981"
    elif pts >= 1200: return "🥇 정직원 (GOLD)", "#F59E0B"
    elif pts >= 1000: return "🥈 계약직 연구원 (SILVER)", "#64748B"
    elif pts >= 500: return "🥉 인턴 사원 (BRONZE)", "#B45309"
    else: return "🪵 침수된 시말서 대상자 (IRON)", "#EF4444"

# 🔴 AREA A: 부장님 디펜스 모드 (스페이스바 연타 시 렌더링되는 진짜 업무 차트인 척하는 방어막)
if is_boss_mode:
    st.error("🔒 [보안 통제] 本 화면은 사내 인트라넷 보안 자산입니다. 인가되지 않은 외부 유출을 엄금합니다.")
    st.title("📊 전사_인프라_클라우드_리소스_최적화_KPI_보고서")
    st.markdown("---")
    st.subheader("📈 2026 상반기 리소스 가동률 분석 트렌드")
    st.dataframe({"인프라 인덱스 코드": ["NODE-A_0660", "NODE-B_5930", "NODE-C_4270", "NODE-D_5380"], "가동 효율성": ["94.2%", "81.5%", "98.7%", "74.1%"], "상태": ["정상 (STABLE)", "최적화 필요", "정상 (STABLE)", "관망 안정화"]}, use_container_width=True)
    if st.button("🔄 시스템 인트라넷 세션 복구"): st.query_params["boss_mode"] = "false"; st.rerun()

# 위장형 로그인 패널 게이트웨이 (사내 VPN 인증창으로 위장)
elif st.session_state["user_login_data"] is None:
    st.markdown("""
        <div style="margin-top: 50px; background-color: #F8FAFC; padding: 20px; border: 1px solid #CBD5E1; border-radius: 6px;">
            <span style="font-size: 11px; color: #64748B; font-weight: bold; letter-spacing: 1px;">🔐 INTERNAL VPN GATEWAY</span>
            <h2 style="color: #1E293B; font-size: 24px; font-weight: 800; margin: 2px 0 10px 0;">사내망 인트라넷 파이프라인 인증 시스템</h2>
            <p style="color: #64748B; font-size: 12px; margin: 0;">리소스 모니터링 터미널 접속을 위해 사원 식별 토큰을 입력하십시오.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<span style='font-size:12px; color:#475569; font-weight:bold;'>인증 프로토콜 설정</span>", unsafe_allow_html=True)
        login_nick = st.text_input("💻 사원 로그인 익명 ID (사내 메신저용)", placeholder="예: 김대리_업무중")
        login_birth = st.text_input("🔑 보안 사번 식별 코드 (숫자 8자리)", placeholder="예: 19961025", max_chars=8)
        
        if st.button("🖥️ 시스템 게이트웨이 인증", use_container_width=True):
            if not login_nick or len(login_birth) < 8:
                st.error("🚨 사원 코드 검증에 실패했습니다. 올바른 포맷을 기입하세요!")
            else:
                st.session_state["user_login_data"] = {"nickname": login_nick, "birth": login_birth}
                st.session_state["my_arena_profile"] = {
                    "voted_hours": [],
                    "nickname": login_nick,
                    "points": 1000,
                    "total_matches": 0,
                    "win_matches": 0,
                    "title": "🥈 계약직 연구원 (SILVER)"
                }
                st.toast("✅ 사내망 연동 성공. 데이터 스트림을 로드합니다.", icon="💾")
                st.rerun()

# 정식 아레나 가동 (위장형 스텔스 업무 대시보드 테마)
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

    # 지루하고 엄숙한 사내 인트라넷 보고서 스타일 상단 헤더
    st.markdown("""
        <div style="background-color: #FFFFFF; padding: 15px 20px; border-radius: 4px; border: 1px solid #E2E8F0; border-left: 5px solid #1E40AF; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div>
                <h2 style="color: #1E293B; font-size: 22px; font-weight: 800; margin: 0; letter-spacing: -0.5px;">
                    📊 [보안] 전사 리소스 데이터 최적화 파이프라인 (v3.0)
                </h2>
                <p style="font-size: 11px; color: #64748B; margin: 2px 0 0 0; font-weight: bold; letter-spacing: 0.5px;">SYSTEM RE-ROUTING MONITORING CONSOLE & INFRASTRUCTURE DATA</p>
            </div>
            <div style="background-color: #F1F5F9; border: 1px solid #CBD5E1; padding: 5px 12px; border-radius: 4px; font-size: 11px; color: #475569; font-weight: bold;">
                🔒 SSL 내부 통신 3계층 가동 중
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 마켓 실시간 데이터 전광판 바 (사내 텍스트 로그 스타일로 튜닝)
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
                    ticker_strings.append(f"<span style='color: #334155; font-weight: bold;'>[SYS_{tk.split('.')[0]}]</span> <span style='color: #1E40AF; font-weight:bold;'>{int(current_live_price):,}</span>")
                    live_prices_dict[clean_name] = current_live_price
                else:
                    live_prices_dict[clean_name] = 0
                    ticker_strings.append(f"<span style='color: #94A3B8;'>{clean_name} NULL</span>")
            except:
                live_prices_dict[clean_name] = 0
                ticker_strings.append(f"<span style='color: #EF4444;'>{clean_name} ERR</span>")
        return " &nbsp;&nbsp; | &nbsp;&nbsp; ".join(ticker_strings), live_prices_dict

    live_ticker_html, actual_live_prices = fetch_market_realtime_prices()
    
    st.markdown(f"""
        <div style="background-color: #F8FAFC; padding: 6px 12px; border-radius: 4px; border: 1px solid #E2E8F0; font-size: 11px; margin-bottom: 20px; white-space: nowrap; overflow-x: auto; font-family: monospace;">
            🖨️ <b>INFRA_LOG_FEED:</b> {live_ticker_html}
        </div>
    """, unsafe_allow_html=True)

    # 시간 동기화 및 10분 정시 매크로 연산
    server_utc = datetime.datetime.utcnow()
    kst_now = server_utc + datetime.timedelta(hours=9)
    current_hour = kst_now.hour
    current_minute = kst_now.minute
    current_second = kst_now.second
    
    block_start_min = (current_minute // 10) * 10
    next_block_min = block_start_min + 10
    minute_offset = current_minute % 10
    
    is_voting_window = (minute_offset == 0)

    if next_block_min >= 60:
        target_display_time = f"{(current_hour + 1) % 24}:00"
    else:
        target_display_time = f"{current_hour}:{next_block_min:02d}"
    
    macro_match_id = f"{kst_now.strftime('%Y%m%d')}_{current_hour}_{block_start_min}"

    if "last_processed_id" not in st.session_state:
        st.session_state["last_processed_id"] = macro_match_id

    if st.session_state["last_processed_id"] != macro_match_id:
        for s_n in global_server["current_match_votes"]:
            global_server["current_match_votes"][s_n] = {"UP": 0, "DOWN": 0}
        st.session_state["last_processed_id"] = macro_match_id

    # 직급 판별 가동 (위장형 스텔스 칭호 연동)
    profile = st.session_state["my_arena_profile"]
    my_tier_title, my_tier_color = calculate_stealth_title(profile["points"])
    profile["title"] = my_tier_title
    calc_win_rate = (profile["win_matches"] / profile["total_matches"] * 100) if profile["total_matches"] > 0 else 0.0

    # 좌우 구조 분할 레이아웃
    main_layout, chat_layout = st.columns([2.4, 0.9], gap="medium")

    # ==================== [LEFT SIDE] 메인 업무 위장 구역 ====================
    with main_layout:
        tab1, tab2 = st.tabs(["📊 전사 인프라 트래픽 시뮬레이션", "📁 부서별 리소스 누적 가동률"])
        
        # TAB 1: 배팅 터미널 ➡️ 트래픽 시뮬레이션 보드로 위장
        with tab1:
            st.markdown(f"""
                <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 15px; border-radius: 4px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 11px; color: #64748B; font-weight: bold;">👤 인트라넷 접속 계정 계급</span>
                        <h4 style="margin: 0; color: #1E293B; font-size: 16px; font-weight: bold;">{profile['nickname']} <span style='font-size:12px; color:{my_tier_color}; font-weight:bold;'>[{my_tier_title.split(" (")[0]}]</span></h4>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 11px; color: #64748B; font-weight: bold;">📊 가용 리소스 밸런스</span>
                        <h3 style="margin: 0; color: #1E40AF; font-size: 18px; font-weight: 800;">{profile['points']:,} P</h3>
                        <span style="font-size:11px; color:#475569;">시뮬레이션 효율성: {calc_win_rate:.1f}% ({profile['win_matches']}회 승인)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            current_now_str = kst_now.strftime('%H:%M:%S')
            
            if is_voting_window:
                st.markdown(f"""<div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 10px 12px; border-radius: 4px; color: #1E40AF; font-size: 12px; margin-bottom: 20px; font-family:monospace;">💡 <b>[STATUS: RUNNING]</b> {block_start_min:02d}분 블록 데이터 수집 채널 개방됨 (스케줄러 인터벌 타임 {60 - current_second}초 남음)</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px 12px; border-radius: 4px; color: #64748B; font-size: 12px; margin-bottom: 20px; font-family:monospace;">🔒 <b>[STATUS: QUEUED]</b> {block_start_min:02d}분 수집 완료. 시스템 정산 기점 타겟 시각 [{target_display_time}] 동기화 추적 중</div>""", unsafe_allow_html=True)
            
            st.markdown(f"##### 📋 가동 모델링: {block_start_min:02d}분 인덱스 ➡️ {target_display_time} 구간 효율성 추정")
            st.caption("※ 본 인터페이스는 10분 단위 정시 자동 매크로 프로토콜에 의해 엄격하게 통제됩니다.")

            # 🛠️ 종목 카드를 완벽한 인프라 장비 코드 명세서 스타일로 위장 변경
            # 예: 삼성전자 ➡️ KR-NODE-5930 (삼성전자)
            for raw_name in ["SK하이닉스", "삼성전자", "한미반도체", "현대차", "LG에너지솔루션", "삼성바이오로직스", "셀트리온"]:
                live_p = actual_live_prices.get(raw_name, 0)
                votes = global_server["current_match_votes"][raw_name]
                tk_code = STOCK_TICKER_MAP[f"{raw_name} (000000.KS)" if "KS" not in raw_name else raw_name].split(".")[0]
                
                up_cnt = votes["UP"]
                down_cnt = votes["DOWN"]
                
                if up_cnt == down_cnt:
                    up_div = "1.50x (기본)"
                    down_div = "1.50x (기본)"
                elif up_cnt > down_cnt:
                    up_div = "1.30x (정방향)"
                    down_div = "1.70x (역방향)"
                else:
                    up_div = "1.70x (역방향)"
                    down_div = "1.30x (정방향)"

                unique_macro_user_vote_key = f"{macro_match_id}_{raw_name}"

                with st.container():
                    st.markdown(f"""
                        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 12px; border-radius: 4px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <b style="font-size: 14px; color: #1E293B; font-family: monospace;">🖥️ KR-NODE-{tk_code} ({raw_name})</b>
                                    <span style="font-size: 11px; color: #64748B; margin-left: 10px;">현재 리소스 스케일: {int(live_p):,} unit</span>
                                </div>
                                <span style="font-size: 11px; color: #1E40AF; font-weight: bold; font-family: monospace;">[NODE_STABLE]</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    has_voted_this_macro_turn = unique_macro_user_vote_key in profile["voted_hours"]
                    button_disabled = (not is_voting_window) or has_voted_this_macro_turn or profile["points"] < 100

                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button(f"▲ 부하 증가 추정 ({up_div})", key=f"up_{raw_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100
                            is_up_jeong = up_cnt >= down_cnt if (up_cnt != down_cnt) else None
                            global_server["current_match_votes"][raw_name]["UP"] += 1
                            profile["voted_hours"].append(unique_macro_user_vote_key)
                            profile["total_matches"] += 1
                            
                            if random.choice([True, False]): 
                                profile["win_matches"] += 1
                                reward = 130 if is_up_jeong is True else (170 if is_up_jeong is False else 150)
                                profile["points"] += reward
                                st.toast("📊 리소스 최적화 시뮬레이션 승인 완료. 데이터 보상이 급여 포인트에 가산되었습니다.", icon="💾")
                            else: 
                                st.toast("❌ 추정 오차 발생. 리소스 가치 100 P가 감가상각 소멸되었습니다.", icon="📉")
                            st.rerun()
                            
                    with c2:
                        if st.button(f"▼ 부하 감소 추정 ({down_div})", key=f"down_{raw_name}", use_container_width=True, disabled=button_disabled):
                            profile["points"] -= 100
                            is_down_jeong = down_cnt >= up_cnt if (up_cnt != down_cnt) else None
                            global_server["current_match_votes"][raw_name]["DOWN"] += 1
                            profile["voted_hours"].append(unique_macro_user_vote_key)
                            profile["total_matches"] += 1
                            
                            if random.choice([True, False]):
                                profile["win_matches"] += 1
                                reward = 130 if is_down_jeong is True else (170 if is_down_jeong is False else 150)
                                profile["points"] += reward
                                st.toast("📊 리소스 최적화 시뮬레이션 승인 완료. 데이터 보상이 급여 포인트에 가산되었습니다.", icon="💾")
                            else:
                                st.toast("❌ 추정 오차 발생. 리소스 가치 100 P가 감가상각 소멸되었습니다.", icon="📉")
                            st.rerun()
                    
                    total_votes = votes["UP"] + votes["DOWN"]
                    if total_votes > 0:
                        up_per = (votes["UP"] / total_votes) * 100
                        st.progress(int(up_per))
                        st.markdown(f"<p style='font-size:11px; color:#64748B; margin-top:2px; margin-bottom:15px; font-family:monospace;'>📊 데이터 밸런싱: 가중치(▲) {up_per:.1f}% | 가중치(▼) {100-up_per:.1f}% (샘플 집계 {total_votes}개)</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='font-size:11px; color:#94A3B8; margin-top:2px; margin-bottom:15px; font-family:monospace;'>📊 파이프라인 샘플 수집 대기 중 (동등 분배 조건 가동)</p>", unsafe_allow_html=True)

        # TAB 2: 글로벌 서열 보드 ➡️ 부서별 리소스 실시간 평가 순위표로 위장
        with tab2:
            st.markdown("### 📁 부서 인프라 평가 데이터 레이팅 명세서")
            st.caption("사내 리소스 시뮬레이션 전적과 승인 효율성을 취합하여 보안 등급 관제 서열을 나열합니다.")
            st.write("")
            
            st.markdown(f"""
                <div style="background-color: #F8FAFC; border: 1px solid #1E40AF; padding: 12px 20px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <span style="font-size:12px; font-weight:bold; color:#1E40AF; width:150px;">{my_tier_title.split(' (')[0]}</span>
                    <span style="font-size:13px; font-weight:bold; color:#1E293B; flex:1;">{profile['nickname']} (본인 사원 세션)</span>
                    <span style="font-size:12px; color:#1E40AF; font-weight:bold; width:120px; text-align:center;">{profile['points']:,} 리소스 점수</span>
                    <span style="font-size:12px; color:#475569; font-weight:bold; width:100px; text-align:right;">효율 {calc_win_rate:.1f}%</span>
                </div>
            """, unsafe_allow_html=True)

            for user in global_server["leaderboard"]:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #E2E8F0; padding: 10px 20px; border-radius: 4px; background-color: #FFFFFF; margin-bottom: 6px;">
                        <div style="font-size: 11px; font-weight: bold; color: #475569; width: 150px; font-family:monospace;">[TITLES] {user['rank'].split(' ')[1]}</div>
                        <div style="font-size: 13px; color: #334155; flex: 1;">{user['name']} 사원</div>
                        <div style="font-size: 12px; color: #1E40AF; width: 120px; text-align: center; font-weight:bold;">{user['points'].replace(' P', '')} P</div>
                        <div style="font-size: 12px; color: #475569; width: 100px; text-align: right;">{user['win_rate']}</div>
                    </div>
                """, unsafe_allow_html=True)

    # ==================== [RIGHT SIDE] 우측 고정 슬랙 메인 대화 채널 위장 레이아웃 ====================
    with chat_layout:
        try:
            from streamlit.runtime.runtime import Runtime
            stats = Runtime.instance()._session_mgr.list_active_sessions()
            real_active_users = len(stats)
            if real_active_users < 1: real_active_users = 1
        except:
            real_active_users = 1
            
        st.markdown(f"<h3 style='margin-top:23px; font-size:13px; color:#334155; font-family:monospace;'># infra-simulation-logs <span style='font-size:10px; color:#10B981; font-weight:normal;'>🟢 노드접속: {real_active_users}</span></h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:#F1F5F9; padding:4px 10px; border-radius:4px; font-size:11px; border:1px solid #CBD5E1; color:#475569; font-weight:bold; text-align:center; font-family:monospace;'>[USER_ROLE]: {my_tier_title.split(' (')[0]}</div>", unsafe_allow_html=True)

        # 🛠️ 채팅방을 사내 슬랙 메신저 로그 텍스트처럼 위장 렌더링
        chat_container = st.container(height=360)
        with chat_container:
            for msg in global_server["global_chat_stream"]:
                with st.chat_message("user", avatar="💻"):
                    st.markdown(f"<span style='font-size:11px; font-weight:bold; color:#1E40AF;'>{msg['name']}</span>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:12px; color:#334155; margin:0;'>{msg['text']}</p>", unsafe_allow_html=True)

        if user_live_input := st.chat_input("사내 메신저 패킷 전송..."):
            clean_badge = my_tier_title.split(" ")[1] if len(my_tier_title.split(" ")) > 1 else "직원"
            colored_name = f"[{clean_badge}] {profile['nickname']}"
            
            global_server["global_chat_stream"].append({
                "name": colored_name, 
                "text": user_live_input
            })
            st.rerun()

        # 후원 보드
        st.write("---")
        st.markdown("<h4 style='font-size:11px; color:#64748B;'>☕ 시스템 인프라 유지 비용 정산</h4>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: #F8FAFC; border: 1px dashed #CBD5E1; padding: 12px; border-radius: 4px; margin-bottom: 8px; text-align: center;">
                <p style="margin: 0; font-size: 11px; color: #475569; line-height: 1.4; font-family:monospace;">
                    ⚙️ [NOTICE] 무한 매크로 통신 파이프라인의 실시간 연동 클라우드 서버 유지 비용을 클라우드 아키텍트 커피값 명목으로 정산 후원받고 있습니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.link_button("☕ 클라우드 아키텍트 지원하기 (Toss)", url="https://toss.me", use_container_width=True)

        # 익명 종목 건의함
        st.write("---")
        st.markdown("<h4 style='font-size:11px; color:#64748B;'>🤫 데이터 모델링 추가 건의 채널</h4>", unsafe_allow_html=True)
        with st.form("suggest_form", clear_on_submit=True):
            s_input = st.text_input("📝 건의할 인프라/노드", placeholder="예: 코스닥 3배 노드 추가 요망", label_visibility="collapsed")
            s_submit = st.form_submit_button("🔒 내부 보안망 전송")
            if s_submit and s_input:
                cur_t = datetime.datetime.now().strftime("%H:%M")
                if "suggested_stocks" not in st.session_state:
                    st.session_state["suggested_stocks"] = []
                st.session_state["suggested_stocks"].append({"time": cur_t, "text": s_input})
                st.toast("✅ 건의 사항이 보안 프로토콜 DB에 아카이브되었습니다.", icon="🔒")

        # 백엔드 어드민 콘솔
        is_admin = st.toggle("⚙️ INTERNAL ROOT ACCESS", value=False)
        if is_admin:
            st.markdown("<h5 style='font-size:11px; color:#FFD700;'>📂 BACKEND SUGGESTED STREAM</h5>", unsafe_allow_html=True)
            if "suggested_stocks" in st.session_state:
                for s in st.session_state["suggested_stocks"]:
                    st.markdown(f"<p style='font-size:10px; margin:2px 0; color:#1E40AF; font-family:monospace;'><b>[{s['time']}]</b> {s['text']}</p>", unsafe_allow_html=True)
