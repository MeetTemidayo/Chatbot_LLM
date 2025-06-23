import streamlit as st
from datetime import datetime
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# The LangChain Setup 
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""
model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# The Streamlit Configuratiomn
st.set_page_config(page_title="Temidayo Chatbot", layout="centered")

# The session state 
if "history" not in st.session_state:
    st.session_state.history = []
if "context" not in st.session_state:
    st.session_state.context = ""

# Page style, colors, etc 
st.markdown("""
<style>
body {
    background-color: #e5ddd5;
    font-family: Arial, sans-serif;
}
.chat-bubble {
    padding: 10px 15px;
    margin: 8px;
    border-radius: 10px;
    max-width: 75%;
    display: inline-block;
}
.user-bubble {
    background-color: #dcf8c6;
    align-self: flex-end;
    text-align: right;
    margin-left: auto;
}
.bot-bubble {
    background-color: #ffffff;
    align-self: flex-start;
    margin-right: auto;
}
.chat-container {
    display: flex;
    flex-direction: column;
}
.timestamp {
    font-size: 0.7em;
    color: #888;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# The title that will be displayed in the GUI webpage
st.markdown("<h2 style='color: green;'>💬 Temidayo Chatbot</h2>", unsafe_allow_html=True)

# The part responsible for chat Display 
for speaker, message, ts in st.session_state.history:
    bubble_class = "user-bubble" if speaker == "You" else "bot-bubble"
    st.markdown(f"""
    <div class="chat-container">
        <div class="chat-bubble {bubble_class}">
            {message}
            <div class="timestamp">{ts}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# This is the User Input part of the code
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", placeholder="Message", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Saving the user message
    now = datetime.now().strftime("%H:%M")
    st.session_state.history.append(("You", user_input, now))

    # Building context and getting the LLM response
    context_text = "\n".join(f"User: {u}\nAI: {a}" for u, a, _ in st.session_state.history if u == "You")
    result = chain.invoke({"context": context_text, "question": user_input})
    
    # Saving my bot response
    st.session_state.history.append(("Bot", str(result), datetime.now().strftime("%H:%M")))

    # Force rerun to show the new messages immediately
    # st.experimental_rerun()
    
    st.rerun()

    # pass

    # run it with: streamlit run main2.py

