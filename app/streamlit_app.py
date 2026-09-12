import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))import streamlit as st
from chatbot import chatbot_response
from sentiment import analyze_reviews, get_wordcloud_figure
st.set_page_config(page_title="Healthcare Chatbot", page_icon="🩺", layout="wide")

st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: linear-gradient(135deg, #000000 0%, #0a0e1a 30%, #0d1b2e 60%, #0f2647 100%) !important;
    background-size: 200% 200% !important;
    animation: gradientShift 4s ease infinite !important;
}
.main, .block-container,
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stBottom"] > div,
[data-testid="stBottom"] * {
    background: transparent !important;
    background-color: transparent !important;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
h1, h2, h3, .stMarkdown, .stTextInput label, p {
    color: #e6edf3 !important;
}
h1 {
    font-weight: 700 !important;
    background: linear-gradient(90deg, #ffffff, #58a6ff, #ffffff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 1.2s linear infinite;
}
@keyframes shine {
    to { background-position: 200% center; }
}
.stTextInput input {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: #e6edf3 !important;
    border-radius: 8px !important;
    border: 1px solid rgba(88, 166, 255, 0.3) !important;
}
.stButton button {
    background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
    color: white !important;
    border-radius: 6px !important;
    border: none !important;
    padding: 8px 24px !important;
    font-weight: 600 !important;
}
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(88, 166, 255, 0.15) !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] input {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(88, 166, 255, 0.3) !important;
    border-radius: 20px !important;
    color: #e6edf3 !important;
}
[role="tablist"] {
    gap: 10px !important;
    background-color: rgba(255, 255, 255, 0.03) !important;
    padding: 8px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(88, 166, 255, 0.15) !important;
    display: inline-flex !important;
}
[data-testid="stTab"] {
    background-color: transparent !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: all 0.25s ease !important;
}
[data-testid="stTab"] p {
    color: #9aa5b5 !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}
[data-testid="stTab"] svg {
    fill: #9aa5b5 !important;
    transition: fill 0.25s ease !important;
}
[data-testid="stTab"]:hover {
    background-color: rgba(88, 166, 255, 0.1) !important;
}
[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
    box-shadow: 0 0 14px rgba(88, 166, 255, 0.5) !important;
}
[data-testid="stTab"][aria-selected="true"] p {
    color: white !important;
}
[data-testid="stTab"][aria-selected="true"] svg {
    fill: white !important;
}
</style>

<div id="ekg-bg">
  <svg width="200%" height="100%" preserveAspectRatio="none" viewBox="0 0 800 200">
    <polyline class="ekg-line" fill="none" stroke="#58a6ff" stroke-width="2.5"
      points="0,100 60,100 90,100 110,60 130,140 150,20 170,180 190,100
              260,100 320,100 350,100 370,60 390,140 410,20 430,180 450,100
              520,100 580,100 610,100 630,60 650,140 670,20 690,180 710,100
              780,100
              800,100 860,100 890,100 910,60 930,140 950,20 970,180 990,100
              1060,100 1120,100 1150,100 1170,60 1190,140 1210,20 1230,180 1250,100
              1320,100 1380,100 1410,100 1430,60 1450,140 1470,20 1490,180 1510,100
              1580,100"/>
  </svg>
</div>
<style>
#ekg-bg {
    position: fixed;
    top: 40%;
    left: 0;
    width: 100%;
    height: 200px;
    z-index: 0;
    opacity: 0.35;
    pointer-events: none;
    overflow: hidden;
}
#ekg-bg svg {
    animation: ekgScroll 6s linear infinite;
}
@keyframes ekgScroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.ekg-line {
    filter: drop-shadow(0 0 4px #58a6ff) drop-shadow(0 0 10px #58a6ff);
    animation: ekgPulse 2s ease-in-out infinite;
}
@keyframes ekgPulse {
    0%, 100% { filter: drop-shadow(0 0 4px #58a6ff) drop-shadow(0 0 10px #58a6ff); opacity: 0.7; }
    50% { filter: drop-shadow(0 0 8px #58a6ff) drop-shadow(0 0 18px #58a6ff); opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🩺 Healthcare Chatbot")
    st.subheader("Please enter your name to continue")
    name = st.text_input("Your name")
    if st.button("Enter"):
        if name.strip() != "":
            st.session_state.user_name = name
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("Please enter a name.")
    st.stop()

st.title("🩺 Healthcare Chatbot")
st.write(f"Welcome, **{st.session_state.user_name}**!")

tab1, tab2 = st.tabs([":material/chat: Chatbot", ":material/monitoring: Sentiment Dashboard"])

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        st.markdown("<p style='color:#8b93b0;'>Try asking:</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        example_clicked = None
        with col1:
            if st.button("Symptoms of dengue?"):
                example_clicked = "What are the symptoms of dengue?"
        with col2:
            if st.button("How to prevent diabetes?"):
                example_clicked = "How to prevent diabetes?"
        with col3:
            if st.button("Treatment for asthma?"):
                example_clicked = "What is the treatment for asthma?"
        if example_clicked:
            st.session_state.messages.append({"role": "user", "content": example_clicked})
            with st.spinner("Thinking..."):
                answer = chatbot_response(example_clicked)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🩺"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    question = st.chat_input("Ask a health question...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="👤"):
            st.write(question)
        with st.chat_message("assistant", avatar="🩺"):
            with st.spinner("Thinking..."):
                answer = chatbot_response(question)
                st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

with tab2:
    st.subheader("Patient Sentiment Analysis")
    st.write("Analysis of sample patient reviews using VADER sentiment analysis.")

    results = analyze_reviews()

    col1, col2, col3 = st.columns(3)
    counts = results["sentiment"].value_counts()
    col1.metric("Positive", counts.get("Positive", 0))
    col2.metric("Negative", counts.get("Negative", 0))
    col3.metric("Neutral", counts.get("Neutral", 0))

    st.bar_chart(counts)

    st.write("### Word Clouds")
    wc_col1, wc_col2 = st.columns(2)
    with wc_col1:
        st.write("**Positive Reviews**")
        fig_pos = get_wordcloud_figure(results, "Positive")
        if fig_pos:
            st.pyplot(fig_pos)
    with wc_col2:
        st.write("**Negative Reviews**")
        fig_neg = get_wordcloud_figure(results, "Negative")
        if fig_neg:
            st.pyplot(fig_neg)

    st.write("### All Reviews")
    st.dataframe(results, use_container_width=True)
