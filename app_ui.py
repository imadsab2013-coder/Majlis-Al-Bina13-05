import streamlit as st

# ═══════════════════════════════════════════════════════════════
# إعدادات الهيكل الأساسي
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="مجلس البينة",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════
# CSS والتنسيق
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    * { direction: rtl; }
    
    .main {
        background-color: #010307;
    }
    
    /* السبورة الشبكية */
    .the-board {
        background-color: #000000;
        background-image: 
            linear-gradient(rgba(0, 204, 255, 0.08) 1.5px, transparent 1.5px), 
            linear-gradient(90deg, rgba(0, 204, 255, 0.08) 1.5px, transparent 1.5px);
        background-size: 45px 45px;
        border: 2px solid #102030;
        border-radius: 12px;
        height: 520px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: inset 0 0 40px rgba(0, 150, 255, 0.1);
        margin-bottom: 15px;
    }
    
    /* أزرار الأعضاء */
    .stButton > button {
        background: linear-gradient(180deg, #0d1b2a, #050a0f);
        color: #b0d4ff;
        border: 1px solid #1a3a5a;
        font-size: 14px !important;
        font-weight: 800;
        padding: 12px 8px;
        width: 100%;
        border-radius: 8px;
        transition: 0.3s all ease-in-out;
    }
    
    .stButton > button:hover {
        border-color: #00ccff;
        color: #ffffff;
        box-shadow: 0 0 25px rgba(0, 204, 255, 0.6);
    }
    
    .stButton > button:active {
        transform: scale(1.02);
    }
    
    /* النصوص */
    .header-text {
        color: #00ccff;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .section-label {
        color: #224466;
        font-size: 12px;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* أيقونة القرآن */
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
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0f1a;
    }
    
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# تهيئة Session State
# ═══════════════════════════════════════════════════════════════

if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False

if 'show_agents' not in st.session_state:
    st.session_state.show_agents = False

if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = None

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

if 'model' not in st.session_state:
    st.session_state.model = "Gemini"

if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7

# ═══════════════════════════════════════════════════════════════
# قاموس الأعضاء
# ═══════════════════════════════════════════════════════════════

AGENTS = {
    'A1': {'name': 'المستقبل', 'prompt': 'أنت المستقبل - تجمع البيانات والمعطيات الأولية...'},
    'A2': {'name': 'المحلل', 'prompt': 'أنت المحلل - تحلل السياق والعلاقات...'},
    'A3': {'name': 'المقارن', 'prompt': 'أنت المقارن - تقارن بين الآيات والنصوص...'},
    'A4': {'name': 'الملاحظ', 'prompt': 'أنت الملاحظ - تلاحظ التفاصيل الدقيقة...'},
    'A5': {'name': 'الناقد', 'prompt': 'أنت الناقد - تنقد المنطق والاستنتاجات...'},
    'A6': {'name': 'المقعد', 'prompt': 'أنت المقعد - تحافظ على القواعس والمعايير...'},
    'A7': {'name': 'المراقب', 'prompt': 'أنت المراقب - تصنف وتنظم النتائج...'},
    'A8': {'name': 'الحاكم', 'prompt': 'أنت الحاكم - تصدر الأوامر والتوجيهات...'},
    'A9': {'name': 'المسجل', 'prompt': 'أنت المسجل - تسجل وتصيغ النتائج النهائية...'},
    'A10': {'name': 'الاستراتيجي', 'prompt': 'أنت الاستراتيجي - تنسق بين الجميع...'},
}

# ═══════════════════════════════════════════════════════════════
# الشريط الجانبي
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("<div style='text-align:center; color:#00ccff; font-size:18px; font-weight:bold;'>مجلس البينة</div>", unsafe_allow_html=True)
    st.write("---")
    
    # زر الإعدادات
    if st.button("⚙️ الإعدادات", use_container_width=True):
        st.session_state.show_settings = not st.session_state.show_settings
    
    # عرض الإعدادات
    if st.session_state.show_settings:
        st.write("---")
        st.markdown("### 🔑 مفتاح API")
        st.session_state.api_key = st.text_input(
            "أدخل المفتاح:",
            value=st.session_state.api_key,
            type="password",
            label_visibility="collapsed"
        )
        
        st.markdown("### 🔧 اختر الموديل")
        st.session_state.model = st.radio(
            "الموديل:",
            ["Gemini", "GPT (قريباً)"],
            label_visibility="collapsed"
        )
        
        st.markdown("### 🔥 درجة الحرارة")
        st.session_state.temperature = st.slider(
            "Temperature:",
            0.0, 1.0, 0.7, 0.1,
            label_visibility="collapsed"
        )
        
        if st.button("🔗 اختبار الاتصال", use_container_width=True):
            if st.session_state.api_key:
                st.success("✅ متصل!")
            else:
                st.error("❌ أدخل المفتاح أولاً")
        
        st.write("---")
        st.markdown("### 📂 الكاتالوكات")
        st.info("فهارس المصطلحات المادية وسجل القواعس")
        
        st.markdown("### 📊 إدارة البيانات")
        if st.button("مزامنة ملفات xlsx", use_container_width=True):
            st.info("جاري المزامنة...")
    
    st.write("---")
    
    # زر الأعضاء
    if st.button("👥 الأعضاء", use_container_width=True):
        st.session_state.show_agents = not st.session_state.show_agents
    
    # عرض الأعضاء
    if st.session_state.show_agents:
        st.write("---")
        st.markdown("### اختر عضو:")
        
        for agent_id, agent_info in AGENTS.items():
            if st.button(f"{agent_id}: {agent_info['name']}", use_container_width=True, key=f"agent_{agent_id}"):
                st.session_state.selected_agent = agent_id
        
        if st.session_state.selected_agent:
            st.write("---")
            st.markdown(f"### {st.session_state.selected_agent}: {AGENTS[st.session_state.selected_agent]['name']}")
            st.markdown("#### System Prompt:")
            st.code(AGENTS[st.session_state.selected_agent]['prompt'], language="text")
    
    st.write("---")
    st.markdown("""
    <div class='quran-container'>
        <div class='quran-symbol'>📖</div>
        <div style='color:#deff9a; font-size:14px; font-weight:bold;'>البيان القرآني</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# المحتوى الرئيسي
# ═══════════════════════════════════════════════════════════════

# العنوان
st.markdown("<div class='header-text'>📖 مجلس البينة</div>", unsafe_allow_html=True)

# الأعضاء العلويون (A1-A5)
st.markdown("<div class='section-label'>وحدات التحليل الأفقي (A1-A5)</div>", unsafe_allow_html=True)

cols_top = st.columns(5)
top_agents = ['A1', 'A2', 'A3', 'A4', 'A5']

for idx, col in enumerate(cols_top):
    with col:
        agent_id = top_agents[idx]
        agent_name = AGENTS[agent_id]['name']
        st.button(f"{agent_id}: {agent_name}", key=f"top_{agent_id}")

# المنطقة الوسطى
st.write("")

# السبورة والأعضاء اليمينيون
main_col, right_col = st.columns([8, 2])

with main_col:
    # السبورة
    st.markdown("<div class='the-board'>", unsafe_allow_html=True)
    st.markdown("<div style='color:#0a1a2a; font-family:monospace; font-size:35px;'>[ SYSTEM_READY ]</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # صندوق الإدخال
    query = st.text_input(
        "",
        placeholder="صندوق السحر: أدخل الكلمة للبدء في استخراج البينة المادية..."
    )

with right_col:
    # الأعضاء اليمينيون (A6-A10)
    st.markdown("<div class='section-label'>وحدات الضبط والتدقيق</div>", unsafe_allow_html=True)
    
    right_agents = ['A6', 'A7', 'A8', 'A9', 'A10']
    
    for agent_id in right_agents:
        agent_name = AGENTS[agent_id]['name']
        st.button(f"{agent_id}: {agent_name}", key=f"right_{agent_id}", use_container_width=True)
    
    # أيقونة القرآن
    st.markdown("""
    <div class='quran-container'>
        <div class='quran-symbol'>📖</div>
        <div style='color:#deff9a; font-size:12px; font-weight:bold;'>البيان<br>القرآني</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# التفاعل
# ═══════════════════════════════════════════════════════════════

if query:
    st.toast(f"🔍 يتم البحث عن: {query}")
