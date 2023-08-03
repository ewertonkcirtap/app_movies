import streamlit as st
import pandas as pd

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False, sep=';').encode('ISO-8859-1')
    

def main():
    
    st.title("Test your vocabulary in English")
    st.write("Do you know the word below? Yes or No")
    #st.title(word)


    df = pd.DataFrame(
        [
            {"word": "Make", "translation": '', "know?": False},
            {"word": "Closer", "translation": '', "know?": False},
            {"word": "His", "translation": '', "know?": False},
            {"word": "Any", "translation": '', "know?": False},
            {"word": "But", "translation": '', "know?": False},
            {"word": "Have", "translation": '', "know?": False},
            {"word": "Take", "translation": '', "know?": False},
            {"word": "Fever", "translation": '', "know?": False},
            {"word": "Also", "translation": '', "know?": False},
            {"word": "Some", "translation": '', "know?": False},
       ]
    )
    
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    #favorite_command = edited_df.loc[edited_df["translation"].idxmax()]["command"]
    #st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

    csv = convert_df(edited_df)
    
    st.download_button(
        label="Download data",
        data=csv,
        file_name='word_list.csv',
        mime='text/csv',
    )


if __name__ == "__main__":
    main()
