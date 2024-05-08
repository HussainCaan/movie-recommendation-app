import streamlit as st
import pickle
import requests

# Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="Movie recommendation system Using ML",
    page_icon="🎥",
    layout="wide",
)
st.header('MOVIE RECOMMENDATION SYSTEM', divider='rainbow')

footer = """
<style>
    .footer p {
    position: fixed;
    margin:0;
    padding:0;
    left: 0;
    bottom: 0;
    width: 100%;
    background-image: linear-gradient(90deg,orange,yellow);
    text-align: center;
    color: white;
    }
</style>

<div class="footer">
    <p>Developed by Team No-Itihad</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
# Function to fetch movie poster URL


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8bb921015d2d20ee4b1b630ac130a216&language=en-US".format(
        movie_id
    )
    data = requests.get(url)
    data = data.json()
    poster_path = data["poster_path"]
    full_path = "http://image.tmdb.org/t/p/w500" + poster_path
    return full_path


# Function to recommend movies based on a selected movie
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distance = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]]["movie_id"]
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name, recommended_movies_poster


def recommend_Dir(movie):
    index = director[director['title'] == movie].index[0]
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in director.index:
        if director.loc[i, "crew"] == director.loc[index, "crew"] and director.loc[i, "title"] != director.loc[index, "title"]:
            recommended_movies_poster.append(
                fetch_poster(director.iloc[i].movie_id))
            recommended_movies_name.append(director.iloc[i])
    if len(recommended_movies_name) == 0:
        recommended_movies_poster.append(
            fetch_poster(director.iloc[index].movie_id))
        recommended_movies_name.append(director.iloc[index])
    return recommended_movies_name, recommended_movies_poster


def recommend_with_cast(movie):
    actor = cast_df[cast_df["title"] == movie]["cast"].iloc[0][0]
    recommended_movies_name = []
    recommended_movies_poster = []
    for index, row in cast_df.iterrows():
        if actor in row["cast"]:
            recommended_movies_poster.append(fetch_poster(row["movie_id"]))
            recommended_movies_name.append(row["title"])
    return recommended_movies_name, recommended_movies_poster


def recommend_genres(movie):
    index = Genres[movies['title'] == movie].index[0]
    recommended_movies_name = []
    recommended_movies_poster = []
    distances = sorted(
        list(enumerate(similarity2[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]["movie_id"]
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster


# Load movie data and similarity matrix
movies = pickle.load(open("Pickle\movie_list.pkl", "rb"))
similarity = pickle.load(open("Pickle\similarity.pkl", "rb"))
director = pickle.load(open("Pickle\director.pkl", "rb"))
cast_df = pickle.load(open("Pickle\Actor.pkl", "rb"))
Genres = pickle.load(open("Pickle\Genres.pkl", "rb"))
similarity2 = pickle.load(open("Pickle\similarity2.pkl", "rb"))

movie_list = movies["title"].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendation', movie_list)

if st.button("Show Recommendation"):
    st.subheader(':orange[Recommended Movies]')
    recommended_movies_name, recommended_movies_poster = recommend(
        selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movies_poster[0])
        st.text(recommended_movies_name[0])
    with col2:
        st.image(recommended_movies_poster[1])
        st.text(recommended_movies_name[1])
    with col3:
        st.image(recommended_movies_poster[2])
        st.text(recommended_movies_name[2])
    with col4:
        st.image(recommended_movies_poster[3])
        st.text(recommended_movies_name[3])
    with col5:
        st.image(recommended_movies_poster[4])
        st.text(recommended_movies_name[4])

    st.subheader(f":orange[Other Movies with Same Genre]")
    recommended_movies_name, recommended_movies_poster = recommend_genres(
        selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movies_poster[0])
        st.text(recommended_movies_name[0])
    with col2:
        st.image(recommended_movies_poster[1])
        st.text(recommended_movies_name[1])
    with col3:
        st.image(recommended_movies_poster[2])
        st.text(recommended_movies_name[2])
    with col4:
        st.image(recommended_movies_poster[3])
        st.text(recommended_movies_name[3])
    with col5:
        st.image(recommended_movies_poster[4])
        st.text(recommended_movies_name[4])

    st.subheader(f":orange[Movie's Director Other Movies]")
    recommended_movies_name, recommended_movies_poster = recommend_Dir(
        selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movies_poster[0])
        st.text(recommended_movies_name[0].title)
    with col2:
        st.image(recommended_movies_poster[1])
        st.text(recommended_movies_name[1].title)
    with col3:
        st.image(recommended_movies_poster[2])
        st.text(recommended_movies_name[2].title)
    with col4:
        st.image(recommended_movies_poster[3])
        st.text(recommended_movies_name[3].title)
    with col5:
        st.image(recommended_movies_poster[4])
        st.text(recommended_movies_name[4].title)

    st.subheader(f":orange[Movie's Actor Other Movies]")
    recommended_movies_name, recommended_movies_poster = recommend_with_cast(
        selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movies_poster[5])
        st.text(recommended_movies_name[5])
    with col2:
        st.image(recommended_movies_poster[1])
        st.text(recommended_movies_name[1])
    with col3:
        st.image(recommended_movies_poster[2])
        st.text(recommended_movies_name[2])
    with col4:
        st.image(recommended_movies_poster[3])
        st.text(recommended_movies_name[3])
    with col5:
        st.image(recommended_movies_poster[4])
        st.text(recommended_movies_name[4])

with open('style.css') as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
