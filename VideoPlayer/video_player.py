from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QStyle, QSizePolicy, QFileDialog, QTreeWidget, QTreeWidgetItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interactive Media Player")
        self.setGeometry(0, 0, 1024, 720)
        
        self.init_ui()
        
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.show()


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

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
        self.media_player.stop()
        self.play_pause_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))



    def slider_position_changed(self, position):
        # position is time value in milliseconds
        self.slider.setValue(position)
        print(self.media_player.duration(), "  ", position)


    def slider_duration_changed(self, duration):
        # duration itself is the total time of the video content in milliseconds
        self.slider.setRange(0, duration)
        
    

    def set_position(self, position):
        self.media_player.setPosition(position)

    
    def populate_tree_widget(self):
        for i in range(4):
            parent_it = QTreeWidgetItem(["{}-{}gdsgddhjdkhgdfgkhgfsjfhxvnbmcbn,cmghcgjg".format(i, l) for l in range(2)])
            self.tree.addTopLevelItem(parent_it)
            for j in range(5):
                it =  QTreeWidgetItem(["{}-{}-{}".format(i, j, l) for l in range(2)])
                parent_it.addChild(it)
        self.tree.expandAll()

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        print(it, col, it.text(col))
        # self.set_position(6000)
    
    def init_ui(self):
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Video widget
        video_widget = QVideoWidget()

        # Create open Button
        open_btn = QPushButton('Open Video')
        open_btn.clicked.connect(self.open_file)

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
        self.tree.setMaximumWidth(300)
    

        # Hbox layout
        hboxlayout = QHBoxLayout()
        hboxlayout.setContentsMargins(0, 0, 0, 0)
        hboxlayout.addWidget(open_btn)
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
        hboxrootlayout.addWidget(self.tree)
        hboxrootlayout.addLayout(vboxlayout)
        

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