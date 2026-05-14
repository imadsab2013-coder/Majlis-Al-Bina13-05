import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="مجلس البينة", layout="wide", initial_sidebar_state="expanded")

# 2. CSS مخصص لإزالة "صندوق السحر" وضبط الواجهة
st.markdown("""
    <style>
    /* حذف الخط العمودي الوهمي */
    [data-testid="stVerticalBlock"] > div > div > div > div { border: none !important; }
    
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
        height: 450px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: inset 0 0 40px rgba(0, 150, 255, 0.1);
        margin-bottom: 10px;
        color: #00ccff;
        font-family: monospace;
        font-size: 24px;
    }

    /* أزرار الأعضاء - خط عريض جداً 900 */
    .stButton>button {
        background: linear-gradient(180deg, #0d1b2a, #050a0f);
        color: #b0d4ff;
        border: 1px solid #1a3a5a;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 8px;
    }

    /* إخفاء تسمية صندوق الإدخال تماماً */
    label[data-testid="stWidgetLabel"] { display: none !important; }
    
    .quran-glow {
        text-align: center;
        filter: drop-shadow(0 0 10px rgba(222, 255, 154, 0.6));
    }
    </style>
    """, unsafe_allow_html=True)

# 3. تهيئة البيانات في Session State
if 'active_member' not in st.session_state: st.session_state.active_member = "[ SYSTEM_READY ]"
if 'api_key' not in st.session_state: st.session_state.api_key = ""
if 'model' not in st.session_state: st.session_state.model = "Gemini"

# 4. الشريط الجانبي (الإعدادات كاملة)
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#00ccff;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    
    # قسم مفتاح الذكاء
    st.markdown("### 🔑 مفتاح API")
    st.session_state.api_key = st.text_input("المفتاح:", value=st.session_state.api_key, type="password")
    
    # قسم الموديل
    st.markdown("### 🔧 اختر الموديل")
    st.session_state.model = st.selectbox("الموديل الحالي:", ["Gemini", "GPT-4 (قريباً)", "Local LLM"])
    
    st.write("---")
    
    # قسم الداتا والكاتالوكات
    st.markdown("### 📂 إدارة البيانات")
    if st.button("🔄 مزامنة ملفات xlsx"):
        st.info("جاري فحص الكاتالوكات والمصطلحات المادية...")
    
    st.write("---")
    st.button("📜 سجل القواعد §")
    st.button("🛠️ أيقونة البروتوكولات")

# 5. المحتوى الرئيسي
st.markdown("<h1 style='text-align:center; color:#00ccff;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)

# الأعضاء العلويين (A1-A5)
h_names = ["A1: المُستقبِل", "A2: المُحلل السياقي", "A3: المُقارن المادي", "A4: المُلاحظ والراصد", "A5: الناقد المنطقي"]
cols = st.columns(5)
for i, col in enumerate(cols):
    if col.button(h_names[i]):
        st.session_state.active_member = f"نشط الآن: {h_names[i]}"

st.write("")

# الوسط: السبورة + الأعضاء الجانبيين
main_col, side_col = st.columns([8.5, 1.5])

with main_col:
    st.markdown(f"<div class='the-board'>{st.session_state.active_member}</div>", unsafe_allow_html=True)
    # صندوق الإدخال بدون أي عنوان فوقه
    query = st.text_input("", placeholder="أدخل المصطلح المادي هنا للبحث في البينة...")

with side_col:
    v_names = ["A6: حارس القواعد §", "A7: المُصنف والمبوب", "A8: الآمر والحاكم", "A9: الصائغ النهائي", "A10: المنسق العام"]
    for name in v_names:
        if st.button(name):
            st.session_state.active_member = f"نشط الآن: {name}"
    
    st.markdown("<div class='quran-glow'><div style='font-size:50px;'>📖</div><b style='color:#deff9a;'>البيان القرآني</b></div>", unsafe_allow_html=True)

if query:
    st.toast(f"جاري التحليل المادي لـ: {query}")
