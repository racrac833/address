import streamlit as st

st.set_page_config(
    page_title="주소 대조 및 스마트 관리 프로그램",
    page_icon="🔍",
    layout="wide"
)

# 세션 상태 초기화
if "master_addresses" not in st.session_state:
    st.session_state.master_addresses = []

if "selected_item_info" not in st.session_state:
    st.session_state.selected_item_info = None

st.title("🔍 주소 대조 및 스마트 관리 프로그램")
st.markdown("이름과 기준 주소를 관리하고 신규 주소와 대조하는 프로그램입니다.")

st.divider()

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.subheader("📁 기준 금지 주소 관리 (좌측)")
    
    # 대량 텍스트 등록 영역
    with st.expander("📥 구글 시트 대량 한 번에 등록하기 (클릭해서 열기)", expanded=True):
        st.markdown("구글 시트의 내용을 복사해서 아래에 붙여넣으세요. (형식: `이름, 주소`)")
        bulk_input = st.text_area("대량 데이터 입력", placeholder="강민*, 경기 의정부시 배꽃길 63...\n강아*, 경상북도 칠곡군...", height=100, key="input_bulk")
        
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
    
    # 개별 등록 영역
    st.markdown("#### ➕ 개별 주소 추가")
    new_name_input = st.text_input("이름 (상호명/고객명)", placeholder="예: 홍길동", key="input_name")
    new_master_input = st.text_input("기준 주소", placeholder="예: 서울특별시 성동구 성수일로 10", key="input_addr")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("개별 항목 추가", use_container_width=True, key="btn_add"):
            if new_master_input.strip():
                item = {
                    "name": new_name_input.strip() if new_name_input.strip() else "이름 없음", 
                    "address": new_master_input.strip()
                }
                if item not in st.session_state.master_addresses:
                    st.session_state.master_addresses.append(item)
                    st.success("등록되었습니다!")
                    st.rerun()
            else:
                st.warning("기준 주소를 입력해주세요.")
    with col_b2:
        if st.button("🗑️ 전체 리스트 초기화", use_container_width=True, key="btn_clear"):
            st.session_state.master_addresses = []
            st.session_state.selected_item_info = None
            st.rerun()

    if st.session_state.selected_item_info:
        st.info(f"🔎 **[선택한 항목 상세 정보]**\n\n- **이름:** {st.session_state.selected_item_info['name']}\n\n- **주소:** {st.session_state.selected_item_info['address']}")

    st.markdown("---")
    st.markdown(f"### 📋 현재 등록된 금지 목록 ({len(st.session_state.master_addresses)}건)")
    if not st.session_state.master_addresses:
        st.info("등록된 기준 주소가 없습니다. 위에서 대량 등록이나 주소를 추가해 주세요.")
    else:
        for i, item in enumerate(st.session_state.master_addresses):
            c1, c2, c3 = st.columns([0.7, 0.15, 0.15])
            with c1:
                st.markdown(f"**{i+1}.** {item['name']}")
            with c2:
                if st.button("🔍", key=f"view_idx_{i}"):
                    st.session_state.selected_item_info = item
                    st.rerun()
            with c3:
                if st.button("❌", key=f"del_idx_{i}"):
                    if st.session_state.selected_item_info == item:
                        st.session_state.selected_item_info = None
                    st.session_state.master_addresses.pop(i)
                    st.rerun()

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
