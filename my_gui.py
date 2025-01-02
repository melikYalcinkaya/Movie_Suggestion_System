import PySimpleGUI as sg
import pandas as pd
from my_matrix import user_movie_matrix
from my_apriori import (
    user_based_recommendation_general,
    top_10_popular_movies,
    top_10_popular_movies_by_genre,
    user_based_recommendation_genre,
    recommend_movies_by_title_search_general,
    recommend_similar_movies_by_title_genre
)

class RecommendationGUI:
    def __init__(self):
        # Load data
        self.movies_df = pd.read_csv('unique_top_movies.csv')
        self.users_list = user_movie_matrix.index.tolist()

        # Define layout with all required components
        self.layout = [
            [sg.Text("Film Öneri Sistemi", font=('Helvetica', 16))],
            [sg.Text("Öneri Türü Seçin:"), sg.Combo(
                ["Popüler Film Önerileri", "Kişiselleştirilmiş Film Önerileri",
                 "Film Başlığına Göre Öneriler", "Girilen Filme Benzer Filmler"],
                key="recommendation_type", default_value="Popüler Film Önerileri", enable_events=True
            )],
            [sg.Text("Öneri Şartını Seçin:"), sg.Combo(["Film Türüne Göre Öneriler"], key="criteria_type", default_value="Film Türüne Göre Öneriler", enable_events=True)],
            [sg.Text("Kullanıcı Seçin (Kişiselleştirilmiş Seçildiğinde):"), sg.Listbox(values=self.users_list, size=(20, 6), key="user_id", visible=False)],
            [sg.Text("Film Türünü Seçin:"), sg.Listbox(values=['Action', 'Comedy', 'Drama', 'Horror', 'Romance'], size=(20, 6), key="genre", visible=False)],
            [sg.Text("Film Başlığını Girin (Başlık Bazlı veya Benzerlik Bazlı Öneri Seçildiğinde):"), sg.InputText(key="movie_title", visible=False)],
            [sg.Button("Film Önerisi Göster"), sg.Button("Çıkış")],
            [sg.Text("Önerilen Film:", font=('Helvetica', 14))],
            [sg.Output(size=(60, 10), key="output")]
        ]

        # Create the window
        self.window = sg.Window("Film Öneri Sistemi", self.layout)

    def update_visibility(self, values):
        # Update visibility for different GUI components based on selected options
        self.window["user_id"].update(visible=values["recommendation_type"] == "Kişiselleştirilmiş Film Önerileri")
        self.window["genre"].update(visible=values["criteria_type"] == "Film Türüne Göre Öneriler")
        self.window["movie_title"].update(visible=values["recommendation_type"] in ["Film Başlığına Göre Öneriler", "Girilen Filme Benzer Filmler"])

    def recommend_movie(self, values):
        # Generate a movie recommendation based on the selected options
        recommendation_type = values["recommendation_type"]
        criteria_type = values["criteria_type"]
        user_id = values.get("user_id")[0] if values.get("user_id") else None
        genre = values["genre"][0] if values["genre"] else None
        movie_title = values["movie_title"] if values["movie_title"] else None

        # Generate recommendations based on the selected options
        if recommendation_type == "Popüler Film Önerileri":
            if criteria_type == "Film Türüne Göre Öneriler" and genre:
                return top_10_popular_movies_by_genre(self.movies_df, genre)
            else:
                return top_10_popular_movies(self.movies_df)

        elif recommendation_type == "Kişiselleştirilmiş Film Önerileri" and user_id:
            if criteria_type == "Film Türüne Göre Öneriler" and genre:
                return user_based_recommendation_genre(user_id, genre, user_movie_matrix, self.movies_df)
            else:
                return user_based_recommendation_general(user_id, user_movie_matrix, self.movies_df)

        elif recommendation_type == "Film Başlığına Göre Öneriler" and movie_title:
            if criteria_type == "Film Türüne Göre Öneriler" and genre:
                return recommend_similar_movies_by_title_genre(movie_title, genre, self.movies_df)
            else:
                return recommend_movies_by_title_search_general(movie_title, self.movies_df)

        elif recommendation_type == "Girilen Filme Benzer Filmler" and movie_title :
            return recommend_similar_movies_by_title_genre(movie_title, self.movies_df)

    def run(self):
        # Run the main event loop for the GUI
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED or event == "Çıkış":
                break

            # Update visibility based on selected options
            self.update_visibility(values)

            # Show recommendation when the button is pressed
            if event == "Film Önerisi Göster":
                recommendation = self.recommend_movie(values)
                self.window["output"].update(recommendation)

        self.window.close()


# Run the GUI
if __name__ == "__main__":
    gui = RecommendationGUI()
    gui.run()
