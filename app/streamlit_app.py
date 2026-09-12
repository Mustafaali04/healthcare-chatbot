import streamlit as st
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

[data-testid="stChatInput"] {
    background: transparent !important;
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

.stTextInput input:focus {
    border: 1px solid #58a6ff !important;
    box-shadow: 0 0 12px rgba(88, 166, 255, 0.4) !important;
}

.stButton button {
    background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
    color: white !important;
    border-radius: 6px !important;
    border: none !important;
    padding: 8px 24px !important;
    font-weight: 600 !important;
    box-shadow: 0 0 12px rgba(88, 166, 255, 0.3) !important;
}

.stButton button:hover {
    box-shadow: 0 0 18px rgba(88, 166, 255, 0.6) !important;
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
</style>
""", unsafe_allow_html=True)

# ---- LOGIN ----
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

# ---- MAIN APP ----
st.title("🩺 Healthcare Chatbot")
st.write(f"Welcome, **{st.session_state.user_name}**! Ask me about symptoms, treatment, or prevention for common diseases.")

tab1, tab2 = st.tabs(["💬 Chatbot", "📊 Sentiment Dashboard"])

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if len(st.session_state.messages) == 0:
        st.markdown("<p style='color:#8b93b0; margin-top: 20px;'>Try asking:</p>", unsafe_allow_html=True)
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
    col2.metric("Negative", counts.get("Negative",0))
    col3.metric("Neutral", counts.get("Neutral"))

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