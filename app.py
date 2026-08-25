import streamlit as st
import re

st.set_page_config(
    page_title="BLACK LIST",
    page_icon="🔍",
    layout="wide"
)

# 원본 텍스트 그대로 적용된 금지 리스트 데이터
initial_data = [
    {"name": "강민*", "addresses": ["경기 의정부시 배꽃길 63 지식산업센터 *동 2*4호"]},
    {"name": "강아*", "addresses": ["경상북도 칠곡군 왜관읍 금산로3길 ** 칠곡왜관******* 10*동 16**호"]},
    {"name": "구향*", "addresses": ["경남 진주시 충무공동 30* 혁신도시***아파트 *단지 80*동 15**호"]},
    {"name": "권시*/최수*", "addresses": ["서울특별시 광진구 뚝섬로 7**"]},
    {"name": "김관*", "addresses": ["경기도 의정부시 용현로 18*-* 3층 ( 민락동 )"]},
    {"name": "김낙*", "addresses": ["경기도 안양시 박달로 3** 2층"]},
    {"name": "김명*/조명*", "addresses": ["경기도 시흥시 은행로 24*-1*"]},
    {"name": "김문*", "addresses": ["경기도 화성시 향남읍 발안로 464번길 **-*"]},
    {"name": "김민*", "addresses": ["대구광역시 수성구 동대구로 3** 범어서*****아파트"]},
    {"name": "김민*", "addresses": ["서울특별시 성동구 성수일로 10,IT*T지산센터 150*호 ( 성수동1가 )"]},
    {"name": "김성*/신선*", "addresses": ["인천광역시 계양구 효성동 62*-* 하나아파트 4동 7**호"]},
    {"name": "김수*/최재*", "addresses": ["경상북도 칠곡군 북삼읍 금오대로1길 **-** 금**** 10*호"]},
    {"name": "김승*", "addresses": ["인천광역시 연수구 인천타워대로 9* 택배보관함 1층"]},
    {"name": "김아*", "addresses": ["남양주시 평내동 이편***"]},
    {"name": "김예*", "addresses": ["경기도 남양주시 진접읍 부평로 3* 1**동 10**호"]},
    {"name": "김용*", "addresses": ["경기도 고양시 덕양구 덕*동 0 DM* 한강숲 중흥S-CLASS 11*동 170*호"]},
    {"name": "김우*", "addresses": []},
    {"name": "김유*", "addresses": ["인천광역시 서구 용해로2* 1**동 8**호"]},
    {"name": "김ㅎ", "addresses": ["서울 동대문구 왕산로 68 용운빌딩 5**호"]},
    {"name": "루ㅇ(주문자 박주ㄹ)", "addresses": ["경기도 하남시 미사강변동로 1*7 경서*워 90*호(망월동)"]},
    {"name": "박교*", "addresses": ["서울특별시 성동구 상원*길 26 13*5호"]},
    {"name": "박병*", "addresses": ["서울특별시 영등포구 신길동 42*-3 영등포제*스포츠센터 *층 무인택배함"]},
    {"name": "박수*", "addresses": ["서울특별시 성북구 보문로29다길 25-* 10*동 6**호"]},
    {"name": "박용*", "addresses": ["부산광역시 수영구 광일로 * 3층(광안동)"]},
    {"name": "박종*", "addresses": ["경기도 용인시 기흥구 흥덕2로1**번길 2"]},
    {"name": "박지*", "addresses": ["경기도 화성시 향남읍 발안로 4**번길 1*-2"]},
    {"name": "배지*", "addresses": ["경기도 안양시 동안구 경수대로8*4번길 12 109-6*1호"]},
    {"name": "복영*", "addresses": ["강서구 양천로1*길 2* (방화동, 삼***을아파트) 10*동 6**호", "서초구 서초대로77길 5* (에*** 스**) 8층"]},
    {"name": "봉성* (삼실)", "addresses": ["인천광역시 연수구 송도동 2*-8 송도씨*크인테라스*라 C동 1*29호 (주문자: 최*홍)"]},
    {"name": "서동*", "addresses": ["인천광역시 서구 크리스탈로102번길 8-** 8**호 (청라동)"]},
    {"name": "서현*", "addresses": ["경기도 동두천시 송내동 69*-* 우진프라자 2**호"]},
    {"name": "신명*", "addresses": ["인천광역시 연수구 송도동 315-* 송도 S* **** 10*동 36**호"]},
    {"name": "신성*", "addresses": ["경기도 김포시 장기동 20*8-1 한강신도시 초당마을중흥에스-클래스리버티 3*3동 2*3호"]},
    {"name": "양기*", "addresses": ["서울특별시 마포구 양화로 18* 11층"]},
    {"name": "양은*", "addresses": ["경기도 수원시 영통구 망포동 723 한양수자인 에듀파크 10*동 190*호"]},
    {"name": "양현*", "addresses": ["서울특별시 구로구 디지털로34길 ** 3층 3**호"]},
    {"name": "엄형*", "addresses": ["경기도 화성시 향남읍 발안로 4**번길 10-*"]},
    {"name": "우지*", "addresses": ["경기도 용인시 기흥구 농서로 8* ***에동 6**호 ( 농서동 )"]},
    {"name": "윤소*/윤현*", "addresses": ["서울특별시 금천구 독산동 9** ** ****타워 5**호"]},
    {"name": "이가*", "addresses": ["경기도 화성시 우정읍 조암서로13번길 ** **아파트 10*동 8**호"]},
    {"name": "이광*", "addresses": ["충청남도 공주시 신풍면 봉갑리 3** 타**장"]},
    {"name": "이미*", "addresses": ["경기도 파주시 다율동 10** 푸**오 파**나 140*동 11**호"]},
    {"name": "이승*", "addresses": ["경기도 성남시 분당구 정자동 193 정든마을한진8단지아파트 80*동 14**호"]},
    {"name": "이영*", "addresses": ["서울특별시 구로구 신로림동 64* 신도림1차동*아파트 110동 180*호"]},
    {"name": "이원*/이은*", "addresses": ["서울특별시 영등포구 디지털로70길 1*-3 101호"]},
    {"name": "이유*", "addresses": ["광주광역시 서구 풍암동 11** 10*동 14**호"]},
    {"name": "이주*/루*", "addresses": ["경기도 하남시 미사강변동로 1*7 경**원"]},
    {"name": "이창*", "addresses": ["인천광역시 서해구 가*동 70* 루원시티 S* Leaders VI*W 오피스텔 1차 2*1동 18*6호"]},
    {"name": "이해*", "addresses": ["대구 방촌동822-* 해** 행정**센터"]},
    {"name": "이현*", "addresses": ["서울특별시 서초구 서초대로77길 ** 8층 엘리베이터 앞", "인천광역시 서구 서곶로 120 2*8동 7*2호"]},
    {"name": "장승*", "addresses": ["경기도 의정부시 민락동 92*-* 의정부 더** 센텀스퀘어* 지식산업센터 3동 2**호"]},
    {"name": "장현*/장호*", "addresses": ["서울특별시 강남구 역삼동 673-** 베**캠프 센터필드점"]},
    {"name": "정슬*", "addresses": ["강동구 양재대로98길 43-4* 2**호"]},
    {"name": "정용*", "addresses": ["울산광역시 북구 양정동 52*-* 1층"]},
    {"name": "정진*", "addresses": ["서울특별시 강서구 등촌동 6*8-5 아임20*0 등촌역 6*7호", "서울특별시 강서구 공항대로5*가길 14 6*7호"]},
    {"name": "조현*", "addresses": ["경기도 수원시 장안구 조원동 8** 수원 **타운 11*동 17**호"]},
    {"name": "최재*", "addresses": ["경기도 구리시 체육관로 12* 10*동 17**호"]},
    {"name": "최진*", "addresses": ["인천광역시 부평구 경원대로 1344번길 ** 10*동 13**호"]},
    {"name": "한승*", "addresses": ["헤트라스***"]},
    {"name": "정인*", "addresses": ["경기도 하남시 망월동 11** 미사강변도시씨3단지 30*동 25**호"]}
]

