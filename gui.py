from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
import sys

class Window(QWidget):
    '''
    This window class builds all the user interface screens from the movie watchlist app
    '''
    def __init__(self) -> None:
        '''
        Builds the main window.
        Sets up the QStackedWidget.
        Builds all screens
        '''
        # Had to research how to do Stacked Widgets instead of having a switch_screen method
        super().__init__()
        self.setWindowTitle("Final Project 2")
        self.setFixedSize(300, 440)

        self.stack = QStackedWidget()

        self.home_screen = QWidget()
        self.add_screen = QWidget()
        self.list_screen = QWidget()
        self.edit_screen = QWidget()

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.add_screen)
        self.stack.addWidget(self.list_screen)
        self.stack.addWidget(self.edit_screen)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

        self._build_home_ui()
        self._build_add_ui()
        self._build_list_ui()
        self._build_edit_ui()

    def _build_home_ui(self) -> None:
        '''
        This function builds the home screen
        The home screen features a title, a display, and some buttons to switch screens
        The display screen features movie counts depending on what the user has watched, hasn't watched, and the total
        This screen also has a success message that appears for 3 seconds when a user adds or edits a movie
        Add button should bring user to the Add Movie screen
        View button should bring user to the Movie List screen
        '''
        layout = QVBoxLayout()
        self.home_screen.setLayout(layout)

        # Home Page Title
        home_title = QLabel("Movie Watchlist")
        home_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        home_title.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(home_title)

        # Home Page Watched Movies Count
        row = QHBoxLayout()
        self.watched_label = QLabel("Watched:")
        self.watched_label.setStyleSheet("font-size: 25px; font-weight: bold;")
        self.watched_count = QLabel("0")
        self.watched_count.setStyleSheet("font-size: 25px; font-weight: bold;")
        row.addWidget(self.watched_label)
        row.addStretch()
        row.addWidget(self.watched_count)
        layout.addLayout(row)

        # Home Page Remaining Movies Count
        row = QHBoxLayout()
        self.remaining_label = QLabel("Remaining:")
        self.remaining_label.setStyleSheet("font-size: 25px; font-weight: bold;")
        self.remaining_count = QLabel("0")
        self.remaining_count.setStyleSheet("font-size: 25px; font-weight: bold;")
        row.addWidget(self.remaining_label)
        row.addStretch()
        row.addWidget(self.remaining_count)
        layout.addLayout(row)

        # Home Page Total Movies Count
        row = QHBoxLayout()
        self.total_label = QLabel("Total:")
        self.total_label.setStyleSheet("font-size: 25px; font-weight: bold;")
        self.total_count = QLabel("0")
        self.total_count.setStyleSheet("font-size: 25px; font-weight: bold;")
        row.addWidget(self.total_label)
        row.addStretch()
        row.addWidget(self.total_count)
        layout.addLayout(row)

        # Home Page Success
        self.success_message = QLabel("")
        self.success_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_message.setStyleSheet("font-size: 15px; color: green;")
        layout.addWidget(self.success_message)

        # Home Page Buttons
        button_row = QHBoxLayout()
        self.add_button = QPushButton("Add Movie")
        self.add_button.setStyleSheet("font-size: 18px;")
        self.add_button.setFixedHeight(75)
        self.view_button = QPushButton("View Movies")
        self.view_button.setStyleSheet("font-size: 18px;")
        self.view_button.setFixedHeight(75)
        button_row.addWidget(self.add_button)
        button_row.addWidget(self.view_button)
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(button_row)

    def _build_add_ui(self) -> None:
        '''
        This builds the Add Movie screen
        Contains an input field for the title, dropdowns for movie details, and buttons to navigate and save the data
        Cancel button takes user back to home screen
        Save button saves the movies data to the csv file
        '''

        layout = QVBoxLayout()
        self.add_screen.setLayout(layout)

        # Add Movie Page: Title
        home_title = QLabel("Add a Movie")
        home_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        home_title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(home_title)

        # Add Movie Page: Title and Dropdown
        movie_title = QLabel("Title")
        movie_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        movie_title.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(movie_title)

        self.input_movie = QLineEdit()
        self.input_movie.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.input_movie.setStyleSheet("font-size: 11px; font-weight: bold;")
        self.input_movie.setPlaceholderText("e.g. Interstellar")
        self.input_movie.setFixedHeight(25)
        layout.addWidget(self.input_movie)

        # Add Movie Page: Genre and Dropdown
        genre_title = QLabel("Genre")
        genre_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        genre_title.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(genre_title)

        self.drop_genre = QComboBox()
        self.drop_genre.setFixedHeight(25)
        self.drop_genre.setStyleSheet("font-size: 11px; font-weight: bold;")
        self.drop_genre.addItems([
            "Select Genre", "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family",
            "Fantasy","Horror", "Musical", "Mystery", "Romance", "Sci-fi", "Thriller", "War", "Western"
        ])
        layout.addWidget(self.drop_genre)

        # Add Movie Page: Year and Dropdown
        year_title = QLabel("Year")
        year_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        year_title.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(year_title)

        self.drop_year = QComboBox()
        self.drop_year.setFixedHeight(25)
        self.drop_year.setStyleSheet("font-size: 11px; font-weight: bold;")
        self.drop_year.addItems(["Select Year"])
        for year in range(2026, 1899, -1):
            self.drop_year.addItem(str(year))
        layout.addWidget(self.drop_year)

        # Add Movie Page: Rating and Dropdown
        rating_title = QLabel("Rating (Out of 10)")
        rating_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        rating_title.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(rating_title)

        self.drop_rating = QComboBox()
        self.drop_rating.setFixedHeight(25)
        self.drop_rating.setStyleSheet("font-size: 11px; font-weight: bold;")
        self.drop_rating.addItems([
            "Select Rating", "NA", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"
        ])
        layout.addWidget(self.drop_rating)

        # Add Movie Page: Status and Dropdown
        status_title = QLabel("Status")
        status_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        status_title.setStyleSheet("font-size: 13px; font-weight: bold;")
        layout.addWidget(status_title)

        self.drop_status = QComboBox()
        self.drop_status.setFixedHeight(25)
        self.drop_status.setStyleSheet("font-size: 11px; font-weight: bold;")
        self.drop_status.addItems([
            "Select Status", "Watched", "Not Watched"
        ])
        layout.addWidget(self.drop_status)

        # Add Movie Page: Cancel and Save Buttons
        button_row = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("font-size: 18px;")
        self.cancel_button.setFixedSize(110, 50)
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("font-size: 18px;")
        self.save_button.setFixedSize(110, 50)
        button_row.addWidget(self.cancel_button)
        button_row.addWidget(self.save_button)
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(button_row)

    def _build_list_ui(self) -> None:
        '''
        Builds a scrollable movie list screen
        The screen features a container that changes according to the movies in the list
        It's not explicitly here, but the screen appears with a random message if the movie list is empty
        Also, each movie has an X or a checkmark depending if the user has watched the movie or not
        Back button takes you to the home screen
        Edit buttons (only if there's a movie) takes you to that particular movie's edit screen
        '''
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        self.list_screen.setLayout(outer_layout)

        # https://doc.qt.io/archives/qtforpython-5/PySide2/QtWidgets/QScrollBar.html
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        self.list_layout = QVBoxLayout()
        self.list_layout.setContentsMargins(10, 10, 10, 10)
        container.setLayout(self.list_layout)

        # Movie List Page: Title
        list_title = QLabel("Movie List")
        list_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        list_title.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.list_layout.addWidget(list_title)

        # Movie List Page: Movie containers
        self.movies_container = QVBoxLayout()
        self.list_layout.addLayout(self.movies_container)

        # Movie List Page: Back Button
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("font-size: 18px;")
        self.back_button.setFixedSize(110, 60)
        self.list_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)


    def _build_edit_ui(self) -> None:
        '''
        Builds the edit screen
        This screen depicts the movie title, year, genre, and rating
        Like the Add Screen, this screen contains dropdowns about the movie details
        This screen updates the movie's info in the csv file
        Back button takes user to list screen
        Save button takes user to home screen
        '''
        layout = QVBoxLayout()
        self.edit_screen.setLayout(layout)

        # Edit Movie Page: Title
        edit_title = QLabel("Title Details")
        edit_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        edit_title.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(edit_title)

        # Edit Movie Page: Placeholder Movie Details
        self.edit_movie_title = QLabel("Movie Title (XXXX)")
        self.edit_movie_title.setWordWrap(True)
        self.edit_movie_title.setFixedWidth(250)
        self.edit_movie_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.edit_movie_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.edit_movie_title)

        self.edit_movie_genre = QLabel("Genre - Rating/10")
        self.edit_movie_genre.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.edit_movie_genre.setStyleSheet("font-size: 17px; font-weight: bold;")
        layout.addWidget(self.edit_movie_genre)

        # Edit Movie Page: Year Dropdown
        row = QHBoxLayout()
        self.edit_year_label = QLabel("Year")
        self.edit_year_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.edit_year_dropdown = QComboBox()
        self.edit_year_dropdown.setStyleSheet("font-size: 15px")
        self.edit_year_dropdown.setFixedWidth(140)
        self.edit_year_dropdown.addItems(["XXXX"])
        for year in range(2026, 1899, -1):
            self.edit_year_dropdown.addItem(str(year))

        row.addWidget(self.edit_year_label)
        row.addStretch()
        row.addWidget(self.edit_year_dropdown)
        layout.addLayout(row)


        # Edit Movie Page: Genre Dropdown
        row = QHBoxLayout()
        self.edit_genre_label = QLabel("Genre")
        self.edit_genre_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.edit_genre_dropdown = QComboBox()
        self.edit_genre_dropdown.setStyleSheet("font-size: 15px")
        self.edit_genre_dropdown.setFixedWidth(140)
        self.edit_genre_dropdown.addItems([
            "Genre", "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family",
            "Fantasy","Horror", "Musical", "Mystery", "Romance", "Sci-fi", "Thriller", "War", "Western"
        ])

        row.addWidget(self.edit_genre_label)
        row.addStretch()
        row.addWidget(self.edit_genre_dropdown)
        layout.addLayout(row)

        # Edit Movie Page: Status Dropdown
        row = QHBoxLayout()
        self.edit_status_label = QLabel("Status")
        self.edit_status_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.edit_status_dropdown = QComboBox()
        self.edit_status_dropdown.setStyleSheet("font-size: 15px")
        self.edit_status_dropdown.setFixedWidth(140)
        self.edit_status_dropdown.addItems([
            "Status", "Watched", "Not Watched"
        ])

        row.addWidget(self.edit_status_label)
        row.addStretch()
        row.addWidget(self.edit_status_dropdown)
        layout.addLayout(row)

        # Edit Movie Page: Rating Dropdown
        row = QHBoxLayout()
        self.edit_rating_label = QLabel("Rating")
        self.edit_rating_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.edit_rating_dropdown = QComboBox()
        self.edit_rating_dropdown.setStyleSheet("font-size: 15px")
        self.edit_rating_dropdown.setFixedWidth(140)
        self.edit_rating_dropdown.addItems([
            "Rating", "NA", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"
        ])

        row.addWidget(self.edit_rating_label)
        row.addStretch()
        row.addWidget(self.edit_rating_dropdown)
        layout.addLayout(row)

        # Edit Movie Page: Back and Save Button
        button_row = QHBoxLayout()
        self.edit_back_button = QPushButton("Back")
        self.edit_back_button.setStyleSheet("font-size: 18px;")
        self.edit_back_button.setFixedSize(110, 50)
        self.edit_save_button = QPushButton("Save")
        self.edit_save_button.setStyleSheet("font-size: 18px;")
        self.edit_save_button.setFixedSize(110, 50)
        button_row.addWidget(self.edit_back_button)
        button_row.addWidget(self.edit_save_button)
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(button_row)
