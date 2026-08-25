import streamlit as st

st.set_page_config(
    page_title="주소 대조 및 스마트 관리 프로그램",
    page_icon="🔍",
    layout="wide"
)

# 기본 금지 리스트 데이터 자동 세팅
initial_data = [
    {"name": "강민*", "address": "경기 의정부시 배꽃길 63 지식산업센터"},
    {"name": "강아*", "address": "경상북도 칠곡군 왜관읍 금산로3길"},
    {"name": "구향*", "address": "경남 진주시 충무공동 혁신도시"},
    {"name": "권시*/최수*", "address": "서울특별시 광진구 뚝섬로"},
    {"name": "김관*", "address": "경기도 의정부시 용현로"},
    {"name": "김낙*", "address": "경기도 안양시 박달로"},
    {"name": "김명*/조명*", "address": "경기도 시흥시 은행로"},
    {"name": "김문*", "address": "경기도 화성시 향남읍 발안로"},
    {"name": "김민*", "address": "대구광역시 수성구 동대구로"},
    {"name": "김민*", "address": "서울특별시 성동구 성수일로 10"},
    {"name": "김성*/신선*", "address": "인천광역시 계양구 효성동"},
    {"name": "김수*/최재*", "address": "경상북도 칠곡군 북삼읍 금오대로1길"},
    {"name": "김승*", "address": "인천광역시 연수구 인천타워대로"},
    {"name": "김아*", "address": "남양주시 평내동"},
    {"name": "김예*", "address": "경기도 남양주시 진접읍 부평로"},
    {"name": "김용*", "address": "경기도 고양시 덕양구 덕동"},
    {"name": "김유*", "address": "인천광역시 서구 용해로"},
    {"name": "김ㅎ", "address": "서울 동대문구 왕산로 68"},
    {"name": "박주ㄹ(루ㅇ)", "address": "경기도 하남시 미사강변동로"},
    {"name": "박교*", "address": "서울특별시 성동구 상원길 26"},
    {"name": "박병*", "address": "서울특별시 영등포구 신길동"},
    {"name": "박수*", "address": "서울특별시 성북구 보문로29다길"},
    {"name": "박용*", "address": "부산광역시 수영구 광일로"},
    {"name": "박종*", "address": "경기도 용인시 기흥구 흥덕2로"},
    {"name": "박지*", "address": "경기도 화성시 향남읍 발안로"},
    {"name": "배지*", "address": "경기도 안양시 동안구 경수대로84번길"},
    {"name": "복영*", "address": "강서구 양천로"},
    {"name": "서동*", "address": "인천광역시 서구 크리스탈로"},
    {"name": "서현*", "address": "경기도 동두천시 송내동"},
    {"name": "신명*", "address": "인천광역시 연수구 송도동"},
    {"name": "신성*", "address": "경기도 김포시 장기동"},
    {"name": "양기*", "address": "서울특별시 마포구 양화로"},
    {"name": "양은*", "address": "경기도 수원시 영통구 망포동"},
    {"name": "양현*", "address": "서울특별시 구로구 디지털로34길"},
    {"name": "엄형*", "address": "경기도 화성시 향남읍 발안로"},
    {"name": "우지*", "address": "경기도 용인시 기흥구 농서로"},
    {"name": "윤현*", "address": "서울특별시 금천구 독산동"},
    {"name": "이가*", "address": "경기도 화성시 우정읍 조암서로13번길"},
    {"name": "이광*", "address": "충청남도 공주시 신풍면 봉갑리"},
    {"name": "이미*", "address": "경기도 파주시 다율동"},
    {"name": "이승*", "address": "경기도 성남시 분당구 정자동"},
    {"name": "이영*", "address": "서울특별시 구로구 신도림동"},
    {"name": "이원*/이은*", "address": "서울특별시 영등포구 디지털로70길"},
    {"name": "이유*", "address": "광주광역시 서구 풍암동"},
    {"name": "이주*/루*", "address": "경기도 하남시 미사강변동로"},
    {"name": "이창*", "address": "인천광역시 서구 루원시티"},
    {"name": "이해*", "address": "대구 방촌동"},
    {"name": "이현*", "address": "서울특별시 서초구 서초대로77길"},
    {"name": "이현*", "address": "인천광역시 서구 서곶로 120"},
    {"name": "장승*", "address": "경기도 의정부시 민락동"},
    {"name": "장현*/장호*", "address": "서울특별시 강남구 역삼동"},
    {"name": "정슬*", "address": "강동구 양재대로98길"},
    {"name": "정용*", "address": "울산광역시 북구 양정동"},
    {"name": "정진*", "address": "서울특별시 강서구 등촌동"},
    {"name": "정진*", "address": "서울특별시 강서구 공항대로"},
    {"name": "조현*", "address": "경기도 수원시 장안구 조원동"},
    {"name": "최재*", "address": "경기도 구리시 체육관로"},
    {"name": "최진*", "address": "인천광역시 부평구 경원대로"},
    {"name": "정인*", "address": "경기도 하남시 망월동"}
]

