import pandas as pd
import streamlit as st

st.set_page_config(layout='wide')

st.header('Netflix')
# Le o arquivo CSV em um DataFrame
netflix_base_dataframe = pd.read_csv(r'C:\Users\Dell\Desktop\datasets\netflix\netflix_titles.csv')

# Converte 'date_added' para formato datetime
netflix_base_dataframe['date_added'] = pd.to_datetime(netflix_base_dataframe['date_added'], errors='coerce')

# Extrai apenas o ano de 'date_added'
netflix_base_dataframe['year_added'] = netflix_base_dataframe['date_added'].dt.year

# Remove valores NaN e converter para int
netflix_base_dataframe = netflix_base_dataframe.dropna(subset=['year_added'])
netflix_base_dataframe['year_added'] = netflix_base_dataframe['year_added'].astype(int)

# Cria um selectbox no sidebar com anos únicos
anos_unicos = sorted(netflix_base_dataframe['year_added'].unique())
ano_selecionado = st.sidebar.selectbox('Ano', anos_unicos)

# Mostra o DataFrame filtrado pelo ano selecionado quando o botão for clicado
filtered_df_year = netflix_base_dataframe[netflix_base_dataframe['year_added'] == ano_selecionado]

if 'button_df_toggle_df' not in st.session_state:
    st.session_state.button_df_toggle_df = False

    # Botão de exibição do DataFrame
if st.sidebar.button(label='Mostrar/baixar Dataframe', key='show_df'):
    st.session_state.button_df_toggle_df = not st.session_state.button_df_toggle_df

if st.session_state.button_df_toggle_df:
    filtered_df_year = netflix_base_dataframe[netflix_base_dataframe['year_added'] == ano_selecionado]

    st.subheader('Dataframe completo:')
    st.dataframe(netflix_base_dataframe)

    st.subheader('Dataframe filtrado usado no momento:')
    st.dataframe(filtered_df_year)

    # Convertendo DataFrame filtrado para CSV
    csv = filtered_df_year.to_csv(index=False).encode('utf-8')

    st.download_button(
        label='Baixar DF filtrado',
        data=csv,
        file_name='Dataframe_filtrado_por_ano.csv',
        mime='text/csv',
    )


#graficos de filmes lancados no ano:

if ano_selecionado:
    st.subheader('Títulos por ano')
    st.text('Disponibilizando títulos, direção e ano de lançamento')
    col1, col2, col3 = st.columns(3)
    for title, cast, direc, re_year in zip(filtered_df_year['title'].values, filtered_df_year['cast'].values,
                           filtered_df_year['director'].values, filtered_df_year['release_year'].values):
        col1.write(title[:40])
        col2.write(direc[:40] if pd.notna(direc) else 'Não informado')
        col3.write(re_year if pd.notna(re_year) else 'Não informado')










