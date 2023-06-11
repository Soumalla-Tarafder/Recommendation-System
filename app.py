import streamlit as st
import pandas as pd
import numpy as np
import pickle
import urllib.request
import json
movies=pickle.load(open('notebook\movies.pkl','rb'))

movies_dict=pickle.load(open('notebook\movies_dict.pkl','rb'))

#movie = pd.DataFrame(movies_dict)

movies_list=movies['title'].unique()

similarity=pickle.load(open('notebook\similarity.pkl','rb'))

def fetch_poster(movie_id):
    #tmdb url
    url = "https://api.themoviedb.org/3/movie/{}?api_key=4e320adfc359959c2d9189781461fdc0&language=en-US".format(movie_id)
    data = urllib.request.urlopen(url)
    data = data.read()
    data = json.loads(data)
    
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    print("full_path",full_path)
    return full_path


def recommend_movies(movie):
    movie_index =  movies[movies['title'] == movie].index[0]
    distance = similarity[ movie_index]
    movies_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    result=[]
    recommended_movie_posters=[]
    movie_id=""
    print(movies_list)
    for i in movies_list:
        movie_id=i[0]
        
        result.append(movies.iloc[i[0]].title)
    return result

st.title('Movie Recommendation System')

selected_movie = st.selectbox(
    'Select Movie Name',
    movies_list
)

if st.button('Recommend'):
    recommendations= recommend_movies(selected_movie)
    for i in recommendations:
        st.write(i)


