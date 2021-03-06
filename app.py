from flask import Flask,Response, render_template, request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



df = pd.read_csv('final_data(movies 1950-2020).csv')
movies_name = list(df['movie_title'])
df['comb'] = df['actor_1_name'] + ' ' + df['actor_2_name'] + ' '+ df['actor_3_name'] + ' '+ df['director_name'] +' ' + df['genres']
df['comb'] = df['comb'].fillna('unknown')
df['genres'] = df['genres'].replace('None', ' ')
df.set_index('movie_title', inplace = True)

# instantiating and generating the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(df['comb'])

# creating a Series for the movie titles so they are associated to an ordered numerical
# list I will use later to match the indexes
indices = pd.Series(df.index)


cosine_sim = cosine_similarity(count_matrix)
# function that takes in movie_title as input and returns the top 10 recommended movies

def recommendations(title):

    recommended_movies = []
    ratings = []
    title = title.lower()
    # getting the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)

    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_movies.append(list(df.index)[i])
        ratings.append(list(df['tmdb_ratings'])[i])
    return recommended_movies, ratings


def genre_recomd(title):
    recommended_movies = []
    ratings = []
    title = title.lower()
    df1 = np.array(df['comb'])
    df1 = np.append(title, df1)

    idx = 0
    count1 = CountVectorizer()
    count_matrix = count1.fit_transform(df1)
    c2 = cosine_similarity(count_matrix)

    score_series = pd.Series(c2[0]).sort_values(ascending=False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)

    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_movies.append(list(df.index)[i - 1])
        ratings.append(list(df['tmdb_ratings'])[i - 1])

    return recommended_movies, ratings




app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/genre')
def genre():
    return render_template('genre.html')


@app.route("/genre_recomdf")
def genre_recomdf():
    title = request.args.get('title')
    m = genre_recomd(title)[0]
    r = genre_recomd(title)[1]
    return render_template('recommend.html', title=title, m=m, r=r)

@app.route("/recommend")
def recommend():
    title = request.args.get('title')
    m = recommendations(title)[0]
    r = recommendations(title)[1]
    return render_template('recommend.html', title=title, m=m, r=r)

if __name__ == '__main__':
    app.run(debug=True)