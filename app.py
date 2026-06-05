import streamlit as st
import streamlit.components.v1 as components
import datetime
import random
import yfinance as yf

# 1. 껄무새 & 청개구리 아레나 다크모드 기반 최적화 설정
st.set_page_config(
    page_title="🐸 청개구리 인덱스 - 인간 지표 서열 아레나 v1.1", 
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

# 🛠️ [글로벌 데이터 허브 공유 설정] 모든 온라인 유저가 실시간 투표율과 서열 보드를 공유하게 만드는 메모리 락커
@st.cache_resource
def get_global_arena_db():
    return {
        "global_votes": {
            "SK하이닉스": {"UP": 342, "DOWN": 120},
            "삼성전자": {"UP": 115, "DOWN": 498},
            "엔비디아": {"UP": 512, "DOWN": 88},
            "마이크론": {"UP": 184, "DOWN": 195}
        },
        "leaderboard": [
            {"rank": "👑 1", "name": "여의도작두가리가리", "type": "오라클 (The Oracle)", "win_rate": "92.4%", "color": "#81C995"},
            {"rank": "🔮 GOAT", "name": "반대로만사는대리", "type": "흑마법사 (인간 지표)", "win_rate": "4.2%", "color": "#FF8DA1"},
            {"rank": "🥉 3", "name": "서학개미구조대", "type": "오라클 (The Oracle)", "win_rate": "88.1%", "color": "#81C995"},
            {"rank": "🔮 4", "name": "내가사면폭락장", "type": "흑마법사 (인간 지표)", "win_rate": "7.5%", "color": "#FF8DA1"},
            {"rank": "🪵 5", "name": "평범한나무토막", "type": "침수된 나무토막", "win_rate": "51.0%", "color": "#AAADB0"}
        ]
    }

global_db = get_global_arena_db()

# 세션 데이터 독립 보안 포맷 설정
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "user", "name": "서학개미_119", "text": "와 대리님 오늘 마이크론 상방에 배팅했대요; 다들 인버스 타라 ㅋㅋ"}, 
        {"role": "user", "name": "반대로만사는대리", "text": "왜 내가 마이크론 상승 누르자마자 프리마켓 파란불 들어오냐.. 소름 돋네"},
        {"role": "user", "name": "갓파더지망생", "text": "오늘 오라클 1위 픽 오픈 언제 됨? 모이 충전하러 간다"}
    ]
if "suggested_stocks" not in st.session_state:
    st.session_state["suggested_stocks"] = [
        {"time": "16:21", "text": "애플(AAPL)이랑 코인(BTC) 종목도 예측 아레나에 추가해주세요!"}
    ]
if "my_arena_profile" not in st.session_state:
    st.session_state["my_arena_profile"] = {"voted": False, "nickname": f"루팡지망생_{random.randint(100,999)}", "win_rate": "?? %", "title": "🪵 침수된 나무토막"}

# 🔴 AREA A: 부장님 방어막
if is_boss_mode:
    st.error("🔒 [보안] 本 화면은 사내 인트라넷 자산입니다. 외부 유출을 금합니다.")
    st.title("📊 2026_전사_리소스_최적화_KPI_Data")
    st.dataframe({"Index": [1, 2], "Task": ["Next-Gen ERP 구축", "Data Pipeline v3"], "Progress": ["94.2%", "81.2%"]}, use_container_width=True)
    if st.button("🔄 시스템 세션 새로고침"): st.query_params["boss_mode"] = "false"; st.rerun()

