import streamlit as st
import time

# ==========================================
# 1. إعدادات الهيكل والتصميم (CSS)
# ==========================================
st.set_page_config(page_title="مجلس البينة", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #010307; direction: rtl; }
    /* تصميم نهر المحادثة */
    .chat-river {
        background-color: #000000; border: 1px solid #102030;
        border-radius: 15px; height: 550px; overflow-y: auto;
        padding: 25px; margin-bottom: 20px;
    }
    .data-block {
        background: #001a33; border-right: 5px solid #00ccff;
        padding: 15px; margin: 15px 0; border-radius: 8px; color: #ffffff; font-size: 20px;
    }
    .agent-block {
        background-color: #0d0d0d; border: 1px solid #1a1a1a;
        padding: 15px; margin: 10px 50px 10px 10px; border-radius: 12px;
        color: #00ccff; font-family: 'Courier New', monospace;
    }
    .agent-sig { font-weight: bold; color: #ff3366; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. إدارة الجلسة والمنطق (Session State)
# ==========================================
if 'river_content' not in st.session_state: st.session_state.river_content = []
if 'active_agents' not in st.session_state: st.session_state.active_agents = []
if 'conn_ready' not in st.session_state: st.session_state.conn_ready = False

# ==========================================
# 3. محرك البحث (البيان القرآني) - "مخزن للنسخ"
# ==========================================
with st.sidebar:
    st.title("⚙️ لوحة التحكم")
    with st.expander("📖 أيقونة البيان القرآني", expanded=False):
        mode = st.radio("نوع البحث:", ["بالآية", "باللفظ"])
        if mode == "بالآية":
            st.selectbox("السورة:", ["البقرة", "آل عمران", "..."])
            st.number_input("الآية:", min_value=1)
        else:
            st.text_input("اللفظ المادي:")
        st.info("انسخ النتيجة يدويًا وضعها في السبورة أدناه.")

    with st.expander("🤖 إعدادات المحرك والـ API"):
        st.text_input("Gemini API Key:", type="password")
        if st.button("تفعيل الاتصال"): st.session_state.conn_ready = True

# ==========================================
# 4. الواجهة الرئيسية (نهر المحادثة)
# ==========================================
st.markdown("<h1 style='text-align:center; color:#00ccff;'>📖 مجلس البينة</h1>", unsafe_allow_html=True)

# شريط الأعضاء (الضغط للاستدعاء للسبورة)
st.write("### 👥 استدعاء الأعضاء للنقاش")
cols = st.columns(10)
for i in range(1, 11):
    if cols[i-1].button(f"A{i}"):
        if f"A{i}" not in st.session_state.active_agents:
            st.session_state.active_agents.append(f"A{i}")
            st.session_state.river_content.append({"type": "sys", "msg": f"تم دخول العضو A{i} إلى قاعة النقاش."})

# عرض السبورة (النهر)
st.markdown('<div class="chat-river">', unsafe_allow_html=True)
for item in st.session_state.river_content:
    if item['type'] == "data":
        st.markdown(f"<div class='data-block'><b>المادة الخام:</b><br>{item['msg']}</div>", unsafe_allow_html=True)
    elif item['type'] == "agent":
        st.markdown(f"<div class='agent-block'><div class='agent-sig'>👤 العضو {item['sender']}</div>{item['msg']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color:gray; font-size:12px; text-align:center;'>{item['msg']}</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# منطقة الإدخال والتفاعل
input_col, action_col = st.columns([8, 2])
with input_col:
    user_text = st.text_area("", placeholder="لصق الآية هنا أو كتابة أمر...", height=100)
with action_col:
    if st.button("🚀 إرسال للسبورة"):
        st.session_state.river_content.append({"type": "data", "msg": user_text})
        st.rerun()
    
    # أزرار تفعيل الأعضاء الحاضرين
    st.write("---")
    for agent in st.session_state.active_agents:
        if st.button(f"تفعيل {agent} ⚡"):
            # المنطق المادي: العضو يقرأ آخر مادة في النهر ويحللها
            analysis = f"تحليل مادي من العضو {agent} بناءً على البروتوكول الخاص به..."
            st.session_state.river_content.append({"type": "agent", "sender": agent, "msg": analysis})
            st.rerun()

# ==========================================
# 5. رسالة للمبرمج (The Programmer's Map)
# ==========================================
# ملاحظة للمبرمج: 
# 1. ملف data_engine.py يجب أن يغذي قائمة السور والبحث في الشريط الجانبي.
# 2. ملف agent_matrix.py يجب أن يحتوي على برومبتات الأعضاء ويربطها بـ Gemini API.
# 3. التفاعل يتم عبر st.session_state.river_content لضمان تدفق "النهر".
