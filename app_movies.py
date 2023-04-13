#Importando Bibliotecas
import streamlit as st
import pandas as pd
import requests

#Digite no terminal para executar o App -> streamlit run app_movies.py

#Extraindo DF
link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdcvSTtG8KKphzQ3h4i2Lyp8Osh0FLTqs59Sf4zhtSea9lmX7xm9-A1HPgsFnf77HabNfRwcyhEljU/pub?gid=0&single=true&output=csv"
df = pd.read_csv(link).drop(columns=['Nota','Avaliacao'],axis=1)#Excluindo Colunas
df = df.fillna("") # Ajustando vazios

df_pais = df["Pais"].drop_duplicates()
df_genero = df["Genero"].drop_duplicates()



#Definindo Configurações da Página
st.set_page_config(
    page_title="movies",
    page_icon=":film_projector:",
    layout="wide", #centered
    initial_sidebar_state="expanded",
)


#Layout Inicial
st.sidebar.text("""@ewertonkcirtap""")
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write("""## Que tal aplicar alguns filtros para sugerir filmes à você.""")
st.sidebar.write('\n')

### Definindo Filtros - Selecao Multipla

#filtro2 = st.sidebar.multiselect("# Avaliação", ["Excelente", "Muito bom", "Bom"]) - removido na atualiação 12.04
filtro1 = st.sidebar.multiselect("# País", df_pais.sort_values())
filtro3 = st.sidebar.multiselect("# Gênero", df_genero.sort_values())# Genero
filtro2 = st.sidebar.slider("# Mínimo IMDb Rating ",0.0, 10.0)


st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('\n')

### Buscar por filme - IMDB
st.sidebar.write("""## Você pode pesquisar por qualquer filme aqui :mag_right:""")
filme = st.sidebar.text_input('Insira o nome do filme')

#Multiplas Condições - # Usar .isin(passar as condições) - Construindo DataFrame

#df1 = df[df['Pais'].isin(filtro1) & df['Avaliacao'].isin(filtro2)] - removido na atualiação 12.04
#df2 = df[df['Avaliacao'].isin(filtro2)]#Condição de Multi - Filtro 2 - removido na atualiação 12.04

df1 = (df[(df['IMDb Rating']>=filtro2)  & df['Pais'].isin(filtro1)])
df2 = df[df['IMDb Rating']>=(filtro2)]#Condição de Multi - Filtro 2 - Imdb Rating
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
    st.write(f"### *Dá um olhada nos {len(df1)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download",convert_excel(df1))#Baixar em Excel
    st.write('')
    #st.dataframe(df1.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    #st.table(df1.sort_values(by=['IMDb Rating'],ascending=False).reset_index(drop=True))
    
    df1 = df1.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df1.index = df1.index+1
    st.table(df1)
    
    if bt:
        st.success('Arquivo baixado com sucesso!')

elif filtro2 and filme =="":
    csv = convert_df(df2)
    st.write('')
    st.write(f"### *Dá um olhada nos {len(df2)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download", convert_excel(df2))#Baixar em Excel
    st.write('')
    #st.dataframe(df2.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    #st.table(df2.sort_values(by=['IMDb Rating'],ascending=False).reset_index(drop=True))
    df2 = df2.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df2.index = df2.index+1
    st.table(df2)
    
    if bt:
        st.success('Arquivo baixado com sucesso!')

elif filtro1 and filme =="":
    csv = convert_df(df3)
    st.write('')
    st.write(f"### *Dá um olhada nos {len(df3)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista",csv,file_name='filmes_recomendados.csv')
    #st.download_button("Press to Download",convert_excel(df3))#Baixar em Excel
    st.write('')
    #st.dataframe(df3.sort_values(by=['Filme']).reset_index(drop=True), width=2800, height=400)
    #st.table(df3.sort_values(by=['IMDb Rating'],ascending=False).reset_index(drop=True))
    
    df3 = df3.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df3.index = df3.index+1
    st.table(df3)
    
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
    #st.write("""### Vou te recomendar alguns filmes :film_projector:""")  # Titulo App
    st.write('\n')
    #st.image('https://pipocanamadrugada.com.br/site/wp-content/uploads/2016/09/melhores-filmes_pipoca-na-madrugada-.jpg')#Foto de capa
    st.image('https://3.bp.blogspot.com/-tvtI9qdqqqA/Wk66fQLJcQI/AAAAAAAAE6U/TOjlrtn3Bgkf3zzovLWKyaX6HnyY5-_CQCLcBGAs/s1600/melhores%2Bfilmes%2Bde%2B2017.jpg')#Foto de capa
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
