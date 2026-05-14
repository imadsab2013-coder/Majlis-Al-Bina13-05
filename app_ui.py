import streamlit as st

# 1. إعدادات الهيكل الأساسي
st.set_page_config(page_title="Majlis Al-Bina v2.9", layout="wide", initial_sidebar_state="expanded")

# 2. هندسة المظهر التقني (CSS)
st.markdown("""
    <style>
    .main { background-color: #010307; }
    
    /* الصبورة الشبكية */
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

    /* تصميم أزرار الأعضاء بوضوح عالي وبالعربية */
    .stButton>button {
        background: linear-gradient(180deg, #0d1b2a, #050a0f);
        color: #b0d4ff;
        border: 1px solid #1a3a5a;
        font-size: 14px !important; /* حجم واضح للخط العربي */
        font-weight: 800;
        padding: 12px 5px;
        width: 100%;
        border-radius: 8px;
        transition: 0.3s all ease-in-out;
        font-family: 'Arial', sans-serif;
    }
    
    /* تأثير التشغيل عند النقر */
    .stButton>button:active, .stButton>button:focus {
        border-color: #00ccff;
        color: #ffffff;
        box-shadow: 0 0 25px rgba(0, 204, 255, 0.6);
        transform: scale(1.02);
    }

    /* أيقونة القرآن الكريم في الأسفل */
    .quran-container {
        text-align: center;
        margin-top: 20px;
        padding: 15px;
        border-top: 1px solid #102030;
    }
    .quran-symbol {
        font-size: 55px;
        color: #deff9a;
        filter: drop-shadow(0 0 15px #deff9a66);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. الشريط الجانبي (مركز التحكم المركزي) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#00ccff;'>⚙️ مركز التحكم</h2>", unsafe_allow_html=True)
    st.write("---")
    
    with st.expander("📂 الكاتالوك (Catalyst)", expanded=True):
        st.info("• فهارس المصطلحات المادية")
        st.info("• سجل القواعد §")
        
    with st.expander("👥 حالة الأعضاء (Status)", expanded=True):
        st.success("الأعضاء (1-5): نشط 🟢")
        st.success("الأعضاء (6-10): جاهز 🟢")
        
    with st.expander("📊 إدارة الداتا (Data)", expanded=False):
        st.button("مزامنة ملفات الإكسيل")
        
    with st.expander("🧠 وحدة الذكاء (AI Core)", expanded=False):
        st.write("المحرك: Majlis-Logic-v2")

# --- 4. توزيع الأعضاء حسب الكتالوج رقم 3 ---

# أ) الصف العلوي: الأعضاء (A1-A5) - تحليل أفقي
st.markdown("<p style='font-size:12px; color:#224466; text-align:center;'>وحدات التحليل الأفقي (A1-A5)</p>", unsafe_allow_html=True)
h_cols = st.columns(5)
# الأسماء المعتمدة في الكتالوج 3
h_names = ["A1: المُستقبِل", "A2: المُحلل السياقي", "A3: المُقارن المادي", "A4: المُلاحظ والراصد", "A5: الناقد المنطقي"]

for i, col in enumerate(h_cols):
    col.button(h_names[i])

# ب) المنطقة الوسطى: الصبورة + الأعضاء (A6-A10)
body_left, body_right = st.columns([8.2, 1.8])

with body_left:
    # الصبورة الكبرى
    st.markdown("<div class='the-board'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#0a1a2a; font-family:monospace; font-size:35px;'>[ SYSTEM_READY ]</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # صندوق السحر
    query = st.text_input("", placeholder="صندوق السحر: أدخل الكلمة للبدء في استخراج البينة المادية...")

with body_right:
    # الأعضاء العموديون (A6-A10) حسب الكتالوج 3
    st.markdown("<p style='font-size:11px; color:#224466; text-align:center;'>وحدات الضبط والتدقيق</p>", unsafe_allow_html=True)
    v_names = ["A6: حارس القواعد", "A7: المُصنف والمبوب", "A8: الآمر والحاكم", "A9: الصائغ النهائي", "A10: المنسق العام"]
    
    for name in v_names:
        st.button(name)
    
    # أيقونة القرآن في الأسفل
    st.markdown("""
        <div class='quran-container'>
            <div class='quran-symbol'>📖</div>
            <div style='color:#deff9a; font-size:14px; font-weight:bold;'>البيان القرآني</div>
        </div>
    """, unsafe_allow_html=True)

# 5. التفاعل المبدئي
if query:
    st.toast(f"يتم استدعاء البينة لتحليل: {query}")
