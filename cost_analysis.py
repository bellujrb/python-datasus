import streamlit as st


def run():
    st.title('Visualizador de Analise de Custo')

    allCity = ['Osvaldo Cruz', 'Presidente Prudente', 'Marília', 'Adamantina',
                     'São Paulo', 'Campinas', 'Ribeirão Preto', 'Bauru', 'Sorocaba']

    allSpecialist = ['Oftalmologia', 'Cardiologia', 'Neurologia', 'Pediatria', 'Ortopedia']

    st.subheader("Seleção de Cidades e Especialidades")
    selected_origin = st.selectbox('Selecione a cidade de origem:', options=allCity, key="origem_key")
    selected_destinations = st.multiselect('Selecione as cidades de destino:', options=allCity,
                                           key="destinos_key")
    selected_specialities = st.multiselect('Selecione as especialidades:', options=allSpecialist,
                                           key="especialidades_key")

    st.button('Gerar gráfico')

# Lembre-se de chamar a função run() se este arquivo for seu script principal
