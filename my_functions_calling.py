# main.py
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from my_matrix import user_movie_matrix
from my_apriori import top_10_popular_movies, top_10_popular_movies_by_genre, user_based_recommendation_genre,  user_based_recommendation_general,recommend_movies_by_title_search_general,recommend_similar_movies_by_title_genre

# Veriler
movies_df = pd.read_csv('unique_top_movies.csv')

# En popüler 10 filmi listeleme
print("\nEn popüler 10 film:")
top_10_popular_movies(movies_df)

# Belirli türe göre en popüler 10 filmi listeleme
genre = 'Fantasy'
print(f"\n{genre} türünde en popüler 10 film:")
top_10_popular_movies_by_genre(movies_df,genre)


kullanici_id = 1
secilen_tur = 'Horror'
# user_movie_matrix ve movies_df veri çerçevelerini uygun şekilde geçirin
onerilen_filmler = user_based_recommendation_genre(kullanici_id, secilen_tur, user_movie_matrix, movies_df)

# Sonuçları yazdiriyoruz
print("\n Önerilen Filmler:")
for film in onerilen_filmler:
    print(film)
