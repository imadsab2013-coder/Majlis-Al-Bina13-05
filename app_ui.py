import streamlit as st
import data_engine as engine

# 1. الإعدادات والبروتوكولات (بلا نقصان)
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
    .agent-name { color: #ff3366; font-weight: 900; margin-left: 10px; }
    .data-text { color: #ffffff; font-size: 22px; border-right: 4px solid #00ccff; padding-right: 15px; line-height: 1.6; }
    .agent-content { color: #00ccff; font-size: 18px; padding-right: 40px; }
    .stButton>button { font-weight: 900 !important; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة بيانات الجلسة
if 'board_content' not in st.session_state: st.session_state.board_content = []
if 'present_agents' not in st.session_state: st.session_state.present_agents = []
if 'show_search' not in st.session_state: st.session_state.show_search = False

# 3. لوحة التحكم الجانبية (Sidebar) - هاهي رجعات كاملة
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
    if st.button("📖", help="افتح مختبر البيان"):
        st.session_state.show_search = not st.session_state.show_search
        st.rerun()

# 5. مختبر البيان (مساحة البحث الموسعة)
if st.session_state.show_search:
    st.markdown("---")
    tab1, tab2 = st.tabs(["📖 بحث السياق (13 آية)", "🗂️ جرد الألفاظ الشامل"])
    with tab1:
        c1, c2 = st.columns(2)
        surahs = engine.get_surah_list()
        s_name = c1.selectbox("السورة:", surahs if surahs else ["البقرة"], key="s_search")
        v_num = c2.number_input("الآية المركزية:", min_value=1, value=1, key="v_search")
        if st.button("إظهار السياق الموسع"):
            res = engine.get_context_block(s_name, v_num)
            st.text_area("الكتلة المادية:", res, height=400)
    with tab2:
        word_q = st.text_input("أدخل اللفظ للجرد (مثلاً: الحمد، كتاب):", key="w_search")
        if st.button("بدء الجرد الجماعي"):
            res = engine.get_word_collection(word_q)
            st.text_area("نتائج الجرد:", res, height=400)
    st.write("---")

# 6. استدعاء الأعضاء (A1-A10) - رجعوا لبلاصتهم
st.write("### 👥 استدعاء الأعضاء")
agent_cols = st.columns(10)
agent_names = [f"A{i}" for i in range(1, 11)]
for i, col in enumerate(agent_cols):
    if col.button(agent_names[i]):
        if agent_names[i] not in st.session_state.present_agents:
            st.session_state.present_agents.append(agent_names[i])
            st.rerun()

# 7. السبورة السوداء
st.markdown('<div class="the-black-board">', unsafe_allow_html=True)
if st.session_state.present_agents:
    p_cols = st.columns(len(st.session_state.present_agents))
    for idx, agent in enumerate(st.session_state.present_agents):
        with p_cols[idx]:
            st.markdown(f"<div style='text-align:center; color:#ff3366; font-weight:bold;'>👤 {agent}</div>", unsafe_allow_html=True)
            if st.button(f"تكلم {agent}", key=f"btn_{agent}"):
                last_user = next((item['text'] for item in reversed(st.session_state.board_content) if item['role'] == "USER"), "لا توجد مادة")
                st.session_state.board_content.append({"role": agent, "text": f"تحليل مادي لـ {agent} بناءً على: {last_user[:30]}..."})
                st.rerun()

for entry in st.session_state.board_content:
    if entry['role'] == "USER":
        st.markdown(f"<div class='chat-entry'><div class='data-text'>{entry['text']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-entry'><span class='agent-name'>{entry['role']}:</span> <span class='agent-content'>{entry['text']}</span></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 8. منطقة الإدخال
with st.container():
    c_in, c_send = st.columns([8.5, 1.5])
    user_msg = c_in.text_input("ضع النص المادي للتحليل...", label_visibility="collapsed")
    if c_send.button("🚀 إرسال"):
        if user_msg:
            st.session_state.board_content.append({"role": "USER", "text": user_msg})
            st.rerun()
