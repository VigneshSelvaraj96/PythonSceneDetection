import json
import os.path
from datetime import datetime, timedelta

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QSlider, QLabel, QStyle, QSizePolicy, QFileDialog, QTreeWidget, QTreeWidgetItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import os

dirname = os.path.dirname(__file__)

# data = {"00:00:00.000": {"00:00:00.000": [0.0, 14.256394557823128, 15.401972789115646, 17.77392290249433, 20.260997732426304, 21.783242630385487, 24.66780045351474, 31.200226757369613], "00:00:36.000": [36.0], "00:00:37.700": [37.7, 91.47480725623583, 98.6436507936508], "00:01:48.133": [108.133], "00:01:50.067": [110.067]}, "00:01:58.200": {"00:01:58.200": [118.2, 131.9855328798186, 134.27607709750566, 136.5936961451247], "00:02:24.867": [144.867], "00:02:41.467": [161.467, 162.75112698412698, 163.82938095238097, 171.15396145124717, 183.339947845805], "00:03:06.633": [186.633]}, "00:03:24.667": {"00:03:24.667": [204.667, 206.7152993197279], "00:03:30.067": [210.067]}, "00:03:48.533": {"00:03:48.533": [228.533], "00:03:54.900": [234.9]}, "00:04:13.033": {"00:04:13.033": [253.033, 254.4427052154195]}, "00:04:15.633": {"00:04:15.633": [255.633], "00:04:21.167": [261.167]}, "00:04:29.333": {"00:04:29.333": [269.333], "00:04:35.633": [275.633]}}


json_file = open(os.path.join(dirname, './Data/dict_of_start_times.json'))
data = json.load(json_file)


def convert_time_to_milli(time_component):
    return ((float(time_component[0]) * 60 + float(time_component[1])) * 60 + float(time_component[2])) * 1000


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interactive Media Player")
        self.setGeometry(0, 0, 1600, 900)

        self.section_map = {}
        self.reverse_map = {}
        self.object_map = {}    # timestamp -> List of QTreeWidgetItem

        self.init_ui()
        self.open_file()

        # p = self.palette()
        # p.setColor(QPalette.Window, Qt.black)
        # self.setPalette(p)

        self.show()

    def open_file(self):
        # filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        filename = os.path.join(dirname, './Data/InputVideo.mp4')
        if filename != '':
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.play_pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
            self.play_video()

    def play_video(self):

        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_pause_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.media_player.play()
            self.play_pause_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def stop_video(self):
        print('Position == ', self.media_player.position())
        position = self.media_player.position()
        break_point = 'Scene1'
        for key in self.reverse_map.keys():
            print(key)
            if position <= key:
                break
            else:
                break_point = self.reverse_map[key]

        new_pos = self.section_map[break_point.split(' ')[0]]
        self.media_player.setPosition(int(new_pos))
        self.media_player.pause()
        self.play_pause_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    # def update_tree_item(self, position, item):
    #
    #     item.setSelected(True)
    #     for i in range(item.childCount()):
    #         child = item.child(i)
    #         print(child.text())
    #         self.update_selected_tree_item(position, item)

    def slider_position_changed(self, position):
        # position is time value in milliseconds
        self.slider.setValue(position)
        # print(self.media_player.duration(), "  ", position)
        self.paint_item(position)
        # self.update_tree_item(position, item)

    def paint_item(self, position):
        for timestamp in self.object_map.keys():
            if timestamp <= position:
                for item in self.object_map.get(timestamp):
                    item.setForeground(0, QtGui.QBrush(QtGui.QColor("#00d1b2")))
            else:
                for item in self.object_map.get(timestamp):
                    item.setForeground(0, QtGui.QBrush(QtGui.QColor("#000000")))

    def slider_duration_changed(self, duration):
        # duration itself is the total time of the video content in milliseconds
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(int(position))

    def insert_into_object_map(self, timestamp, item):
        if timestamp not in self.object_map.keys():
            self.object_map[timestamp] = [item]
        else:
            self.object_map[timestamp].append(item)

    def populate_tree_widget(self):

        parents = [k for k in data.keys()]
        time_format = "%H:%M:%S.%f"
        idx = 1
        for scene in parents:
            time_component = scene.split(':')
            time_milli = convert_time_to_milli(time_component)

            key1 = 'Scene' + str(idx)
            self.section_map[key1] = time_milli
            self.reverse_map[time_milli] = key1

            parent_it = QTreeWidgetItem([key1])
            self.insert_into_object_map(time_milli, parent_it)
            idx1 = 1
            self.tree.addTopLevelItem(parent_it)
            for shot in data[scene]:
                time_component = shot.split(':')
                time_milli = convert_time_to_milli(time_component)
                key2 = key1 + ' Shot' + str(idx1)
                self.section_map[key2] = time_milli
                self.reverse_map[time_milli] = key2

                it = QTreeWidgetItem([key2])
                self.insert_into_object_map(time_milli, it)

                idx1 += 1
                idx2 = 1
                parent_it.addChild(it)
                for subshot in data[scene][shot]:
                    time_milli = float(subshot) * 1000
                    key3 = key2 + ' Subshot' + str(idx2)
                    self.section_map[key3] = time_milli
                    self.reverse_map[time_milli] = key3

                    sit = QTreeWidgetItem([key3])
                    self.insert_into_object_map(time_milli, sit)
                    it.addChild(sit)
                    idx2 += 1

            idx += 1

        # print(len(set(self.section_map.values())))
        print(self.object_map)
        self.tree.expandAll()

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        key = it.text(col)
        if key in self.section_map:
            self.set_position(self.section_map[key])
        # self.set_position(6000)

    def init_ui(self):
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Video widget
        video_widget = QVideoWidget()

        # Create open Button
        # open_btn = QPushButton('Open Video')
        # open_btn.clicked.connect(self.open_file)

        # Play/Pause Button
        self.play_pause_btn = QPushButton()
        self.play_pause_btn.setEnabled(False)
        self.play_pause_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_pause_btn.clicked.connect(self.play_video)

        # Stop Button
        self.stop_btn = QPushButton()
        self.stop_btn.setEnabled(False)
        self.stop_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_btn.clicked.connect(self.stop_video)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Error Label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Tree Widget
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.populate_tree_widget()
        self.tree.itemClicked.connect(self.onItemClicked)

        # Hbox layout
        hboxlayout = QHBoxLayout()
        hboxlayout.setContentsMargins(0, 0, 0, 0)
        # hboxlayout.addWidget(open_btn)
        hboxlayout.addWidget(self.slider)
        hboxlayout.addWidget(self.play_pause_btn)
        hboxlayout.addWidget(self.stop_btn)

        # Vbox layout
        vboxlayout = QVBoxLayout()
        vboxlayout.addWidget(video_widget)
        vboxlayout.addLayout(hboxlayout)
        vboxlayout.addWidget(self.label)

        # Root HBox layout
        hboxrootlayout = QHBoxLayout()
        hboxrootlayout.addWidget(self.tree, 2)
        hboxrootlayout.addLayout(vboxlayout, 8)

        self.setLayout(hboxrootlayout)
        self.media_player.setVideoOutput(video_widget)

        # Media player signals
        self.media_player.positionChanged.connect(self.slider_position_changed)
        self.media_player.durationChanged.connect(self.slider_duration_changed)
        self.media_player.error.connect(self.handle_errors)

    def handle_errors(self):
        self.play_pause_btn.setEnabled(False)
        self.label.setText("Error: " + self.media_player.errorString())


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
