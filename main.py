import pandas as pd
import numpy as np
from my_matrix import rules
from my_apriori import top_10_popular_movies, top_10_popular_movies_by_genre, user_based_recommendation_genre, user_based_recommendation_general

movies_df = pd.read_csv('movie.csv')
ratings_df = pd.read_csv('rating.csv')

# the moives that i chose.
selected_genres = ['Film-Noir', 'IMAX', 'Western', 'Musical', 'War', 'Animation', 'Children', 'Fantasy', 'Mystery', 'Sci-Fi']

# im gonna clean the lists. just the movies which i chose will stay.
filtered_movies_df = movies_df[movies_df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]

filtered_movies_df.to_csv("filtered_movie.csv", index=False)


#------------------------- pick the most popular 50 movies--------------------*/

filtered_movies_df.to_csv("filtered_movie.csv", index=False)

## im gonna use the new movie list for my base 'movies_df'
movies_df = pd.read_csv('filtered_movie.csv')  # Filtrelediğim 10 türden oluşan dosya
ratings_df = pd.read_csv('rating.csv')

movie_ratings = ratings_df.groupby('movieId')['rating'].mean().reset_index()
movie_ratings.columns = ['movieId', 'avg_rating']

#merge the all movies and ratings
movies_with_ratings = pd.merge(movies_df, movie_ratings, on='movieId', how='left')

# Pick the 50 most popular movies in every genre
top_movies = (
    movies_with_ratings.assign(genres=movies_with_ratings['genres'].str.split('|'))
    .explode('genres')  # slicing the genres
    .sort_values(['genres', 'avg_rating'], ascending=[True, False])  # Group by genre and sort by popularityClick to apply
    .groupby('genres').head(50)  # pick the most popular 50 movies for every genre
    .drop_duplicates(subset="movieId")
)

top_movies.to_csv("unique_top_movies.csv", index=False)
movies_df = pd.read_csv('unique_top_movies.csv')
#------------------------------------done------------------------------*/


