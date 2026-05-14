import streamlit as st

# إعدادات الصفحة لتكون سوداء بالكامل وبدون هوامش كبيرة
st.set_page_config(page_title="مجلس البينة v2.0", layout="wide", initial_sidebar_state="collapsed")

# CSS متطور لمحاكاة التصميم الذي أرسلته (الشبكة والألوان السماوية)
st.markdown("""
    <style>
    .main { background-color: #050a10; }
    /* تصميم الصبورة مع الشبكة */
    .the-board {
        background-color: #000000;
        background-image: linear-gradient(#112233 1px, transparent 1px), linear-gradient(90deg, #112233 1px, transparent 1px);
        background-size: 40px 40px;
        border: 2px solid #224466;
        border-radius: 10px;
        height: 500px;
        padding: 20px;
        position: relative;
    }
    /* الأزرار والأيقونات الصغيرة */
    .stButton>button {
        background-color: rgba(34, 68, 102, 0.2);
        color: #88ccff;
        border: 1px solid #224466;
        font-size: 12px;
        border-radius: 4px;
    }
    .stButton>button:hover { border-color: #00ccff; color: white; }
    /* صندوق السحر */
    .magic-box {
        border-top: 2px solid #224466;
        padding-top: 10px;
        margin-top: 10px;
        color: #88ccff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الصف العلوي: الإعدادات (أصغر ما يمكن) والوكلاء ---
top_left, top_center, top_right = st.columns([1, 8, 2])

with top_left:
    if st.button("⚙️"): # زر الإعدادات الصغير
        st.toast("فتح الإعدادات المصغرة...")

with top_center:
    # عرض الوكلاء كأزرار صغيرة متراصة
    agent_cols = st.columns(10)
    agents = ["Research", "Marketing", "Resources", "Sales", "Legal", "Design", "Operations", "Support", "Finance", "Development"]
    for i, col in enumerate(agent_cols):
        col.button(f"💠 {agents[i]}")

with top_right:
    st.markdown("<span style='color:#88ccff;'>📖 القرآن الكريم</span>", unsafe_allow_html=True)

# --- منطقة الصبورة (The Board) ---
st.markdown("<div class='the-board'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#446688; opacity:0.5;'>The Board (الصبورة)</h2>", unsafe_allow_html=True)
# هنا ستظهر النتائج والرسوم البيانية لاحقاً
st.markdown("</div>", unsafe_allow_html=True)

# --- صندوق السحر (The Magic Box) ---
st.markdown("<div class='magic-box'>", unsafe_allow_html=True)
query = st.text_input("The Magic Box (صندوق السحر)", placeholder="أدخل استفسارك هنا للبحث المادي...")
st.markdown("</div>", unsafe_allow_html=True)

# --- الشريط الجانبي الأيمن (Catalyst / System) ---
with st.sidebar:
    st.markdown("### Catalyst (الكاتالوك)")
    st.write("Connection Status: 🟢")
    st.markdown("---")
    st.markdown("### System (النظام)")
    st.write("Reciters / Mind")
