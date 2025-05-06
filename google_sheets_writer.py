import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def salvar_em_planilha_google(dados):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        # Carrega as credenciais do secrets.toml
        creds_dict = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"],
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
        }
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # Restante do código (abrir planilha, append_row, etc.)
        planilha_id = "15wouW6yV1EHxXSs9y_WmxZJUZh0MZqeZy6CiXwxZcQw"
        sheet = client.open_by_key(planilha_id).sheet1
        sheet.append_row(dados)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar no Google Sheets: {e}")
        return False