
import sys
import random
import pygame
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QSlider, QLineEdit, QHBoxLayout, QVBoxLayout,
                                QComboBox, QGroupBox)
from PyQt5.QtCore import (pyqtSlot, Qt)
from PyQt5.QtGui import (QPixmap, QImage, QIcon)
from PyQt5.QtMultimedia import QMediaPlayer
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
        "song_path":"songs/Still-Feelin-It_Mix.wav",
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

        #Volume Slider
        self.vol_slider = QSlider()
        self.vol_slider.setOrientation(Qt.Horizontal)
        self.vol_slider.setRange(0,10)
        self.vol_slider.setValue(5)
        # self.vol_slider.setTickPosition(QSlider.TicksBelow)
        # self.vol_slider.setTickInterval(5)
        self.vol_slider.valueChanged.connect(self.vol_change)
        # self.vol_slider.size(100,100)

        #volume control
        self.my_volume = QMediaPlayer()
        # self.my_volume.setVolume(50)



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

        #main v layout
        main_v_layout = QVBoxLayout()
        main_v_layout.addLayout(outer_h_layout_contain_inner)
        main_v_layout.addWidget(self.song_list)
        # add volume slider here
        main_v_layout.addWidget(self.vol_slider)
        main_v_layout.addLayout(outer_h_layout_contain_buttons)
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
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.set_allowed(pygame.USEREVENT)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.5)
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

    @pyqtSlot()
    def vol_change(self):
        my_text = self.vol_slider.value()
        my_text = my_text/10
        # pygame.mixer.music.set_volume(my_text)
        # print(pygame.mixer.music.get_volume())
        # self.my_volume.setVolume(my_text)
        print(my_text)


app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
pygame.mixer.quit()
