import streamlit as st

# 1. إعدادات الصفحة (Theme)
st.set_page_config(page_title="مجلس البينة", layout="wide", initial_sidebar_state="collapsed")

# كود CSS لتخصيص المظهر (الصبورة السوداء والألوان التقنية)
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stButton>button { 
        width: 100%; border-radius: 5px; height: 3em; 
        background-color: #1a1a1a; color: #deff9a; border: 1px solid #333;
    }
    .stButton>button:hover { border: 1px solid #deff9a; color: white; }
    .board-container { 
        background-color: #0a0a0a; border: 2px solid #1a1a1a; 
        padding: 20px; border-radius: 15px; min-height: 400px;
    }
    .icon-box { text-align: center; padding: 10px; border: 1px dashed #444; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- الهيكل العلوي (أيقونات الأعضاء/الأدوات) ---
cols = st.columns(10)
for i, col in enumerate(cols):
    with col:
        st.markdown(f"<div class='icon-box'>🛠️<br><small>عضو {i+1}</small></div>", unsafe_allow_html=True)

st.write("---")

# --- منطقة التحكم الرئيسية ---
left_col, right_col = st.columns([1, 4])

with left_col:
    st.subheader("🗂️ الخزانة")
    show_quran = st.button("📖 ملف الآيات")
    show_catalog = st.button("📚 الكتالوجات")
    st.write("---")
    show_board = st.button("📺 تفعيل الصبورة")

with right_col:
    # منطق الظهور: لا يظهر شيء إلا إذا تم الضغط على الزر
    if show_board:
        st.markdown("<div class='board-container'>", unsafe_allow_html=True)
        st.title("📺 الصبورة السوداء الكبرى")
        st.info("الصبورة جاهزة الآن لاستقبال التحليلات... أدخل استفسارك.")
        query = st.text_input("🔍 ابحث في البينة:", placeholder="اكتب الكلمة أو الآية هنا...")
        if query:
            st.success(f"جاري تحليل: {query}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif show_quran:
        st.header("📖 بيانات ملف الآيات")
        st.write("سيتم عرض جداول الإكسيل هنا فور استدعائها...")
        # هنا سيتم ربط ملف data_quran.xlsx لاحقاً
        
    elif show_catalog:
        st.header("📚 كتالوجات المصطلحات")
        st.write("استعراض الكلمات وتكرارها...")
        
    else:
        # الحالة الافتراضية (قبل فتح أي شيء)
        st.markdown("""
            <div style='text-align: center; padding-top: 100px; color: #444;'>
                <h3>المجلس في حالة انتظار</h3>
                <p>اختر عنصراً من الخزانة أو قم بتفعيل الصبورة لبدء العمل</p>
            </div>
            """, unsafe_allow_html=True)
