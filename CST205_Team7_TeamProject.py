
import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import (QPixmap, QImage, QIcon)
from PIL import Image


my_new_dict = {
"Red":{"RGB":"(255,0,0)","HEX":"#FF0000"},
"Blue":{"RGB":"(0,0,255)","HEX":"#0000FF"},
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
        self.song_name = QLabel()
        self.song_name.setText("Select a song to Play!!!")
        # label to display artist name
        self.artist_name = QLabel()

        # Dislay image for the song if any
        self.image = QLabel()





        inner_v_layout_song_info = QVBoxLayout()
        inner_v_layout_song_info.addWidget(self.song_name)
        inner_v_layout_song_info.addWidget(self.artist_name)
        # inner_v_layout_song_info.addWidget(self.song_list)
        inner_v_layout_disp_image = QVBoxLayout()
        inner_v_layout_disp_image.addWidget(self.image)


        outer_h_layout_contain_inner = QHBoxLayout()
        outer_h_layout_contain_inner.addLayout(inner_v_layout_song_info)
        outer_h_layout_contain_inner.addLayout(inner_v_layout_disp_image)




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
        outer_v_layout.addLayout(outer_h_layout_contain_inner)
        outer_v_layout.addWidget(self.song_list)
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
        self.song_name.setText("Song name here "+my_text)
        self.artist_name.setText("Artist name here!!")
        pixmap = QPixmap('images/my_image.jpg')
        pixmap = pixmap.scaledToWidth(150)
        self.image.setPixmap(pixmap)
        # self.hex_out_label.setText(my_new_dict[my_text]["HEX"])
        # self.rgb_out_label.setText(my_new_dict[my_text]["RGB"])

        # print(my_text)

app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
