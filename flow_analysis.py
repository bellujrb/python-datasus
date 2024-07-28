import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Carregar o arquivo CSV
def load_data(file_name, separator_list):
    with st.spinner(f"Carregando dados de {file_name}..."):
        try:
            for separator in separator_list:
                data = pd.read_csv(file_name, sep=separator, low_memory=False)
                data.columns = data.columns.str.strip()
                if data.shape[1] > 1:
                    return data
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {file_name}: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

def generate_sankey(data, city_origin, selected_specialties, cities, specialties):
    if not data.empty:
        node_labels = [cities[city_origin]]
        node_colors = ['rgba(0, 0, 255, 0.3)']  # Azul com 30% de transparência
        link_colors = []
        sources = []
        targets = []
        values = []

        specialty_start_index = len(node_labels)

        for spec in selected_specialties:
            node_labels.append(specialties[spec])
            node_colors.append('rgba(0, 255, 0, 0.3)')  # Verde com 30% de transparência

        destination_start_index = len(node_labels)

        possible_destinations = [code for code in cities if code != city_origin]
        for dest in possible_destinations:
            node_labels.append(cities[dest])
            node_colors.append('rgba(255, 0, 0, 0.3)')  # Vermelho com 30% de transparência

        for spec_index, spec in enumerate(selected_specialties, start=specialty_start_index):
            filtered_data = data[(data['munic_res'] == city_origin) & (data['espec'] == spec)]
            for dest in possible_destinations:
                dest_index = possible_destinations.index(dest) + destination_start_index
                count = filtered_data[filtered_data['munic_mov'] == dest].shape[0]
                if count > 0:
                    sources.extend([0, spec_index])
                    targets.extend([spec_index, dest_index])
                    values.extend([count, count])
                    link_colors.append('rgba(0, 0, 255, 0.3)')  # Azul para links da cidade
                    link_colors.append('rgba(0, 255, 0, 0.3)')  # Verde para links das especialidades

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_labels,
                color=node_colors
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=link_colors
            )
        )])

        # Configuração do layout com tamanho de fonte maior
        fig.update_layout(font=dict(size=20, color='black'))

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Os dados não estão disponíveis.")

def run():
    st.title("Gráfico de Fluxo de Pacientes por Especialidade e Período")

    cities = {
        353460: "Osvaldo Cruz",
        354140: "Presidente Prudente",
        352900: "Marília",
        350010: "Adamantina",
    }

    specialties = {
        1: "Ortopedia",
        2: "Neurologia",
        3: "Cardiologia",
        4: "Oftalmologia",
        5: "Pediatria",
        6: "Medicina do Trabalho",
        7: "Ortopedia e Traumalogia",
    }

    amb_data = load_data("ambulatorio.csv", [',', ';', '\t', ' '])
    int_data = load_data("internacao.csv", [',', ';', '\t', ' '])

    if not amb_data.empty and not int_data.empty:
        combined_data = pd.concat([amb_data, int_data], axis=1)

        city_origin = st.selectbox("Selecione a cidade de origem:", list(cities.keys()), format_func=lambda x: f"{cities[x]} ({x})", key='city_origin')
        selected_specialties = st.multiselect("Selecione as especialidades médicas:", list(specialties.keys()), format_func=lambda x: f"{specialties[x]}", key='specialties')

        # Caixa de seleção para escolher o ano, padrão para 2024
        year = st.selectbox("Selecione o ano:", range(2018, 2025), index=range(2018, 2025).index(2024))

        if 'city_origin' in st.session_state and 'specialties' in st.session_state and st.session_state.specialties:
            generate_sankey(combined_data, st.session_state.city_origin, st.session_state.specialties, cities, specialties)
