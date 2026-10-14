from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from pydantic import BaseModel, Field
from groq import Groq
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

app = FastAPI(
    title="AI Infrastructure Inquiry Bot",
    description="بوت استعلام ذكي للبنية التحتية مع ذاكرة وفلترة متقدمة",
    version="3.0",
)

EXCEL_FILE = "Training_Servers_80Rows.xlsx"

# تحميل ملف الإكسل عند بداية التشغيل
try:
    df = pd.read_excel(EXCEL_FILE)
    df.columns = df.columns.str.strip()
except Exception as e:
    df = None
    print(f"تحذير: تعذر تحميل ملف الإكسل: {e}")

# ذاكرة المحادثة
chat_memory: List[Dict[str, str]] = []

# عميل GROQ
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# نماذج التحقق من المدخلات
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=300)


@app.get("/", tags=["Home"])
def home():
    return {"message": "مرحباً بك في نظام الاستعلام الذكي للبنية التحتية!"}


# 1️⃣ محادثة ذكاء اصطناعي مع ذاكرة
@app.post("/api/chat", tags=["Chat"])
def chat_with_memory(request: ChatRequest):
    if df is None:
        raise HTTPException(status_code=500, detail="بيانات الإكسل غير متوفرة.")

    user_msg = request.message.strip()
    chat_memory.append({"role": "user", "content": user_msg})

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "أنت مساعد متخصص في بيانات السيرفرات."},
            *chat_memory
        ],
    )

    bot_response = completion.choices[0].message.content
    chat_memory.append({"role": "assistant", "content": bot_response})

    return {
        "response": bot_response,
        "history_length": len(chat_memory),
        "chat_history": chat_memory,
    }


@app.post("/api/chat/reset", tags=["Chat"])
def reset_chat_memory():
    global chat_memory
    chat_memory = []
    return {"message": "تم مسح ذاكرة المحادثة بنجاح."}


# 2️⃣ استعلام ذكاء اصطناعي — فهم السؤال وتحويله إلى فلترة
@app.post("/api/query", tags=["AI Query"])
def ai_query(request: QueryRequest):
    if df is None:
        raise HTTPException(status_code=500, detail="بيانات الإكسل غير متوفرة.")

    question = request.question.strip()

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": """
أنت مساعد متخصص في تحليل أسئلة الاستعلام عن السيرفرات.
استخرج من السؤال:
- intent: search أو stats
- field: أحد الحقول (Server_Name, Host_Name, Source_IP, NAT_IP, Port, Environment)
- value: قيمة البحث
أرجع النتيجة بصيغة JSON فقط.
                """
            },
            {"role": "user", "content": question},
        ],
    )

    import json
    parsed = json.loads(completion.choices[0].message.content)

    intent = parsed.get("intent")
    field = parsed.get("field")
    value = parsed.get("value")

    if intent == "search":
        if field not in df.columns:
            raise HTTPException(status_code=400, detail="حقل غير موجود في الإكسل.")
        result = df[df[field].astype(str).str.contains(str(value), case=False, na=False)]
        return {"count": len(result), "results": result.to_dict(orient="records")}

    elif intent == "stats":
        if field not in df.columns:
            raise HTTPException(status_code=400, detail="حقل غير موجود.")
        stats = df[field].value_counts().to_dict()
        return {"stats": stats}

    return {"error": "تعذر فهم السؤال."}


# 3️⃣ فلترة متقدمة (IP + Port + Environment)
@app.get("/api/servers/filter", tags=["Servers Filter"])
def filter_servers(
    ip: Optional[str] = Query(None),
    port: Optional[int] = Query(None),
    environment: Optional[str] = Query(None),
):
    if df is None:
        raise HTTPException(status_code=500, detail="بيانات الإكسل غير متوفرة.")

    filtered_df = df.copy()

    for col in filtered_df.columns:
        col_lower = col.lower()

        if ip and ("ip" in col_lower or "address" in col_lower):
            filtered_df = filtered_df[
                filtered_df[col].astype(str).str.contains(ip, case=False, na=False)
            ]

        if port and ("port" in col_lower):
            filtered_df = filtered_df[filtered_df[col].astype(str) == str(port)]

        if environment and ("env" in col_lower or "environment" in col_lower):
            filtered_df = filtered_df[
                filtered_df[col].astype(str).str.contains(environment, case=False, na=False)
            ]

    return {"count": len(filtered_df), "results": filtered_df.to_dict(orient="records")}


# 4️⃣ عرض جميع السيرفرات
@app.get("/api/servers", tags=["Servers"])
def get_all_servers():
    if df is None:
        raise HTTPException(status_code=500, detail="بيانات الإكسل غير متوفرة.")
    return df.to_dict(orient="records")
