import pandas as pd
import streamlit as st
import os
import re

# دالة تنميط النص: تجعل "كتاب" و "كتٰب" و "الكتاب" متساوية مادياً في البحث
def normalize_arabic(text):
    if not isinstance(text, str): return ""
    text = text.strip()
    # إزالة التشكيل (الفتحة، الضمة، الكسرة...)
    text = re.sub(r"[\u064B-\u0652]", "", text)
    # توحيد الألفات بجميع أشكالها (أ، إ، آ، ٱ) إلى "ا"
    text = re.sub(r"[إأآٱ]", "ا", text)
    # توحيد الياء والألف المقصورة
    text = re.sub(r"[ىي]", "ي", text)
    # توحيد التاء المربوطة والهاء
    text = re.sub(r"[ةه]", "ه", text)
    return text

@st.cache_data
def load_all_data():
    q_path, w_path = "data/data_quran.xlsx", "data/data_words.xlsx"
    try:
        if not os.path.exists(q_path) or not os.path.exists(w_path):
            st.error("⚠️ ملفات الداتا غير موجودة في مجلد data")
            return None, None
        df_q = pd.read_excel(q_path).ffill()
        df_w = pd.read_excel(w_path).ffill()
        return df_q, df_w
    except Exception as e:
        st.error(f"⚠️ خطأ في القراءة: {e}")
        return None, None

def get_surah_list():
    df, _ = load_all_data()
    return df['السورة'].unique().tolist() if df is not None else []

def get_context_block(surah, verse_num):
    df, _ = load_all_data()
    if df is not None:
        # توسيع السياق لـ 13 آية (6 قبل و 6 بعد)
        start, end = max(1, verse_num - 6), verse_num + 6
        mask = (df['السورة'] == surah) & (df['رقم الآية'].between(start, end))
        res = df[mask].sort_values('رقم الآية')
        if not res.empty:
            block = f"📖 سياق سورة {surah} | النطاق: {start} - {res['رقم الآية'].max()}\n" + "="*50 + "\n"
            for _, r in res.iterrows():
                tag = "⭐ " if r['رقم الآية'] == verse_num else "⬅️ "
                block += f"{tag} ﴿{r['نص الآية']}﴾ [{r['رقم الآية']}]\n\n"
            return block
    return "لا توجد نتائج."

def get_word_collection(word):
    _, df = load_all_data()
    if df is not None:
        target = normalize_arabic(word)
        # البحث في عمود 'اللفظ' بعد تنظيفه من التشكيل والهمزات
        mask = df['اللفظ'].apply(lambda x: target in normalize_arabic(str(x)))
        results = df[mask]
        
        if not results.empty:
            output = f"📊 جرد اللفظ ({word}) | المواضع المكتشفة: {len(results)}\n" + "="*50 + "\n"
            for i, (_, r) in enumerate(results.iterrows(), 1):
                output += f"{i}. [{r['السورة']}:{r['رقم الآية']}] ﴿{r['نص الآية الكاملة']}﴾\n\n"
            return output
    return f"اللفظ ({word}) لم يظهر في الجرد. تأكد من وجوده في ملف data_words.xlsx"
