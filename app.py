import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Chatbot AI do analizy magazynu i sprzedaży")

user_question = st.text_input("Zadaj pytanie:")

if st.button("Wyślij"):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Jesteś ekspertem analizującym sprzedaż, magazyn i promocje. Podaj wyniki w formacie odpowiednim do generowania pliku Excel."},
            {"role": "user", "content": user_question}
        ],
        temperature=0.2,
        max_tokens=1000
    )

    answer = response.choices[0].message.content
    
    # Przykład: zamiana odpowiedzi na DataFrame (zakładam że odpowiedź GPT jest tabelą)
    data = {
        "Produkt": ["Lakier 401", "Lakier 402"],
        "Ilość do zamówienia": [380, 230]
    }
    df = pd.DataFrame(data)

    st.markdown("### Odpowiedź Chatbota")
    st.write(df)

    # Generowanie pliku Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Zamówienia')
        writer.save()
        processed_data = output.getvalue()

    st.download_button(
        label="📥 Pobierz Excel z zamówieniem",
        data=processed_data,
        file_name="zamowienia.xlsx",
        mime="application/vnd.ms-excel"
    )
