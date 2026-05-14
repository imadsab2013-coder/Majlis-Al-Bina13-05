import streamlit as st

# 1. إعدادات الهيكل والتصميم الصارم
st.set_page_config(page_title="مجلس البينة", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #010307; direction: rtl; }
    
    /* السبورة السوداء الكبيرة - ميدان العمل */
    .the-black-board {
        background-color: #000000;
        border: 2px solid #1a1a1a;
        border-radius: 20px;
        min-height: 600px;
        padding: 30px;
        margin-bottom: 20px;
        position: relative;
        overflow-y: auto;
    }

    /* أيقونة القرآن المستقلة في الواجهة */
    .quran-icon-main {
        font-size: 50px;
        cursor: pointer;
        transition: 0.3s;
        text-align: center;
    }
    
    /* فقاعات النقاش داخل السبورة */
    .chat-entry {
        border-bottom: 1px solid #111;
        padding: 15px 0;
        margin-bottom: 10px;
    }
    .agent-tag {
        color: #ff3366;
        font-weight: bold;
        margin-left: 10px;
    }
    .data-text {
        color: #ffffff;
        font-size: 20px;
        border-right: 3px solid #00ccff;
        padding-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة الجلسة
if 'board_content' not in st.session_state: st.session_state.board_content = []
if 'present_agents' not in st.session_state: st.session_state.present_agents = []

# 3. لوحة التحكم (الإعدادات فقط)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    with st.expander("📊 إدارة الداتا والملفات"):
        st.file_uploader("رفع كاتالوج جديد")
    with st.expander("🛠️ إدارة البروتوكولات"):
        st.write("تعديل منطق الأعضاء (A1-A10)")
    with st.expander("📜 سجل القواعد §"):
        st.write("القواعد المنطقية المعتمدة")

# 4. الواجهة الرئيسية
col_title, col_quran = st.columns([8, 2])
with col_title:
    st.markdown("<h1 style='color:#00ccff;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)
with col_quran:
    # أيقونة القرآن المستقلة
    if st.button("📖", help="اضغط للبحث في القرآن"):
        st.session_state.show_search = True

# محرك البحث (يظهر فقط عند الضغط على الأيقونة)
if st.session_state.get('show_search', False):
    with st.container():
        st.markdown("### 🔍 محرك البحث المادي")
        t1, t2 = st.tabs(["البحث بالآيات", "البحث بالألفاظ"])
        with t1:
            st.selectbox("السورة:", ["البقرة", "آل عمران"]) # تجلب من الداتا لاحقاً
            st.number_input("الآية:", min_value=1)
            st.info("انسخ الآية وضعها في السبورة أدناه.")
        with t2:
            st.text_input("أدخل اللفظ:")
        if st.button("إغلاق المحرك"):
            st.session_state.show_search = False
            st.rerun()

# أزرار استدعاء الأعضاء (A1-A10)
st.write("### 👥 استدعاء الأعضاء (اضغط مرتين للإدخال للسبورة)")
agent_cols = st.columns(10)
for i in range(1, 11):
    if agent_cols[i-1].button(f"A{i}"):
        if f"A{i}" not in st.session_state.present_agents:
            st.session_state.present_agents.append(f"A{i}")

# 5. السبورة السوداء الكبيرة (محل النقاش والنتائج)
st.markdown('<div class="the-black-board">', unsafe_allow_html=True)

# عرض الأعضاء الحاضرين داخل السبورة كأيقونات نشطة
if st.session_state.present_agents:
    cols = st.columns(len(st.session_state.present_agents))
    for idx, agent in enumerate(st.session_state.present_agents):
        with cols[idx]:
            st.markdown(f"<div style='text-align:center; color:#ff3366;'>👤 {agent}</div>", unsafe_allow_html=True)
            if st.button(f"تكلم {agent}", key=f"speak_{agent}"):
                st.session_state.board_content.append({"role": agent, "text": f"تحليل مادي من {agent}..."})

# عرض "نهر المحادثة" داخل السبورة
for entry in st.session_state.board_content:
    if entry['role'] == "USER":
        st.markdown(f"<div class='chat-entry'><div class='data-text'>{entry['text']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-entry'><span class='agent-tag'>{entry['role']}:</span> <span style='color:#00ccff;'>{entry['text']}</span></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 6. منطقة الإدخال (تحت السبورة مباشرة)
with st.container():
    col_input, col_send = st.columns([8, 2])
    with col_input:
        user_msg = st.text_input("أدخل الآية أو الأمر هنا...", label_visibility="collapsed")
    with col_send:
        if st.button("🚀 إرسال للسبورة"):
            if user_msg:
                st.session_state.board_content.append({"role": "USER", "text": user_msg})
                st.rerun()
