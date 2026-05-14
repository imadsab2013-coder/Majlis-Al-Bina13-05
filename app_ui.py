import streamlit as st

# 1. إعدادات الهيكل الأساسي (الوضع العريض + إخفاء القوائم الافتراضية)
st.set_page_config(page_title="Majlis Al-Bina v2.8", layout="wide", initial_sidebar_state="expanded")

# 2. هندسة المظهر التقني (CSS)
st.markdown("""
    <style>
    /* الخلفية السوداء العميقة */
    .main { background-color: #010307; }
    
    /* تصميم الصبورة الشبكية (The Board) */
    .the-board {
        background-color: #000000;
        background-image: 
            linear-gradient(rgba(0, 204, 255, 0.08) 1.5px, transparent 1.5px), 
            linear-gradient(90deg, rgba(0, 204, 255, 0.08) 1.5px, transparent 1.5px);
        background-size: 45px 45px;
        border: 2px solid #102030;
        border-radius: 12px;
        height: 520px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: inset 0 0 40px rgba(0, 150, 255, 0.1);
        margin-bottom: 15px;
    }

    /* أزرار الأعضاء - وضوح عالي جداً */
    .stButton>button {
        background: linear-gradient(180deg, #0d1b2a, #050a0f);
        color: #b0d4ff;
        border: 1px solid #1a3a5a;
        font-size: 15px !important; /* تكبير الخط ليكون واضحاً */
        font-weight: 800; /* خط سميك */
        padding: 10px 5px;
        width: 100%;
        border-radius: 8px;
        text-transform: uppercase;
        transition: 0.3s all ease-in-out;
    }
    
    /* تأثير التشغيل (Active Glow) */
    .stButton>button:hover {
        border-color: #00ccff;
        color: #ffffff;
        box-shadow: 0 0 20px rgba(0, 204, 255, 0.4);
        transform: translateY(-2px);
    }

    /* أيقونة القرآن الكريم المطورة */
    .quran-container {
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        border-top: 1px solid #102030;
    }
    .quran-symbol {
        font-size: 60px;
        filter: drop-shadow(0 0 15px #deff9a88);
        color: #deff9a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. الشريط الجانبي المركزي (Sidebar Control) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ccff; text-align:center;'>لوحة التحكم المركزية</h2>", unsafe_allow_html=True)
    st.write("---")
    
    with st.expander("📂 الكاتالوك (Catalyst)", expanded=True):
        st.info("• فهرس المصطلحات المادية")
        st.info("• خرائط التقاطع البياني")
        
    with st.expander("👥 حالة الأعضاء (Status)", expanded=True):
        st.success("A1-A5: Active 🟢")
        st.success("A6-A10: Standby 🔵")
        
    with st.expander("📊 إدارة الداتا (Data)", expanded=False):
        st.button("تزامن ملفات الإكسيل")
        st.caption("Last Sync: 14 May 2026")
        
    with st.expander("🧠 وحدة الذكاء (AI Core)", expanded=False):
        st.slider("دقة المحرك المنطقي", 0, 100, 98)
        st.code("Model: Majlis-Logic-v2")

# --- 4. الهيكل الرئيسي للواجهة ---

# أ) الصف العلوي: الوكلاء الأفقيون (A1-A5)
st.markdown("<p style='font-size:12px; color:#224466;'>Horizontal Analysis Units (A1-A5)</p>", unsafe_allow_html=True)
h_cols = st.columns(5)
h_agents = ["RESEARCH", "MARKETING", "RESOURCES", "SALES", "LEGAL"]
for i, col in enumerate(h_cols):
    col.button(f"💠 {h_agents[i]}")

# ب) المنطقة الوسطى: الصبورة + الوكلاء الجانبيون (A6-A10)
body_left, body_right = st.columns([8.2, 1.8])

with body_left:
    # الصبورة المركزية
    st.markdown("<div class='the-board'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#0a1a2a; font-family:monospace; font-size:35px;'>[ SYSTEM_ONLINE ]</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # صندوق السحر
    query = st.text_input("", placeholder="The Magic Box (صندوق السحر) - أدخل المصطلح المادي هنا للتحليل...")

with body_right:
    # الوكلاء العموديون (A6-A10)
    st.markdown("<p style='font-size:10px; color:#224466; text-align:center;'>Vertical Units</p>", unsafe_allow_html=True)
    v_agents = ["DESIGN", "OPERAT.", "SUPPORT", "FINANCE", "DEV"]
    for agent in v_agents:
        st.button(f"⚡ {agent}")
    
    # أيقونة القرآن في الأسفل
    st.markdown("""
        <div class='quran-container'>
            <div class='quran-symbol'>📖</div>
            <div style='color:#deff9a; font-size:14px; font-weight:bold;'>البيان القرآني</div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. منطق التشغيل المبدئي ---
if query:
    st.toast(f"جاري تحليل البينة لـ: {query}")
