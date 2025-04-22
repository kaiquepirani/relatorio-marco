
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Etco Tur - Março 2025", page_icon="🚌", layout="wide")

st.image("logo.png", width=250)
st.title("Etco Tur - Viagens Março 2025")

uploaded_file = st.file_uploader("Carregar novo relatório Excel", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    st.warning("Por favor, carregue um arquivo Excel.")

if uploaded_file:
    st.sidebar.header("Filtros")
    motoristas = sorted(df["Motorista"].unique())
    prefixos = sorted(df["Prefixo"].unique())
    destinos = sorted(df["Destino"].unique())
    setores = sorted(df["Setor"].unique())

    sel_motoristas = st.sidebar.multiselect("Motoristas", motoristas, default=motoristas)
    sel_prefixos = st.sidebar.multiselect("Prefixos", prefixos, default=prefixos)
    sel_destinos = st.sidebar.multiselect("Destinos", destinos, default=destinos)
    sel_setores = st.sidebar.multiselect("Setores", setores, default=setores)

    df_filtered = df[
        (df["Motorista"].isin(sel_motoristas)) &
        (df["Prefixo"].isin(sel_prefixos)) &
        (df["Destino"].isin(sel_destinos)) &
        (df["Setor"].isin(sel_setores))
    ]

    total_km = df_filtered["KM"].sum()
    total_viagens = len(df_filtered)
    total_custo = df_filtered["Combustível"].sum() + df_filtered["Pedágio"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total KM", f"{total_km:.0f} km")
    col2.metric("Total Viagens", total_viagens)
    col3.metric("Custo Total", f"R${total_custo:.2f}")

    st.subheader("Gráfico de Viagens por Motorista")
    viagens_motorista = df_filtered.groupby("Motorista")["KM"].count().reset_index()
    fig = px.bar(viagens_motorista, x="Motorista", y="KM", title="Viagens por Motorista")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Tabela de Viagens")
    st.dataframe(df_filtered)
