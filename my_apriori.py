from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

from my_matrix import user_movie_matrix
# Verileri yükleyin
#movies_df = pd.read_csv('unique_top_movies.csv')
#ratings_df = pd.read_csv('rating.csv')


#-------------------------KULLANICI ID'SINDEN ----------> FILM ONERISI----------*/

def user_based_recommendation_general(user_id, user_movie_matrix, movies_df, min_support=0.10, metric="confidence", min_threshold=0.5):
    # Kullanıcının izlediği filmleri seçiyorum
    user_watched = user_movie_matrix.loc[user_id]
    watched_movies = user_watched[user_watched == True].index.tolist()

    # Apriori algoritmasını uygulayarak sık öğe kümelerini buluyorum
    frequent_itemsets = apriori(user_movie_matrix, min_support=min_support, use_colnames=True)

    # Birliktelik kurallarını oluşturuyorum
    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)

    # İzlenen filmlerden türeyen yeni öneriler aşağıda verlmiştir
    recommended_movies = []
    for movie in watched_movies:
        recommendations = rules[(rules['antecedents'].apply(lambda x: movie in x)) & (
            rules['consequents'].apply(lambda x: not any(i in watched_movies for i in x)))]

        recommended_movies.extend([list(consequents)[0] for consequents in recommendations['consequents']])

    # Önerileri tekrarları kaldırarak listeledim
    recommended_movies = list(set(recommended_movies))

    # Önerilen filmler ID listesi asagida
    recommended_ids = recommended_movies

    # ID'leri movies_df içinde arayarak karşılık gelen film isimlerini aldim
    recommended_movies = movies_df[movies_df['movieId'].isin(map(int, recommended_ids))][['movieId', 'title']]

    # Film adlarını birleştirip geri döndür
    result = []
    for _, row in recommended_movies.iterrows():
        result.append(f"Film ID: {row['movieId']}, Film Adı: {row['title']}")
    return '\n'.join(result)

#------------------------------------------DONE-----------------------------------------*/

#-----------------------GENEL POPULER FILM ONERISI---------------------------------------*/

def top_10_popular_movies(movies_df):
    """
    Rating'i en yüksek olan ilk 10 filmi döndürür.
    """
    # Rating değerine göre azalan şekilde sırala ve ilk 10 filmi seç
    top_movies = movies_df.sort_values(by="avg_rating", ascending=False).head(10)

    # Filmleri ID ve isim olarak listele
    result = []
    for _, row in top_movies.iterrows():
        result.append(f"Film ID: {row['movieId']}, Film Adı: {row['title']}, Rating: {row['avg_rating']}")
    return '\n'.join(result)



#--------------------------------DONE-----------------------------*/

#--------------------------------POPULER FILMLER AMA TURE GORE-----------*/
def top_10_popular_movies_by_genre(movies_df, genre):
    """
    Verilen türe göre en yüksek rating'e sahip ilk 10 filmi döndürür.
    """
    # Belirtilen türe göre filtrele
    filtered_movies = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]

    # Rating değerine göre azalan şekilde sırala ve ilk 10 filmi seç
    top_movies = filtered_movies.sort_values(by="avg_rating", ascending=False).head(10)

    # Filmleri ID ve isim olarak listele
    result = []
    for _, row in top_movies.iterrows():
        result.append(f"Film ID: {row['movieId']}, Film Adı: {row['title']}, Rating: {row['avg_rating']}")
    return '\n'.join(result)


#---------------------------------DONE----------------------------------*/

#-----------------------------------KULLANICI ID VE TURUNDEN --> FILM ONERISI-----------*/

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from collections import Counter
import random

