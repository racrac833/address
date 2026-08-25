import streamlit as st
import re

st.set_page_config(
    page_title="주소 대조 및 스마트 관리 프로그램",
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
    {"name": "이승*", "addresses": ["경기도 성남시 분당구 정자동 193 정든마울한진8단지아파트 80*동 14**호"]},
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

# 세션 상태 초기화 및 데이터 호환성 보정
if "master_addresses" not in st.session_state or not st.session_state.master_addresses:
    st.session_state.master_addresses = initial_data.copy()
else:
    for item in st.session_state.master_addresses:
        if "addresses" not in item:
            if "address" in item:
                item["addresses"] = [item["address"]] if item["address"] else []
                del item["address"]
            else:
                item["addresses"] = []

if "matched_items_list" not in st.session_state:
    st.session_state.matched_items_list = []

if "check_results" not in st.session_state:
    st.session_state.check_results = []

# 자릿수 및 패턴 일치 엄격 매칭 함수
def is_address_matched(master_addr, target_addr):
    if master_addr in target_addr or target_addr in master_addr:
        return True
        
    m_words = master_addr.split()
    road_keywords = [w.replace('*', '') for w in m_words if any(w.endswith(s) for s in ['로', '길', '동', '읍', '면', '리', '가', '센터', '아파트', '오피스텔', '빌딩', '타워']) and len(w.replace('*', '')) >= 2]
    
    if road_keywords:
        matched_road = any(rk in target_addr for rk in road_keywords)
        if not matched_road:
            return False
    
    m_num_patterns = re.findall(r'\d+\**', master_addr)
    t_nums = re.findall(r'\d+', target_addr)
    
    if m_num_patterns and t_nums:
        for mp in m_num_patterns:
            if '*' in mp:
                expected_len = len(mp)
                prefix = mp.split('*')[0]
                if prefix:
                    has_matching_num = any(t_num.startswith(prefix) and len(t_num) == expected_len for t_num in t_nums)
                    if not has_matching_num:
                        return False
                        
    return True if road_keywords else False

st.title("🔍 주소 대조 및 스마트 관리 프로그램")
st.markdown("이름과 기준 주소를 관리하고 신규 주소와 대조하는 프로그램입니다.")

st.divider()

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.subheader("📁 기준 금지 주소 관리 (좌측)")
    
    # 📥 텍스트 파일(메모장) 다운로드 및 업로드 기능 영역
    with st.expander("📂 메모장(TXT) 파일로 다운로드 및 일괄 수정 (클릭해서 열기)", expanded=False):
        st.markdown("현재 등록된 금지 목록을 메모장 파일로 다운로드하거나, 수정된 파일을 업로드하여 일괄 반영할 수 있습니다.")
        
        # 현재 리스트를 텍스트 형식으로 변환 (이름, 주소 형태)
        txt_content = ""
        for item in st.session_state.master_addresses:
            name = item.get("name", "")
            addrs = item.get("addresses", [])
            if addrs:
                for addr in addrs:
                    txt_content += f"{name},{addr}\n"
            else:
                txt_content += f"{name},\n"
                
        # 다운로드 버튼
        st.download_button(
            label="💾 금지 목록 메모장 다운로드 (.txt)",
            data=txt_content,
            file_name="forbidden_addresses.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.markdown("---")
        
        # 업로드 영역
        uploaded_file = st.file_uploader("수정된 메모장 파일(.txt) 업로드", type=["txt"])
        if uploaded_file is not None:
            if st.button("🚀 업로드한 파일로 목록 일괄 덮어쓰기", use_container_width=True, type="primary"):
                try:
                    file_bytes = uploaded_file.getvalue()
                    file_text = file_bytes.decode("utf-8")
                    lines = file_text.splitlines()
                    
                    new_master_data = []
                    current_name = None
                    current_addrs = []
                    
                    for line in lines:
                        line_str = line.strip()
                        if not line_str:
                            continue
                            
                        if "," in line_str:
                            parts = line_str.split(",", 1)
                            name_val = parts[0].strip()
                            addr_val = parts[1].strip()
                            
                            # 같은 이름이 연속되거나 신규 이름일 경우 처리
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
                        st.session_state.matched_items_list = []
                        st.session_state.check_results = []
                        st.success(f"총 {len(new_master_data)}건의 금지 목록이 성공적으로 일괄 반영되었습니다!")
                        st.rerun()
                    else:
                        st.warning("파일에서 올바른 데이터를 읽지 못했습니다.")
                except Exception as e:
                    st.error(f"파일 처리 중 오류가 발생했습니다: {e}")

    st.markdown("---")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("🔄 기본 데이터로 복구", use_container_width=True, key="btn_reset"):
            st.session_state.master_addresses = initial_data.copy()
            st.session_state.matched_items_list = []
            st.session_state.check_results = []
            st.success("기본 데이터가 로드되었습니다!")
            st.rerun()
    with col_b2:
        if st.button("🗑️ 전체 리스트 비우기", use_container_width=True, key="btn_clear"):
            st.session_state.master_addresses = []
            st.session_state.matched_items_list = []
            st.session_state.check_results = []
            st.rerun()

    st.markdown("---")
    st.markdown(f"### 📋 현재 등록된 금지 목록 ({len(st.session_state.master_addresses)}건)")
    
    if not st.session_state.master_addresses:
        st.info("등록된 기준 주소가 없습니다.")
    else:
        list_container = st.container(height=400)
        with list_container:
            for i, item in enumerate(st.session_state.master_addresses):
                name_display = item.get('name', '(이름 없음)')
                st.markdown(f"**{i+1}. `{name_display}`**")
                
                addrs = item.get('addresses', [])
                if addrs:
                    for addr in addrs:
                        st.text(f"    {addr}")
                else:
                    st.text(f"    (등록된 주소 없음)")
                    
                st.markdown("---")

with col_right:
    st.subheader("⚡ 신규 주소 대조 검사 (우측)")
    st.markdown("검사할 주소를 입력하면 왼쪽 기준 리스트와 대조하여 결과를 표시합니다.")
    
    target_input = st.text_area(
        "대조할 주소 입력 (줄바꿈으로 여러 개 가능)",
        placeholder="서울특별시 성동구 성수일로 10\n강남구 테헤란로 123",
        key="target_textarea",
        height=250
    )
    
    if st.button("🔍 대조 및 판정 실행", type="primary", use_container_width=True, key="btn_check"):
        if not target_input.strip():
            st.warning("대조할 주소를 입력해주세요.")
        else:
            targets = [t.strip() for t in target_input.split("\n") if t.strip()]
            st.session_state.matched_items_list = []
            st.session_state.check_results = []
            
            for t in targets:
                matched_item = None
                
                for item in st.session_state.master_addresses:
                    item_addrs = item.get('addresses', [])
                    is_matched = False
                    
                    for addr in item_addrs:
                        if is_address_matched(addr, t):
                            is_matched = True
                            break
                            
                    if is_matched:
                        matched_item = item
                        break
                
                if matched_item:
                    if matched_item not in st.session_state.matched_items_list:
                        st.session_state.matched_items_list.append(matched_item)
                    st.session_state.check_results.append(("STOP", t, matched_item.get('name', '알 수 없음')))
                else:
                    st.session_state.check_results.append(("PASS", t, ""))
            
            st.rerun()

    # 판정 결과 출력 영역
    if st.session_state.check_results:
        st.markdown("### 🚦 대조 결과 판정")
        for res_type, t_val, m_name in st.session_state.check_results:
            if res_type == "STOP":
                st.error(f"🛑 **STOP** | `{t_val}` ➡️ **[금지된 이름: {m_name}]**")
            else:
                st.success(f"🟢 **PASS** | `{t_val}` (신규 주소)")

    # 🚨 매칭된 금지 목록 상세 전용 창 (우측 하단 별도 표시)
    if st.session_state.matched_items_list:
        st.markdown("---")
        st.markdown("### 🚨 매칭된 금지 목록 상세 정보")
        match_container = st.container(height=300)
        with match_container:
            for m_item in st.session_state.matched_items_list:
                m_name = m_item.get('name', '(이름 없음)')
                st.markdown(f"**🚨 [매칭됨] `{m_name}`**")
                m_addrs = m_item.get('addresses', [])
                if m_addrs:
                    for addr in m_addrs:
                        st.text(f"    {addr}")
                else:
                    st.text(f"    (등록된 주소 없음)")
                st.markdown("---")
