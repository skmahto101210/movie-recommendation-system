import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):   
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OGM0MmU0N2ZmNjk5YjM5ODU1MGUwNGFlMjJhYTcwOCIsInN1YiI6IjY2NDg3MTBhZWU4Y2FiNjBkNzc4YTRjNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IldYFxeulBxFLC5OLU2D8uIK9qQNXM_PlpCbhI9wae0"
        }

        response = requests.get(url, headers=headers)
        # st.text(response.json())
        data = response.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except Exception as e:
        print(e)

def recommend(movie):
    movie_ind = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_ind]
    movies_list =  sorted(list(enumerate(distances)),key = lambda x:x[1],reverse=True)[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # st.text(movie_id)
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movies Recommender System') 
selected_movie_name = st.selectbox(
   "Type or select a movie from the dropdown",
   movies['title'].values)



if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    
    for i, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
        if poster is None:
            st.write(f"Poster URL for {name} is None")
            continue
        try:
            if i == 0:
                with col1:
                    st.text(name)
                    st.image(poster)
            elif i == 1:
                with col2:
                    st.text(name)
                    st.image(poster)
            elif i == 2:
                with col3:
                    st.text(name)
                    st.image(poster)
            elif i == 3:
                with col4:
                    st.text(name)
                    st.image(poster)
            elif i == 4:
                with col5:
                    st.text(name)
                    st.image(poster)
        except Exception as e:
            st.write(f"Error displaying image for {name}: {e}")