st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.3rem !important;
        font-weight: 700 !important;
        font-size: 1.17rem !important;
        height: auto !important;
        width: 100% !important;
        border: none !important;
        text-align: center !important;
    }
    .pass-box {
        background-color: #1E90FF;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        font-weight: 700;
        font-size: 1.17rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .caution-box {
        background-color: #FF8C00;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        font-weight: 700;
        font-size: 1.17rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .stop-box {
        background-color: #FF4B4B;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        font-weight: 700;
        font-size: 1.17rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "master_addresses" not in st.session_state or not st.session_state.master_addresses:
    st.session_state.master_addresses = initial_data.copy()
else:
    for item in st.session_state.master_addresses:
        if "addresses" not in item:
            item["addresses"] = [item["address"]] if item.get("address") else []
            if "address" in item:
                del item["address"]

if "matched_details_list" not in st.session_state:
    st.session_state.matched_details_list = []

if "check_results" not in st.session_state:
    st.session_state.check_results = []

if "partial_results" not in st.session_state:
    st.session_state.partial_results = None
if "last_search_keyword" not in st.session_state:
    st.session_state.last_search_keyword = ""

# --- 매칭 함수들 ---
def is_name_matched(master_name, target_text):
    for sub in master_name.split('/'):
        sub = sub.strip()
        if not sub:
            continue
        if '*' in sub:
            escaped = re.escape(sub)
            regex_pattern = escaped.replace(r'\*', r'[가-힣A-Za-z0-9]')
            if re.search(regex_pattern, target_text):
                return True
        else:
            if sub in target_text:
                return True
    return False

# 1. 기존 완벽 일치(STOP) 알고리즘
def is_address_matched(master_addr, target_addr):
    m_clean = master_addr.replace(" ", "")
    t_clean = target_addr.replace(" ", "")

    if m_clean in t_clean: return True
    if not any(ch.isdigit() for ch in master_addr):
        base_text = master_addr.replace('*', '').replace(' ', '')
        return bool(base_text) and base_text in t_clean

    m_tokens = master_addr.split()
    for m_token in m_tokens:
        if '*' in m_token and m_token in target_addr: continue
            
        if any(ch.isdigit() or ch == '*' for ch in m_token):
            chars = []
            for ch in m_token:
                if ch == '*': chars.append(r'\S')
                else: chars.append(re.escape(ch))
            flex_pattern = r'\s*'.join(chars)
            
            if m_token[0].isdigit() or m_token[0] == '*':
                flex_pattern = r'(?<!\S)' + flex_pattern
            if m_token[-1].isdigit() or m_token[-1] == '*':
                flex_pattern = flex_pattern + r'(?!\S)'
                
            if not re.search(flex_pattern, target_addr):
                return False
        else:
            if m_token.replace(" ", "") not in t_clean:
                return False
    return True

# 2. [신규 추가] 부분 일치 (CAUTION) 알고리즘
def is_address_caution(master_addr, target_addr):
    # 숫자가 아예 없는 순수 텍스트(헤트라스 등)는 부분 일치 검사 제외 (정확도 확보)
    if not any(ch.isdigit() for ch in master_addr):
        return False

    t_clean = target_addr.replace(" ", "")
    m_tokens = master_addr.split()
    
    # 단어가 3개 미만인 짧은 주소는 오탐 방지를 위해 CAUTION 생략
    if len(m_tokens) < 3:
        return False

    match_count = 0
    for m_token in m_tokens:
        if '*' in m_token:
            chars = [r'\S' if ch == '*' else re.escape(ch) for ch in m_token]
            flex_pattern = r'\s*'.join(chars)
            # CAUTION은 끝부분 누락 등도 허용해야 하므로 경계선 검증(?<!\S) 생략
            if re.search(flex_pattern, target_addr):
                match_count += 1
        else:
            if m_token.replace(" ", "") in t_clean:
                match_count += 1

    ratio = match_count / len(m_tokens)
    
    # [CAUTION 조건]
    # 1. 3단어 이상 매칭되었고, 
    # 2. 전체 마스터 주소의 65% 이상이 입력 주소에 포함되어 있거나, 혹은 딱 1단어만 누락된 경우
    if match_count >= 3 and (ratio >= 0.65 or match_count >= len(m_tokens) - 1):
        return True
        
    return False

# --- 메인 UI 구성 ---
st.markdown("<h2 style='font-size: 1.9rem;'>BLACK LIST</h2>", unsafe_allow_html=True)

col_left, col_right = st.columns(2, gap="medium")

with col_left:
    st.markdown("<h4 style='font-size: 1.1rem;'>블랙리스트</h4>", unsafe_allow_html=True)
    
    with st.expander("리스트(TXT) 다운로드 / 업로드", expanded=False):
        txt_content = ""
        for item in st.session_state.master_addresses:
            name = item.get("name", "")
            addrs = item.get("addresses", [])
            if addrs:
                for addr in addrs:
                    txt_content += f"{name},{addr}\n"
            else:
                txt_content += f"{name},\n"
                
        st.download_button(
            label="다운로드 (.txt)",
            data=txt_content,
            file_name="forbidden_addresses.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        uploaded_file = st.file_uploader("수정된 리스트 업로드", type=["txt"])
        if uploaded_file is not None:
            if st.button("업로드 파일로 덮어쓰기", use_container_width=True, type="primary"):
                try:
                    file_text = uploaded_file.getvalue().decode("utf-8")
                    new_master_data = []
                    current_name = None
                    current_addrs = []
                    
                    for line in file_text.splitlines():
                        line_str = line.strip()
                        if not line_str:
                            continue
                        if "," in line_str:
                            parts = line_str.split(",", 1)
                            name_val = parts[0].strip()
                            addr_val = parts[1].strip()
                            if current_name and current_name != name_val:
                                new_master_data.append({"name": current_name, "addresses": current_addrs})
                                current_name = name_val
                                current_addrs = [addr_val] if addr_val else []
                            else:
                                current_name = name_val
                                if addr_val:
                                    current_addrs.append(addr_val)
                        else:
                            if current_name:
                                current_addrs.append(line_str)
                            else:
                                current_name = line_str
                                current_addrs = []
                                
                    if current_name:
                        new_master_data.append({"name": current_name, "addresses": current_addrs})
                        
                    if new_master_data:
                        st.session_state.master_addresses = new_master_data
                        st.session_state.matched_details_list = []
                        st.session_state.check_results = []
                        st.session_state.partial_results = None
                        st.success(f"총 {len(new_master_data)}건 반영 완료!")
                        st.rerun()
                except Exception as e:
                    st.error(f"오류 발생: {e}")

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("기본 복구", use_container_width=True, key="btn_reset"):
            st.session_state.master_addresses = initial_data.copy()
            st.session_state.matched_details_list = []
            st.session_state.check_results = []
            st.session_state.partial_results = None
            st.rerun()
    with col_b2:
        if st.button("전체 비우기", use_container_width=True, key="btn_clear"):
            st.session_state.master_addresses = []
            st.session_state.matched_details_list = []
            st.session_state.check_results = []
            st.session_state.partial_results = None
            st.rerun()

    st.markdown("---")
    
    # 일부 검색 (단어 검색 기능)
    st.markdown("**🔍 일부 검색** (단어 포함 리스트 찾기)")
    col_search1, col_search2 = st.columns([3, 1])
    with col_search1:
        search_keyword = st.text_input("단어 입력", placeholder="예: 구로구", label_visibility="collapsed")
    with col_search2:
        if st.button("검색", use_container_width=True, key="btn_partial_search"):
            keyword = search_keyword.strip()
            if keyword:
                st.session_state.last_search_keyword = keyword
                found_items = []
                for idx, item in enumerate(st.session_state.master_addresses):
                    n = item.get("name", "")
                    ads = item.get("addresses", [])
                    if keyword in n or any(keyword in a for a in ads):
                        found_items.append((idx + 1, item))
                st.session_state.partial_results = found_items
            else:
                st.session_state.partial_results = None
                st.session_state.last_search_keyword = ""
                
    if st.session_state.partial_results is not None:
        st.markdown(f"<span style='color:#FFD700; font-weight:bold;'>'{st.session_state.last_search_keyword}'</span> 검색 결과 ({len(st.session_state.partial_results)}건)", unsafe_allow_html=True)
        if len(st.session_state.partial_results) > 0:
            search_container = st.container(height=200)
            with search_container:
                for m_idx, m_item in st.session_state.partial_results:
                    m_name = m_item.get('name', '(이름 없음)')
                    st.markdown(f"<p style='margin:0; font-weight:bold;'>{m_idx}. <code>{m_name}</code></p>", unsafe_allow_html=True)
                    for addr in m_item.get('addresses', []):
                        st.markdown(f"<p style='margin:0 0 2px 15px; font-size:13px; color:#FFFFFF;'>{addr}</p>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin:4px 0; border:0; border-top:1px solid #444;'>", unsafe_allow_html=True)
        else:
            st.info("일치하는 결과가 없습니다.")
            
    st.markdown("---")

    # 블랙리스트 전체 목록 표시
    st.markdown(f"**블랙리스트 전체 목록 ({len(st.session_state.master_addresses)}건)**")
    
    if not st.session_state.master_addresses:
        st.info("등록된 기준 주소가 없습니다.")
    else:
        list_container = st.container(height=400)
        with list_container:
            for i, item in enumerate(st.session_state.master_addresses):
                name_display = item.get('name', '(이름 없음)')
                st.markdown(f"<p style='margin:0; font-weight:bold;'>{i+1}. <code>{name_display}</code></p>", unsafe_allow_html=True)
                
                addrs = item.get('addresses', [])
                if addrs:
                    for addr in addrs:
                        st.markdown(f"<p style='margin:0 0 2px 15px; font-size:13px; color:#FFFFFF;'>{addr}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='margin:0 0 2px 15px; font-size:13px; color:#AAAAAA;'>(등록된 주소 없음)</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0; border:0; border-top:1px solid #444;'>", unsafe_allow_html=True)


with col_right:
    st.markdown("<h4 style='font-size: 1.1rem;'>체크리스트 (STOP / CAUTION / PASS 판독기)</h4>", unsafe_allow_html=True)
    
    target_input = st.text_area(
        "대조할 주소 입력 (줄바꿈으로 여러 개 가능)",
        placeholder="서울특별시 성동구 성수일로 10\n강남구 테헤란로 123",
        key="target_textarea",
        height=180
    )
    
    if st.button("CHECK", use_container_width=True, key="btn_check"):
        if not target_input.strip():
            st.warning("대조할 주소를 입력해주세요.")
        else:
            targets = [t.strip() for t in target_input.split("\n") if t.strip()]
            st.session_state.matched_details_list = []
            st.session_state.check_results = []
            
            for t in targets:
                res_type = "PASS"
                matched_item = None
                matched_index = -1
                
                # 1. 완벽 일치 (STOP) 검증
                for idx, item in enumerate(st.session_state.master_addresses):
                    item_name = item.get('name', '')
                    item_addrs = item.get('addresses', [])
                    
                    is_matched = False
                    if is_name_matched(item_name, t):
                        is_matched = True
                    else:
                        for addr in item_addrs:
                            if is_address_matched(addr, t):
                                is_matched = True
                                break
                                
                    if is_matched:
                        res_type = "STOP"
                        matched_item = item
                        matched_index = idx + 1
                        break
                
                # 2. 부분 일치 (CAUTION) 검증 (STOP이 아닐 때만 실행)
                if res_type == "PASS":
                    for idx, item in enumerate(st.session_state.master_addresses):
                        item_addrs = item.get('addresses', [])
                        
                        is_caution = False
                        for addr in item_addrs:
                            if is_address_caution(addr, t):
                                is_caution = True
                                break
                                
                        if is_caution:
                            res_type = "CAUTION"
                            matched_item = item
                            matched_index = idx + 1
                            break
                
                # 결과 기록
                if matched_item:
                    st.session_state.check_results.append((res_type, t, matched_index, matched_item))
                    if (matched_index, matched_item) not in st.session_state.matched_details_list:
                        st.session_state.matched_details_list.append((matched_index, matched_item))
                else:
                    st.session_state.check_results.append(("PASS", t, 0, None))
            
            st.rerun()

    # 판정 결과 출력
    if st.session_state.check_results:
        for res_type, t_val, m_idx, m_item in st.session_state.check_results:
            if res_type == "STOP":
                st.markdown('<div class="stop-box">STOP</div>', unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 0; margin-bottom: 10px;'>{t_val}</p>", unsafe_allow_html=True)
            elif res_type == "CAUTION":
                st.markdown('<div class="caution-box">CAUTION (주소 일부 일치 - 확인요망)</div>', unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 0; margin-bottom: 10px;'>{t_val}</p>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="pass-box">PASS</div>', unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 0; margin-bottom: 10px;'>{t_val}</p>", unsafe_allow_html=True)

    # 매칭/주의 금지 목록 상세 전용 창
    if st.session_state.matched_details_list:
        match_container = st.container(height=220)
        with match_container:
            for m_idx, m_item in st.session_state.matched_details_list:
                m_name = m_item.get('name', '(이름 없음)')
                st.markdown(f"<p style='margin:0; font-weight:bold;'>{m_idx}. <code>{m_name}</code></p>", unsafe_allow_html=True)
                
                m_addrs = m_item.get('addresses', [])
                if m_addrs:
                    for addr in m_addrs:
                        st.markdown(f"<p style='margin:0 0 2px 15px; font-size:13px; color:#FFFFFF;'>{addr}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='margin:0 0 2px 15px; font-size:13px; color:#AAAAAA;'>(등록된 주소 없음)</p>", unsafe_allow_html=True)
                st.markdown("<hr style='margin:4px 0; border:0; border-top:1px solid #444;'>", unsafe_allow_html=True)
