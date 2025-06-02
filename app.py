import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas 2024",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cores e estilo
colors = {
    "primary": "#1a76d2",
    "secondary": "#3c4b64",
    "success": "#4caf50",
    "info": "#00bcd4",
    "warning": "#ff9800",
    "danger": "#f44336",
    "light": "#f8f9fa",
    "dark": "#343a40",
    "background": "#ffffff",
    "text": "#212529"
}

# Função para carregar dados
@st.cache_data
def load_data():
    # Carregar dados processados com tratamento para espaços em branco
    df = pd.read_csv('Vendas2024_Processado.csv', skipinitialspace=True)
    
    # Limpar nomes das colunas (remover espaços extras)
    df.columns = [col.strip() for col in df.columns]
    
    # Renomear a coluna 'Data de Ganho' para 'Data' para compatibilidade
    if 'Data de Ganho' in df.columns:
        df = df.rename(columns={'Data de Ganho': 'Data'})
    
    # Renomear a coluna 'Valor USD Convertido' para 'Valor_USD' para compatibilidade
    if 'Valor USD Convertido' in df.columns:
        df = df.rename(columns={'Valor USD Convertido': 'Valor_USD'})
    
    # Converter data para datetime
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Carregar análises específicas
    vendas_mensais = pd.read_csv('analise_vendas_mensais.csv', skipinitialspace=True)
    vendas_mensais.columns = [col.strip() for col in vendas_mensais.columns]
    
    vendedores = pd.read_csv('analise_vendedores.csv', skipinitialspace=True)
    vendedores.columns = [col.strip() for col in vendedores.columns]
    
    vendedores_mensal = pd.read_csv('analise_vendedores_mensal.csv', skipinitialspace=True)
    vendedores_mensal.columns = [col.strip() for col in vendedores_mensal.columns]
    
    top10_clientes = pd.read_csv('analise_top10_clientes.csv', skipinitialspace=True)
    top10_clientes.columns = [col.strip() for col in top10_clientes.columns]
    
    comportamento_clientes = pd.read_csv('analise_comportamento_clientes.csv', skipinitialspace=True)
    comportamento_clientes.columns = [col.strip() for col in comportamento_clientes.columns]
    
    resumo_moedas = pd.read_csv('analise_resumo_moedas.csv', skipinitialspace=True)
    resumo_moedas.columns = [col.strip() for col in resumo_moedas.columns]
    
    return df, vendas_mensais, vendedores, vendedores_mensal, top10_clientes, comportamento_clientes, resumo_moedas

# Carregar dados
df, vendas_mensais, vendedores, vendedores_mensal, top10_clientes, comportamento_clientes, resumo_moedas = load_data()

# Título e descrição
st.title("Dashboard de Vendas 2024")
st.markdown("Análise detalhada das vendas de 2024, incluindo principais clientes, vendas mensais, métricas por vendedor e distribuição por moeda.")

# Sidebar com filtros
st.sidebar.title("Filtros")

