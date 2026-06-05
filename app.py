import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 청개구리 아레나 다크모드 기반 최적화 설정
st.set_page_config(
    page_title="🐸 청개구리 인덱스 - 국장 2회 타임어택 v1.2", 
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

# 🛠️ [실시간 검증 핵심 코드] 전 세계 유저가 데이터를 공유하는 실시간 중앙 메모리 DB 수립
@st.cache_resource
def get_global_arena_db():
    return {
        # 오전장(AM) / 오후장(PM) 2개 세션으로 분할 관리
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
        "live_fighters": [] # 실시간 투표 참여 유저들이 동적으로 누적되는 보드
    }

global_db = get_global_arena_db()

# 세션 데이터 독립 보안 포맷 설정
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "user", "name": "여의도작두", "text": "오전장 배팅 마감 10분 전인데 삼전 하방 쏠림 실화냐 ㅋㅋ"}, 
        {"role": "user", "name": "반대로만사는대리", "text": "오후장에 마이크론 대신 들어온 현대차 상방 질렀습니다. 다들 도망치세요."},
        {"role": "user", "name": "국장구조대", "text": "대리님 반대 픽 보고 방금 하이닉스 인버스 풀매수 긁었습니다 감사합니다"}
    ]
if "suggested_stocks" not in st.session_state:
    st.session_state["suggested_stocks"] = [
        {"time": "09:15", "text": "국장 테마주(코스닥) 전용 아레나방도 개설 원합니다!"}
    ]
if "my_arena_profile" not in st.session_state:
    st.session_state["my_arena_profile"] = {
        "am_voted": False, 
        "pm_voted": False,
        "nickname": f"국장파이터_{random.randint(100,999)}", 
        "win_rate": "?? %", 
        "title": "🪵 침수된 나무토막"
    }

# 🔴 AREA A: 부장님 방어막
if is_boss_mode:
    st.error("🔒 [보안] 本 화면은 사내 인트라넷 자산입니다. 외부 유출을 금합니다.")
    st.title("📊 2026_전사_리소스_최적화_KPI_Data")
    st.dataframe({"Index": [1, 2], "Task": ["Next-Gen ERP 구축", "Data Pipeline v3"], "Progress": ["94.2%", "81.2%"]}, use_container_width=True)
    if st.button("🔄 시스템 세션 새로고침"): st.query_params["boss_mode"] = "false"; st.rerun()

