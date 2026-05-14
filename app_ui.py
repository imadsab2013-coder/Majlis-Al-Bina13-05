"""
═══════════════════════════════════════════════════════════════════════════════
مشروع: مجلس البينة | Majlis Al-Bina
الملف الأول: الواجهة الرئيسية | File: app_ui.py (Main UI) - النسخة 2.0
═══════════════════════════════════════════════════════════════════════════════

التصميم الجديد:
- سبورة مركزية في إطار
- 5 أعضاء على اليسار + 5 على اليمين
- شريط جانبي على اليسار (الإعدادات)
- ألوان داكنة عصرية
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 إعدادات الصفحة
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="مجلس البينة | Majlis Al-Bina",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS مخصص - تصميم داكن عصري
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* الإعدادات الأساسية */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
        margin: 0;
        padding: 0;
    }
    
    /* الخلفية الداكنة */
    .stApp {
        background-color: #0a0e27;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0a0e27 !important;
    }
    
    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #1a2342 !important;
    }
    
    /* النصوص */
    .stMarkdown, label, p {
        color: #e0e6ed !important;
    }
    
    /* الأيقونات - الأعضاء (5 على اليسار) */
    .agent-icon-left {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 65px;
        height: 65px;
        border-radius: 12px;
        background: linear-gradient(135deg, #1e2d4d, #2d3f5f);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        position: relative;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .agent-icon-left:hover {
        transform: translateY(-5px);
        border-color: #4299e1;
        box-shadow: 0 6px 20px rgba(66, 153, 225, 0.3);
    }
    
    .agent-icon-left.active {
        background: linear-gradient(135deg, #4299e1, #3182ce);
        border-color: #2b6cb0;
        box-shadow: 0 6px 25px rgba(66, 153, 225, 0.5);
    }
    
    /* الأيقونات - الأعضاء (5 على اليمين) */
    .agent-icon-right {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 65px;
        height: 65px;
        border-radius: 12px;
        background: linear-gradient(135deg, #1e2d4d, #2d3f5f);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        position: relative;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .agent-icon-right:hover {
        transform: translateY(-5px);
        border-color: #38a169;
        box-shadow: 0 6px 20px rgba(56, 161, 105, 0.3);
    }
    
    .agent-icon-right.active {
        background: linear-gradient(135deg, #38a169, #22863a);
        border-color: #1e5631;
        box-shadow: 0 6px 25px rgba(56, 161, 105, 0.5);
    }
    
    /* مؤشر الحالة */
    .status-indicator {
        position: absolute;
        top: 2px;
        right: 2px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    .status-indicator.online {
        background-color: #48bb78;
        box-shadow: 0 0 10px rgba(72, 187, 120, 0.8);
    }
    
    .status-indicator.offline {
        background-color: #f56565;
        box-shadow: 0 0 10px rgba(245, 101, 101, 0.8);
    }
    
    .status-indicator.waiting {
        background-color: #ecc94b;
        animation: blink 0.8s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* نص الأيقونة */
    .agent-label {
        font-size: 10px;
        font-weight: bold;
        color: #e0e6ed;
        text-align: center;
        margin-top: 4px;
        width: 100%;
    }
    
    /* السبورة */
    .board-frame {
        background: linear-gradient(135deg, #0f1829, #1a2f4d);
        border: 2px solid #4299e1;
        border-radius: 12px;
        padding: 20px;
        min-height: 500px;
        box-shadow: 0 8px 32px rgba(66, 153, 225, 0.15);
    }
    
    /* بلوك الرسالة */
    .message-block {
        background: linear-gradient(135deg, #1a2f4d, #243353);
        border-right: 4px solid #4299e1;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .message-block:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        transform: translateX(-2px);
    }
    
    .message-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    .message-id {
        background: #4299e1;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 11px;
    }
    
    .message-name {
        font-weight: bold;
        color: #4299e1;
        font-size: 14px;
    }
    
    .message-content {
        color: #cbd5e0;
        font-size: 13px;
        line-height: 1.6;
        padding-right: 40px;
    }
    
    .message-time {
        color: #718096;
        font-size: 11px;
        margin-top: 6px;
    }
    
    /* صندوق الإدخال */
    .input-container {
        background: linear-gradient(135deg, #1a2f4d, #243353);
        border: 2px solid #4299e1;
        border-radius: 8px;
        padding: 16px;
        margin-top: 16px;
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #4299e1, #3182ce) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3182ce, #2c5aa0) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3) !important;
    }
    
    /* عنصر الإدخال النصي */
    .stTextInput > div > input,
    .stTextArea > div > textarea {
        background-color: #0f1829 !important;
        color: #e0e6ed !important;
        border: 1px solid #4299e1 !important;
        border-radius: 6px !important;
    }
    
    .stTextInput > div > input::placeholder,
    .stTextArea > div > textarea::placeholder {
        color: #718096 !important;
    }
    
    /* الـ Expander */
    .streamlit-expanderHeader {
        background-color: #1a2342 !important;
        color: #4299e1 !important;
    }
    
    /* عنوان الصفحة */
    .page-title {
        text-align: center;
        background: linear-gradient(135deg, #4299e1, #38a169);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .page-subtitle {
        text-align: center;
        color: #718096;
        font-size: 13px;
        margin-bottom: 20px;
    }
    
    /* أيقونة الحالة */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
    }
    
    .status-badge.online {
        background-color: rgba(72, 187, 120, 0.2);
        color: #48bb78;
        border: 1px solid #48bb78;
    }
    
    .status-badge.offline {
        background-color: rgba(245, 101, 101, 0.2);
        color: #f56565;
        border: 1px solid #f56565;
    }
    
    /* الجدول */
    .rules-table {
        width: 100%;
        border-collapse: collapse;
        background-color: transparent !important;
    }
    
    .rules-table th {
        background: #1a2342;
        color: #4299e1;
        padding: 8px;
        text-align: right;
        border-bottom: 2px solid #4299e1;
        font-weight: bold;
    }
    
    .rules-table td {
        padding: 8px;
        color: #cbd5e0;
        border-bottom: 1px solid #243353;
    }
    
    .rules-table tr:hover {
        background: #1a2f4d;
    }
    
    /* الرسائل */
    .stSuccess {
        background-color: rgba(72, 187, 120, 0.15) !important;
        color: #48bb78 !important;
    }
    
    .stError {
        background-color: rgba(245, 101, 101, 0.15) !important;
        color: #f56565 !important;
    }
    
    .stWarning {
        background-color: rgba(237, 137, 54, 0.15) !important;
        color: #ed8936 !important;
    }
    
    .stInfo {
        background-color: rgba(66, 153, 225, 0.15) !important;
        color: #4299e1 !important;
    }
    
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 تهيئة Session State
# ═══════════════════════════════════════════════════════════════════════════════

def initialize_session():
    """تهيئة جميع متغيرات الجلسة"""
    
    defaults = {
        'api_key': "",
        'model_choice': "Gemini",
        'temperature': 0.7,
        'rules': [],
        'conversation_history': [],
        'active_agent': None,
        'connection_status': {
            'api': False,
            'data_quran': False,
            'data_words': False
        },
        'board_output': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session()

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 تعريف الأعضاء
# ═══════════════════════════════════════════════════════════════════════════════

AGENTS_LEFT = {
    '1A': {'name': 'المستقبل', 'emoji': '📥', 'role': 'Receiver'},
    '2A': {'name': 'المحلل', 'emoji': '🔍', 'role': 'Analyzer'},
    '3A': {'name': 'المقارن', 'emoji': '⚖️', 'role': 'Comparator'},
    '4A': {'name': 'الراصد', 'emoji': '👁️', 'role': 'Observer'},
    '5A': {'name': 'الناقد', 'emoji': '❌', 'role': 'Critic'},
}

AGENTS_RIGHT = {
    '6A': {'name': 'حارس القواعس', 'emoji': '⚔️', 'role': 'Rule Guardian'},
    '7A': {'name': 'المصنف', 'emoji': '📚', 'role': 'Classifier'},
    '8A': {'name': 'الآمر', 'emoji': '👑', 'role': 'Commander'},
    '9A': {'name': 'الصيغ', 'emoji': '✍️', 'role': 'Formatter'},
    '10A': {'name': 'المحرك', 'emoji': '⚙️', 'role': 'Orchestrator'},
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 دوال الفحص
# ═══════════════════════════════════════════════════════════════════════════════

def check_data_files():
    """فحص وجود ملفات البيانات"""
    data_path = Path("data")
    return {
        'data_quran': (data_path / "data_quran.xlsx").exists(),
        'data_words': (data_path / "data_words.xlsx").exists()
    }

def test_api_connection(api_key):
    """اختبار اتصال API"""
    if not api_key or len(api_key) < 10:
        return False
    return True

def update_connection_status():
    """تحديث حالة الاتصال"""
    data_files = check_data_files()
    st.session_state.connection_status['data_quran'] = data_files['data_quran']
    st.session_state.connection_status['data_words'] = data_files['data_words']
    
    if st.session_state.api_key:
        st.session_state.connection_status['api'] = test_api_connection(st.session_state.api_key)

# ═══════════════════════════════════════════════════════════════════════════════
# 📌 الشريط الجانبي (Sidebar)
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    
    # قسم API Key
    with st.expander("🔑 مفتاح الذكاء الاصطناعي", expanded=True):
        st.session_state.api_key = st.text_input(
            "أدخل مفتاح API:",
            value=st.session_state.api_key,
            type="password",
            label_visibility="collapsed",
            placeholder="أدخل مفتاح Gemini API هنا"
        )
        
        st.session_state.model_choice = st.radio(
            "اختر الموديل:",
            ["Gemini", "GPT (قريباً)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.session_state.temperature = st.slider(
            "درجة الحرارة:",
            0.0, 1.0, 0.7, 0.1,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔗 اختبار", use_container_width=True):
                update_connection_status()
                if st.session_state.connection_status['api']:
                    st.success("✅ متصل!")
                else:
                    st.error("❌ فشل الاتصال")
        
        with col2:
            if st.button("🔄 تحديث", use_container_width=True):
                update_connection_status()
                st.rerun()
    
    # حالة الاتصال
    with st.expander("🟢 حالة الاتصال", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**API:**")
            status_text = "🟢 متصل" if st.session_state.connection_status['api'] else "🔴 غير متصل"
            st.markdown(status_text)
        
        with col2:
            st.markdown("**البيانات:**")
            data_status = "🟢 محملة" if (st.session_state.connection_status['data_quran'] and st.session_state.connection_status['data_words']) else "🔴 ناقصة"
            st.markdown(data_status)
    
    # إدارة القواعس §
    with st.expander("📋 القواعس §", expanded=False):
        st.markdown("#### إضافة قاعدة جديدة")
        
        new_rule_name = st.text_input(
            "اسم القاعدة:",
            label_visibility="collapsed",
            placeholder="مثال: قاعدة تعريف الأسماء"
        )
        
        new_rule_desc = st.text_area(
            "شرح القاعدة:",
            height=60,
            label_visibility="collapsed",
            placeholder="أدخل شرح القاعدة..."
        )
        
        if st.button("➕ إضافة القاعدة", use_container_width=True):
            if new_rule_name:
                st.session_state.rules.append({
                    'id': len(st.session_state.rules) + 1,
                    'name': new_rule_name,
                    'description': new_rule_desc,
                    'enabled': True,
                    'created_at': datetime.now().isoformat()
                })
                st.success(f"✅ تمت إضافة القاعدة: {new_rule_name}")
                st.rerun()
            else:
                st.error("❌ يجب إدخال اسم للقاعدة")
        
        # عرض القواعس
        if st.session_state.rules:
            st.markdown("#### القواعس المفعلة")
            for idx, rule in enumerate(st.session_state.rules):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**§ {rule['name']}**")
                    st.caption(rule['description'][:100] + "...")
                with col2:
                    if st.button("🗑️", key=f"del_{idx}", help="حذف"):
                        st.session_state.rules.pop(idx)
                        st.rerun()
        else:
            st.info("لا توجد قواعس حالياً")

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 المحتوى الرئيسي
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="page-title">📖 مجلس البينة</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Majlis Al-Bina | نظام تحليل النص القرآني الذكي</div>', unsafe_allow_html=True)

st.divider()

# التخطيط الرئيسي
left_col, center_col, right_col = st.columns([1, 1.5, 1])

# ─────────────────────────────────────────────────────────────────────────────
# العمود الأيسر - 5 أعضاء
# ─────────────────────────────────────────────────────────────────────────────

with left_col:
    st.markdown("### 👥 الفريق")
    
    for agent_id in ['1A', '2A', '3A', '4A', '5A']:
        agent = AGENTS_LEFT[agent_id]
        
        # أيقونة العضو
        is_active = st.session_state.active_agent == agent_id
        
        st.markdown(f"""
        <div class="agent-icon-left {'active' if is_active else ''}">
            <div style="font-size: 28px;">{agent['emoji']}</div>
            <div class="agent-label">{agent_id}</div>
            <div class="status-indicator {'online' if st.session_state.connection_status['api'] else 'offline'}"></div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(agent['name'], key=f"agent_{agent_id}", use_container_width=True):
            st.session_state.active_agent = agent_id
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# العمود الأوسط - السبورة
# ─────────────────────────────────────────────────────────────────────────────