def user_based_recommendation_genre(kullanici_id, secilen_tur, user_movie_matrix, movies_df, min_support=0.1,
                                    min_threshold=0.5):
    # Seçilen türe göre filtreleme yapicam
    secili_filmler = movies_df[movies_df['genres'].str.contains(secilen_tur, na=False)]
    secili_film_ids = set(secili_filmler['movieId'].astype(str))

    # Apriori algoritması ile sık öğe kümeleri ve ilişki kuralları oluşturma
    frequent_itemsets = apriori(user_movie_matrix, min_support=0.1, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

    def film_onerileri(user_id, user_item_matrix, rules, secili_film_ids):
        izlenen_filmler = set(user_item_matrix.columns[user_item_matrix.loc[user_id]])  # Kullanıcının izlediği filmler
        oneriler = set()
        confidence_dict = {}

        for _, row in rules.iterrows():
            if row['antecedents'].issubset(izlenen_filmler) and not row['consequents'].issubset(izlenen_filmler):
                for movie_id in row['consequents']:
                    if movie_id in secili_film_ids:  # Seçilen türdeki filmleri öner
                        oneriler.add(movie_id)
                        confidence_dict[movie_id] = row['confidence']

        oneriler_sirali = sorted(oneriler, key=lambda x: confidence_dict.get(x, 0), reverse=True)
        öneri_sayilari = Counter(oneriler_sirali)
        en_yaygin_oneriler = öneri_sayilari.most_common()

        return [film_id for film_id, _ in en_yaygin_oneriler]

    def film_adlarini_bul(film_ids, movies_df):
        movie_id_to_title = dict(zip(movies_df['movieId'].astype(str), movies_df['title']))
        return [movie_id_to_title[movie_id] for movie_id in film_ids if movie_id in movie_id_to_title]

    # Kullanıcıya önerilen filmleri aldik
    user_id = kullanici_id
    onerilen_film_ids = film_onerileri(user_id, user_movie_matrix, rules, secili_film_ids)
    onerilen_filmler_string = film_adlarini_bul(onerilen_film_ids, movies_df)

    # Seçilen türde rastgele 3 film önerisi
    random_films = random.sample(list(secili_filmler['title'].head(50)), 3)
    for film in random_films:
        if film not in onerilen_filmler_string:
            onerilen_filmler_string.append(film)

    # Seçilen türdeki en popüler 3 film
    top_movies_df = pd.read_csv('unique_top_movies.csv')
    op_movies = top_movies_df[top_movies_df['genres'].str.contains(secilen_tur)].head(3)

    for title in op_movies['title'].tolist():
        if title not in onerilen_filmler_string:
            onerilen_filmler_string.append(title)

    # Önerilen filmleri bastırma printleme
    print("Önerilen Filmler:")
    for film in onerilen_filmler_string:
        print(film)

    return '\n'.join(onerilen_filmler_string)


#-------------------------------done--------------------------------------------*/

#---------------------NAME------->MOVIE SUGGESTION-------------------------------*/

def recommend_movies_by_title_search_general(keyword, movies_df):
    """
    Verilen bir kelimeyi film isimlerinde arayarak kullanıcıya film önerisinde bulunur.
    """
    # Kelimeye göre film başlıklarını filtrele (case insensitive)
    matching_movies = movies_df[movies_df['title'].str.contains(keyword, case=False, na=False)]

    # Eşleşen filmleri döndür
    if not matching_movies.empty:
        result = f"'{keyword}' kelimesini içeren filmler:\n"
        for _, row in matching_movies.iterrows():
            result += f"Film ID: {row['movieId']}, Film Adı: {row['title']}\n"
    else:
        result = f"'{keyword}' kelimesini içeren film bulunamadı.\n"

    return result

#-----------------------------------DONE-------------------------------------*/

#------------------------ismi girilen filme benzer turde film onerme---------*/
def recommend_similar_movies_by_title_genre(movie_title, movies_df, top_n=5):

    # Giriş yapılan filmin türünü bul
    selected_movie = movies_df[movies_df['title'].str.contains(movie_title, case=False, na=False)]

    if selected_movie.empty:
        return [f"{movie_title} adında bir film bulunamadı."]

    # İlk eşleşen filmin türünü al
    movie_genre = selected_movie.iloc[0]['genres']

    # Aynı türdeki filmleri bul ve popülariteye göre sırala
    similar_movies = movies_df[movies_df['genres'].str.contains(movie_genre, case=False, na=False)]
    similar_movies = similar_movies.sort_values(by='avg_rating', ascending=False).head(top_n)

    # Öneri listesi oluştur
    recommendations = [
        f"Film ID: {row['movieId']}, Film Adı: {row['title']}, Tür: {row['genres']}, Rating: {row['avg_rating']}"
        for _, row in similar_movies.iterrows()
    ]

    return recommendations
#-------------------------------------------------------------------------DONE------------------------*/
