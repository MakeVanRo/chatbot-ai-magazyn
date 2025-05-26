import streamlit as st
from openai import OpenAI
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import traceback

# --- KONFIGURACJA ---
st.set_page_config(page_title="Chatbot Magazynowy", page_icon="📦")
st.title("📦 Chatbot Magazynowy (AI + Google Sheets)")

# --- AUTORYZACJA ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    credentials = Credentials.from_service_account_info(
        st.secrets["google_credentials"],
        scopes=SCOPES
    )
    gc = gspread.authorize(credentials)
except Exception as e:
    st.error("❌ Błąd autoryzacji Google:")
    st.code(traceback.format_exc())
    st.stop()

# --- WYBÓR ARKUSZA ---
try:
    sheets = gc.open("Subiekt API")  # ← możesz też dodać selectbox do wyboru
    worksheet = sheets.sheet1  # lub .worksheet("nazwa_zakładki")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error("❌ Błąd podczas wczytywania danych:")
    st.code(traceback.format_exc())
    st.stop()

# --- WYSWIETL DANE (opcjonalnie) ---
with st.expander("📊 Zobacz dane z arkusza"):
    st.dataframe(df)

# --- KONFIGURACJA OPENAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- INTERFEJS PYTANIA ---
user_question = st.text_input("🧠 Zadaj pytanie o dane magazynowe:")

if st.button("🔍 Zapytaj"):
    try:
        prompt = f"""
        Oto dane magazynowe z Google Sheets:\n{df.to_csv(index=False)}\n
        Na ich podstawie odpowiedz na pytanie użytkownika:\n{user_question}
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś pomocnikiem magazynowym. Analizujesz dane i odpowiadasz rzeczowo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        st.success("✅ Odpowiedź AI:")
        st.markdown(answer)

    except Exception as e:
        st.error("❌ Błąd podczas komunikacji z GPT:")
        st.code(traceback.format_exc())
