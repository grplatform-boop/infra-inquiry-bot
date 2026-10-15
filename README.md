# 🚀 AI-Powered Infrastructure Inquiry Bot

نظام استعلام ذكي للبنية التحتية يعتمد على **FastAPI**, **Pandas**, وذكاء اصطناعي من **GROQ** لتحليل الأسئلة الطبيعية والبحث داخل بيانات السيرفرات.

---

## 🧠 فكرة المشروع
هذا المشروع يوفر واجهة برمجية (API) للاستعلام عن بيانات السيرفرات المخزّنة داخل ملف Excel، مع دعم:

- محادثة ذكاء اصطناعي مع ذاكرة (Chat Memory)
- استعلام ذكي يفهم الأسئلة الطبيعية (AI Query)
- فلترة متقدمة حسب IP / Port / Environment
- عرض جميع السيرفرات
- واجهة توثيق Swagger جاهزة

---

## 🛠 المتطلبات التشغيلية

- Python 3.10+
- FastAPI
- Uvicorn
- Pandas
- OpenPyXL
- GROQ API Key
- ملف Excel: `Training_Servers_80Rows.xlsx`

---

## 📦 تثبيت المكتبات

```bash
pip install fastapi uvicorn pandas openpyxl pydantic groq python-dotenv
```

---

## 🔐 إعداد ملف البيئة `.env`

أنشئ ملف `.env` وضع داخله:

```
GROQ_API_KEY=ضع_مفتاحك_هنا
```

---

## ▶️ تشغيل السيرفر

```bash
uvicorn main:app --reload
```

ثم افتح المتصفح:

```
http://127.0.0.1:8000/docs
```

---

## 📡 قائمة الـ Endpoints

### 🗨️ Chat Endpoints
| Endpoint | Method | الوصف |
|---------|--------|--------|
| `/api/chat` | POST | محادثة ذكاء اصطناعي مع ذاكرة |
| `/api/chat/reset` | POST | مسح ذاكرة المحادثة |

### 🤖 AI Query
| Endpoint | Method | الوصف |
|---------|--------|--------|
| `/api/query` | POST | استعلام ذكاء اصطناعي يفهم السؤال ويستخرج intent + field + value |

### 🔍 فلترة السيرفرات
| Endpoint | Method | الوصف |
|---------|--------|--------|
| `/api/servers/filter` | GET | فلترة حسب IP / Port / Environment |

### 🗂 عرض السيرفرات
| Endpoint | Method | الوصف |
|---------|--------|--------|
| `/api/servers` | GET | عرض جميع السيرفرات |

---

## 🧠 مثال على `/api/query`

```json
{
  "question": "اعطني السيرفرات في بيئة TEST"
}
```

---

## 🧩 مثال على `/api/chat`

```json
{
  "message": "اعطني السيرفرات في بيئة PROD"
}
```

---

## 🏗 Architecture Diagram (ASCII)

```
User → FastAPI → GROQ AI → Intent Extraction → Excel Data → Response
```

---

## 🎓 جاهز كمشروع تخرج

المشروع مكتمل، منظم، ويدعم الذكاء الاصطناعي، ويمكن تقديمه كـ:

- مشروع تخرج جامعي  
- مشروع تدريبي  
- مشروع عملي في البنية التحتية  
- مشروع توظيف في مجال الـ DevOps / Infrastructure  

---

## 📁 هيكلة المشروع

```
infra-inquiry-bot/
│── main.py
│── README.md
│── .env
│── venv/
│── Training_Servers_80Rows.xlsx
```

---

## ✨ مميزات إضافية

- يدعم الذكاء الاصطناعي عبر GROQ (مجاني وسريع)
- يدعم ذاكرة المحادثة
- يدعم فلترة متقدمة
- يدعم استخراج Intent تلقائيًا
- واجهة توثيق جاهزة عبر Swagger

---

## 👨‍💻 المطوّر
ابرار القرني-مشروع بنية تحتية ذكي يعتمد على الذكاء الاصطناعي.