# 🟢 AREA B: 청개구리 인덱스 아레나 가동
else:
    # 대장주 4종 매핑 리스트 (마이크론 탑재)
    STOCK_TICKER_MAP = {
        "SK하이닉스 (000660.KS)": "000660.KS",
        "삼성전자 (005930.KS)": "005930.KS",
        "엔비디아 (NVDA)": "NVDA",
        "마이크론 (MU)": "MU"
    }

    # 헤더 영역
    st.markdown("""
        <div style="margin-bottom: 2px;">
            <span style="font-size: 38px; font-weight: 800; background: linear-gradient(45deg, #A3E635, #10B981, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px;">
                🐸 청개구리 인덱스
            </span>
            <span style="font-size: 13px; color: #AAADB0; font-weight: normal; margin-left: 10px;">인간 지표 서열 아레나 v1.1</span>
        </div>
    """, unsafe_allow_html=True)

    # [실시간 마켓 주가 전광판 티커 바]
    @st.cache_data(ttl=600)
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
        return " &nbsp;&nbsp; | &nbsp;&nbsp; ".join(ticker_strings) if ticker_strings else "실시간 마켓 데이터 교신 중..."

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
        tab1, tab2, tab3 = st.tabs(["🎮 아레나 일일 배팅소", "🏆 글로벌 인간지표 서열", "🧠 청개구리 포모 분석실"])
        
        # TAB 1: 아레나 일일 배팅소
        with tab1:
            st.markdown("### 🎯 금일 장마감 상승 vs 하락 실시간 배팅")
            st.caption(f"📅 당일 기준 예측 | 내 파이터 프로필명: **{st.session_state['my_arena_profile']['nickname']}** ({st.session_state['my_arena_profile']['title']})")
            st.write("")
            
            for stock_name in ["SK하이닉스", "삼성전자", "엔비디아", "마이크론"]:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1.5, 1.2, 1.3])
                    with c1:
                        st.markdown(f"<div style='font-size:18px; font-weight:bold; margin-top:8px;'>{stock_name}</div>", unsafe_allow_html=True)
                    with c2:
                        if st.button(f"▲ 오늘 무조건 상승", key=f"up_{stock_name}"):
                            if not st.session_state["my_arena_profile"]["voted"]:
                                global_db["global_votes"][stock_name]["UP"] += 1
                                st.session_state["my_arena_profile"]["voted"] = True
                                
                                rand_fail = random.choice([True, False])
                                if rand_fail:
                                    st.session_state["my_arena_profile"]["title"] = "🔮 흑마법사 (인간 지표)"
                                    st.session_state["my_arena_profile"]["win_rate"] = "8.3 %"
                                    st.toast("🔮 기적의 똥손 기운 감지! '흑마법사' 칭호 획득!", icon="🔮")
                                else:
                                    st.session_state["my_arena_profile"]["title"] = "👑 오라클 (The Oracle)"
                                    st.session_state["my_arena_profile"]["win_rate"] = "91.2 %"
                                    st.toast("👑 시장 트렌드 마스터! '오라클' 칭호 획득!", icon="👑")
                                st.rerun()
                            else:
                                st.warning("🚨 일일 의결권 배팅은 하루에 딱 한 번만 가능합니다! 장마감 결과를 기다리세요.")
                                
                    with c3:
                        if st.button(f"▼ 오늘 무조건 하락", key=f"down_{stock_name}"):
                            if not st.session_state["my_arena_profile"]["voted"]:
                                global_db["global_votes"][stock_name]["DOWN"] += 1
                                st.session_state["my_arena_profile"]["voted"] = True
                                st.toast("▼ 하방 배팅 접수 완료! 실시간 인간지표에 반영되었습니다.", icon="🐸")
                                st.rerun()
                            else:
                                st.warning("🚨 일일 의결권 배팅은 하루에 딱 한 번만 가능합니다! 장마감 결과를 기다리세요.")
                    
                    # 실시간 글로벌 투표율 계산 가로 바 시각화
                    votes = global_db["global_votes"][stock_name]
                    v_total = votes["UP"] + votes["DOWN"]
                    up_per = (votes["UP"] / v_total) * 100
                    st.progress(int(up_per))
                    st.caption(f"📊 실시간 배팅 쏠림 현황: 상승(▲) {up_per:.1f}% vs 하락(▼) {100-up_per:.1f}% (전 세계 {v_total}명 참여 중)")

        # TAB 2: 글로벌 인간지표 서열 보드
        with tab2:
            st.markdown("### 🏆 글로벌 인간지표 아레나 실시간 티어 서열")
            st.caption("실시간 API 결과와 비교 분석하여, 완벽히 맞추는 자(오라클)와 완벽히 틀리는 자(흑마법사)의 탑 서열을 갱신합니다.")
            st.write("")
            
            for user in global_db["leaderboard"]:
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; border: 1px solid #3C4043; padding: 12px 20px; border-radius: 8px; background-color: #1A1D20; margin-bottom: 8px;">
                        <div style="font-size: 15px; font-weight: bold; color: {user['color']}; width: 80px;">{user['rank']}</div>
                        <div style="font-size: 14px; font-weight: 500; color: #FFFFFF; flex: 1;">{user['name']}</div>
                        <div style="font-size: 12px; color: #AAADB0; width: 140px; text-align: center;">{user['type']}</div>
                        <div style="font-size: 15px; font-weight: bold; color: {user['color']}; width: 80px; text-align: right;">{user['win_rate']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.write("")
            st.info("💡 **수익 분양 리워드 꿀팁:** 승률 5% 미만의 전설적인 '흑마법사' 티어가 되면, 일반 유저들이 님들의 예측을 확인하기 위해 '모이 포인트'를 지불해야 합니다. 똥손이 곧 돈이 되는 역발상 신세계를 누리세요!")

        # TAB 3: 청개구리 포모 분석실
        with tab3:
            st.markdown("### 🧠 뇌과학 기반 청개구리 역발상 기회비용 정산실")
            st.caption("내가 탕진한 비용을 아껴 청개구리 흑마법사 1위의 '반대 픽'으로 우량주를 모았을 때의 실시간 스노우볼을 역산합니다.")
            
            HABIT_PRICE_MAP = {
                "탕후루/마라탕 수명 단축 쿨타임 (1회 18,000원)": 18000,
                "스타벅스 바닐라라떼+디저트 (1회 11,000원)": 11000, 
                "올리브영 세일 '구경만' 가기 (1회 45,000원)": 45000,
                "불금 배달 떡볶이+치킨 세트 (1회 32,000원)": 32000,
                "지그재그/W컨셉 충동 의류 매수 (1회 65,000원)": 65000,
                "매달 속눈썹 펌/네일 정기권 (1회 55,000원)": 55000
            }
            
            selected_option = st.selectbox("🛍️ 매달 탕진 중인 시발비용 선택", list(HABIT_PRICE_MAP.keys()))
            
            with st.form("arena_audit_form"):
                col1, col2 = st.columns(2)
                with col1: count = st.slider("📊 주간 평균 소비 빈도", 1, 14, 3)
                with col2:
                    target_asset = st.selectbox("📈 추적할 역매매 연동 자산", list(STOCK_TICKER_MAP.keys()))
                    years = st.slider("⏳ 역산 추적 기간 (N년)", 1, 5, 3)
                submitted = st.form_submit_button("⚡ 청개구리 퀀텀점프 연산 실행")

            if submitted:
                unit_price = HABIT_PRICE_MAP[selected_option]
                total_seed = unit_price * count * 52 * years
                
                ticker_symbol = STOCK_TICKER_MAP[target_asset]
                try:
                    ticker_data = yf.Ticker(ticker_symbol)
                    today_df = ticker_data.history(period="1d")
                    current_price = today_df['Close'].iloc[-1]
                    
                    target_date = datetime.date.today() - datetime.timedelta(days=365 * years)
                    then_price = None
                    attempts = 0
                    while then_price is None and attempts < 10:
                        start_query = target_date.strftime('%Y-%m-%d')
                        end_query = (target_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                        past_df = ticker_data.history(start=start_query, end=end_query)
                        if not past_df.empty: then_price = past_df['Close'].iloc[0]
                        else: target_date -= datetime.timedelta(days=1); attempts += 1
                    if then_price is None: then_price = current_price * 0.5
                except:
                    then_price = 115000 if "000660" in ticker_symbol else 55
                    current_price = 2345000 if "000660" in ticker_symbol else 132

                is_foreign = ".KS" not in ticker_symbol
                exchange_rate = 1380 if is_foreign else 1
                
                total_shares = total_seed / (then_price * exchange_rate)
                final_value = total_shares * current_price * exchange_rate
                total_asset_growth = ((current_price - then_price) / then_price) * 100
                asset_clean_name = target_asset.split(" (")[0]
                
                st.write("---")
                st.markdown(f"#### 🔮 청개구리 흑마법사 추종 정산 결과")
                st.markdown(f"귀하가 낭비한 **{int(total_seed):,}원**을 아껴서 흑마법사 1위 신호 반대로 **'{asset_clean_name}'** 주식을 모았다면, 누적 수익률 **{total_asset_growth:+.1f}%**를 기록하며 오늘 자산은 무려 **{int(final_value):,}원**으로 퀀텀점프해 있었을 것입니다!")

        # 실시간 금융 속보
        st.write("---")
        st.markdown(f"#### 📰 아레나 실시간 청개구리 소망 속보 <span style='font-size:12px; color:#A3E635; font-weight:normal;'> LIVE</span>", unsafe_allow_html=True)
        flash_news = [
            f"⚡ [속보] 전설의 승률 4.2% '반대로만사는대리' 파이터, 마이크론 상방 배팅 소식에 숏 진영 패닉 스위칭 확인",
            f"⚡ [긴급] 마이크론 하방 배팅률 72% 돌파, 청개구리 역발상 인덱스 마스터들 '바닥 신호 포착' 대규모 매수 준비"
        ]
        st.caption(random.choice(flash_news))

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
        st.caption(f"🏅 **내 현재 티어:** {st.session_state['my_arena_profile']['title']}")

        chat_container = st.container(height=320)
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
                    **🦜: "파이터님들이 날려먹은 기회비용 연산하느라 아레나 서버 CPU가 타들어 가고 있어요... 시발비용 딱 1,000원만 아껴서 껄무새 모이값 보태주시면 안 될까요? (우물쭈물)"**
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.link_button("🦜 껄무새에게 모이 1,000원 쾌척하기", url="https://toss.me", use_container_width=True)

        # 익명 종목 건의함
        st.write("---")
        st.markdown("<h4 style='font-size:13px; color:#AAADB0;'>🤫 익명 종목 추가 건의함</h4>", unsafe_allow_html=True)
        with st.form("suggest_form", clear_on_submit=True):
            s_input = st.text_input("📝 건의할 종목명/기능", placeholder="예: 비트코인 추가해줘", label_visibility="collapsed")
            s_submit = st.form_submit_button("🔒 개발자 비밀 전송")
            if s_submit and s_input:
                cur_t = datetime.datetime.now().strftime("%H:%M")
                st.session_state["suggested_stocks"].append({"time": cur_t, "text": s_input})
                st.toast("✅ 개발자 비밀 DB에 안심 전송되었습니다!", icon="🔒")

        # 백엔드 어드민 토글 콘솔
        is_admin = st.toggle("🛠️ 개발자 관리 콘솔", value=False)
        if is_admin:
            st.markdown("<h5 style='font-size:12px; color:#FFD700;'>📂 유저들의 비밀 종목 건의 리스트</h5>", unsafe_allow_html=True)
            for s in st.session_state["suggested_stocks"]:
                st.markdown(f"<p style='font-size:11px; margin:2px 0; color:#81C995;'><b>[{s['time']}]</b> {s['text']}</p>", unsafe_allow_html=True)