with center_col:
    st.markdown("### 📊 السبورة (The Board)")
    
    with st.container(border=True):
        # عرض الرسائل
        if st.session_state.board_output:
            for msg in st.session_state.board_output:
                agent_id = msg.get('agent_id', 'System')
                agent_name = "المستخدم" if agent_id == 'USER' else agent_id
                
                st.markdown(f"""
                <div class="message-block">
                    <div class="message-header">
                        <div class="message-id">{agent_id}</div>
                        <div class="message-name">{agent_name}</div>
                    </div>
                    <div class="message-content">{msg.get('content', '')}</div>
                    <div class="message-time">{msg.get('timestamp', '')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🌫️ السبورة فارغة. ابدأ بإدخال استفسار!")
        
        # صندوق الإدخال
        st.divider()
        
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_area(
                "أدخل استفسارك:",
                height=80,
                label_visibility="collapsed",
                placeholder="ابحث عن كلمة أو اسأل عن سياق..."
            )
        
        with col2:
            submit_btn = st.button("📤 إرسال", use_container_width=True, type="primary")
        
        if submit_btn and user_input:
            st.session_state.board_output.append({
                'agent_id': 'USER',
                'content': user_input,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            st.session_state.conversation_history.append({
                'role': 'user',
                'content': user_input
            })
            st.rerun()
    
    # أزرار التحكم
    st.divider()
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("🗑️ مسح", use_container_width=True):
            if st.checkbox("تأكيد المسح", key="confirm_clear_v2"):
                st.session_state.board_output = []
                st.session_state.conversation_history = []
                st.success("✅ تم المسح")
                st.rerun()
    
    with btn_col2:
        if st.button("💾 حفظ", use_container_width=True):
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'rules': st.session_state.rules,
                'conversation': st.session_state.conversation_history,
                'board': st.session_state.board_output
            }
            with open('session_backup.json', 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            st.success("✅ تم الحفظ")
    
    with btn_col3:
        if st.button("🔄 تحديث", use_container_width=True):
            update_connection_status()
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# العمود الأيمن - 5 أعضاء
# ─────────────────────────────────────────────────────────────────────────────

with right_col:
    st.markdown("### 👥 الفريق")
    
    for agent_id in ['6A', '7A', '8A', '9A', '10A']:
        agent = AGENTS_RIGHT[agent_id]
        
        # أيقونة العضو
        is_active = st.session_state.active_agent == agent_id
        
        st.markdown(f"""
        <div class="agent-icon-right {'active' if is_active else ''}">
            <div style="font-size: 28px;">{agent['emoji']}</div>
            <div class="agent-label">{agent_id}</div>
            <div class="status-indicator {'online' if st.session_state.connection_status['api'] else 'offline'}"></div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(agent['name'], key=f"agent_{agent_id}", use_container_width=True):
            st.session_state.active_agent = agent_id
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# التنبيهات والرسائل
# ─────────────────────────────────────────────────────────────────────────────

st.divider()

update_connection_status()

if not (st.session_state.connection_status['data_quran'] and st.session_state.connection_status['data_words']):
    st.warning("""
    ⚠️ **ملفات البيانات ناقصة:**
    
    ضع الملفات التالية في مجلد `data/`:
    - `data_quran.xlsx`
    - `data_words.xlsx`
    """)

if not st.session_state.connection_status['api']:
    st.info(
        "ℹ️ **الواجهة تعمل بدون API:** يمكنك استخدام الواجهة بالكامل حتى بدون مفتاح API."
    )

# ─────────────────────────────────────────────────────────────────────────────
# التذييل
# ─────────────────────────────────────────────────────────────────────────────

st.divider()

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.caption("📖 مجلس البينة v2.0")

with col_f2:
    st.caption(f"📊 {len(st.session_state.board_output)} رسالة")

with col_f3:
    st.caption("🔒 بيانات محفوظة محلياً")
