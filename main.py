import streamlit as st
from google_sheets_writer import salvar_em_planilha_google, buscar_por_data
from datetime import datetime

st.title("Cadastro Vestidos 👗")
st.link_button("Link para consultar número dos vestidos", "https://saraiva142.github.io/Consulta-Junino/")

with st.form("form"):
    nome = st.text_input("Nome da Cliente")
    telefone = st.number_input("Telefone", format="%d", step=1, min_value=0)
    data_retirada = st.date_input("Data de Retirada")
    data_devolucao = st.date_input("Data de Devolução")
    numero_vestido = st.number_input("Número do Vestido", format="%d", step=1, min_value=0)
    observacoes = st.text_area("Observações")
    submit_button = st.form_submit_button("Enviar")
    
    if submit_button:
        dados = [
            nome,
            str(telefone),
            str(data_retirada),
            str(data_devolucao),
            str(numero_vestido),
            observacoes,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
        ]
        
        sucesso = salvar_em_planilha_google(dados)
        if sucesso:
            st.success("Dados salvos com sucesso no Google Sheets!")
        else:
            st.error("Erro ao salvar os dados.")

st.header("🔍 Consultar vestidos por data")

data_pesquisa = st.date_input("Selecione uma data")
buscar = st.button("Buscar vestidos para retirada ou devolução")

if buscar:
    data_str = str(data_pesquisa)
    resultados = buscar_por_data(data_str)

    if resultados:
        st.subheader("📋 Resultados encontrados:")
        for item in resultados:
            st.markdown(f"""
            👗 Vestido nº: {item['Vestido']}  
            👤 Cliente: {item['Nome']}  
            📞 Telefone: {item['Telefone']}  
            📅 Retirada: {item['Retirada']}  
            📅 Devolução: {item['Devolução']}  
            ---
            """)
    else:
        st.warning("Nenhum vestido marcado para essa data.")
