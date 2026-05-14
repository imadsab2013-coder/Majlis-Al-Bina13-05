import streamlit as st
import time

# 1. إعدادات الهيكل الأساسي
st.set_page_config(page_title="مجلس البينة", layout="wide", initial_sidebar_state="expanded")

# 2. هندسة المظهر (CSS) - إخفاء العناوين وضبط الإضاءة
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div > div > div > div { border: none !important; }
    .main { background-color: #010307; direction: rtl; }
    
    /* السبورة */
    .the-board {
        background-color: #000000;
        border: 2px solid #102030;
        border-radius: 12px;
        height: 420px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: inset 0 0 40px rgba(0, 150, 255, 0.1);
        color: #00ccff;
        font-family: monospace;
        font-size: 24px;
        margin-bottom: 15px;
    }

    /* إخفاء تسمية صندوق الإدخال (صندوق السحر) */
    label[data-testid="stWidgetLabel"] { display: none !important; }

    /* أزرار الأعضاء - خط 900 */
    .stButton>button {
        font-weight: 900 !important;
        border-radius: 8px;
        width: 100%;
    }

    /* مؤشر LED */
    .led-green {
        height: 15px; width: 15px;
        background-color: #00ff00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00ff00;
        margin-right: 10px;
    }
    .led-off {
        height: 15px; width: 15px;
        background-color: #333;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'conn_status' not in st.session_state: st.session_state.conn_status = False
if 'active_member' not in st.session_state: st.session_state.active_member = "[ SYSTEM_READY ]"

# 4. الشريط الجانبي - منطق الإعدادات التسلسلي
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#00ccff;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    
    # المرحلة 1: نوع الذكاء
    provider = st.selectbox("نوع الذكاء الاصطناعي:", ["اختر المزود...", "Gemini", "ChatGPT"])
    
    if provider != "اختر المزود...":
        # المرحلة 2: الموديلات بناءً على النوع
        if provider == "Gemini":
            model = st.selectbox("اختر موديل Gemini:", ["Gemini 1.5 Pro", "Gemini 1.5 Flash", "Gemini 1.0 Ultra"])
        else:
            model = st.selectbox("اختر موديل GPT:", ["GPT-4o", "GPT-4 Turbo", "GPT-3.5"])
        
        # المرحلة 3: مفتاح API
        api_key = st.text_input("أدخل مفتاح API الخاص بك:", type="password")
        
        if api_key:
            # المرحلة 4: زر الاتصال والمؤشر
            col_led, col_btn = st.columns([1, 4])
            with col_btn:
                if st.button("⚡ اختبار الاتصال السريع"):
                    with st.spinner('جاري المصافحة...'):
                        time.sleep(0.8) # محاكاة سرعة الاتصال
                        st.session_state.conn_status = True
            
            with col_led:
                if st.session_state.conn_status:
                    st.markdown("<div class='led-green'></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='led-off'></div>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 📂 البيانات")
    st.button("🔄 مزامنة الكاتالوكات")

# 5. الواجهة الرئيسية
st.markdown("<h1 style='text-align:center; color:#00ccff;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)

# الأعضاء العلويون (A1-A5)
h_names = ["A1: المُستقبِل", "A2: المُحلل السياقي", "A3: المُقارن المادي", "A4: المُلاحظ والراصد", "A5: الناقد المنطقي"]
cols = st.columns(5)
for i, col in enumerate(cols):
    if col.button(h_names[i]):
        st.session_state.active_member = f"الكيان النشط: {h_names[i]}"

# الوسط: السبورة والأعضاء الضابطون
main_col, side_col = st.columns([8.5, 1.5])

with main_col:
    st.markdown(f"<div class='the-board'>{st.session_state.active_member}</div>", unsafe_allow_html=True)
    query = st.text_input("", placeholder="أدخل المصطلح المادي هنا للبحث في البينة المادية...")

with side_col:
    v_names = ["A6: حارس القواعد §", "A7: المُصنف والمبوب", "A8: الآمر والحاكم", "A9: الصائغ النهائي", "A10: المنسق العام"]
    for name in v_names:
        if st.button(name):
            st.session_state.active_member = f"الكيان النشط: {name}"
    
    st.markdown("<div style='text-align:center; margin-top:20px;'><div style='font-size:45px;'>📖</div><small style='color:#deff9a;'>البيان القرآني</small></div>", unsafe_allow_html=True)
