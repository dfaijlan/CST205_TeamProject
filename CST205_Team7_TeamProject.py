
import sys
import random
import pygame
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import (QPixmap, QImage, QIcon)
from PIL import Image
from pygame import mixer

my_new_dict = {
"Still Feelin It":{"song_path":"songs/Still-Feelin-It_Mix.wav","img_path":"images/stf_img.jpg"},
"Random":{"song_path":"songs/Track01.mp3","img_path":"images/my_img.jpg"},
"Green":{"RGB":"(0,255,0)","HEX":"#00FF00"},
"Vermilion":{"RGB":"(227,66,52)","HEX":"#e34234"}
}




class Window(QWidget):
    def __init__(self):
        super().__init__()

        #inner vlayout
        # add QComboBox for the song list
        self.song_list = QComboBox()
        self.song_list.addItems(my_new_dict.keys())
        # add label to display current playing song name
        self.main_label = QLabel()
        self.main_label.setText("Select a song to Play!!!")
        # Dislay image for the song if any
        self.image = QLabel()





        inner_v_layout = QVBoxLayout()
        inner_v_layout.addWidget(self.main_label)
        inner_v_layout.addWidget(self.song_list)
        inner_v_layout.addWidget(self.image)

        #inner hlayout
        # self.rgb_label = QLabel()
        # self.rgb_label.setText("RGB:")
        # self.rgb_out_label = QLabel()
        # self.hex_label = QLabel()
        # self.hex_label.setText("Hex:")
        # self.hex_out_label = QLabel()

        # self.rgb_out_label.setText()
        # self.rgb_out_label.setalignment()
        # self.hex_out_label.setText()
        # inner_h_layout = QHBoxLayout()
        # inner_h_layout.addWidget(self.rgb_label)
        # inner_h_layout.addWidget(self.rgb_out_label)
        # inner_h_layout.addWidget(self.hex_label)
        # inner_h_layout.addWidget(self.hex_out_label)

        #outer v layout
        outer_v_layout = QVBoxLayout()
        outer_v_layout.addLayout(inner_v_layout)
        # outer_v_layout.addLayout(inner_h_layout)
        self.setLayout(outer_v_layout)

        self.song_list.currentIndexChanged.connect(self.update_ui)
        # first two arguments for position on screen
        # second two arguments for dimensions of window (width, height)
        # self.setGeometry(200, 200, 600, 400)

        self.setWindowTitle("My Player")


        # self.resize(pixmap.width(),pixmap.height())


    @pyqtSlot()
    def update_ui(self):
        my_text = self.song_list.currentText()
        self.main_label.setText(my_text)
        pixmap = QPixmap(my_new_dict[my_text]["img_path"])
        pixmap = pixmap.scaledToWidth(150)
        self.image.setPixmap(pixmap)
        # self.hex_out_label.setText(my_new_dict[my_text]["HEX"])
        # self.rgb_out_label.setText(my_new_dict[my_text]["RGB"])

        # print(my_text)
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load(my_new_dict[my_text]["song_path"])
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.event.set_allowed(pygame.USEREVENT)
        pygame.mixer.music.play()
        pygame.event.wait()

app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
