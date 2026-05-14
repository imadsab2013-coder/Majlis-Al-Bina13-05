import pandas as pd
import streamlit as st
import os

# 1. تحميل البيانات مع التخزين المؤقت لضمان السرعة المادية
@st.cache_data
def load_all_data():
    # تحديد مسارات الملفات
    quran_path = "data/data_quran.xlsx"
    words_path = "data/data_words.xlsx"
    
    try:
        # التحقق من وجود الملفات قبل التحميل
        if not os.path.exists(quran_path) or not os.path.exists(words_path):
            st.error("⚠️ خطأ مادي: ملفات الإكسيل غير موجودة في مجلد data")
            return None, None
            
        # تحميل الملفات
        df_quran = pd.read_excel(quran_path) 
        df_words = pd.read_excel(words_path)
        
        # تنظيف البيانات (معالجة الخلايا المدمجة ffill)
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
        # ترتيب فريد للسور حسب ظهورها في المصحف
        return df_quran['السورة'].unique().tolist()
    return []

# 3. محرك بحث السياق (الآية السابقة + المختارة + اللاحقة)
def get_context_block(surah, verse_num):
    df_quran, _ = load_all_data()
    if df_quran is not None:
        # جلب الآيات الثلاث (السياق المادي المحيط)
        mask = (df_quran['السورة'] == surah) & \
               (df_quran['رقم الآية'].isin([verse_num - 1, verse_num, verse_num + 1]))
        results = df_quran[mask].sort_values(by='رقم الآية')
        
        if not results.empty:
            block = ""
            for _, row in results.iterrows():
                # تمييز الآية المختارة بنجمة
                tag = "⭐ " if row['رقم الآية'] == verse_num else "⬅️ "
                block += f"{tag} ﴿{row['نص الآية']}﴾ [{row['رقم الآية']}]\n"
            return block
    return "لا توجد بيانات لهذا السياق."

# 4. محرك بحث الجمع والجرد (جرد كافة مواضع اللفظ)
def get_word_collection(word):
    _, df_words = load_all_data()
    if df_words is not None:
        # البحث عن اللفظ في العمود المخصص للألفاظ
        results = df_words[df_words['اللفظ'].str.contains(word, na=False)]
        
        if not results.empty:
            collection = f"📊 نتائج جرد اللفظ ({word}):\n\n"
            for _, row in results.iterrows():
                collection += f"• [{row['السورة']}:{row['رقم الآية']}] ﴿{row['نص الآية الكاملة']}﴾\n"
            return collection
    return f"لم يتم العثور على اللفظ ({word}) في ملف الجرد."
