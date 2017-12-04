
import sys
import random
from PIL import Image
import pygame
import datetime
from pygame import mixer
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QSlider, QLineEdit, QHBoxLayout, QVBoxLayout,
                                QComboBox, QGroupBox, QRadioButton)
from PyQt5.QtCore import (pyqtSlot, Qt)
from PyQt5.QtGui import (QPixmap, QImage, QIcon)



my_new_dict = {
    "Pick a song":{
        "artist_name" : "",
        "song_path" : "",
        "img_path" : "",
        "song_length" : ""
    },
    "Still Feelin It":{
        "artist_name" : "Mistah F.A.B.",
        "song_path":"songs/Still-Feelin-It_Mix.mp3",
        "img_path":"images/stf_img.jpg",
        "song_length" : 86
    },
    "Random":{
        "artist_name" : "Unknown",
        "song_path":"songs/Track01.mp3",
        "img_path":"images/my_img.jpg",
        "song_length" : 40
    }
}

button_list =["Rewind","Play","Pause","Next","Stop"]


class Window(QWidget):
    def __init__(self):
        super().__init__()

        #inner vlayout
        # add QComboBox for the song list
        self.song_list = QComboBox()
        self.song_list.addItems(my_new_dict.keys())
        self.song_name = QLabel("Select a song to Play!!!")
        # self.song_name.setText("Select a song to Play!!!")
        # label to display artist name
        self.artist_name = QLabel()
        # Dislay image for the song if any
        self.cover_image = QLabel()

        inner_v_layout_song_info = QVBoxLayout()
        inner_v_layout_song_info.addWidget(self.song_name)
        inner_v_layout_song_info.addWidget(self.artist_name)
        # inner_v_layout_song_info.addWidget(self.song_list)
        inner_v_layout_disp_image = QVBoxLayout()
        inner_v_layout_disp_image.addWidget(self.cover_image)

        # Music Image
        self.music_image = QLabel()
        music_pic = QPixmap("images/music.png")
        music_pic = music_pic.scaledToWidth(150)
        self.music_image.setPixmap(music_pic)

        #Volume Controls
        self.volume_label = QLabel("Volume: ")
        self.vol_slider = QSlider()
        self.vol_slider.setOrientation(Qt.Horizontal)
        self.vol_slider.setRange(0,100)
        self.vol_slider.setValue(5)
        self.vol_slider.valueChanged.connect(self.vol_change)
        self.mute_label = QLabel("Mute: ")
        self.mute_button = QRadioButton()
        self.mute_button.toggled.connect(self.mute_me)
        #layout for volume Controls
        inner_h_layout_volume_controls = QHBoxLayout()
        inner_h_layout_volume_controls.addSpacing(50)
        inner_h_layout_volume_controls.addWidget(self.volume_label)
        inner_h_layout_volume_controls.addSpacing(10)
        inner_h_layout_volume_controls.addWidget(self.vol_slider)
        inner_h_layout_volume_controls.addSpacing(50)
        inner_h_layout_volume_controls.addWidget(self.mute_label)
        inner_h_layout_volume_controls.addSpacing(10)
        inner_h_layout_volume_controls.addWidget(self.mute_button)
        inner_h_layout_volume_controls.addSpacing(50)




        # layout for song info and image
        outer_h_layout_contain_inner = QHBoxLayout()
        outer_h_layout_contain_inner.addWidget(self.music_image)
        outer_h_layout_contain_inner.addLayout(inner_v_layout_song_info)
        outer_h_layout_contain_inner.addLayout(inner_v_layout_disp_image)
        # layout for Buttons
        self.outer_h_layout_contain_buttons = QHBoxLayout()
        # Buttons
        for i in button_list:
            my_button = QPushButton(i)
            my_button.setStyleSheet("background-color: #B6C6D1, border-style: outset")
            my_button.clicked.connect(self.on_click)
            self.outer_h_layout_contain_buttons.addWidget(my_button)
        # Layout for song song_progress
        outer_h_layout_contain_progress = QHBoxLayout()
        # Song progress tracker
        self.song_progress = QLabel()
        self.song_max = QLabel("/0:00:00")
        outer_h_layout_contain_progress.addWidget(self.song_progress)
        outer_h_layout_contain_progress.addWidget(self.song_max)

        #main v layout
        main_v_layout = QVBoxLayout()
        main_v_layout.addLayout(outer_h_layout_contain_inner)
        main_v_layout.addWidget(self.song_list)
        main_v_layout.addLayout(self.outer_h_layout_contain_buttons)
        # add volume slider here
        main_v_layout.addLayout(inner_h_layout_volume_controls)
        # main_v_layout.addWidget(self.vol_slider)
        main_v_layout.addLayout(outer_h_layout_contain_progress)
        # outer_v_layout.addLayout(inner_h_layout)
        self.setLayout(main_v_layout)

        self.song_list.currentIndexChanged.connect(self.update_ui)

        # first two arguments for position on screen
        # second two arguments for dimensions of window (width, height)
        # self.setGeometry(200, 200, 600, 400)

        self.setWindowTitle("My Player")
        self.progress_of_song()
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.progress_of_song)
        self.my_timer.start(60)
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
            self.song_max.setText("/" + str(datetime.timedelta(seconds=my_new_dict[my_text]["song_length"])))
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.set_allowed(pygame.USEREVENT)
            pygame.mixer.music.play()
            if(self.mute_button.isChecked()):
                pygame.mixer.music.set_volume(0.0)
            else:
                pygame.mixer.music.set_volume(self.vol_slider.value()/100)

    @pyqtSlot()
    def on_click(self):
        button = self.sender()
        if(pygame.init()):
                # widget.setStyleSheet("background-color: #B6C6D1")
            if(button.text()=="Pause"):
                pygame.mixer.music.pause()
            elif(button.text()=="Play"):
                pygame.mixer.music.unpause()
            elif(button.text()=="Stop"):
                pygame.mixer.music.stop()
                self.song_name.setText("Select a song to Play!!!")
                self.artist_name.setText("")
                index = self.song_list.findText("Pick a song")
                self.song_list.setCurrentIndex(index)
                self.song_max.setText("/0:00:00")
                self.cover_image.clear()
            elif(button.text()=="Next"):
                index = int(self.song_list.currentIndex()) + 1
                if (index < len(my_new_dict)):
                    self.song_list.setCurrentIndex(index)


    def vol_change(self):
        if(pygame.init()):
            my_vol = self.vol_slider.value()/100
            if(self.mute_button.isChecked() == False):
                pygame.mixer.music.set_volume(my_vol)

    def mute_me(self):
        if(pygame.init()):
            if(self.mute_button.isChecked()):
                pygame.mixer.music.set_volume(0.0)
            else:
                pygame.mixer.music.set_volume(self.vol_slider.value()/100)

    def progress_of_song(self):
        if(pygame.init()):
            current_time = int(pygame.mixer.music.get_pos() / 1000)
            self.song_progress.setText(str(datetime.timedelta(seconds=current_time)))
            self.update()


app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
pygame.mixer.music.quit()
