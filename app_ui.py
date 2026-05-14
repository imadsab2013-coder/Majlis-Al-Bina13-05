import streamlit as st
import data_engine as engine

st.set_page_config(page_title="مجلس البينة", layout="wide")

# استعادة التصميم المادي الأصلي
st.markdown("""
    <style>
    .main { background-color: #010307; direction: rtl; }
    .the-black-board {
        background-color: #000000; border: 2px solid #1a1a1a;
        border-radius: 20px; min-height: 500px; padding: 30px; margin-bottom: 20px;
    }
    .data-text { color: #ffffff; font-size: 20px; border-right: 3px solid #00ccff; padding-right: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'board_content' not in st.session_state: st.session_state.board_content = []
if 'present_agents' not in st.session_state: st.session_state.present_agents = []
if 'show_search' not in st.session_state: st.session_state.show_search = False

# رأس الصفحة
c1, c2 = st.columns([9, 1])
with c1: st.markdown("<h1 style='color:#00ccff;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)
with c2: 
    if st.button("📖"): st.session_state.show_search = not st.session_state.show_search; st.rerun()

# مختبر البيان (التصحيح المادي)
if st.session_state.show_search:
    st.markdown("### 🔍 مختبر البيان")
    t1, t2 = st.tabs(["📖 السياق", "🗂️ الألفاظ"])
    with t1:
        s_list = engine.get_surah_list()
        s_name = st.selectbox("السورة:", s_list if s_list else ["البقرة"])
        v_num = st.number_input("الآية:", min_value=1, value=1)
        if st.button("توليد السياق"):
            st.text_area("النتيجة:", engine.get_context_block(s_name, v_num), height=300)
    with t2:
        w_in = st.text_input("اللفظ:")
        if st.button("بدء الجرد"):
            st.text_area("النتيجة:", engine.get_word_collection(w_in), height=300)

# استعادة الأعضاء (A1-A10)
st.write("### 👥 الأعضاء")
agent_cols = st.columns(10)
for i in range(1, 11):
    if agent_cols[i-1].button(f"A{i}"):
        if f"A{i}" not in st.session_state.present_agents:
            st.session_state.present_agents.append(f"A{i}")
            st.rerun()

# السبورة السوداء
st.markdown('<div class="the-black-board">', unsafe_allow_html=True)
if st.session_state.present_agents:
    p_cols = st.columns(len(st.session_state.present_agents))
    for idx, agent in enumerate(st.session_state.present_agents):
        if p_cols[idx].button(f"تكلم {agent}"):
            last_msg = next((m['text'] for m in reversed(st.session_state.board_content) if m['role']=="USER"), "نص فارغ")
            st.session_state.board_content.append({"role": agent, "text": f"تحليل مادي لـ {agent}: {last_msg[:30]}"})
            st.rerun()

for entry in st.session_state.board_content:
    st.markdown(f"<b>{entry['role']}:</b><div class='data-text'>{entry['text']}</div><br>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# الإدخال
user_msg = st.text_input("لصق الآية...")
if st.button("🚀"):
    if user_msg: st.session_state.board_content.append({"role": "USER", "text": user_msg}); st.rerun()
