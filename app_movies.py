#Importando Bibliotecas
import streamlit as st
import pandas as pd

#Digite no terminal para executar o App -> streamlit run app_movies.py

#meu DataFrame

link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdcvSTtG8KKphzQ3h4i2Lyp8Osh0FLTqs59Sf4zhtSea9lmX7xm9-A1HPgsFnf77HabNfRwcyhEljU/pub?gid=0&single=true&output=csv"

df = pd.read_csv(link).drop(columns='Nota',axis=1)#Excluindo Coluna Nota

df_pais = df["Pais"].drop_duplicates()

#Definindo Layout Aplicação

#Definindo Configurações da Página
st.set_page_config(
    page_title="movies",
    page_icon=":film_projector:",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Layout Inicial
titulo = st.write("""# Filmes Recomendados :film_projector:""")#Titulo App
st.sidebar.write("""# Menu""")
st.sidebar.write('\n')
st.sidebar.write("""## Que tal aplicar alguns filtros ? para exibir alguns filmes para você! :smile:""")
st.sidebar.write('\n')

### Definindo Filtros - Selecao Multipla
filtro1 = st.sidebar.multiselect("# País", df_pais.sort_values())
filtro2 = st.sidebar.multiselect("# Avaliação", ["Excelente","Muito bom","Bom"])

#Multiplas Condições - # Usar .isin(passar as condições) - Construindo DataFrame
df1 = df[df['Pais'].isin(filtro1) & df['Avaliacao'].isin(filtro2)]
df2 = df[df['Avaliacao'].isin(filtro2)]#Condição de Multi - Filtro 2 - Avaliacao
df3 = df[df['Pais'].isin(filtro1)]#Condição de Multi - Filtro 3 - Pais

#Função para Baixar Arquivo
def convert_df(X):
    return X.to_csv(index=False, sep=';').encode('ISO-8859-1')#Elimina Index , Define Separador e Formato

#def convert_excel(X):
    #return X.to_excel(r"C:\Users\Ewerton\Downloads" + "\movies.xlsx",index=False)

#Exibir DataFrame de Acordo com os Filtros Aplicados:
if filtro1 and filtro2:
    csv = convert_df(df1)
    st.write('')
    st.write("### *Show, dá um olhada nos filmes que filtrei para você* :sunglasses:")
    bt = st.download_button("Press to Download",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download",convert_excel(df1))#Baixar em Excel
    st.write('')
    st.dataframe(df1.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    if bt:
        st.success('Arquivo baixado com sucesso!')


elif filtro2:
    csv = convert_df(df2)
    st.write('')
    st.write("### *Show, dá um olhada nos filmes que filtrei para você* :sunglasses:")
    bt = st.download_button("Press to Download",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download", convert_excel(df2))#Baixar em Excel
    st.write('')
    st.dataframe(df2.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    if bt:
        st.success('Arquivo baixado com sucesso!')


elif filtro1:
    csv = convert_df(df3)
    st.write('')
    st.write("### *Show, dá um olhada nos filmes que filtrei para você* :sunglasses:")
    bt = st.download_button("Press to Download",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download",convert_excel(df3))#Baixar em Excel
    st.write('')
    st.dataframe(df3.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    if bt:
        st.success('Arquivo baixado com sucesso!')

else:
    #Definindo Layout Aplicação
    st.write('\n')
    #st.warning(""" ### Que tal aplicar alguns filtros ? Que eu exibo alguns filmes para você! :smile: """)
    st.image('https://i2.wp.com/geekiegames.geekie.com.br/blog/wp-content/uploads/2018/07/gosto-filmes-profissao-1.png?fit=1097%2C630&',)
    st.write('\n')
    st.write("""### Gostaria de receber a lista com os filmes por e-mail ?:""")
    st.text_input('Insira seu e-mail')
    st.write('\n')
    st.write("""### Como você conheceu o recomendador ?:""")
    st.radio('', options=['Site','Instagram', 'Outros'])

