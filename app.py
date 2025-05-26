import streamlit as st
from openai import OpenAI
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound

# Konfiguracja GPT
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Konfiguracja Google Sheets
try:
    google_credentials = Credentials.from_service_account_info(st.secrets["google_credentials"])
    gc = gspread.authorize(google_credentials)
except Exception as e:
    st.error("❌ Błąd autoryzacji Google Sheets. Sprawdź sekcję `secrets`.")
    st.stop()

# Próbuj wczytać arkusz
# TEST: Czy mamy dostęp do plików na Google Drive
try:
    files = gc.openall()
    st.success("📄 Znalezione arkusze:")
    for f in files:
        st.write(f"📘 {f.title}")
except Exception as e:
    st.error("❌ Błąd podczas pobierania listy arkuszy. Sprawdź, czy konto serwisowe ma dostęp i poprawne API.")
    st.code(str(e))
    st.stop()
except SpreadsheetNotFound:
    st.error("❌ Nie znaleziono arkusza 'Subiekt API'. Upewnij się, że nazwa jest poprawna i że konto serwisowe ma dostęp.")
    st.stop()
except WorksheetNotFound:
    st.error("❌ Nie znaleziono zakładki 'produkty_magazyn'. Sprawdź, czy taka istnieje.")
    st.stop()

# UI
st.title("🤖 Chatbot AI z Google Sheets")

user_question = st.text_input("Zadaj pytanie lub polecenie dotyczące danych:")

if st.button("Wyślij") and user_question:
    try:
        response = client.chat.completions.create(
            model="gpt-4.0",  # lub gpt-4.1 jeśli masz dostęp
            messages=[
                {"role": "system", "content": "Jesteś asystentem do aktualizacji danych magazynowych w Google Sheets."},
                {"role": "user", "content": user_question}
            ],
            temperature=0.2,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        st.write("🧠 Odpowiedź AI:", answer)

        # Prosty przykład: przetwarzanie polecenia
        if "Dodaj etykietę" in user_question:
            product_name = "Lakier 401 Glossy 8ml"
            label_code = "E-401-BUT"

            cell = worksheet.find(product_name)
            row_number = cell.row
            worksheet.update_cell(row_number, 6, label_code)

            st.success(f"Dodano etykietę '{label_code}' do produktu '{product_name}'.")

    except Exception as e:
        st.error(f"❌ Wystąpił błąd podczas przetwarzania: {e}")
