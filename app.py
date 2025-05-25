import streamlit as st
from openai import OpenAI

# Inicjalizacja klienta OpenAI z twoim kluczem API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("Chatbot AI do analizy magazynu i sprzedaży")

user_question = st.text_input("Zadaj pytanie:")

if st.button("Wyślij"):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Jesteś ekspertem, który pomaga analizować sprzedaż, magazyn oraz promocje w firmie. Podajesz konkretne rekomendacje."},
            {"role": "user", "content": user_question}
        ],
        temperature=0.3,
        max_tokens=800
    )
    
    answer = response.choices[0].message.content
    st.markdown(answer)
