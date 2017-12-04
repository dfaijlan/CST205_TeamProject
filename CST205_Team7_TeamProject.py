
import sys
import random
import pygame
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QSlider, QLineEdit, QHBoxLayout, QVBoxLayout,
                                QComboBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import (QPixmap, QImage, QIcon)
from PIL import Image
from pygame import mixer

my_new_dict = {
    "Pick a song":{
        "artist_name" : "",
        "song_path" : "",
        "img_path" : ""
    },
    "Still Feelin It":{
        "artist_name" : "Mistah F.A.B.",
        "song_path":"songs/Still-Feelin-It_Mix.mp3",
        "img_path":"images/stf_img.jpg"
    },
    "Random":{
        "artist_name" : "Unknown",
        "song_path":"songs/Track01.mp3",
        "img_path":"images/my_img.jpg"
    }
}

button_list =["Rewind","Play","Pause","Forward","Stop"]


class Window(QWidget):
    def __init__(self):
        super().__init__()

        #inner vlayout
        # add QComboBox for the song list
        self.song_list = QComboBox()
        self.song_list.addItems(my_new_dict.keys())
        # add label to display current playing song name
        self.song_name = QLabel()
        self.song_name.setText("Select a song to Play!!!")
        # label to display artist name
        self.artist_name = QLabel()
        # Dislay image for the song if any
        self.cover_image = QLabel()


        # Music Image
        self.music_image = QLabel()
        music_pic = QPixmap("images/music.png")
        music_pic = music_pic.scaledToWidth(150)
        self.music_image.setPixmap(music_pic)


        inner_v_layout_song_info = QVBoxLayout()
        inner_v_layout_song_info.addWidget(self.song_name)
        inner_v_layout_song_info.addWidget(self.artist_name)
        # inner_v_layout_song_info.addWidget(self.song_list)
        inner_v_layout_disp_image = QVBoxLayout()
        inner_v_layout_disp_image.addWidget(self.cover_image)

        # layout for song info and image
        outer_h_layout_contain_inner = QHBoxLayout()
        outer_h_layout_contain_inner.addWidget(self.music_image)
        outer_h_layout_contain_inner.addLayout(inner_v_layout_song_info)
        outer_h_layout_contain_inner.addLayout(inner_v_layout_disp_image)
        # layout for Buttons
        outer_h_layout_contain_buttons = QHBoxLayout()
        # Buttons
        for i in button_list:
            my_button = QPushButton(i)
            my_button.setStyleSheet("background-color: #5280c9")
            my_button.clicked.connect(self.on_click)
            outer_h_layout_contain_buttons.addWidget(my_button)
        # Layout for song song_progress
        outer_h_layout_contain_progress = QHBoxLayout()
        # Song progress tracker
        self.song_progress = QLabel()
        self.song_max = QLabel()
        outer_h_layout_contain_progress.addWidget(self.song_progress)
        outer_h_layout_contain_progress.addWidget(self.song_max)

        #main v layout
        main_v_layout = QVBoxLayout()
        main_v_layout.addLayout(outer_h_layout_contain_inner)
        main_v_layout.addWidget(self.song_list)
        main_v_layout.addLayout(outer_h_layout_contain_buttons)
        main_v_layout.addLayout(outer_h_layout_contain_progress)
        # outer_v_layout.addLayout(inner_h_layout)
        self.setLayout(main_v_layout)

        self.song_list.currentIndexChanged.connect(self.update_ui)

        # first two arguments for position on screen
        # second two arguments for dimensions of window (width, height)
        # self.setGeometry(200, 200, 600, 400)

        self.setWindowTitle("My Player")

        # self.resize(pixmap.width(),pixmap.height())


    @pyqtSlot()
    def update_ui(self):
        my_text = self.song_list.currentText()
        pygame.mixer.quit()
        if (my_text != "Pick a song"):
            self.song_name.setText(my_text)
            self.artist_name.setText(my_new_dict[my_text]["artist_name"])
            pixmap = QPixmap(my_new_dict[my_text]["img_path"])
            pixmap = pixmap.scaledToWidth(150)
            self.cover_image.setPixmap(pixmap)
            pygame.mixer.init()
            pygame.init()
            pygame.mixer.music.load(my_new_dict[my_text]["song_path"])
            self.song_max.setText("/" + a.get_length())
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.set_allowed(pygame.USEREVENT)
            pygame.mixer.music.play()
            pygame.event.wait()

    @pyqtSlot()
    def on_click(self):
        button = self.sender()
        if(button.text()=="Pause"):
            # button.setStyleSheet("background-color: #447c43")
            pygame.mixer.music.pause()
        elif(button.text()=="Play"):
            pygame.mixer.music.unpause()
        elif(button.text()=="Stop"):
            pygame.mixer.music.stop()




app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
pygame.mixer.quit()
