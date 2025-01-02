import pandas as pd  # 'pandas' kütüphanesini kullanmalısın
from mlxtend.frequent_patterns import association_rules, fpgrowth

# CSV dosyalarını güncelledim
movies_df = pd.read_csv('unique_top_movies.csv')
ratings_df = pd.read_csv('rating.csv')

# Kullanıcı-film matrisini oluşturuyorum
user_movie_matrix = ratings_df[ratings_df['movieId'].isin(movies_df['movieId'])] \
                    .pivot_table(index='userId', columns='movieId', values='rating', fill_value=0)

# İzlenen filmler için True, izlenmeyenler için False olarak işaretledim
user_movie_matrix = user_movie_matrix.apply(lambda col: col.map(lambda x: True if x > 0 else False))


user_movie_matrix.to_csv("user_movie_matrix.csv")

# Oluşturulan kullanıcı-film matrisini kontrol edelim
user_movie_matrix_df = pd.read_csv('user_movie_matrix.csv')

# Kullanıcı-film matrisini yükle
user_movie_matrix = pd.read_csv("user_movie_matrix.csv", index_col=0)

movies_df = pd.read_csv('unique_top_movies.csv')

# Minimum destek değeri
minsupport = 0.10
min_confidence = 0.10

# FP-Growth algoritmasını kullanarak sık öğe kümelerini buluyorum
frequent_itemsets = fpgrowth(user_movie_matrix, min_support=minsupport, use_colnames=True)





# Birliktelik kuralları
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_csv('association_rules_filtered.csv', index=False)

