import streamlit as st

# إعدادات الشاشة
st.set_page_config(page_title="Majlis Al-Bina", layout="wide", initial_sidebar_state="collapsed")

# هندسة المظهر (CSS)
st.markdown("""
    <style>
    .main { background-color: #020408; }
    
    /* الصبورة الشبكية المركزية */
    .the-board {
        background-color: #000000;
        background-image: 
            linear-gradient(rgba(0, 204, 255, 0.05) 1px, transparent 1px), 
            linear-gradient(90deg, rgba(0, 204, 255, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        border: 1px solid #1a3a5a;
        border-radius: 5px;
        height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }

    /* تصميم الأزرار الصغيرة جداً */
    .stButton>button {
        background: rgba(10, 20, 30, 0.8);
        color: #55aaff;
        border: 1px solid #1a3a5a;
        font-size: 10px !important;
        padding: 2px;
        width: 100%;
    }
    
    .stButton>button:hover { border-color: #00ccff; color: #fff; }

    /* صندوق السحر */
    .magic-box {
        border-top: 1px solid #1a3a5a;
        padding-top: 10px;
        color: #446688;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الصف الأول: الإعدادات + الوكلاء (A1-A5) + القرآن ---
header_left, header_center, header_right = st.columns([0.5, 7, 2])

with header_left:
    if st.button("⚙️"): # إعدادات مجهرية
        st.toast("Settings Accessed")

with header_center:
    # الوكلاء الأفقيون (A1-A5)
    h_cols = st.columns(5)
    h_agents = ["Research", "Marketing", "Resources", "Sales", "Legal"]
    for i, col in enumerate(h_cols):
        col.button(f"◈ {h_agents[i]}")

with header_right:
    st.markdown("<div style='text-align:right; font-size:12px; color:#88ccff;'>📖 القرآن الكريم</div>", unsafe_allow_html=True)

# --- المنطقة المركزية: الصبورة + الوكلاء الجانبيون (A6-A10) ---
body_left, body_right = st.columns([8.5, 1.5])

with body_left:
    # الصبورة الكبرى
    st.markdown("<div class='the-board'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#1a3a5a; font-family:monospace;'>[ GRID SYSTEM ACTIVE ]</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # صندوق السحر
    st.markdown("<div class='magic-box'>", unsafe_allow_html=True)
    query = st.text_input("The Magic Box (صندوق السحر)", placeholder="أدخل استفسارك هنا...")
    st.markdown("</div>", unsafe_allow_html=True)

with body_right:
    # الوكلاء العموديون (A6-A10)
    st.markdown("<p style='font-size:9px; color:#224466; text-align:center;'>Vertical Units</p>", unsafe_allow_html=True)
    v_agents = ["Design", "Operations", "Support", "Finance", "Development"]
    for agent in v_agents:
        st.button(f"◈ {agent}")
    
    st.markdown("---")
    st.markdown("<div style='font-size:10px;'>Catalyst 🟢</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;'>System 🟢</div>", unsafe_allow_html=True)