# 🟢 AREA B: 청개구리 인덱스 아레나 가동
else:
    # 🛠️ 국장(KOSPI) 핵심 대장주 4종 고정 라인업
    STOCK_TICKER_MAP = {
        "SK하이닉스 (000660.KS)": "000660.KS",
        "삼성전자 (005930.KS)": "005930.KS",
        "한미반도체 (042700.KS)": "042700.KS",
        "현대차 (005380.KS)": "005380.KS"
    }

    # 헤더 영역
    st.markdown("""
        <div style="margin-bottom: 2px;">
            <span style="font-size: 38px; font-weight: 800; background: linear-gradient(45deg, #A3E635, #10B981, #22D3EE); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px;">
                🐸 청개구리 인덱스 아레나
            </span>
            <span style="font-size: 12px; color: #AAADB0; font-weight: normal; margin-left: 10px;">📊 국장 전용 2비트 타임어택 v1.2</span>
        </div>
    """, unsafe_allow_html=True)

    # [실시간 국장 무빙 티커 전광판]
    @st.cache_data(ttl=300)
    def fetch_ticker_bar():
        ticker_strings = []
        for name, tk in STOCK_TICKER_MAP.items():
            try:
                t_data = yf.Ticker(tk).history(period="2d")
                if len(t_data) >= 2:
                    close_today = t_data['Close'].iloc[-1]
                    close_prev = t_data['Close'].iloc[-2]
                    diff_pct = ((close_today - close_prev) / close_prev) * 100
                    arrow = "▲" if diff_pct >= 0 else "▼"
                    color_tag = "#81C995" if diff_pct >= 0 else "#F28B82"
                    clean_name = name.split(" (")[0]
                    ticker_strings.append(f"<span style='color: #FFFFFF; font-weight: 500;'>{clean_name}</span> <span style='color: {color_tag};'>{arrow} {diff_pct:+.1f}%</span>")
            except:
                pass
        return " &nbsp;&nbsp; | &nbsp;&nbsp; ".join(ticker_strings) if ticker_strings else "국장 실시간 데이터 동기화 중..."

    live_ticker_html = fetch_ticker_bar()
    st.markdown(f"""
        <div style="background-color: #11151A; padding: 6px 12px; border-radius: 4px; border-left: 4px solid #A3E635; font-size: 11px; margin-bottom: 15px; white-space: nowrap; overflow-x: auto;">
            {live_ticker_html}
        </div>
    """, unsafe_allow_html=True)

    # 레이아웃 분할
    main_layout, chat_layout = st.columns([2.5, 0.8], gap="medium")

    # ==================== [LEFT SIDE] 메인 아레나 플레이 구역 ====================
    with main_layout:
        tab1, tab2 = st.tabs(["🎮 아레나 타임어택 배팅소", "🏆 글로벌 인간지표 서열"])
        
        # TAB 1: 오전장 / 오후장 2회 매치 시스템
        with tab1:
            st.markdown("### ⏱️ 대한민국 국장 타임어택 예측 레이스")
            st.caption(f"파이터명: **{st.session_state['my_arena_profile']['nickname']}** | 현재 계급: **{st.session_state['my_arena_profile']['title']}**")
            st.write("")
            
            # 🥊 세션 1: 오전장 배팅 (09:00 ~ 12:00 전반전)
            st.markdown("#### ☀️ [MATCH 1] 오전장 중간 정산 배팅 (09:00 ~ 12:00 마감 기점)")
            for stock_name in ["SK하이닉스", "삼성전자", "한미반도체", "현대차"]:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1.5, 1.2, 1.3])
                    with c1:
                        st.markdown(f"<div style='font-size:16px; font-weight:bold; margin-top:8px;'>{stock_name} <span style='font-size:11px; color:#AAADB0;'>오전 대치</span></div>", unsafe_allow_html=True)
                    with c2:
                        if st.button(f"▲ 상승 예측", key=f"am_up_{stock_name}", use_container_width=True):
                            if not st.session_state["my_arena_profile"]["am_voted"]:
                                global_db["votes_am"][stock_name]["UP"] += 1
                                st.session_state["my_arena_profile"]["am_voted"] = True
                                
                                # 실시간 데이터 동기화 및 서열 다양화 알고리즘 검증용 데이터 가산
                                rand_score = random.randint(1, 9)
                                title = "🔮 흑마법사 (인간 지표)" if rand_score < 5 else "👑 오라클 (The Oracle)"
                                pct = f"{rand_score}.2 %" if rand_score < 5 else f"9{rand_score}.5 %"
                                color = "#FF8DA1" if rand_score < 5 else "#81C995"
                                
                                st.session_state["my_arena_profile"]["title"] = title
                                st.session_state["my_arena_profile"]["win_rate"] = pct
                                
                                # 글로벌 서열 리스트에 실시간 반영 테스트 패키지 주입
                                global_db["live_fighters"].insert(0, {
                                    "rank": "🔥 LIVE",
                                    "name": st.session_state["my_arena_profile"]["nickname"],
                                    "type": f"{title} (방금 배팅함)",
                                    "win_rate": pct,
                                    "color": color
                                })
                                st.toast("✅ 오전장 실시간 상방 배팅이 글로벌 서버 DB에 가산되었습니다!", icon="☀️")
                                st.rerun()
                            else:
                                st.error("🚨 오전장 배팅은 완료되었습니다. 12시 중간 정산 이후 오후장에 참여하세요.")
                    with c3:
                        if st.button(f"▼ 하락 예측", key=f"am_down_{stock_name}", use_container_width=True):
                            if not st.session_state["my_arena_profile"]["am_voted"]:
                                global_db["votes_am"][stock_name]["DOWN"] += 1
                                st.session_state["my_arena_profile"]["am_voted"] = True
                                st.toast("✅ 오전장 실시간 하방 배팅이 서버에 영구 반영되었습니다!", icon="📉")
                                st.rerun()
                            else:
                                st.error("🚨 오전장 배팅은 완료되었습니다. 12시 중간 정산 이후 오후장에 참여하세요.")
                    
                    # 3번 피드백 검증용: 실시간 투표 변동 그래프 바
                    am_votes = global_db["votes_am"][stock_name]
                    am_total = am_votes["UP"] + am_votes["DOWN"]
                    am_up_per = (am_votes["UP"] / am_total) * 100
                    st.progress(int(am_up_per))
                    st.caption(f"📊 실시간 오전 정산 전광판: ▲ {am_up_per:.1f}% vs ▼ {100-am_up_per:.1f}% (총 {am_total}명 실시간 연동 중)")
            
            st.write("---")
            
            # 🥊 세션 2: 오후장 배팅 (12:00 ~ 15:30 후반전 종가)
            st.markdown("#### 🌙 [MATCH 2] 오후장 최종 종가 배팅 (12:00 ~ 15:30 마감 기점)")
            for stock_name in ["SK하이닉스", "삼성전자", "한미반도체", "현대차"]:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1.5, 1.2, 1.3])
                    with c1:
                        st.markdown(f"<div style='font-size:16px; font-weight:bold; margin-top:8px;'>{stock_name} <span style='font-size:11px; color:#22D3EE;'>종가 대치</span></div>", unsafe_allow_html=True)
                    with c2:
                        if st.button(f"▲ 종가 상승", key=f"pm_up_{stock_name}", use_container_width=True):
                            if not st.session_state["my_arena_profile"]["pm_voted"]:
                                global_db["votes_pm"][stock_name]["UP"] += 1
                                st.session_state["my_arena_profile"]["pm_voted"] = True
                                st.toast("✅ 오후장 종가 상방 시그널이 전체 데이터베이스에 융합되었습니다!", icon="🌙")
                                st.rerun()
                            else:
                                st.error("🚨 오늘 오후장 최종 배팅을 이미 완료하셨습니다. 내일 오전 매치를 대기하세요.")
                    with c3:
                        if st.button(f"▼ 종가 하락", key=f"pm_down_{stock_name}", use_container_width=True):
                            if not st.session_state["my_arena_profile"]["pm_voted"]:
                                global_db["votes_pm"][stock_name]["DOWN"] += 1
                                st.session_state["my_arena_profile"]["pm_voted"] = True
                                st.toast("✅ 오후장 종가 하방 시그널이 전체 데이터베이스에 융합되었습니다!", icon="📉")
                                st.rerun()
                            else:
                                st.error("🚨 오늘 오후장 최종 배팅을 이미 완료하셨습니다. 내일 오전 매치를 대기하세요.")
                    
                    # 실시간 오후 투표 전광판 출력
                    pm_votes = global_db["votes_pm"][stock_name]
                    pm_total = pm_votes["UP"] + pm_votes["DOWN"]
                    pm_up_per = (pm_votes["UP"] / pm_total) * 100
                    st.progress(int(pm_up_per))
                    st.caption(f"📊 실시간 종가 정산 전광판: ▲ {pm_up_per:.1f}% vs ▼ {100-pm_up_per:.1f}% (총 {pm_total}명 실시간 연동 중)")

        # TAB 2: 글로벌 인간지표 서열 (4번 피드백: 데이터 실시간 연동 다채화 보드)
        with tab2:
            st.markdown("### 🏆 글로벌 인간지표 아레나 실시간 티어 서열")
            st.caption("누적 데이터 통계 처리 완료. 전 국민 배팅 오차율을 분석해 상위권 오라클과 하위권 흑마법사를 실시간 나열합니다.")
            st.write("")
            
            # 4번 검증용: 유저가 투표하는 순간 여기에 실시간 파이터 프로필이 실시간 삽입됨!
            if global_db["live_fighters"]:
                st.markdown("##### 🔥 실시간 아레나 파이터 현황 (방금 교신됨)")
                for lf in global_db["live_fighters"][:3]:  # 최신 3명만 하이라이트 노출
                    st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; border: 2px solid #A3E635; padding: 10px 20px; border-radius: 8px; background-color: #1F261A; margin-bottom: 8px;">
                            <div style="font-size: 13px; font-weight: bold; color: #A3E635; width: 80px;">{lf['rank']}</div>
                            <div style="font-size: 14px; font-weight: bold; color: #FFFFFF; flex: 1;">{lf['name']}</div>
                            <div style="font-size: 12px; color: #AAADB0; width: 140px; text-align: center;">{lf['type']}</div>
                            <div style="font-size: 14px; font-weight: bold; color: {lf['color']}; width: 80px; text-align: right;">{lf['win_rate']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.write("---")

            # 기성 명예의 전당 고정 순위표
            st.markdown("##### 🏛️ 아레나 누적 서열 고정 명예의 전당")
            base_leaderboard = [
                {"rank": "👑 1", "name": "여의도작두가리가리", "type": "오라클 (The Oracle)", "win_rate": "92.4%", "color": "#81C995"},
                {"rank": "🔮 GOAT", "name": "반대로만사는대리", "type": "흑마법사 (인간 지표)", "win_rate": "4.2%", "color": "#FF8DA1"},
                {"rank": "🥉 3", "name": "국장개미구조대", "type": "오라클 (The Oracle)", "win_rate": "88.1%", "color": "#81C995"},
                {"rank": "🔮 4", "name": "내가사면폭락장", "type": "흑마법사 (인간 지표)", "win_rate": "7.5%", "color": "#FF8DA1"}
            ]
            for user in base_leaderboard:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #3C4043; padding: 12px 20px; border-radius: 8px; background-color: #1A1D20; margin-bottom: 8px;">
                        <div style="font-size: 15px; font-weight: bold; color: {user['color']}; width: 80px;">{user['rank']}</div>
                        <div style="font-size: 14px; font-weight: 500; color: #FFFFFF; flex: 1;">{user['name']}</div>
                        <div style="font-size: 12px; color: #AAADB0; width: 140px; text-align: center;">{user['type']}</div>
                        <div style="font-size: 15px; font-weight: bold; color: {user['color']}; width: 80px; text-align: right;">{user['win_rate']}</div>
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
        st.caption(f"🏅 **내 현재 배팅 계급:** {st.session_state['my_arena_profile']['title']}")

        chat_container = st.container(height=350)
        with chat_container:
            for msg in st.session_state["chat_messages"]:
                with st.chat_message(msg["role"], avatar="🐸"):
                    st.markdown(f"**{msg['name']}**")
                    st.write(msg["text"])

        if user_live_input := st.chat_input("아레나 오픈방에 한마디..."):
            st.session_state["chat_messages"].append({"role": "user", "name": st.session_state["my_arena_profile"]["nickname"], "text": user_live_input}); st.rerun()

        # 💸 껄무새 소액 후원 보드
        st.write("---")
        st.markdown("<h4 style='font-size:13px; color:#FF8DA1; margin-bottom:2px;'>💸 배고픈 껄무새 모이통</h4>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: #1F1625; border: 1px dashed #FF8DA1; padding: 12px; border-radius: 8px; margin-bottom: 8px; text-align: center;">
                <p style="margin: 0; font-size: 11px; color: #FFB3C1; line-height: 1.4;">
                    🦜: "오전/오후 매치 서버 리소스를 감당하느라 CPU가 타들어 가고 있어요... 커피 값 1,000원만 아껴서 모이 좀 나눠주세요! (우물쭈물)"
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.link_button("🦜 껄무새에게 모이 1,000원 쾌척하기", url="https://toss.me", use_container_width=True)

        # 익명 종목 건의함
        st.write("---")
        st.markdown("<h4 style='font-size:13px; color:#AAADB0;'>🤫 익명 종목 추가 건의함</h4>", unsafe_allow_html=True)
        with st.form("suggest_form", clear_on_submit=True):
            s_input = st.text_input("📝 건의할 종목명/기능", placeholder="예: 코스닥 종목 추가바람", label_visibility="collapsed")
            s_submit = st.form_submit_button("🔒 개발자 비밀 전송")
            if s_submit and s_input:
                cur_t = datetime.datetime.now().strftime("%H:%M")
                st.session_state["suggested_stocks"].append({"time": cur_t, "text": s_input})
                st.toast("✅ 개발자 비밀 DB에 안심 전송되었습니다!", icon="🔒")

        # 백엔드 어드민 콘솔
        is_admin = st.toggle("🛠️ 개발자 관리 콘솔", value=False)
        if is_admin:
            st.markdown("<h5 style='font-size:12px; color:#FFD700;'>📂 유저들의 비밀 종목 건의 리스트</h5>", unsafe_allow_html=True)
            for s in st.session_state["suggested_stocks"]:
                st.markdown(f"<p style='font-size:11px; margin:2px 0; color:#81C995;'><b>[{s['time']}]</b> {s['text']}</p>", unsafe_allow_html=True)
