# Importando Bibliotecas
import streamlit as st
import pandas as pd
import requests

# Digite no terminal para executar o App -> streamlit run app_movies.py
link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdcvSTtG8KKphzQ3h4i2Lyp8Osh0FLTqs59Sf4zhtSea9lmX7xm9-A1HPgsFnf77HabNfRwcyhEljU/pub?gid=0&single=true&output=csv"
df = pd.read_csv(link).drop(columns=['Nota', 'Avaliacao'], axis=1)  # Excluindo Colunas
df = df.fillna("")  # Ajustando vazios

df_pais = df["Pais"].drop_duplicates() # Lista de Países
df_genero = df["Genero"].drop_duplicates() # Lista de Gêneros

# Definindo Configurações da Página
st.set_page_config(
    page_title="movies",
    page_icon=":film_projector:",
    layout="wide",  # centered
    initial_sidebar_state="expanded",
)

# Layout
st.sidebar.write('\n')
st.sidebar.write("""## Que tal aplicar alguns filtros ? """)
st.sidebar.write('\n')

### Definindo Filtros - Selecao Multipla
filtro1 = st.sidebar.multiselect("# País", df_pais.sort_values()) # País
filtro2 = st.sidebar.multiselect("# Gênero", df_genero.sort_values())  # Gênero
filtro3 = st.sidebar.slider("# Mínimo IMDb Rating ", 0.0, 10.0) # Rating
#filtro2 = st.sidebar.multiselect("# Avaliação", ["Excelente", "Muito bom", "Bom"]) - Removido na Atualiação 12.04

st.sidebar.write('\n')
st.sidebar.write('\n')

### Buscar por filme - IMDB
st.sidebar.write("""## Você pode pesquisar por qualquer filme aqui :mag_right:""")
filme = st.sidebar.text_input('Insira o nome do filme')
st.sidebar.write('\n')
st.sidebar.write('\n')
st.sidebar.write('## Contatos')
st.sidebar.write(":man-pouting: Linkedin : [link](https://www.linkedin.com/in/ewerton-nascimento-46aa0a100/)")
st.sidebar.write(":cloud: Repo : [link](https://github.com/ewertonkcirtap/app_movies)")

# Funções
def convert_df(X):
    return X.to_csv(index=False, sep=';').encode('ISO-8859-1')  # Elimina Index , Define Separador e Formato

def imdb(f, u):
    querystring = {"q": f}
    res = requests.request("GET", u, headers={'x-rapidapi-host': "imdb8.p.rapidapi.com",
                                              'x-rapidapi-key': "548693870emsh0e8d67709883f02p1516cfjsnf1a57f1225f7"},
                           params=querystring)
    res = res.json()
    return res

def rating(x, url="https://imdb8.p.rapidapi.com/title/get-ratings"):
    querystring = {"tconst": x}
    res = requests.request("GET", url, headers={'x-rapidapi-host': "imdb8.p.rapidapi.com",
                                                'x-rapidapi-key': "548693870emsh0e8d67709883f02p1516cfjsnf1a57f1225f7"},
                           params=querystring)
    res = res.json()
    return res['rating']


# Exibir DataFrame de Acordo com os Filtros Aplicados:
# Filtro : Pais, Gênero e Rating
if filtro1 and filtro2 and filtro3 and filme == "":
    df1 = (df[(df['IMDb Rating'] >= filtro3) & df['Pais'].isin(filtro1) & df['Genero'].isin(filtro2)])
    csv = convert_df(df1)
    st.write('')
    st.write(f"### *Dá um olhada nos {len(df1)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista", csv, file_name='filmes_recomendados.csv')
    st.write('')
    df1 = df1.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df1.index = df1.index + 1
    st.table(df1)
 
    if bt:
        st.success('Arquivo baixado com sucesso!')

# Filtro : Pais e Rating
elif filtro1 and filtro3 and filme == "":
    df2 = (df[(df['IMDb Rating'] >= filtro3) & df['Pais'].isin(filtro1)])
    csv = convert_df(df2)
    st.write('')
    st.write(f"### *Dá um olhada nos {len(df2)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista", csv, file_name='filmes_recomendados.csv')
    st.write('')
    df2 = df2.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df2.index = df2.index + 1
    st.table(df2)

    if bt:
        st.success('Arquivo baixado com sucesso!')

