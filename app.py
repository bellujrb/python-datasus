import streamlit as st

import cost_analysis
import flow_analysis
import flow_analysis


def main():
    st.title('Sistema DataSUS')

    st.write("""
    Bem-vindo ao Sistema de DataSUS! Este sistema permite:
    - Visualizar e analisar dados de fluxo de pacientes entre cidades.
    - Auxiliar na tomada de decisões
    """)

    PAGES_INDIVIDUAL = {
        "Análise de Fluxo": flow_analysis,
        "Analise de Custo": cost_analysis,
    }

    st.sidebar.title('Navegação')

    selection = st.sidebar.radio("Ir para", list(PAGES_INDIVIDUAL.keys()), key='page')

    page = PAGES_INDIVIDUAL[selection]
    page.run()


if __name__ == "__main__":
    main()
