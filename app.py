import streamlit as st
import os
from groq import Groq

# تصميم واجهة التطبيق
st.set_page_config(page_title="HERMES AI", page_icon="🪽", layout="centered")
st.markdown("<style>body {direction: rtl; text-align: right;} .stTextInput>div>div>input {direction: rtl;} .stTextArea>div>div>textarea {direction: rtl;}</style>", unsafe_allow_html=True)
st.title("🪽 HERMES AI")

# مفتاح التشغيل
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ملف حفظ الذاكرة والمعلومات
DATA_FILE = "my_data.txt"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write("أنا هيرميس، الذكاء الاصطناعي الخاص بك والمبرمج خصيصاً لمساعدتك.")

# خانة تغذية العقل بالمعلومات
st.header("🧠 تغذية العقل والمعلومات")
new_info = st.text_area("أضف أي معلومات أو بيانات جديدة تريد أن يتعلمها هيرميس:")
if st.button("حفظ وتحديث العقل"):
    if new_info:
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write("\n" + new_info)
        st.success("تم حفظ المعلومات بنجاح وأصبح هيرميس على دراية بها!")

st.divider()

# قسم الدردشة والشات
st.header("💬 الدردشة المباشرة")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# استقبال سؤال المستخدم
user_query = st.chat_input("تحدث مع هيرميس...")
if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # قراءة المعلومات والذاكرة التي أضافها المستخدم
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        stored_data = f.read()

    # إرسال السؤال مع معلومات المستخدم إلى عقل Llama 3 الحديث عبر Groq
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"أنت مساعد ذكي وصديق مقرب اسمه هيرميس. أجب على أسئلة المستخدم بناءً على معلوماته الشخصية التالية إن وجدت:\n{stored_data}"
                },
                {"role": "user", "content": user_query}
            ]
        )
        ai_response = chat_completion.choices[0].message.content
    except Exception as e:
        ai_response = f"عفواً حدث خطأ في الاتصال: {e}"

    # عرض رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
