# Visual AI Automation Workflow Builder

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.1.0--alpha.1-orange)](https://github.com/yourusername/visual-ai-automation)
[![Tests](https://github.com/yourusername/visual-ai-automation/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/yourusername/visual-ai-automation/actions)

## 🤖 نظرة عامة

Visual AI Automation Workflow Builder هو تطبيق يتيح إنشاء سير العمل الآلي المعتمد على الذكاء الاصطناعي بواجهة رسومية. يسمح لك بإنشاء سير عمل (workflows) معقدة مع تدفق وتفرعات متعددة، حيث تعمل كل عقدة على معالجة المدخلات باستخدام نماذج الذكاء الاصطناعي.

## 🔑 الميزات الرئيسية

- **واجهة مستخدم مرئية** - تصميم سير العمل من خلال واجهة رسومية بالسحب والإفلات
- **عقد الذكاء الاصطناعي** - استخدام نموذج Google Gemini للمعالجة الذكية للنصوص
- **قواعد التوجيه المشروطة** - تحديد مسارات وتفرعات الخطوات التالية بناءً على نتائج العقد السابقة
- **البحث عن الويب** - إمكانية استخدام نظام البحث عن الويب للحصول على معلومات محدثة
- **نماذج سير عمل جاهزة** - عدة نماذج معدة مسبقًا لأغراض مختلفة مثل تحليل المشاعر والتصنيف والبحث العميق

## 🏗️ بنية المشروع

```
.
├── README.md               # هذا الملف
├── CHANGELOG.md            # سجل التغييرات
├── run.py                  # ملف تشغيل التطبيق الرئيسي
└── src/                    # كود المصدر
    ├── __init__.py
    ├── config/             # تكوينات وثوابت
    ├── core/               # منطق الأعمال الأساسي
    ├── models/             # تعريفات نماذج البيانات
    ├── ui/                 # مكونات واجهة المستخدم
    ├── utils/              # أدوات مساعدة
    └── workflows/          # نماذج سير العمل الجاهزة
```

## 📋 المتطلبات

- Python 3.8+
- streamlit
- langgraph
- langchain-google-genai
- google-generativeai
- streamlit-agraph (لعرض الرسم البياني)
- **جديد في الإصدار 1.1.0**: دعم لنماذج Anthropic و Cohere

## ⚙️ التثبيت والإعداد

1. **قم بتثبيت المتطلبات**:

```bash
pip install -r requirements.txt
```

2. **احصل على مفاتيح API**:
   - سجل للحصول على مفتاح API لـ Google Gemini من [Google AI Studio](https://ai.google.dev/)
   - اختياري: للاستفادة من الدعم متعدد النماذج في الإصدار 1.1.0:
     - سجل للحصول على مفتاح API لـ Anthropic Claude من [Anthropic Console](https://console.anthropic.com/)
     - سجل للحصول على مفتاح API لـ Cohere من [Cohere Dashboard](https://dashboard.cohere.com/)
   - قم بنسخ ملف `.env.example` إلى `.env` وأضف مفاتيح API الخاصة بك

3. **قم بتشغيل التطبيق**:

```bash
streamlit run run.py
```

أو استخدم السكريبت المرفق:

```bash
./start.sh
```

## 🚀 كيفية الاستخدام

1. **إضافة العقد**:
   - استخدم "Node Palette" في الشريط الجانبي لإضافة عقد جديدة
   - أو اختر أحد نماذج سير العمل الجاهزة للبدء

2. **تكوين العقد**:
   - حدد عقدة لتعديلها في جزء "Node Configuration"
   - قم بتعديل الاسم والنص التحفيزي للنموذج وقواعد التوجيه

3. **تجميع سير العمل**:
   - بعد تكوين جميع العقد، انقر على "Compile Workflow" في الشريط الجانبي

4. **تنفيذ سير العمل**:
   - أدخل الرسالة الأولية في منطقة "Execute Workflow"
   - انقر على "Run Workflow" لبدء التنفيذ
   - شاهد النتائج في منطقة "Execution Results"

## 📝 نماذج سير العمل المتوفرة

- **Summarizer** - نموذج بسيط لتلخيص النصوص
- **Sentiment** - تحليل المشاعر مع مسارات مختلفة للردود الإيجابية والسلبية والمحايدة
- **Classify** - تصنيف نية المستخدم واستخراج المعلومات الهامة
- **Deep Research** - إجراء بحث معمق متعدد الزوايا مع التحقق المتبادل
- **Advanced Hedge Fund** - تحليل استثماري متقدم مع تحليل الاقتصاد الكلي والقطاعات والشركات

## 🧪 الاختبارات

يحتوي المشروع على مجموعة شاملة من الاختبارات للتحقق من صحة المكونات الأساسية:

```bash
pytest --cov=src tests/
```

## 🚀 كيفية تنفيذ نسخة محلية

```bash
# استنساخ المستودع
git clone https://github.com/yourusername/visual-ai-automation.git
cd visual-ai-automation

# تثبيت المتطلبات
pip install -r requirements.txt

# إعداد ملف البيئة
cp .env.example .env
# قم بتحرير ملف .env لإضافة مفاتيح API الخاصة بك

# تشغيل التطبيق
streamlit run run.py
```

## 🤝 المساهمة

نرحب بالمساهمات! الرجاء اتباع هذه الخطوات:

1. قم بتنفيذ fork للمشروع
2. قم بإنشاء فرع الميزة (`git checkout -b feature/amazing-feature`)
3. قم بالالتزام بالتغييرات (`git commit -m 'Add some amazing feature'`)
4. قم بدفع التغييرات إلى الفرع (`git push origin feature/amazing-feature`)
5. قم بفتح طلب سحب (Pull Request)

## 📄 الترخيص

هذا المشروع مرخص بموجب ترخيص MIT - راجع ملف LICENSE للتفاصيل.
