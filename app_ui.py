import streamlit as st
import time

# 1. إعدادات الهيكل الأساسي
st.set_page_config(page_title="مجلس البينة", layout="wide", initial_sidebar_state="expanded")

# 2. هندسة المظهر (CSS) - حلول بصرية نهائية
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div > div > div > div { border: none !important; }
    .main { background-color: #010307; direction: rtl; }
    
    /* السبورة */
    .the-board {
        background-color: #000000;
        border: 2px solid #102030;
        border-radius: 12px;
        height: 400px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: inset 0 0 40px rgba(0, 150, 255, 0.1);
        color: #00ccff;
        font-family: monospace;
        font-size: 22px;
        margin-bottom: 10px;
        text-align: center;
        padding: 20px;
    }

    /* إخفاء تسمية صندوق الإدخال */
    label[data-testid="stWidgetLabel"] { display: none !important; }

    /* أزرار الأعضاء - خط 900 */
    .stButton>button {
        font-weight: 900 !important;
        border-radius: 8px;
        width: 100%;
        transition: 0.3s;
    }

    /* مؤشر LED */
    .led-green {
        height: 12px; width: 12px;
        background-color: #00ff00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00ff00;
        margin-left: 5px;
    }
    .led-off {
        height: 12px; width: 12px;
        background-color: #333;
        border-radius: 50%;
        display: inline-block;
        margin-left: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. تهيئة الجلسة (Session State) لضمان عدم ضياع البيانات
if 'conn_status' not in st.session_state: st.session_state.conn_status = False
if 'active_member' not in st.session_state: st.session_state.active_member = "[ SYSTEM_READY ]"
if 'prompts' not in st.session_state:
    st.session_state.prompts = {f"A{i}": f"أنت العضو A{i}، بروتوكول العمل الخاص بك هو..." for i in range(1, 11)}

# 4. الشريط الجانبي - الإعدادات الشاملة
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#00ccff;'>⚙️ لوحة التحكم</h2>", unsafe_allow_html=True)
    
    # --- قسم الذكاء الاصطناعي ---
    with st.expander("🤖 إعدادات المحرك", expanded=True):
        provider = st.selectbox("المزود:", ["اختر...", "Gemini", "ChatGPT"])
        if provider == "Gemini":
            model = st.selectbox("الموديل:", ["Gemini 2.0 Flash", "Gemini 1.5 Pro", "Gemini 1.5 Flash", "Gemini 1.0 Ultra"])
        elif provider == "ChatGPT":
            model = st.selectbox("الموديل:", ["GPT-4o", "GPT-4 Turbo", "o1-preview"])
        
        if provider != "اختر...":
            api_key = st.text_input("مفتاح API:", type="password")
            col_led, col_btn = st.columns([1, 5])
            with col_btn:
                if st.button("⚡ اتصال سريع"):
                    with st.spinner('جاري الربط...'):
                        time.sleep(0.6)
                        st.session_state.conn_status = True
            with col_led:
                status_class = "led-green" if st.session_state.conn_status else "led-off"
                st.markdown(f"<div class='{status_class}'></div>", unsafe_allow_html=True)

    # --- قسم أيقونة الأعضاء (تغيير البرومبت) ---
    with st.expander("👥 أيقونة الأعضاء"):
        selected_a = st.selectbox("اختر عضو لتعديل مهامه:", list(st.session_state.prompts.keys()))
        new_prompt = st.text_area(f"برومبت {selected_a}:", value=st.session_state.prompts[selected_a], height=100)
        if st.button(f"حفظ تحديث {selected_a}"):
            st.session_state.prompts[selected_a] = new_prompt
            st.success("تم التحديث")

    # --- قسم أيقونة الداتا ---
    with st.expander("📊 أيقونة الداتا"):
        st.write("ملفات العمل (xlsx):")
        st.file_uploader("رفع كاتالوج جديد", type=["xlsx"])
        if st.button("🔄 مزامنة قاعدة البيانات"):
            st.info("جاري فحص المصطلحات المادية...")

    # --- قسم أيقونة القواعد والبروتوكولات ---
    with st.expander("📜 القواعد والبروتوكولات"):
        st.button("📘 سجل القواعد §")
        st.button("🛠️ أيقونة البروتوكولات")

# 5. الواجهة الرئيسية
st.markdown("<h1 style='text-align:center; color:#00ccff;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)

# الأعضاء العلويون (A1-A5)
h_names = ["A1: المُستقبِل", "A2: المُحلل السياقي", "A3: المُقارن المادي", "A4: المُلاحظ والراصد", "A5: الناقد المنطقي"]
cols = st.columns(5)
for i, col in enumerate(cols):
    if col.button(h_names[i]):
        st.session_state.active_member = f"الكيان النشط: {h_names[i]}\n\nالمهام: {st.session_state.prompts[f'A{i+1}']}"

# الوسط: السبورة والأعضاء الضابطون
main_col, side_col = st.columns([8.5, 1.5])

with main_col:
    st.markdown(f"<div class='the-board'>{st.session_state.active_member}</div>", unsafe_allow_html=True)
    query = st.text_input("", placeholder="أدخل المصطلح المادي هنا...")

with side_col:
    v_names = ["A6: حارس القواعد §", "A7: المُصنف والمبوب", "A8: الآمر والحاكم", "A9: الصائغ النهائي", "A10: المنسق العام"]
    for name in v_names:
        if st.button(name):
            st.session_state.active_member = f"الكيان النشط: {name}\n\nالمهام: {st.session_state.prompts[f'A{v_names.index(name)+6}']}"
    
    st.markdown("<div style='text-align:center; margin-top:20px;'><div style='font-size:45px;'>📖</div><small style='color:#deff9a;'>البيان القرآني</small></div>", unsafe_allow_html=True)
