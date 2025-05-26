import streamlit as st
from openai import OpenAI
import gspread
from google.oauth2.service_account import Credentials

# Konfiguracja GPT
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Konfiguracja Google Sheets (klucz API w sekcji Secrets)
google_credentials = Credentials.from_service_account_info(st.secrets["google_credentials"])
gc = gspread.authorize(google_credentials)

# Wczytaj arkusz
spreadsheet = gc.open("Nazwa_Twojego_arkusza")
worksheet = spreadsheet.worksheet("produkty_magazyn")

st.title("Chatbot AI z integracją Google Sheets")

user_question = st.text_input("Zadaj pytanie lub polecenie do aktualizacji arkusza:")

if st.button("Wyślij"):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Interpretujesz polecenia użytkownika dotyczące aktualizacji etykiet produktów w Google Sheets."},
            {"role": "user", "content": user_question}
        ],
        temperature=0.2,
        max_tokens=500
    )
    answer = response.choices[0].message.content

    # Przykładowe polecenie: "Dodaj etykietę butelki E-401-BUT do lakieru 401"
    if "Dodaj etykietę" in user_question:
        product_name = "Lakier 401 Glossy 8ml"  # tutaj można automatycznie rozpoznać z GPT
        label_code = "E-401-BUT"  # analogicznie, wyciągnąć z pytania
        
        # Znajdź produkt w arkuszu
        cell = worksheet.find(product_name)
        row_number = cell.row

        # Zapisz w odpowiedniej kolumnie (np. kolumna F: "Kod etykiety butelka")
        worksheet.update_cell(row_number, 6, label_code)
        
        st.success(f"Dodano {label_code} do produktu {product_name} w arkuszu.")

    st.write("Odpowiedź AI:", answer)
