import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
from datetime import datetime

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
    
def buscar_por_data(data_busca):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
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

        planilha_id = "15wouW6yV1EHxXSs9y_WmxZJUZh0MZqeZy6CiXwxZcQw"
        sheet = client.open_by_key(planilha_id).sheet1
        dados = sheet.get_all_records()

        resultados = []
        for linha in dados:
            retirada_raw = linha.get("DataRetirada", "")
            devolucao_raw = linha.get("DataEntrega", "")

            # Converte para formato YYYY-MM-DD
            try:
                retirada_fmt = datetime.strptime(retirada_raw, "%d/%m/%Y").strftime("%Y-%m-%d")
            except:
                retirada_fmt = ""
            try:
                devolucao_fmt = datetime.strptime(devolucao_raw, "%d/%m/%Y").strftime("%Y-%m-%d")
            except:
                devolucao_fmt = ""

            if retirada_fmt == data_busca or devolucao_fmt == data_busca:
                resultados.append({
                    "Vestido": linha.get("Numero-Vestido", ""),
                    "Nome": linha.get("Nome", ""),
                    "Telefone": linha.get("Telefone", ""),
                    "Retirada": retirada_raw,
                    "Devolução": devolucao_raw
                })

        return resultados

    except Exception as e:
        st.error(f"Erro ao buscar dados no Google Sheets: {e}")
        return []
