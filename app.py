import streamlit as st
import pickle
import pandas as pd
import requests



def fetch_poster(movie_id):
    api_key = 'f7ec7c667c149c65ec987ea31563296c'  # Replace with your actual TMDb API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()

    # Debug output (you can remove later)


    # Safe access to poster_path
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster+Found"


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters = []

    for i in movies_list:
        movie_id=i[0]
        #fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
"ALL THE MOVIES",
movies['title'].values)

if st.button('Recommend movies'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for i in range(5):
        with columns[i]:
            st.text(names[i])
            st.image(posters[i])


