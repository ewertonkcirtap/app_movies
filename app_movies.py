#Importando Bibliotecas
import streamlit as st
import pandas as pd
import requests

#Digite no terminal para executar o App -> streamlit run app_movies.py

#Extraindo DF
link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdcvSTtG8KKphzQ3h4i2Lyp8Osh0FLTqs59Sf4zhtSea9lmX7xm9-A1HPgsFnf77HabNfRwcyhEljU/pub?gid=0&single=true&output=csv"
df = pd.read_csv(link).drop(columns='Nota',axis=1)#Excluindo Coluna Nota
df_pais = df["Pais"].drop_duplicates()

#Definindo Configurações da Página
st.set_page_config(
    page_title="movies",
    page_icon=":film_projector:",
    layout="centered",
    initial_sidebar_state="auto",
)


#Layout Inicial
st.sidebar.text("""@ewertonkcirtap""")
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write("""## Que tal aplicar alguns filtros ? para exibir alguns filmes para você :smile:""")
st.sidebar.write('\n')

### Definindo Filtros - Selecao Multipla
filtro1 = st.sidebar.multiselect("# País", df_pais.sort_values())
filtro2 = st.sidebar.multiselect("# Avaliação", ["Excelente", "Muito bom", "Bom"])
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')

### Buscar por filme - IMDB
st.sidebar.write("""## Você pode pesquisar por qualquer filme aqui :mag_right:""")
filme = st.sidebar.text_input('Insira o nome do filme')

#Multiplas Condições - # Usar .isin(passar as condições) - Construindo DataFrame
df1 = df[df['Pais'].isin(filtro1) & df['Avaliacao'].isin(filtro2)]
df2 = df[df['Avaliacao'].isin(filtro2)]#Condição de Multi - Filtro 2 - Avaliacao
df3 = df[df['Pais'].isin(filtro1)]#Condição de Multi - Filtro 3 - Pais

#Função para Baixar Arquivo
def convert_df(X):
    return X.to_csv(index=False, sep=';').encode('ISO-8859-1')#Elimina Index , Define Separador e Formato

def imdb(f, u):
    querystring = {"q": f}
    res = requests.request("GET", u, headers={'x-rapidapi-host': "imdb8.p.rapidapi.com",'x-rapidapi-key': "548693870emsh0e8d67709883f02p1516cfjsnf1a57f1225f7"}, params=querystring)
    res = res.json()
    return res

def rating(x,url="https://imdb8.p.rapidapi.com/title/get-ratings"):
    querystring = {"tconst": x}
    res = requests.request("GET", url, headers={'x-rapidapi-host': "imdb8.p.rapidapi.com",'x-rapidapi-key': "548693870emsh0e8d67709883f02p1516cfjsnf1a57f1225f7"},params=querystring)
    res = res.json()
    return res['rating']

#Exibir DataFrame de Acordo com os Filtros Aplicados:

if filtro1 and filtro2 and filme =="":
    csv = convert_df(df1)
    st.write('')
    st.write("### *Show, dá um olhada nos filmes que filtrei para você* :sunglasses:")
    bt = st.download_button("Press to Download",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download",convert_excel(df1))#Baixar em Excel
    st.write('')
    #st.dataframe(df1.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    st.table(df1.sort_values(by=['Filme']).reset_index(drop=True))
    if bt:
        st.success('Arquivo baixado com sucesso!')

elif filtro2 and filme =="":
    csv = convert_df(df2)
    st.write('')
    st.write("### *Show, dá um olhada nos filmes que filtrei para você* :sunglasses:")
    bt = st.download_button("Press to Download",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download", convert_excel(df2))#Baixar em Excel
    st.write('')
    #st.dataframe(df2.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    st.table(df2.sort_values(by=['Filme']).reset_index(drop=True))
    if bt:
        st.success('Arquivo baixado com sucesso!')

elif filtro1 and filme =="":
    csv = convert_df(df3)
    st.write('')
    st.write("### *Show, dá um olhada nos filmes que filtrei para você* :sunglasses:")
    bt = st.download_button("Press to Download",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download",convert_excel(df3))#Baixar em Excel
    st.write('')
    #st.dataframe(df3.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    st.table(df3.sort_values(by=['Filme']).reset_index(drop=True))
    if bt:
        st.success('Arquivo baixado com sucesso!')

elif filme:
    #if filme or filtro1 or filtro2:
        #st.write("""# Olha o que eu encontrei sobre a sua pesquisa""")
        filme = imdb(f=filme,u="https://imdb8.p.rapidapi.com/auto-complete")

        id = filme['d'][0]['id']
        nomefilme = filme['d'][0]['l']
        anofilme = filme['d'][0]['y']
        nota = rating(id)

        info = "https://www.imdb.com/title/" + id

        st.image(filme['d'][0]['i']['imageUrl'])
        st.write('\n')
        st.write("Filme: " + str(nomefilme))
        st.write("Nota Imdb: " + str(nota))
        st.write("Ano: " + str (anofilme))
        st.write(f"Mais informações : [Saiba mais]({info})")

### Layout Tela Inicial
else:
    st.write('\n')
    st.write("""### Vou te recomendar alguns filmes :film_projector:""")  # Titulo App
    st.write('\n')
    st.image('https://i2.wp.com/geekiegames.geekie.com.br/blog/wp-content/uploads/2018/07/gosto-filmes-profissao-1.png?fit=1097%2C630&')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    check = st.multiselect("Como você conheceu essa aplicação ? ", ["Instagram","Linkedin","Google","Outros"])

    if check:
        with st.form("my_form"):
            st.write("Para registrar seu voto vou precisar que preencha os dados abaixo, tudo bem ?")
            nome =  st.text_input("Nome")
            email = st.text_input("E-mail")
            submitted = st.form_submit_button("Confirmar")

        if submitted:
            sucesso = st.success("Obrigado!")
            check = st.empty()
