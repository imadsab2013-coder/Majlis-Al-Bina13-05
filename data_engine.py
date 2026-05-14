import pandas as pd
import streamlit as st
import os

# 1. تحميل البيانات مع التخزين المؤقت لضمان السرعة المادية
@st.cache_data
def load_all_data():
    # تحديد مسارات الملفات (تأكد من وجود مجلد data)
    quran_path = "data/data_quran.xlsx"
    words_path = "data/data_words.xlsx"
    
    try:
        if not os.path.exists(quran_path) or not os.path.exists(words_path):
            st.error("⚠️ خطأ مادي: ملفات الإكسيل غير موجودة في مجلد data")
            return None, None
            
        # تحميل الملفات
        df_quran = pd.read_excel(quran_path) 
        df_words = pd.read_excel(words_path)
        
        # تنظيف البيانات (معالجة الخلايا المدمجة ffill)
        # ضروري جداً لكي يقرأ الكود اسم السورة في كل الأسطر
        df_quran = df_quran.ffill()
        df_words = df_words.ffill()
        
        return df_quran, df_words
    except Exception as e:
        st.error(f"⚠️ فشل تحميل البيانات: {e}")
        return None, None

# 2. وظيفة جلب قائمة السور (لتغذية القائمة المنسدلة في الواجهة)
def get_surah_list():
    df_quran, _ = load_all_data()
    if df_quran is not None:
        # ترتيب فريد للسور حسب ظهورها المادي في المصحف
        return df_quran['السورة'].unique().tolist()
    return []

# 3. محرك بحث السياق (الآية السابقة + المختارة + اللاحقة)
def get_context_block(surah, verse_num):
    df_quran, _ = load_all_data()
    if df_quran is not None:
        # جلب الآيات الثلاث (نظام الكتلة السياقية)
        mask = (df_quran['السورة'] == surah) & \
               (df_quran['رقم الآية'].isin([verse_num - 1, verse_num, verse_num + 1]))
        results = df_quran[mask].sort_values(by='رقم الآية')
        
        if not results.empty:
            block = ""
            for _, row in results.iterrows():
                # تمييز الآية المطلوبة بـ نجمة لسهولة التعرف عليها
                tag = "⭐ " if row['رقم الآية'] == verse_num else "⬅️ "
                block += f"{tag} ﴿{row['نص الآية']}﴾ [{row['رقم الآية']}]\n"
            return block
    return "لا توجد بيانات لهذا السياق في الملف."

# 4. محرك بحث الجمع والجرد (جرد كافة مواضع اللفظ)
def get_word_collection(word):
    _, df_words = load_all_data()
    if df_words is not None:
        # البحث عن اللفظ في العمود المخصص (يدعم البحث الجزئي)
        results = df_words[df_words['اللفظ'].str.contains(word, na=False)]
        
        if not results.empty:
            count = len(results)
            collection = f"📊 جرد مادي للفظ ({word}) - العدد الإجمالي: {count}\n"
            collection += "------------------------------------------\n"
            for i, (_, row) in enumerate(results.iterrows(), 1):
                # عرض السورة والآية والنص الكامل للآية
                collection += f"{i}. [{row['السورة']}:{row['رقم الآية']}] ﴿{row['نص الآية الكاملة']}﴾\n"
            return collection
    return f"اللفظ ({word}) غير موجود في قاعدة بيانات الجرد الحالية."
