import streamlit as st
import data_engine as engine

# 1. إعدادات الهيكل
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
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة بيانات الجلسة
if 'board_content' not in st.session_state: st.session_state.board_content = []
if 'present_agents' not in st.session_state: st.session_state.present_agents = []
if 'show_search' not in st.session_state: st.session_state.show_search = False

# 3. لوحة التحكم
with st.sidebar:
    st.markdown("## ⚙️ لوحة التحكم")
    with st.expander("📊 إدارة الداتا"):
        st.file_uploader("رفع إكسيل جديد")
    with st.expander("📜 سجل القواعد"):
        st.write("القواعد المادية")

# 4. العنوان ومحرك البحث
col_t, col_i = st.columns([8.5, 1.5])
with col_t: st.markdown("<h1 style='color:#00ccff;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)
with col_i: 
    if st.button("📖"):
        st.session_state.show_search = not st.session_state.show_search
        st.rerun()

if st.session_state.show_search:
    st.markdown("---")
    col_ctx, col_coll = st.columns(2)
    with col_ctx:
        st.write("🔍 1. بحث السياق")
        surahs = engine.get_surah_list()
        s_name = st.selectbox("السورة:", surahs if surahs else ["البقرة"], key="s_box")
        v_num = st.number_input("الآية:", min_value=1, key="v_box")
        if st.button("إظهار السياق"):
            st.code(engine.get_context_block(s_name, v_num), language="text")
    with col_coll:
        st.write("🗂️ 2. جرد الألفاظ")
        word_q = st.text_input("أدخل اللفظ:", key="w_box")
        if st.button("بدء الجرد"):
            st.code(engine.get_word_collection(word_q), language="text")

# 5. استدعاء الأعضاء
st.write("### 👥 الأعضاء")
agent_cols = st.columns(10)
for i in range(1, 11):
    if agent_cols[i-1].button(f"A{i}"):
        if f"A{i}" not in st.session_state.present_agents:
            st.session_state.present_agents.append(f"A{i}")
            st.rerun()

# 6. السبورة (تم تصحيح القفل هنا)
st.markdown('<div class="the-black-board">', unsafe_allow_html=True)
if st.session_state.present_agents:
    p_cols = st.columns(len(st.session_state.present_agents))
    for idx, agent in enumerate(st.session_state.present_agents):
        with p_cols[idx]:
            if st.button(f"تكلم {agent}", key=f"talk_{agent}"):
                last_msg = next((m['text'] for m in reversed(st.session_state.board_content) if m['role']=="USER"), "لا يوجد نص")
                st.session_state.board_content.append({"role": agent, "text": f"تحليل مادي لـ: {last_msg[:30]}"})
                st.rerun()

for entry in st.session_state.board_content:
    if entry['role'] == "USER":
        st.markdown(f"<div class='chat-entry'><div class='data-text'>{entry['text']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-entry'><span class='agent-name'>{entry['role']}:</span> <span class='agent-content'>{entry['text']}</span></div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 7. الإدخال
with st.container():
    c_in, c_send = st.columns([8.5, 1.5])
    with c_in: u_input = st.text_input("أدخل النص...", label_visibility="collapsed")
    with c_send:
        if st.button("🚀"):
            if u_input:
                st.session_state.board_content.append({"role": "USER", "text": u_input})
                st.rerun()
