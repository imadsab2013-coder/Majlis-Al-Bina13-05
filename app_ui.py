import streamlit as st

# 1. إعدادات الهيكل الأساسي
st.set_page_config(page_title="Majlis Al-Bina v3.5", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة المظهر (CSS) - الحل الجذري للخط العمودي وتنسيق الأسماء
st.markdown("""
    <style>
    /* حذف الخط العمودي الذي يظهر عند إغلاق Sidebar */
    [data-testid="stVerticalBlock"] > div > div > div > div { border: none !important; }
    [data-testid="stColumn"] { border: none !important; }

    .main { background-color: #010307; direction: rtl; }
    
    /* السبورة التفاعلية */
    .the-board {
        background-color: #000000;
        background-image: 
            linear-gradient(rgba(0, 204, 255, 0.08) 1.5px, transparent 1.5px), 
            linear-gradient(90deg, rgba(0, 204, 255, 0.08) 1.5px, transparent 1.5px);
        background-size: 45px 45px;
        border: 2px solid #102030;
        border-radius: 12px;
        height: 480px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: inset 0 0 40px rgba(0, 150, 255, 0.1);
        margin-bottom: 20px;
        color: #00ccff;
        font-family: 'Courier New', monospace;
        font-size: 28px;
        text-align: center;
    }

    /* أزرار الأعضاء - خط عريض 900 وتصميم مادي */
    .stButton>button {
        background: linear-gradient(180deg, #0d1b2a, #050a0f);
        color: #b0d4ff;
        border: 1px solid #1a3a5a;
        font-size: 14px !important;
        font-weight: 900 !important; /* خط عريض جداً */
        padding: 10px 2px;
        width: 100%;
        border-radius: 8px;
        transition: 0.3s all;
    }
    
    .stButton>button:hover {
        border-color: #00ccff;
        box-shadow: 0 0 15px rgba(0, 204, 255, 0.5);
        color: #ffffff;
    }

    /* أيقونة القرآن بتوهج أخضر */
    .quran-glow {
        text-align: center;
        margin-top: 30px;
        padding: 10px;
        filter: drop-shadow(0 0 10px rgba(222, 255, 154, 0.4));
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة الحالة (Session State) للتفاعلية
if 'active_member' not in st.session_state:
    st.session_state.active_member = "[ SYSTEM_READY ]"

# --- 4. التوزيع الأفقي (A1 - A5) ---
st.markdown("<p style='text-align:center; color:#224466; font-size:12px;'>وحدات التحليل الأفقي (الكتالوج 3)</p>", unsafe_allow_html=True)
h_names = ["A1: المُستقبِل", "A2: المُحلل السياقي", "A3: المُقارن المادي", "A4: المُلاحظ والراصد", "A5: الناقد المنطقي"]
h_cols = st.columns(5)

for i in range(5):
    if h_cols[i].button(h_names[i]):
        st.session_state.active_member = f"العضو النشط: {h_names[i]}"

st.write("") 

# --- 5. الصبورة + التوزيع العمودي (A6 - A10) ---
# توزيع 8.5 لليمن (الصبورة) و 1.5 لليسار (الأعضاء) لتجنب التداخل
main_col, side_col = st.columns([8.5, 1.5])

with main_col:
    # عرض السبورة مع الحالة المحدثة
    st.markdown(f"<div class='the-board'>{st.session_state.active_member}</div>", unsafe_allow_html=True)
    
    # صندوق السحر في المنتصف
    query = st.text_input("", placeholder="صندوق السحر: أدخل الكلمة للبدء في استخراج البينة المادية...")

with side_col:
    st.markdown("<p style='text-align:center; color:#224466; font-size:11px;'>وحدات الضبط</p>", unsafe_allow_html=True)
    v_names = ["A6: حارس القواعد §", "A7: المُصنف والمبوب", "A8: الآمر والحاكم", "A9: الصائغ النهائي", "A10: المنسق العام"]
    
    for name in v_names:
        if st.button(name):
            st.session_state.active_member = f"العضو النشط: {name}"
    
    # أيقونة القرآن المتميزة
    st.markdown("""
        <div class='quran-glow'>
            <div style='font-size:50px;'>📖</div>
            <div style='color:#deff9a; font-size:12px; font-weight:bold;'>البيان القرآني</div>
        </div>
    """, unsafe_allow_html=True)

# 6. شريط جانبي مخفي للإعدادات والبروتوكولات
with st.sidebar:
    st.header("⚙️ الإعدادات")
    st.button("أيقونة البروتوكولات")
    st.button("سجل القواعد §")

if query:
    st.toast(f"جاري معالجة: {query}")