# 세션 상태 초기화
if "master_addresses" not in st.session_state or not st.session_state.master_addresses:
    st.session_state.master_addresses = initial_data.copy()

st.title("🔍 주소 대조 및 스마트 관리 프로그램")
st.markdown("이름과 기준 주소를 관리하고 신규 주소와 대조하는 프로그램입니다.")

st.divider()

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.subheader("📁 기준 금지 주소 관리 (좌측)")
    
    # 대량 등록 영역
    with st.expander("📥 구글 시트 대량 한 번에 등록하기 (클릭해서 열기)", expanded=False):
        st.markdown("구글 시트의 내용을 복사해서 아래에 붙여넣으세요. (형식: `이름, 주소`)")
        bulk_input = st.text_area("대량 데이터 입력", placeholder="이름, 주소 형식으로 입력", height=100, key="input_bulk")
        
        if st.button("🚀 대량 데이터 일괄 등록", use_container_width=True, key="btn_bulk_add"):
            if bulk_input.strip():
                lines = bulk_input.strip().split("\n")
                count = 0
                for line in lines:
                    parts = line.split(",", 1)
                    if len(parts) == 2:
                        name_val = parts[0].strip()
                        addr_val = parts[1].strip()
                        item = {"name": name_val, "address": addr_val}
                        if item not in st.session_state.master_addresses:
                            st.session_state.master_addresses.append(item)
                            count += 1
                st.success(f"총 {count}건이 등록되었습니다!")
                st.rerun()
            else:
                st.warning("내용을 입력해주세요.")

    st.markdown("---")
    
    # 개별 등록 및 초기화 버튼
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("🔄 기본 데이터로 복구", use_container_width=True, key="btn_reset"):
            st.session_state.master_addresses = initial_data.copy()
            st.success("기본 데이터가 로드되었습니다!")
            st.rerun()
    with col_b2:
        if st.button("🗑️ 전체 리스트 비우기", use_container_width=True, key="btn_clear"):
            st.session_state.master_addresses = []
            st.rerun()

    st.markdown("---")
    st.markdown(f"### 📋 현재 등록된 금지 목록 ({len(st.session_state.master_addresses)}건)")
    
    if not st.session_state.master_addresses:
        st.info("등록된 기준 주소가 없습니다.")
    else:
        # 스크롤 가능한 박스 안에서 이름과 주소를 2줄 간격으로 깔끔하게 출력
        list_container = st.container(height=400)
        with list_container:
            for i, item in enumerate(st.session_state.master_addresses):
                st.markdown(f"**{i+1}. {item['name']}**\n\n&nbsp;&nbsp;&nbsp;&nbsp;📍 {item['address']}")
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
            
            st.markdown("### 🚦 대조 결과 판정")
            for t in targets:
                matched_item = None
                for item in st.session_state.master_addresses:
                    m_addr = item["address"]
                    if m_addr in t or t in m_addr:
                        matched_item = item
                        break
                
                if matched_item:
                    st.error(f"🛑 **STOP** | `{t}` ➡️ **[금지된 이름: {matched_item['name']}]**")
                else:
                    st.success(f"🟢 **PASS** | `{t}` (신규 주소)")
