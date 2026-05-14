import streamlit as st
import data_engine as engine

st.set_page_config(page_title="مجلس البينة", layout="wide")

# تصميم السبورة والواجهة
st.markdown("""
    <style>
    .main { background-color: #010307; direction: rtl; }
    .the-black-board {
        background-color: #000000; border: 2px solid #1a1a1a;
        border-radius: 20px; min-height: 600px; padding: 30px;
        margin-bottom: 20px; overflow-y: auto;
    }
    .chat-entry { border-bottom: 1px solid #111; padding: 20px 0; }
    .data-text { color: #ffffff; font-size: 24px; border-right: 4px solid #00ccff; padding-right: 20px; line-height: 1.8; }
    .agent-name { color: #ff3366; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

if 'board_content' not in st.session_state: st.session_state.board_content = []
if 'show_search' not in st.session_state: st.session_state.show_search = False

# رأس الصفحة
col_t, col_i = st.columns([9, 1])
with col_t: st.markdown("<h1 style='color:#00ccff;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)
with col_i: 
    if st.button("📖", help="مختبر البيان المادي"):
        st.session_state.show_search = not st.session_state.show_search
        st.rerun()

# مختبر البيان (المساحة الكبيرة)
if st.session_state.show_search:
    st.markdown("### 🔍 مختبر البيان (المادة الخام)")
    tab1, tab2 = st.tabs(["📖 بحث السياق (13 آية)", "🗂️ جرد الألفاظ الشامل"])
    
    with tab1:
        c1, c2 = st.columns(2)
        surahs = engine.get_surah_list()
        s_name = c1.selectbox("اختر السورة:", surahs if surahs else ["البقرة"], key="s_sel")
        v_num = c2.number_input("الآية المركزية:", min_value=1, value=1, key="v_sel")
        if st.button("توليد السياق الممتد"):
            res = engine.get_context_block(s_name, v_num)
            st.text_area("الكتلة السياقية (6 قبل و 6 بعد):", value=res, height=500)

    with tab2:
        w_in = st.text_input("أدخل اللفظ (كتاب، الحمد، الطور...):", key="w_sel")
        if st.button("بدء الجرد المادي"):
            res = engine.get_word_collection(w_in)
            st.text_area("نتائج الجرد الشامل:", value=res, height=600)
    st.write("---")

# عرض السبورة
st.markdown('<div class="the-black-board">', unsafe_allow_html=True)
for entry in st.session_state.board_content:
    role_color = "#ff3366" if entry['role'] != "USER" else "#00ccff"
    st.markdown(f"""
        <div class="chat-entry">
            <span style="color:{role_color}; font-weight:900;">{entry['role']}:</span><br>
            <div class="data-text">{entry['text']}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# الإدخال
with st.container():
    c_in, c_send = st.columns([9, 1])
    user_input = c_in.text_input("ضع الآية هنا للتحليل...", label_visibility="collapsed")
    if c_send.button("🚀"):
        if user_input:
            st.session_state.board_content.append({"role": "USER", "text": user_input})
            st.rerun()
