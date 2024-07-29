import streamlit as st
import pandas as pd
import plotly.express as px


def load_data(file_names, separator_list):
    data_frames = []
    for file_name in file_names:
        try:
            for separator in separator_list:
                temp_data = pd.read_csv(file_name, sep=separator, low_memory=False)
                temp_data.columns = temp_data.columns.str.strip()
                if temp_data.shape[1] > 1:
                    data_frames.append(temp_data)
                    break
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {file_name}: {e}")
            return pd.DataFrame()
    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        return pd.DataFrame()


def calculate_average_cost(data, selected_city, selected_specialities, specialties_dict):
    if not data.empty:
        filtered_data = data[(data['munic_mov'] == selected_city) & (data['espec'].isin(selected_specialities))]
        if not filtered_data.empty:
            result = filtered_data.groupby('espec').agg({'val_tot': 'sum'})
            result.columns = ['Total Cost']
            result = result.reset_index()
            result['espec'] = result['espec'].map(specialties_dict)
            result = result[['espec', 'Total Cost']]
            result.rename(columns={'espec': 'Especialidade', 'Total Cost': 'Custo Total'}, inplace=True)
            return result
    return pd.DataFrame()


def display_cost_chart(df):
    if not df.empty:
        fig = px.bar(df, x='Especialidade', y='Custo Total', title="Custo Total por Especialidade")
        st.plotly_chart(fig)
    else:
        st.write("Nenhum dado disponível para mostrar.")


def run():
    st.title('Análise de Custo Total por Especialidade')

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

    selected_city = st.selectbox("Selecione a cidade:", options=list(cities.keys()), format_func=lambda x: cities[x])
    selected_specialities = st.multiselect("Selecione as especialidades:", options=list(specialties.keys()),
                                           format_func=lambda x: specialties[x])

    if st.button('Calcular e Exibir Custo Total'):
        with st.spinner('Carregando dados do DATASUS...'):
            data = load_data(["ambulatorio.csv", "internacao.csv"], [',', ';', '\t', ' '])
            if not data.empty:
                total_cost_df = calculate_average_cost(data, selected_city, selected_specialities, specialties)
                display_cost_chart(total_cost_df)


if __name__ == "__main__":
    run()
