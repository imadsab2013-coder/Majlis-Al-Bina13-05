import pandas as pd
import streamlit as st
import os
import re

# دالة التنميط: كتحيد التشكيل والهمزات باش البحث يولي دقيق ومادي
def normalize_arabic(text):
    if not isinstance(text, str): return ""
    text = re.sub(r"[إأآٱا]", "ا", text)
    text = re.sub(r"[ىي]", "ي", text)
    text = re.sub(r"[ةه]", "ه", text)
    text = re.sub(r"[\u064B-\u0652]", "", text) # إزالة التشكيل
    return text.strip()

@st.cache_data
def load_all_data():
    try:
        # تأكد من المسارات الصحيحة للملفات
        df_q = pd.read_excel("data/data_quran.xlsx").ffill()
        df_w = pd.read_excel("data/data_words.xlsx").ffill()
        return df_q, df_w
    except:
        return None, None

def get_surah_list():
    df, _ = load_all_data()
    return df['السورة'].unique().tolist() if df is not None else []

def get_context_block(surah, verse_num):
    df, _ = load_all_data()
    if df is not None:
        # السياق المادي الموسع (6 قبل و 6 بعد)
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
        target = normalize_arabic(word)
        # جرد مادي مرن (يجد كتاب، الكتاب، الحمد... إلخ)
        mask = df['اللفظ'].apply(lambda x: target in normalize_arabic(str(x)))
        res = df[mask]
        if not res.empty:
            output = f"📊 نتائج الجرد المادي لـ ({word}): {len(res)} موضع\n"
            output += "="*30 + "\n"
            for _, r in res.iterrows():
                # التعامل مع اختلاف أسماء الأعمدة في ملف الألفاظ
                v_col = 'رقم الآية' if 'رقم الآية' in r else 'r رقم الآية'
                output += f"• [{r['السورة']}:{r[v_col]}] ﴿{r['نص الآية الكاملة']}﴾\n"
            return output
    return f"اللفظ ({word}) غير موجود في ملف الجرد."
