import streamlit as st

# إعدادات الهيكل الأساسي
st.set_page_config(page_title="Majlis Al-Bina v2.5", layout="wide", initial_sidebar_state="collapsed")

# هندسة المظهر التقني المتطور
st.markdown("""
    <style>
    .main { background-color: #010307; color: #88ccff; }
    
    /* الصبورة الشبكية الكبرى */
    .the-board {
        background-color: #000000;
        background-image: 
            linear-gradient(rgba(0, 204, 255, 0.08) 1px, transparent 1px), 
            linear-gradient(90deg, rgba(0, 204, 255, 0.08) 1px, transparent 1px);
        background-size: 40px 40px;
        border: 2px solid #102030;
        border-radius: 10px;
        height: 550px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 20px;
        box-shadow: inset 0 0 30px rgba(0, 150, 255, 0.05);
    }

    /* تصميم أزرار الأعضاء بوضوح عالي */
    .stButton>button {
        background: linear-gradient(145deg, #0a141e, #050a0f);
        color: #88ccff;
        border: 1px solid #1a3a5a;
        font-size: 14px !important; /* تكبير الخط */
        font-weight: bold;
        padding: 8px 5px;
        width: 100%;
        border-radius: 5px;
        transition: all 0.4s ease;
    }
    
    /* تأثير التشغيل عند النقر (Glow Effect) */
    .stButton>button:active, .stButton>button:focus {
        border-color: #00ccff;
        color: white;
        box-shadow: 0 0 15px #00ccff88;
        transform: scale(1.05);
    }

    /* صندوق السحر المدمج */
    .magic-box {
        background: #000;
        border: 1px solid #1a3a5a;
        padding: 2px;
        border-radius: 5px;
    }

    /* أيقونة القرآن المتميزة */
    .quran-icon {
        font-size: 45px; /* تكبير الحجم */
        color: #deff9a;
        text-align: center;
        margin-top: 20px;
        cursor: pointer;
        filter: drop-shadow(0 0 10px rgba(222, 255, 154, 0.3));
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الإعدادات الجانبي (Sidebar) ---
with st.sidebar:
    st.markdown("### ⚙️ لوحة التحكم المركزية")
    
    with st.expander("📂 الكاتالوك (Catalyst)", expanded=True):
        st.write("• فهارس المصطلحات المادية")
        st.write("• خرائط المفاهيم")
        
    with st.expander("👥 حالة الأعضاء (Status)", expanded=True):
        st.info("A1-A5: Ready 🟢")
        st.info("A6-A10: Ready 🟢")
        
    with st.expander("📊 إدارة الداتا (Data)", expanded=False):
        st.button("تحديث قاعدة بيانات الإكسيل")
        
    with st.expander("🧠 وحدة الذكاء (AI Core)", expanded=False):
        st.write("Model: Majlis-Agent-v1")
        st.slider("درجة دقة التحليل", 0, 100, 95)

# --- 1. الصف العلوي: الإعدادات المجهرية + الوكلاء (A1-A5) ---
head_left, head_center = st.columns([0.5, 9.5])

with head_left:
    st.button("⚙️") # زر لفتح الجانب

with head_center:
    # الوكلاء الأفقيون بأسماء واضحة
    h_cols = st.columns(5)
    h_agents = ["Research", "Marketing", "Resources", "Sales", "Legal"]
    for i, col in enumerate(h_cols):
        col.button(f"💠 {h_agents[i]}")

# --- 2. المنطقة المركزية: الصبورة + الوكلاء الجانبيون (A6-A10) ---
body_left, body_right = st.columns([8.5, 1.5])

with body_left:
    # الصبورة الكبرى (نظيفة بدون نصوص بالأسفل)
    st.markdown("<div class='the-board'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#0a1a2a; font-family:monospace; font-size:30px;'>[ BOARD IDLE ]</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # صندوق السحر
    query = st.text_input("The Magic Box (صندوق السحر)", placeholder="أدخل المصطلح المادي للبحث...")

with body_right:
    # الوكلاء العموديون (A6-A10)
    v_agents = ["Design", "Operations", "Support", "Finance", "Dev"]
    for agent in v_agents:
        st.button(f"💠 {agent}")
    
    # أيقونة القرآن في الأسفل وبحجم أكبر
    st.markdown("<div class='quran-icon'>📖</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:12px; color:#deff9a;'>البيان القرآني</p>", unsafe_allow_html=True)

# التفاعلية
if query:
    st.toast(f"يتم الآن استدعاء البينة لـ: {query}")
