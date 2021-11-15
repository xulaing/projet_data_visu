import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import datetime

st.set_page_config(
    page_title="Projet | Data Visualization",
    page_icon="👩🏻‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Projet | Data Visualization 👩‍💻')
st.caption('Céline KHAUV 20180417')

@st.cache(suppress_st_warning=True)
def log(func):
    def wrapper(*args, **kwargs):
        with open("logs.txt", "a") as f:
            f.write("Called function with " + " ".join(
                [str(arg) for arg in args]) + " at " + str(datetime.datetime.now()) + "\n")
        val = func(*args, **kwargs)
        return val
    return wrapper

@st.cache(suppress_st_warning=True)
def create_map(sub_df):
    sub_df['latitude']=pd.to_numeric(sub_df['latitude'])
    sub_df['longitude']=pd.to_numeric(sub_df['longitude'])
    sub_df.dropna(subset = ['latitude', 'longitude'], inplace = True)
    st.map(sub_df[['latitude', 'longitude']])

@st.cache(suppress_st_warning=True)
def create_hist1(sub_df):
    fig, ax = plt.subplots()
    ax.hist(sub_df["nombre_pieces_principales"])
    plt.xlabel('Nombre de pièce principales')
    plt.ylabel('Nombre d\'appartement')
    plt.title('Nombre d\'appartement par rapport au nombre de pièce principales')
    st.pyplot(fig)
    
@st.cache(suppress_st_warning=True)
def create_hist2(sub_df):
    fig, ax = plt.subplots()
    ax.hist(sub_df["surface_terrain"])
    plt.xlabel('Surface en m²')
    plt.ylabel('Nombre d\'appartement')
    plt.title('Nombre d\'appartement par rapport à la surface en m²')
    st.pyplot(fig)

@st.cache(suppress_st_warning=True)
def create_subplot(sub_df):
    st.header('Valeur foncière des biens par rapport à la surface de terrain')
    sub_df.dropna( subset = ['valeur_fonciere','surface_terrain'])
    sub_df = sub_df.rename(columns={'surface_terrain':'index'}).set_index('index')
    st.line_chart(sub_df['valeur_fonciere'])

@st.cache(suppress_st_warning=True)
def create_pie(sub_df):
    local_count = sub_df['type_local'].value_counts()
    local_count = pd.DataFrame({'Names' :local_count.index, 'Values' :local_count.values})
    fig = px.pie(local_count, values='Values', names='Names')
    st.header("Types de biens disponibles")
    st.plotly_chart(fig)

@st.cache(suppress_st_warning=True)
@log
def display(df) :
    st.sidebar.header('Cherchez un bien :')
    st.sidebar.write('Quel type de local vous intéresse ?')
    maison = st.sidebar.checkbox('Maison', value=True)
    app = st.sidebar.checkbox('Appartement')
    dep = st.sidebar.checkbox('Dépendance')
    loc = st.sidebar.checkbox('Local industriel. commercial ou assimilé')
    num_choice = maison + app + dep + loc

    #option = st.sidebar.selectbox('Quel type de local vous intéresse ?', ('Choisir', 'Maison', 'Appartement', 'Dépendance','Local industriel. commercial ou assimilé'))
    option2 = st.sidebar.selectbox('Combien de piece ?', ['Choisir']+[1,2,3,4,5])
    option3 = st.sidebar.selectbox('Dans quel département ?', ['Choisir']+[cp for cp in range(1000, 97490)])
    option4 = st.sidebar.slider('Nombre de m carré',20,2000)

    data_set = df[['type_local', 'nombre_pieces_principales', 'code_postal', 'valeur_fonciere', 'surface_terrain','latitude', 'longitude']]

    if num_choice == 0:
        st.error('You have to select minimum 1 variable.')
    elif num_choice == 1:
        if maison :
            mask = (data_set['type_local'] == 'Maison')
        elif app :
            mask = (data_set['type_local'] == 'Appartement')
        elif app :
            mask = (data_set['type_local'] == 'Dépendance')
        elif dep :
            mask = (data_set['type_local'] == 'Local industriel. commercial ou assimilé')  
        data_set = data_set[mask]    
    elif num_choice > 1:
        st.error('You can select maximum 1 variable.')

    if option2  :
        mask1 = (data_set['nombre_pieces_principales'] == option2)
        data_set = data_set[mask1]

    if option3  :
        mask2 = (data_set['code_postal'] == option3)
        data_set = data_set[mask2]

    if option4  :
        mask3 = (data_set['surface_terrain'] > option4)
        data_set = data_set[mask3]
            

    reset = st.sidebar.button(label="reset")

    if reset :   
        data_set = df[['type_local', 'nombre_pieces_principales', 'code_postal', "valeur_fonciere", 'surface_terrain','latitude', 'longitude']]
        data_set = data_set.sample(1000)
        
    return data_set

if __name__ == "__main__":
    df =   pd.read_csv('https://jtellier.fr/DataViz/full_2020.csv', delimiter = ',')
    df = df.sample(n=50000)
    create_pie(df)
    a = display(df)
    create_map(a)
    create_subplot(a)
    create_hist1(a)
    create_hist2(a)