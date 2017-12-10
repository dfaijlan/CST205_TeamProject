########## HEADER COMMENTS
# Course: CST205 - Multimedia Programming and Design
# Title: MPy3 Player
# Abstract: MP3 player created with python to play songs. User can pick a song,
#           skip to the next song, stop the song, etc.
# Authors: Gerardo Alcaraz, Dominic Fajilan, Yashkaran Singh
# Date: 12/11/17
#
# Github link: https://github.com/dfaijlan/CST205_TeamProject
##########

import sys
import random
from PIL import Image
import pygame
import datetime
from pygame import mixer
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import (pyqtSlot, Qt)
from PyQt5.QtGui import *

##### All three of us created the dictionaries
my_new_dict = {
    "Pick a song":{
        "artist_name" : "",
        "song_path" : "",
        "img_path" : "",
        "song_length" : ""
    },
    "Still Feelin It":{
        "artist_name" : "Mistah F.A.B.",
        "album name" : "Son of a Pimp",
        "song_path":"songs/Still-Feelin-It_Mix.mp3",
        "img_path":"images/stf_img.jpg",
        "song_length" : 86
    },
    "2" : {
        "artist_name" : "H.E.R.",
        "album name" : "H.E.R.",
        "song_path" : "songs/HER-2.mp3",
        "img_path":"images/her_img.jpg",
        "song_length" : 190
    },
    "Frozen" : {
        "artist_name" : "Sabrina Claudio",
        "album name" : "About Time",
        "song_path" : "songs/Frozen.mp3",
        "img_path":"images/frozen_img.jpg",
        "song_length" : 245
    }
}

button_list =["Back","Play","Pause","Next","Stop"]
#####

