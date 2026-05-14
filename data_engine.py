import pandas as pd
import streamlit as st
import os
import re

# دالة التنميط المادي (Normalization): لا تلمسها، هي المسؤولة عن إيجاد "كتاب" و "الحمد"
def normalize_arabic(text):
    if not isinstance(text, str): return ""
    text = re.sub(r"[\u064B-\u0652]", "", text) # إزالة التشكيل
    text = re.sub(r"[إأآٱا]", "ا", text) # توحيد الألفات
    text = re.sub(r"[ىي]", "ي", text)
    text = re.sub(r"[ةه]", "ه", text)
    return text.strip()

@st.cache_data
def load_all_data():
    try:
        # المسارات الأصلية كما هي في مشروعك
        df_q = pd.read_excel("data/data_quran.xlsx").ffill()
        df_w = pd.read_excel("data/data_words.xlsx").ffill()
        return df_q, df_w
    except Exception as e:
        st.error(f"خطأ مادي في تحميل الملفات: {e}")
        return None, None

def get_surah_list():
    df, _ = load_all_data()
    return df['السورة'].unique().tolist() if df is not None else []

def get_context_block(surah, verse_num):
    df, _ = load_all_data()
    if df is not None:
        # السياق الموسع (6 قبل و 6 بعد) كما طلبت
        start, end = max(1, verse_num - 6), verse_num + 6
        mask = (df['السورة'] == surah) & (df['رقم الآية'].between(start, end))
        res = df[mask].sort_values('رقم الآية')
        block = ""
        for _, r in res.iterrows():
            tag = "⭐ " if r['رقم الآية'] == verse_num else "⬅️ "
            block += f"{tag} ﴿{r['نص الآية']}﴾ [{r['رقم الآية']}]\n"
        return block
    return "لا توجد بيانات."

def get_word_collection(word):
    _, df = load_all_data()
    if df is not None:
        # تطبيق التنميط على الكلمة المبحوث عنها
        target = normalize_arabic(word)
        
        # البحث المادي المرن في عمود اللفظ
        mask = df['اللفظ'].apply(lambda x: target in normalize_arabic(str(x)))
        res = df[mask]
        
        if not res.empty:
            output = f"📊 جرد اللفظ ({word}) | المواضع: {len(res)}\n" + "="*30 + "\n"
            for _, r in res.iterrows():
                # الحفاظ على أسماء الأعمدة كما هي في ملفك (رقم الآية أو r رقم الآية)
                v_col = 'رقم الآية' if 'رقم الآية' in r else 'r رقم الآية'
                output += f"• [{r['السورة']}:{r.get(v_col, '?')}] ﴿{r['نص الآية الكاملة']}﴾\n\n"
            return output
    return f"اللفظ ({word}) غير موجود في المادة الخام."
