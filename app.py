import streamlit as st
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

# تصميم الواجهة
st.set_page_config(page_title="HERMES AI", page_icon="🪽", layout="centered")
st.markdown("<style>body {direction: rtl; text-align: right;} .stTextInput>div>div>input {direction: rtl;} .stTextArea>div>div>textarea {direction: rtl;}</style>", unsafe_allow_html=True)
st.title("🪽 HERMES AI")

# مفتاح التشغيل
os.environ["GROQ_API_KEY"] = "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"

# تشغيل العقل
@st.cache_resource
def load_ai():
    if not os.path.exists("my_data.txt"):
        with open("my_data.txt", "w", encoding="utf-8") as f:
            f.write("أنا هيرميس، الذكاء الاصطناعي الخاص بك.")
    loader = TextLoader("my_data.txt", encoding="utf-8")
    docs = loader.load()
    texts = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50).split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = SKLearnVectorStore.from_documents(texts, embeddings)
    llm = ChatGroq(model_name="llama3-8b-8192")
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectordb.as_retriever(search_kwargs={"k": 2}))

# التغذية
st.header("🧠 تغذية العقل")
new_info = st.text_area("أضف معلومات جديدة هنا:")
if st.button("حفظ المعلومات"):
    if new_info:
        with open("my_data.txt", "a", encoding="utf-8") as f:
            f.write("\n" + new_info)
        st.success("تم الحفظ!")
        st.cache_resource.clear()

st.divider()

# الشات
st.header("💬 الدردشة")
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("تحدث مع هيرميس...")
if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    ai = load_ai()
    response = ai.invoke(user_query)
    
    with st.chat_message("assistant"):
        st.markdown(response["result"])
    st.session_state.messages.append({"role": "assistant", "content": response["result"]})
