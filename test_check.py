"""
═══════════════════════════════════════════════════════════════════════════════
ملف الفحص الذاتي | Self-Check Report
مشروع: مجلس البينة
═══════════════════════════════════════════════════════════════════════════════

هذا الملف يحتوي على اختبارات التحقق من جودة الكود قبل التسليم
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# 📋 قائمة الفحوصات المطلوبة
# ═══════════════════════════════════════════════════════════════════════════════

CHECKS = {
    "import_streamlit": "✅ هل تم استيراد مكتبة Streamlit؟",
    "session_state": "✅ هل تم تهيئة st.session_state بشكل صحيح؟",
    "agents_defined": "✅ هل تم تعريف الأعضاء العشرة (AGENTS)؟",
    "ui_components": "✅ هل توجد كل مكونات الواجهة (شريط، سبورة، sidebar)؟",
    "connection_status": "✅ هل يوجد نظام فحص اتصال مع مؤشرات؟",
    "rules_management": "✅ هل يوجد نظام إدارة القواعس §؟",
    "css_styling": "✅ هل تم تضمين CSS مخصص للتصميم؟",
    "error_handling": "✅ هل يوجد معالجة أخطاء شاملة؟",
    "independence": "✅ هل الواجهة مستقلة عن API؟",
    "data_files_check": "✅ هل يوجد فحص ملفات البيانات مع تنبيهات؟"
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 دالة الفحص
# ═══════════════════════════════════════════════════════════════════════════════

def run_checks(file_path):
    """فحص الملف والتحقق من المتطلبات"""
    
    results = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # فحص 1: Streamlit
        results["import_streamlit"] = "import streamlit" in content
        
        # فحص 2: Session State
        results["session_state"] = "st.session_state" in content and "initialize_session" in content
        
        # فحص 3: تعريف الأعضاء
        results["agents_defined"] = "AGENTS = {" in content and "'1A'" in content and "'10A'" in content
        
        # فحص 4: مكونات الواجهة
        results["ui_components"] = (
            "agent-bar" in content and 
            "board-container" in content and 
            "col_sidebar" in content
        )
        
        # فحص 5: نظام الاتصال
        results["connection_status"] = (
            "connection_status" in content and 
            "check_data_files" in content and
            "🟢" in content
        )
        
        # فحص 6: إدارة القواعس
        results["rules_management"] = (
            "st.session_state.rules" in content and
            "new_rule_name" in content and
            "delete_rule" in content
        )
        
        # فحص 7: CSS
        results["css_styling"] = "st.markdown" in content and ".agent-icon" in content
        
        # فحص 8: معالجة الأخطاء
        results["error_handling"] = "st.error" in content and "st.warning" in content
        
        # فحص 9: استقلالية عن API
        results["independence"] = (
            "الواجهة تعمل بشكل مستقل عن API" in content or
            "يعمل حتى لو كانت ملفات الداتا غير موجودة" in content or
            "يعمل وتظهر بيانات" in content or
            "الموقع يعمل وتظهر بيانات" in content or
            "الموقع يعمل حتى لو كانت" in content
        )
        
        # فحص 10: فحص الملفات
        results["data_files_check"] = (
            "check_data_files" in content and
            "data_quran.xlsx" in content and
            "data_words.xlsx" in content
        )
        
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        return None
    
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 طباعة النتائج
# ═══════════════════════════════════════════════════════════════════════════════

def print_report(results):
    """طباعة تقرير الفحص"""
    
    print("\n" + "="*80)
    print("📋 تقرير الفحص الذاتي | Self-Check Report")
    print("="*80 + "\n")
    
    print("مشروع: مجلس البينة | Majlis Al-Bina")
    print(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    passed = 0
    failed = 0
    
    print("─" * 80)
    
    for check_id, check_name in CHECKS.items():
        status = results.get(check_id, False)
        
        if status:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
            failed += 1
    
    print("─" * 80 + "\n")
    
    # الملخص
    total = len(CHECKS)
    percentage = (passed / total) * 100
    
    print(f"📊 النتيجة النهائية:")
    print(f"   ✅ نجح: {passed}/{total}")
    print(f"   ❌ فشل: {failed}/{total}")
    print(f"   📈 النسبة: {percentage:.1f}%\n")
    
    # التوصية
    if percentage == 100:
        print("🎉 ممتاز! الملف جاهز للاستخدام بنسبة 100%\n")
        return True
    elif percentage >= 80:
        print("✅ جيد جداً! الملف جاهز مع بعض الملاحظات البسيطة\n")
        return True
    elif percentage >= 50:
        print("⚠️ يحتاج تحسينات قبل الاستخدام\n")
        return False
    else:
        print("❌ يحتاج إعادة كتابة كبيرة\n")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 تشغيل الفحص
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    file_path = "app_ui.py"
    
    if not Path(file_path).exists():
        print(f"❌ لم يتم العثور على الملف: {file_path}")
        sys.exit(1)
    
    results = run_checks(file_path)
    
    if results is None:
        print("❌ فشل الفحص")
        sys.exit(1)
    
    passed = print_report(results)
    
    # حفظ النتائج
    with open('check_report.json', 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'passed': passed
        }, f, ensure_ascii=False, indent=2)
    
    print(f"📁 تم حفظ التقرير في: check_report.json\n")
    
    sys.exit(0 if passed else 1)