# Filtro : Rating e Gênero
elif filtro3 and filtro2 and filme == "":
    df7 = (df[(df['IMDb Rating'] >= filtro3) & df['Genero'].isin(filtro2)])
    csv = convert_df(df7)
    st.write('')
    st.write(f"### *Dá um olhada nos {len(df7)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista", csv, file_name='filmes_recomendados.csv')
    st.write('')
    df7 = df7.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df7.index = df7.index + 1
    st.table(df7)
    
    if bt:
        st.success('Arquivo baixado com sucesso!')

# Filtro : Pais e Gênero
elif filtro1 and filtro2 and filme == "":
    df3 = (df[(df['Genero'].isin(filtro2)) & df['Pais'].isin(filtro1)])  #
    csv = convert_df(df3)
    st.write('')
    st.write(f"### *Dá um olhada nos {len(df3)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista", csv, file_name='filmes_recomendados.csv')
    st.write('')
    df3 = df3.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df3.index = df3.index + 1
    st.table(df3)
    
    if bt:
        st.success('Arquivo baixado com sucesso!')

# Filtro : Rating
elif filtro3 and filme == "":
    df4 = df[df['IMDb Rating'] >= (filtro3)]
    csv = convert_df(df4)
    st.write('')
    st.write(f"### *Dá um olhada nos {len(df4)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista", csv, file_name='filmes_recomendados.csv')
    st.write('')
    df4 = df4.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df4.index = df4.index + 1
    st.table(df4)
    
    if bt:
        st.success('Arquivo baixado com sucesso!')

# Filtro : Pais
elif filtro1 and filme == "":
    df5 = df[df['Pais'].isin(filtro1)]
    csv = convert_df(df5)
    st.write('')
    st.write(f"### *Dá um olhada nos {len(df5)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista", csv, file_name='filmes_recomendados.csv')
    st.write('')
    df5 = df5.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df5.index = df5.index + 1
    st.table(df5)
    
    if bt:
        st.success('Arquivo baixado com sucesso!')

# Filtro Gênero
elif filtro2 and filme == "":
    df6 = df[df['Genero'].isin(filtro2)]
    csv = convert_df(df6)
    st.write('')
    st.write(
        f"### *Dá um olhada nos {len(df6)} filmes que filtrei para você de acordo com a classificação do IMDb * :film_projector:")
    bt = st.download_button("Download lista", csv, file_name='filmes_recomendados.csv')
    st.write('')
    df6 = df6.sort_values(by=['IMDb Rating'], ascending=False).reset_index(drop=True)
    df6.index = df6.index + 1
    st.table(df6)
    
    if bt:
        st.success('Arquivo baixado com sucesso!')


# Pesquisando filme
elif filme:

    # st.write("""# Olha o que eu encontrei sobre a sua pesquisa""")
    filme = imdb(f=filme, u="https://imdb8.p.rapidapi.com/auto-complete")

    id = filme['d'][0]['id']
    nomefilme = filme['d'][0]['l']
    anofilme = filme['d'][0]['y']
    nota = rating(id)

    info = "https://www.imdb.com/title/" + id
    
    
    st.write("Filme: " + str(nomefilme))
    st.write("Nota Imdb: " + str(nota))
    st.write("Ano: " + str(anofilme))
    st.write(f"Mais informações : [Saiba mais]({info})")
    st.write('\n')
    st.image(filme['d'][0]['i']['imageUrl'])

### Layout Tela Inicial
else:
    st.write('\n')
    # st.write("""### Vou te recomendar alguns filmes :film_projector:""")  # Titulo App
    st.image('https://blog.videoperola.com.br/wp-content/uploads/2022/04/top10-scaled.jpg')  # Foto de capa
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    check = st.multiselect("Como você conheceu essa aplicação ? ", ["Instagram", "Linkedin", "Google", "Outros"])

    if check:
        with st.form("my_form"):
            st.write("Favor preencher os dados abaixo")
            nome = st.text_input("Nome")
            email = st.text_input("E-mail")
            submitted = st.form_submit_button("Confirmar")

        if submitted:
            sucesso = st.success("Obrigado!")
            check = st.empty()
