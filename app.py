import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Scanner de Ações Pro", layout="wide")

st.title("📊 Dashboard de Análise Fundamentalista")
st.markdown("Faça o upload da sua planilha e ajuste os filtros na barra lateral.")

# --- BARRA LATERAL (FILTROS INTERATIVOS) ---
st.sidebar.header("Configuração dos Filtros")

# Criando os componentes de ajuste
f_pl_max = st.sidebar.number_input("P/L Máximo", value=15.0)
f_roic_min = st.sidebar.number_input("ROIC Mínimo (%)", value=10.0)
f_roe_min = st.sidebar.number_input("ROE Mínimo (%)", value=10.0)
f_liq_min = st.sidebar.number_input("Liquidez 2m Mínima (R$)", value=500000000.0, step=10000000.0)
f_div_max = st.sidebar.slider("Dív. Bruta/Patrimônio Máxima", 0.0, 5.0, 1.0)
f_cresc_min = st.sidebar.number_input("Crescimento Rec. 5a Mín (%)", value=1.0)
f_cresc_max = st.sidebar.number_input("Crescimento Rec. 5a Máx (%)", value=20.0)
f_graham_max = st.sidebar.number_input("P/L * P/VP Máximo (Graham)", value=22.5)

# --- UPLOAD E LÓGICA ---
uploaded_file = st.file_uploader("Arraste seu arquivo Excel aqui", type=['xlsx', 'csv'])

if uploaded_file:
    # Carregar dados
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    
    # Limpeza de nomes de colunas
    df.columns = df.columns.str.strip()

    try:
        # Cálculo do indicador de Graham antecipado para filtragem
        df['Graham_Index'] = df['P/L'] * df['P/VP']

        # Aplicação dos Filtros Dinâmicos
        filtro = (
            (df['P/L'] > 0) & (df['P/L'] <= f_pl_max) &
            (df['ROIC'] >= f_roic_min) &
            (df['ROE'] >= f_roe_min) &
            (df['Liq.2meses'] >= f_liq_min) &
            (df['Div.Brut/Patrim'] >= 0) & (df['Div.Brut/Patrim'] <= f_div_max) &
            (df['Cresc.Rec.5a'] >= f_cresc_min) & (df['Cresc.Rec.5a'] <= f_cresc_max) &
            (df['Graham_Index'] < f_graham_max)
        )

        df_final = df[filtro]

        # Exibição
        st.subheader(f"🔍 Resultados: {len(df_final)} ações encontradas")
        st.dataframe(df_final.style.format(precision=2), use_container_width=True)

        # Download do resultado
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Tabela Filtrada", csv, "analise_acoes.csv", "text/csv")

    except Exception as e:
        st.error(f"Erro ao processar colunas. Verifique se os nomes no Excel estão corretos: {e}")
