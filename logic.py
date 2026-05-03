from gui import *
import csv
import random

class Logic(Window):
    '''
    This class handles all the logic for movie watchlist app.
    '''
    def __init__(self) -> None:
        '''
        Initialize Logic class, connect all the data, and load data
        '''

        super().__init__()
        self.current_movie = None
        self.add_button.clicked.connect(self.handle_add_button)
        self.view_button.clicked.connect(self.handle_view_button)
        self.cancel_button.clicked.connect(self.handle_cancel_button)
        self.back_button.clicked.connect(self.handle_list_back_button)
        self.edit_save_button.clicked.connect(self.handle_edit_save)
        self.edit_back_button.clicked.connect(self.handle_edit_back_button)
        self.save_button.clicked.connect(self.handle_save)
        self.update_display()
        self.load_movies()

    # Simple Screen Navigation
    def handle_add_button(self) -> None:
        '''
        Navigates to the Add Movie screen from Home screen
        '''
        self.stack.setCurrentIndex(1)

    def handle_view_button(self) -> None:
        '''
        Loads movies details
        Navigates to the Movie List screen from Home screen
        '''
        self.load_movies()
        self.stack.setCurrentIndex(2)

    def handle_cancel_button(self) -> None:
        '''
        Navigates back to the Home Screen from the Add Movie screen
        '''
        self.stack.setCurrentIndex(0)

    def handle_list_back_button(self) -> None:
        '''
        Navigates back to the Home screen from the Movie List screen
        '''
        self.stack.setCurrentIndex(0)

    def handle_edit_back_button(self) -> None:
        '''
        Navigates back to the Movie List screen from the Edit Movie screen
        '''
        self.stack.setCurrentIndex(2)

    def handle_edit_button(self, movie: dict) -> None:
        '''
        Loads selected movie details in Edit Movie screen
        Navigates to Edit Movie Screen from Movie List screen
        '''
        self.load_edit_screen(movie)
        self.stack.setCurrentIndex(3)

    # Home Page
    def update_display(self) -> None:
        '''
        The purpose of this function is to make sure the display on the Home Screen stays updated to how many movies
        the user has watched, wants to watch, and their total movies in their watchlist.
        It reads from the movie_details.csv file and checks if a movie is watched. If so, it increases the counter
        If the movie has not been watched, it updates the "Remaining" counter
        The "Total" counter stays updated by adding both counters
        '''
        watched = 0
        remaining = 0

        try:
            with open('movie_details.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    if row["status"] == "Watched":
                        watched += 1
                    else:
                        remaining += 1

            total = watched + remaining
            self.watched_count.setText(str(watched))
            self.remaining_count.setText(str(remaining))
            self.total_count.setText(str(total))
        except FileNotFoundError:
            return

    # Add Page
    def handle_save(self) -> None:
        '''
        The purpose of this function is to handle the logic of the Add screen page.
        It checks if the input box is empty. If it is, then the input box is highlighted red
        Next, it checks if the user selected any value that wasn't the default value in the dropdown boxes.
        If they select the default value, then the box is also highlighted red
        Once the user selects valid inputs and press the save button, the movie's information will be added to the csv file
        Then, the information on the Add Movie page will be cleared and the user will be sent back to the home screen
        Finally, the user should see a success message that appears on the home screen for 3 seconds
        '''
        movie_title = self.input_movie.text()
        valid = True

        # Making sure that the users enters a valid option.
        if movie_title == '':
            self.input_movie.setStyleSheet("font-size: 11px; font-weight: bold; border: 2px solid red")
            valid = False
        else:
            self.input_movie.setStyleSheet("font-size: 11px; font-weight: bold;")

        if self.drop_genre.currentText() == 'Select Genre':
            self.drop_genre.setStyleSheet("font-size: 11px; font-weight: bold; border: 2px solid red")
            valid = False
        else:
            self.drop_genre.setStyleSheet("font-size: 11px; font-weight: bold;")

        if self.drop_year.currentText() == 'Select Year':
            self.drop_year.setStyleSheet("font-size: 11px; font-weight: bold; border: 2px solid red")
            valid = False
        else:
            self.drop_year.setStyleSheet("font-size: 11px; font-weight: bold;")

        if self.drop_rating.currentText() == 'Select Rating':
            self.drop_rating.setStyleSheet("font-size: 11px; font-weight: bold; border: 2px solid red")
            valid = False
        else:
            self.drop_rating.setStyleSheet("font-size: 11px; font-weight: bold;")

        if self.drop_status.currentText() == 'Select Status':
            self.drop_status.setStyleSheet("font-size: 11px; font-weight: bold; border: 2px solid red")
            valid = False
        else:
            self.drop_status.setStyleSheet("font-size: 11px; font-weight: bold;")

        if not valid:
            return

        # Add to csv
        try:
            with open('movie_details.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([movie_title, self.drop_genre.currentText(), self.drop_year.currentText(), self.drop_rating.currentText(), self.drop_status.currentText()])
        except FileNotFoundError:
            return

        # Clear add page
        self.input_movie.clear()
        self.drop_genre.setCurrentIndex(0)
        self.drop_year.setCurrentIndex(0)
        self.drop_rating.setCurrentIndex(0)
        self.drop_status.setCurrentIndex(0)

        self.stack.setCurrentIndex(0)
        self.update_display()

        # I used A.I. to figure out how to use QTimer
        self.success_message.setText("Successfully updated!")
        QTimer.singleShot(3000, lambda: self.success_message.setText(""))

    # List Page
    def load_movies(self) -> None:
        '''
        The purpose of this function is to help build the Movie List screen
        I created a dictionary with messages that randomly appear if the user has not input any movies
        Otherwise, the code displays movie rows for each movie that the use has input and is read from the csv file
        Movies that were not watched have an "X" symbol next to them
        Movies that were watched have a checkmark next to them
        Each movie row has an "Edit" button that'll navigate them to the Edit Movie screen
        The scroll bar also expands when enough movies have been added
        '''
        empty_messages = [
            f"Seems pretty\nempty...",
            f"No movies\nyet!",
            f"Nothing to\nsee here...",
            f"It's a ghost\ntown",
            f"What's going\non here?",
            f"Add a movie to\nget started!",
            f"Your watchlist\nis empty!",
        ]

        while self.movies_container.count():
            item = self.movies_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            with open('movie_details.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                movies = list(reader)
        except FileNotFoundError:
            movies = []

        if len(movies) == 0:
            empty_label = QLabel(random.choice(empty_messages))
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("font-size: 25px;")
            self.movies_container.addWidget(empty_label)
        else:
            for movie in movies:
                row = QHBoxLayout()

                watched = movie['status'] == 'Watched'
                if watched:
                    # Checkmark symbol from google
                    indicator = QLabel("✓")
                else:
                    # X symbol from google
                    indicator = QLabel("✗")
                indicator.setStyleSheet("font-size: 10px;")

                movie_info = QLabel(f"{movie['title']} ({movie['year']})")
                movie_info.setStyleSheet("font-size: 13px;")
                movie_info.setWordWrap(True)
                movie_info.setFixedWidth(120)

                edit_button = QPushButton("Edit")
                edit_button.setFixedSize(60, 35)
                edit_button.clicked.connect(lambda checked, m=movie: self.handle_edit_button(m))
                edit_button.setStyleSheet("font-size: 15px;")

                row.addWidget(indicator)
                row.addWidget(movie_info)
                row.addStretch()
                row.addWidget(edit_button)

                row_widget = QWidget()
                row_widget.setLayout(row)
                self.movies_container.addWidget(row_widget)

    # Edit PAge
    def handle_edit_save(self) -> None:
        '''
        The purpose of this function is to handle the "Save" button in the Edit Movie screen
        Once pressed, it opens and reads the csv file to search for the row that matches a movie's data
        Then, it updates and saves the new data into the csv file
        It also loads the movies, updates the display if the movie went from unwatched to watched, and changes screens
        Also displays a success message in the home screen if they edited a movie
        '''
        rows = []
        try:
            with open('movie_details.csv', 'r') as csvfile:
                for row in csv.DictReader(csvfile):
                    if row['title'] == self.current_movie['title']:
                        row['year'] = self.edit_year_dropdown.currentText()
                        row['genre'] = self.edit_genre_dropdown.currentText()
                        row['rating'] = self.edit_rating_dropdown.currentText()
                        row['status'] = self.edit_status_dropdown.currentText()
                    rows.append(row)

            with open('movie_details.csv', 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['title', 'genre', 'year', 'rating', 'status'])
                writer.writeheader()
                writer.writerows(rows)

            self.load_movies()
            self.update_display()
            self.stack.setCurrentIndex(0)
            self.success_message.setText("Successfully updated!")
            QTimer.singleShot(3000, lambda: self.success_message.setText(""))

        except FileNotFoundError:
            return

    def load_edit_screen(self, movie: dict) -> None:
        '''
        The purpose of this function is to load, or pre-fill, the information in the Edit Movie screen
        It displays the movie, the year it was released, the genre, and its rating given by the user
        Each dropdown should be pre-selected with the data it was given previously
        '''
        self.current_movie = movie
        self.edit_movie_title.setText(f"{movie['title']} ({movie['year']})")
        self.edit_movie_genre.setText(f"{movie['genre']} - {movie['rating']}/10 ")
        self.edit_year_dropdown.setCurrentText(movie['year'])
        self.edit_genre_dropdown.setCurrentText(movie['genre'])
        self.edit_status_dropdown.setCurrentText(movie['status'])
        self.edit_rating_dropdown.setCurrentText(movie['rating'])