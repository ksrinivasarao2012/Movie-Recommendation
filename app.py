import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f14926b49e191ebe9bb1dab1877fb53d&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    k = content_df[content_df['title'] == movie].index[0]
    distances = cosine_df.iloc[k].sort_values(ascending=False)[1:6]
    names, posters = [], []
    for title in distances.index:
        # Find the integer index of this title in content_df
        idx = content_df[content_df['title'] == title].index[0]
        names.append(content_df.iloc[idx]['title'])
        posters.append(fetch_poster(content_df.iloc[idx]['movie_id']))
    return names, posters



# Load data
content_df = pickle.load(open('content.pkl', "rb"))
cosine_df = pickle.load(open('cosine.pkl', "rb"))
movies_list = content_df['title'].values

# UI
st.title('🎬 Movie Recommender System')
selected_movie = st.selectbox('Type or select a movie from the dropdown', movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
