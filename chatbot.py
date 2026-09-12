import os
import requests
from dotenv import load_dotenv
from load_data import load_data, search_data

load_dotenv(dotenv_path="C:/Users/munna/OneDrive/Desktop/healthcare-chatbot/.env")
api_key = os.getenv("OPENROUTER_API_KEY")

def ask_ai(question, context, max_retries=2):
    prompt = f"""Use the following health information to answer the question if it's relevant.
If the information doesn't fully answer the question, use your own general medical knowledge to complete the answer, and mention that part is general knowledge rather than from the verified dataset.

Health Information:
{context}

Question: {question}
Answer:"""

    for attempt in range(max_retries + 1):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "openrouter/free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()

        if "choices" in data:
            answer = data["choices"][0]["message"]["content"]
            # Check if the answer looks like a bad/junk response
            if len(answer.strip()) > 30 and "user safety" not in answer.lower():
                return answer
        # If we get here, either the call failed or the answer looked bad - retry

    return "Sorry, the AI service is having trouble right now. Please try asking again."

def chatbot_response(question):
    df = load_data()
    results = search_data(df, question)

    if len(results) == 0:
        answer = ask_ai(question, context="No specific information available in the knowledge base. Answer using general medical knowledge, and mention this is general information, not from a verified source.")
        return answer

    context = "\n".join(results["content"].tolist())
    answer = ask_ai(question, context)
    return answer

if __name__ == "__main__":
    print("Healthcare Chatbot (type 'quit' to exit)")
    while True:
        question = input("\nYou: ")
        if question.lower() == "quit":
            break
        answer = chatbot_response(question)
        print("Bot:", answer)
