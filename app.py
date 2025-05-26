import streamlit as st
from openai import OpenAI
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError
import traceback

# Konfiguracja GPT
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧪 Test połączenia z Google Sheets")

# Autoryzacja Google
try:
    credentials = Credentials.from_service_account_info(st.secrets["google_credentials"])
    gc = gspread.authorize(credentials)
    st.success("✅ Autoryzacja Google przebiegła pomyślnie.")
except Exception as e:
    st.error("❌ Błąd autoryzacji Google:")
    st.code(traceback.format_exc())
    st.stop()

# TEST: Czy konto serwisowe widzi pliki na Twoim dysku
try:
    st.subheader("📄 Arkusze dostępne dla konta serwisowego:")
    files = gc.openall()
    for f in files:
        st.write(f"📘 {f.title}")
except APIError as e:
    st.error("❌ Błąd podczas pobierania listy arkuszy.")
    st.code(str(e))
    st.stop()
except Exception as e:
    st.error("❌ Inny błąd:")
    st.code(traceback.format_exc())
    st.stop()