# Filtro de data
min_date = df['Data'].min().date()
max_date = df['Data'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Período de Análise",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filtro de moeda
moedas = ['Todas'] + sorted(df['Moeda'].unique().tolist())
moeda_selecionada = st.sidebar.selectbox("Moeda", moedas)

# Filtro de vendedor
vendedores_lista = ['Todos'] + sorted(df['Vendedor'].unique().tolist())
vendedor_selecionado = st.sidebar.selectbox("Vendedor", vendedores_lista)

# Filtro de top 10 clientes
mostrar_top10 = st.sidebar.checkbox("Mostrar apenas Top 10 Clientes", value=False)

# Aplicar filtros aos dados
filtered_df = df.copy()

# Filtro de data
filtered_df = filtered_df[(filtered_df['Data'].dt.date >= start_date) & 
                          (filtered_df['Data'].dt.date <= end_date)]

# Filtro de moeda
if moeda_selecionada != 'Todas':
    filtered_df = filtered_df[filtered_df['Moeda'] == moeda_selecionada]

# Filtro de vendedor
if vendedor_selecionado != 'Todos':
    filtered_df = filtered_df[filtered_df['Vendedor'] == vendedor_selecionado]

# Calcular métricas principais
valor_total = filtered_df['Valor_USD'].sum()
total_projetos = len(filtered_df)
ticket_medio = valor_total / total_projetos if total_projetos > 0 else 0
clientes_unicos = filtered_df['Cliente'].nunique()

# Exibir métricas principais
st.header("Métricas Principais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Valor Total (USD)", f"${valor_total:,.2f}")

with col2:
    st.metric("Total de Projetos", f"{total_projetos}")

with col3:
    st.metric("Ticket Médio (USD)", f"${ticket_medio:,.2f}")

with col4:
    st.metric("Clientes Únicos", f"{clientes_unicos}")

# Análise de Vendas Mensais
st.header("Análise de Vendas Mensais")

# Preparar dados para gráficos mensais
monthly_data = filtered_df.groupby(filtered_df['Data'].dt.strftime('%Y-%m')).agg(
    Valor_Total=('Valor_USD', 'sum'),
    Num_Vendas=('Valor_USD', 'count')
).reset_index()
monthly_data['Data'] = pd.to_datetime(monthly_data['Data'] + '-01')
monthly_data = monthly_data.sort_values('Data')

# Adicionar valor acumulado
monthly_data['Valor_Acumulado'] = monthly_data['Valor_Total'].cumsum()

# Gráfico de vendas mensais
col1, col2 = st.columns(2)

with col1:
    fig_monthly = px.bar(
        monthly_data,
        x='Data',
        y='Valor_Total',
        title='Vendas Mensais (USD)',
        labels={'Data': 'Mês', 'Valor_Total': 'Valor Total (USD)'},
        color_discrete_sequence=[colors['primary']]
    )
    fig_monthly.update_layout(
        plot_bgcolor='white',
        xaxis_title='Mês',
        yaxis_title='Valor Total (USD)',
        xaxis=dict(tickformat='%b %Y')
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

with col2:
    fig_accumulated = px.line(
        monthly_data,
        x='Data',
        y='Valor_Acumulado',
        title='Vendas Acumuladas (USD)',
        labels={'Data': 'Mês', 'Valor_Acumulado': 'Valor Acumulado (USD)'},
        color_discrete_sequence=[colors['success']]
    )
    fig_accumulated.update_layout(
        plot_bgcolor='white',
        xaxis_title='Mês',
        yaxis_title='Valor Acumulado (USD)',
        xaxis=dict(tickformat='%b %Y')
    )
    st.plotly_chart(fig_accumulated, use_container_width=True)

# Gráfico de número de vendas por mês
fig_num_sales = px.bar(
    monthly_data,
    x='Data',
    y='Num_Vendas',
    title='Número de Vendas por Mês',
    labels={'Data': 'Mês', 'Num_Vendas': 'Número de Vendas'},
    color_discrete_sequence=[colors['info']]
)
fig_num_sales.update_layout(
    plot_bgcolor='white',
    xaxis_title='Mês',
    yaxis_title='Número de Vendas',
    xaxis=dict(tickformat='%b %Y')
)
st.plotly_chart(fig_num_sales, use_container_width=True)

# Análise de Clientes
st.header("Análise de Clientes")

# Preparar dados para gráfico de principais clientes
top_clients = filtered_df.groupby('Cliente').agg(
    Valor_Total=('Valor_USD', 'sum')
).reset_index().sort_values('Valor_Total', ascending=False)

if mostrar_top10:
    top_clients = top_clients.head(10)
else:
    top_clients = top_clients.head(15)

# Gráfico de principais clientes
fig_top_clients = px.bar(
    top_clients,
    x='Cliente',
    y='Valor_Total',
    title=f"{'10' if mostrar_top10 else '15'} Principais Clientes por Valor Total (USD)",
    labels={'Cliente': 'Cliente', 'Valor_Total': 'Valor Total (USD)'},
    color='Valor_Total',
    color_continuous_scale=px.colors.sequential.Blues
)
fig_top_clients.update_layout(
    plot_bgcolor='white',
    xaxis_title='Cliente',
    yaxis_title='Valor Total (USD)',
    coloraxis_showscale=False
)
st.plotly_chart(fig_top_clients, use_container_width=True)

# Comparação de vendas por semestre - Top 10 clientes
if not top10_clientes.empty:
    st.subheader("Comparação de Vendas por Semestre - Top 10 Clientes")
    
    # Filtrar top10_clientes com base nos filtros aplicados
    filtered_top10 = top10_clientes.copy()
    
    if moeda_selecionada != 'Todas':
        # Não podemos filtrar por moeda aqui pois os dados já estão agregados
        st.info("Nota: A comparação semestral mostra dados convertidos para USD independente do filtro de moeda.")
    
    if vendedor_selecionado != 'Todos':
        st.info("Nota: A comparação semestral mostra dados de todos os vendedores para os top 10 clientes.")
    
    # Criar gráfico de comparação semestral
    fig_semester = go.Figure()
    
    fig_semester.add_trace(go.Bar(
        x=filtered_top10['Cliente'],
        y=filtered_top10['Valor_S1_USD'],
        name='Jan-Jun 2024',
        marker_color=colors['primary']
    ))
    
    fig_semester.add_trace(go.Bar(
        x=filtered_top10['Cliente'],
        y=filtered_top10['Valor_S2_USD'],
        name='Jul-Dez 2024',
        marker_color=colors['info']
    ))
    
    fig_semester.update_layout(
        title='Comparação de Vendas por Semestre - Top 10 Clientes',
        xaxis_title='Cliente',
        yaxis_title='Valor Total (USD)',
        barmode='group',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig_semester, use_container_width=True)

# Análise de Vendedores
st.header("Análise de Vendedores")

# Filtrar dados de vendedores
filtered_vendedores = vendedores.copy()

if moeda_selecionada != 'Todas':
    st.info("Nota: A análise de vendedores mostra dados convertidos para USD independente do filtro de moeda.")

# Gráficos de vendedores
col1, col2 = st.columns(2)

with col1:
    fig_vendedores_valor = px.bar(
        filtered_vendedores,
        x='Vendedor',
        y='Valor_Total_USD',
        title='Valor Total por Vendedor (USD)',
        labels={'Vendedor': 'Vendedor', 'Valor_Total_USD': 'Valor Total (USD)'},
        color='Valor_Total_USD',
        color_continuous_scale=px.colors.sequential.Greens
    )
    fig_vendedores_valor.update_layout(
        plot_bgcolor='white',
        xaxis_title='Vendedor',
        yaxis_title='Valor Total (USD)',
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_vendedores_valor, use_container_width=True)

with col2:
    fig_vendedores_ticket = px.bar(
        filtered_vendedores,
        x='Vendedor',
        y='Ticket_Medio_USD',
        title='Ticket Médio por Vendedor (USD)',
        labels={'Vendedor': 'Vendedor', 'Ticket_Medio_USD': 'Ticket Médio (USD)'},
        color='Ticket_Medio_USD',
        color_continuous_scale=px.colors.sequential.Oranges
    )
    fig_vendedores_ticket.update_layout(
        plot_bgcolor='white',
        xaxis_title='Vendedor',
        yaxis_title='Ticket Médio (USD)',
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_vendedores_ticket, use_container_width=True)

# Análise por Moeda
st.header("Análise por Moeda")

# Filtrar dados de resumo de moedas
filtered_moedas = resumo_moedas.copy()

# Gráficos de moedas
col1, col2 = st.columns(2)

with col1:
    fig_moedas_valor = px.pie(
        filtered_moedas,
        values='Valor_Total_USD',
        names='Moeda',
        title='Distribuição do Valor Total por Moeda (USD)',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_moedas_valor.update_layout(
        plot_bgcolor='white'
    )
    st.plotly_chart(fig_moedas_valor, use_container_width=True)

with col2:
    fig_moedas_projetos = px.pie(
        filtered_moedas,
        values='Num_Projetos',
        names='Moeda',
        title='Distribuição do Número de Projetos por Moeda',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_moedas_projetos.update_layout(
        plot_bgcolor='white'
    )
    st.plotly_chart(fig_moedas_projetos, use_container_width=True)

# Tabela de resumo de moedas
st.subheader("Resumo por Moeda")
st.dataframe(
    filtered_moedas[['Moeda', 'Valor_Total_USD', 'Percentual', 'Num_Projetos']].rename(
        columns={
            'Valor_Total_USD': 'Valor Total (USD)',
            'Percentual': 'Percentual (%)',
            'Num_Projetos': 'Número de Projetos'
        }
    ).style.format({
        'Valor Total (USD)': '${:,.2f}',
        'Percentual (%)': '{:.2f}%'
    }),
    use_container_width=True
)

# Insights Detalhados por Cliente
st.header("Insights Detalhados por Cliente")

# Converter todos os clientes para string para evitar problemas de tipo
comportamento_clientes['Cliente'] = comportamento_clientes['Cliente'].astype(str)

# Filtrar clientes não vazios
clientes_validos = comportamento_clientes[comportamento_clientes['Cliente'].notna() & (comportamento_clientes['Cliente'] != '')]['Cliente'].unique().tolist()

# Selecionar cliente para análise detalhada
cliente_selecionado = st.selectbox("Selecione um cliente para análise detalhada", clientes_validos)

# Filtrar dados do cliente selecionado
cliente_data = comportamento_clientes[comportamento_clientes['Cliente'] == cliente_selecionado].iloc[0]

# Exibir insights do cliente
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Valor Total (USD)", f"${cliente_data['Valor_Total_USD']:,.2f}")
    st.metric("Número de Projetos", f"{cliente_data['Num_Projetos']}")

with col2:
    st.metric("Ticket Médio (USD)", f"${cliente_data['Ticket_Medio_USD']:,.2f}")
    st.metric("Primeira Compra", f"{pd.to_datetime(cliente_data['Primeira_Compra']).strftime('%d/%m/%Y')}")

with col3:
    st.metric("Recorrência (dias)", f"{cliente_data['Recorrencia_Media_Dias']:.1f}")
    st.metric("Última Compra", f"{pd.to_datetime(cliente_data['Ultima_Compra']).strftime('%d/%m/%Y')}")

# Gráfico de compras do cliente ao longo do tempo
cliente_timeline = filtered_df[filtered_df['Cliente'] == cliente_selecionado].copy()
cliente_timeline = cliente_timeline.sort_values('Data')

if not cliente_timeline.empty:
    fig_cliente_timeline = px.scatter(
        cliente_timeline,
        x='Data',
        y='Valor_USD',
        size='Valor_USD',
        title=f'Compras de {cliente_selecionado} ao Longo do Tempo',
        labels={'Data': 'Data', 'Valor_USD': 'Valor (USD)'},
        color_discrete_sequence=[colors['primary']]
    )
    fig_cliente_timeline.update_layout(
        plot_bgcolor='white',
        xaxis_title='Data',
        yaxis_title='Valor (USD)'
    )
    st.plotly_chart(fig_cliente_timeline, use_container_width=True)
else:
    st.info(f"Não há dados disponíveis para {cliente_selecionado} no período selecionado.")

# Rodapé
st.markdown("---")
st.markdown("Dashboard de Vendas 2024 | Desenvolvido com Streamlit")