class Window(QWidget):
    ########## Yashkaran created most of the GUI, Dominic added song_progress /
    ########## song_max and the timer loop
    def __init__(self):
        super().__init__()

        #inner vlayout
        
        #self.myFont = QtGui
        
        #self.myFont = QtGui.QFont()
        
        # add QComboBox for the song list
        self.song_list = QComboBox()
        self.song_list.addItems(my_new_dict.keys())
        self.song_name = QLabel("Select a Song to Play!!!")

        # label to display artist name
        self.artist_name = QLabel()

        # Dislay image for the song if any
        self.cover_image = QLabel()

        # Display album name
        self.album_name = QLabel()

        inner_v_layout_song_info = QVBoxLayout()
        inner_v_layout_song_info.addWidget(self.song_name)
        inner_v_layout_song_info.addWidget(self.artist_name)

        inner_v_layout_song_info.addWidget(self.album_name)
        inner_v_layout_disp_image = QVBoxLayout()

        # Music Image
        self.music_image = QLabel()
        music_pic = QPixmap("images/music.png")
        # music_pic = music_pic.scaledToWidth(600)
        self.music_image.setPixmap(music_pic)

        #Volume Controls
        self.volume_label = QLabel("<h5>Volume: </h5>")
        self.vol_slider = QSlider()
        self.vol_slider.setOrientation(Qt.Horizontal)
        self.vol_slider.setRange(0,100)
        self.vol_slider.setValue(5)
        self.vol_slider.valueChanged.connect(self.vol_change)
        self.mute_label = QLabel("<h5>Mute: </h5>")
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
        self.button_map = {}
        for i in button_list:
            my_button = QPushButton(i)
            my_button.setStyleSheet("background-color: #FFFFFF")
            my_button.clicked.connect(self.on_click)
            # self.saveButton(my_button)
            self.button_map[my_button.text()] = my_button
            self.outer_h_layout_contain_buttons.addWidget(my_button)

        # Layout for song song_progress
        outer_h_layout_contain_progress = QHBoxLayout()
        
        #Add Stretch to move the progress bar/text to the far right
        outer_h_layout_contain_progress.addStretch(1)

        # Song progress tracker
        self.song_progress = QLabel()
        self.song_max = QLabel("/0:00:00")
        
        outer_h_layout_contain_progress.addWidget(self.song_progress)
        outer_h_layout_contain_progress.addWidget(self.song_max)
        
        #Add Stretch on the right to move the progress bar/text to the center by stretching it from the right side. Aligning it.
        outer_h_layout_contain_progress.addStretch(1)

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

        self.setWindowTitle("My Player")
        self.progress_of_song()
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.progress_of_song)
        self.my_timer.start(60)


    @pyqtSlot()
    ########## This updates the GUI whenever the user changes the song
    ##### Yashkaran made the buttons and general layout
    ##### Gerardo was able to make the songs play and made it display alb
    ##### Dominic set the progress of the song
    def update_ui(self):

        my_text = self.song_list.currentText()

        #Reset button colors
        self.reset_button_color()
        pygame.mixer.quit()
        if (my_text != "Pick a song"):
            # starts the song, displays all information of song, collaborated on by all three members
            self.song_name.setText("<h5>Song:</h5> <br>" + f"<h4>{my_text}</h4>")
            self.artist_name.setText("<h5>Artist:</h5> <br>" + f'<h4>{my_new_dict[my_text]["artist_name"]}</h4>')
            self.album_name.setText("<h5>Album:</h5> <br>" + f'<h4>{my_new_dict[my_text]["album name"]}</h4>')
            pixmap = QPixmap(my_new_dict[my_text]["img_path"])
            pixmap = pixmap.scaledToWidth(600)
            self.music_image.setPixmap(pixmap)
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
    ########## Whenever the user clicks a button, such as stop or play, an event will happen
    ##### Yashkaran made the colors of the buttons change, the play, pause, and stop Buttons
    ##### Dominic made the back, next, and also worked on the stop button
    def on_click(self):
        button = self.sender()
        if(pygame.init()):
            # Revert back color to default
            self.reset_button_color()
            # Change color of the pressed button
            self.button_map[button.text()].setStyleSheet("background-color: #A6C6D1")
            # pauses the music
            if(button.text()=="Pause"):
                pygame.mixer.music.pause()
            # either starts the music from the beginning or go back a song
            elif(button.text()=="Back"):
                current_time = int(pygame.mixer.music.get_pos() / 1000)
                # if the time of the song is longer than 3 seconds, go back tothe beginning of the song
                if (current_time <=3):
                    index = int(self.song_list.currentIndex()) - 1
                    if (index > 0):
                        self.song_list.setCurrentIndex(index)
                    else:
                        self.song_list.setCurrentIndex(len(my_new_dict) -1)
                # else go back a song
                else:
                    my_text = self.song_list.currentText()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(my_new_dict[my_text]["song_path"])
                    pygame.mixer.music.play()
            elif(button.text()=="Play"):
                pygame.mixer.music.unpause()
            # stops the song, and reverts the screen back to default
            elif(button.text()=="Stop"):
                pygame.mixer.music.stop()
                self.song_name.setText("Select a song to Play!!!")
                index = self.song_list.findText("Pick a song")
                self.artist_name.setText("")
                self.album_name.setText("")
                self.song_list.setCurrentIndex(index)
                self.song_max.setText("/0:00:00")
                music_pic = QPixmap("images/music.png")
                music_pic = music_pic.scaledToWidth(600)
                self.music_image.setPixmap(music_pic)
            # picks next song in list
            elif(button.text()=="Next"):
                index = int(self.song_list.currentIndex()) + 1
                if (index < len(my_new_dict)):
                    self.song_list.setCurrentIndex(index)
                else:
                    self.song_list.setCurrentIndex(1)

    # changes the volume, created by Yashkaran
    def vol_change(self):
        if(pygame.init()):
            my_vol = self.vol_slider.value()/100
            if(self.mute_button.isChecked() == False):
                pygame.mixer.music.set_volume(my_vol)

    # mutes the song, created by Yashkaran
    def mute_me(self):
        if(pygame.init()):
            if(self.mute_button.isChecked()):
                pygame.mixer.music.set_volume(0.0)
            else:
                pygame.mixer.music.set_volume(self.vol_slider.value()/100)

    # displays the progess of the song, created by Dominic
    def progress_of_song(self):
        if(pygame.init()):
            current_time = int(pygame.mixer.music.get_pos() / 1000)
            self.song_progress.setText(str(datetime.timedelta(seconds=current_time)))
            self.update()

    # resets the button color, created by Yashkaran
    def reset_button_color(self):
        for widget in self.button_map:
            self.button_map[widget].setStyleSheet("background-color: #FFFFFF")

app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
pygame.mixer.music.quit()
