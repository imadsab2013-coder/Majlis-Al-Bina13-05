import streamlit as st
import data_engine as engine  # الربط المادي بمحرك البيانات

# 1. إعدادات الهيكل الصارم
st.set_page_config(page_title="مجلس البينة", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #010307; direction: rtl; }
    .the-black-board {
        background-color: #000000; border: 2px solid #1a1a1a;
        border-radius: 20px; min-height: 500px; padding: 30px;
        margin-bottom: 20px; overflow-y: auto;
        box-shadow: inset 0 0 50px rgba(0, 204, 255, 0.05);
    }
    .chat-entry { border-bottom: 1px solid #111; padding: 15px 0; margin-bottom: 15px; }
    .agent-name { color: #ff3366; font-weight: 900; margin-left: 10px; font-family: monospace; }
    .data-text { color: #ffffff; font-size: 22px; border-right: 4px solid #00ccff; padding-right: 15px; line-height: 1.6; }
    .agent-content { color: #00ccff; font-size: 18px; padding-right: 40px; }
    .stButton>button { font-weight: 900 !important; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة بيانات الجلسة
if 'board_content' not in st.session_state: st.session_state.board_content = []
if 'present_agents' not in st.session_state: st.session_state.present_agents = []
if 'show_search' not in st.session_state: st.session_state.show_search = False

# 3. لوحة التحكم (الإعدادات)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ لوحة التحكم</h2>", unsafe_allow_html=True)
    with st.expander("📊 إدارة الداتا والملفات"):
        st.file_uploader("رفع كاتالوج جديد (xlsx)")
    with st.expander("🛠️ إدارة البروتوكولات"):
        st.write("تعديل منطق الأعضاء (A1-A10)")
    with st.expander("📜 سجل القواعد §"):
        st.write("القواعد المادية المعتمدة")

# 4. الواجهة الرئيسية
col_title, col_icon = st.columns([8.5, 1.5])
with col_title:
    st.markdown("<h1 style='color:#00ccff; margin-bottom:0;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)
with col_icon:
    if st.button("📖", help="افتح مختبر البيان للبحث والجرد"):
        st.session_state.show_search = not st.session_state.show_search
        st.rerun()

# --- محرك البحث المادي (سياق + جمع) ---
if st.session_state.show_search:
    st.markdown("<div style='background-color:#050505; padding:20px; border-radius:15px; border:1px solid #111;'>", unsafe_allow_html=True)
    st.markdown("### 🔍 مختبر البيان (المادة الخام)")
    col_context, col_collection = st.columns(2)
    
    with col_context:
        st.markdown("#### 1. بحث السياق المادي")
        surahs = engine.get_surah_list() # جلب السور من الداتا فعلياً
        s_name = st.selectbox("السورة:", surahs if surahs else ["البقرة"], key="ctx_s")
        v_num = st.number_input("الآية:", min_value=1, key="ctx_v")
        if st.button("إظهار كتلة السياق"):
            result = engine.get_context_block(s_name, v_num) # نداء المحرك
            st.code(result, language="text")
            st.caption("انسخ النص أعلاه وضعه في السبورة.")

    with col_collection:
        st.markdown("#### 2. بحث الجمع والجرد")
        word_q = st.text_input("أدخل اللفظ المادي لجرد مواضعه:", key="coll_w")
        if st.button("بدء الجرد المادي"):
            result = engine.get_word_collection(word_q) # نداء المحرك
            st.code(result, language="text")
            st.caption("نتائج الجرد من ملف الألفاظ.")
    
    if st.button("إغلاق المختبر ✖️"):
        st.session_state.show_search = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# 5. استدعاء الأعضاء (A1-A10)
st.write("### 👥 استدعاء الأعضاء (اضغط مرتين للدخول للسبورة)")
agent_cols = st.columns(10)
agent_names = [f"A{i}" for i in range(1, 11)]
for i, col in enumerate(agent_cols):
    if col.button(agent_names[i]):
        if agent_names[i] not in st.session_state.present_agents:
            st.session_state.present_agents.append(agent_names[i])
            st.rerun()

# 6. السبورة السوداء الكبيرة (ميدان النقاش)
st.markdown('<div class="the-black-board">', unsafe_allow_html
