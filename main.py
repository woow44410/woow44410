# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#include <QListWidget>
#include <QListWidgetItem>
#include <QLabel>
#include <QUrl>
#include <QDesktopServices>
import requests
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QListView,QMessageBox
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QStringListModel
from PyQt5 import QtGui
from PyQt5 import QtCore
from MainWindow_AV import Ui_MainWindow
import sys
from lxml import etree

videoList = list()
linkList = list()
mp4Link = str()
videoId = str()


class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    VideoTotalTime = str()
    VideoNowTime = str()
    VideoShowTime = str()
    homeLink = "https://www.xvideos.com/"

    def __init__(self,parnet=None):
        #啟動
        super(MainWindow,self).__init__()

        #繼承 MainWindow_AV介面裡的每個元件
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self)

        # 設定標題
        self.setWindowTitle("片片製造機")

        # 設定影片清單
        self.ui.pushButton.clicked.connect(self.playVideo)
        self.putVideoList("https://www.xvideos.com/")

        self.ui.horizontalSlider.setRange(0, 100)

        # 影片設置
        self.ui.mediaPlayer = QtMultimedia.QMediaPlayer(self)
        self.ui.mediaPlayer.setVideoOutput(self.ui.widget)

        #進度條設置
        self.ui.mediaPlayer.positionChanged.connect(self.playSlide)
        self.ui.mediaPlayer.durationChanged.connect(self.mediaTime)
        self.ui.horizontalSlider.sliderMoved.connect(self.setPosition)

        #音量控制
        self.ui.horizontalSlider_2.sliderMoved.connect(self.setVolumn)

        #查詢影片
        self.ui.searchBtn.clicked.connect(self.searchClicked)

        #上一頁/下一頁
        self.ui.nextBtn.clicked.connect(self.nextClicked)
        self.ui.previousBtn.clicked.connect(self.previousClicked)

    #將影片放入清單
    def putVideoList(self,url):
        #設定Model
        slm = QStringListModel()

        getHref(url)

        #設定List
        self.ui.qList = videoList

        #將List變成StringList
        slm.setStringList(self.ui.qList)

        #將StringList變成Model
        self.ui.listView.setModel(slm)

        # 单击触发自定义的槽函数
        self.ui.listView.doubleClicked.connect(self.clicked)

    #播放影片
    def playVideo(self):
        #self.ui.webEngineView.settings.pluginsEnabled: True
        #self.ui.webEngineView.load(QtCore.QUrl("https://video.nkmwrw.xyz/uploads/video/20210106/2596542/76be71ecc8b13bc94f85a84894afd25c_wm.mp4"))

        #url = QtCore.QUrl("https://cdn77-vid.xvideos-cdn.com/hKlBTRl7YWSZChFj81txrw==,1615400081/videos/mp4/0/4/b/xvideos.com_04b5fd7b1090e4733ab78f3b6d480b14.mp4?ui=MzYuMjM4LjEyNi4yMzctL3ZpZGVvNjE1Njc3NTkvMzMybmFtYS0wMjBfZnVs")
        url = QtCore.QUrl(self.mp4Link)

        self.ui.mediaPlayer.setMedia(QtMultimedia.QMediaContent(url))
        self.ui.mediaPlayer.play()

    #讓進度條自己跑
    def playSlide(self, time):
        #self.ui.horizontalSlider.setValue(int(val / 1000))
        self.ui.horizontalSlider.setValue(time)
        hours,minutes, seconds = timeTranslate(time)
        self.VideoNowTime = str(hours)+":"+str(minutes) + ":" + str(seconds)
        self.VideoShowTime = self.VideoNowTime + "/" +self.VideoTotalTime
        self.ui.totalVideoTimeLabel.setText(self.VideoShowTime)


    #設定進度條的總時長
    def mediaTime(self,time):
        self.ui.horizontalSlider.setRange(0,time)
        hours,minutes, seconds = timeTranslate(time)

        self.VideoTotalTime = str(hours)+":"+(minutes) + ":" + str(seconds)
        self.ui.totalVideoTimeLabel.setText(str(hours)+":"+str(minutes)+":"+str(seconds))
        '''self.time = self.ui.mediaPlayer.duration()/1000
        print(self.time)
        self.ui.horizontalSlider.setEnabled(True)
        self.ui.horizontalSlider.setRange(0, int(self.time))
        '''

    #設定拖曳進度時，改變播放的時間點
    def setPosition(self,time):
        self.ui.mediaPlayer.setPosition(time)
        hours,minutes, seconds = timeTranslate(time)
        self.VideoNowTime = str(hours)+":"+str(minutes) + ":" + str(seconds)

    # 設置聲音
    def setVolumn(self, value):
        self.ui.mediaPlayer.setVolume(value)

    # 判斷是不是連結的那行
    def clicked(self,qModelIndex):
        if judgementLink(qModelIndex.row()) == True:
            url= linkList[qModelIndex.row()]
            preViewId = str.split(url, "/")[3]
            videoId = preViewId
            #QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkList[qModelIndex.row()]))
            print("機掰R")
            print(self.homeLink)
            previewUrl = getPreviewUrlMP4(self.homeLink,videoId)
            print(previewUrl)
            url = getVideoUrlMP4(url)
            self.mp4Link =url

            #先播放預設影片
            previewUrl = QtCore.QUrl(previewUrl)
            self.ui.mediaPlayer.setMedia(QtMultimedia.QMediaContent(previewUrl))
            self.ui.mediaPlayer.play()
            return url

    def searchClicked(self):
        mytext = self.ui.textEdit.toPlainText()
        self.ui.textEdit_2.setText("1")
        videoList.clear()
        linkList.clear()
        url = urlTransformer(mytext)
        self.homeLink = url
        self.putVideoList(url)

    def nextClicked(self):
        mytext = self.ui.textEdit_2.toPlainText()
        page = int(mytext) +1
        self.ui.textEdit_2.setText(str(page))
        if self.homeLink == 'https://www.xvideos.com/':
            url = self.homeLink+"new/"+mytext
        else:
            url = self.homeLink+"&p="+mytext
        videoList.clear()
        linkList.clear()
        self.homeLink = url
        self.putVideoList(url)

    def previousClicked(self):
        mytext = self.ui.textEdit_2.toPlainText()
        page = int(mytext) -1
        if(page >0):
            self.ui.textEdit_2.setText(str(page))
            if self.homeLink == 'https://www.xvideos.com/':
                url = self.homeLink + "new/" + mytext
            else:
                url = self.homeLink + "&p=" + mytext
            videoList.clear()
            linkList.clear()
            self.homeLink = url
            self.putVideoList(url)





def getPreviewUrlMP4(url,id):
    print("有近來哦")
    response = requests.get(url).text
    s = etree.HTML(response)
    file = s.xpath('//*[@id="page"]')

    x = etree.tostring(file[0])
    x = str.split(str(x),id)[1]

    x = str.split(x, ":")[1] + ":" + str.split(x, ":")[2]
    x = str.split(x, ",")[0]
    x = str.replace(x, "\\", "")
    x = str.replace(x, '"', "")
    tmp = str.split(x, "src=")[1]
    tmp = str.split(tmp, "data")[0]
    x = tmp
    tmp = str.split(x, "/")[4]
    previewUrl = str.replace(x, tmp, "videopreview")
    tmp = str.split(x, "/")[8]
    previewUrl = str.replace(previewUrl, tmp + "/", "", 1)
    tmp = str.split(x, ".")[3]
    previewUrl = str.replace(previewUrl, tmp, "169", 1)
    previewUrl = str.replace(previewUrl, ".169.jpg", "_169.mp4")

    return previewUrl

def getVideoUrlMP4(url):
    response = requests.get(url).text
    s = etree.HTML(response)
    mp4Url = s.xpath('//*[@id="video-player-bg"]/script[4]')[0].text
    mp4Url = str.split(mp4Url, "\n")[8]
    mp4Url = str.split(mp4Url, "'")[1]

    mp4Link = mp4Url
    return mp4Url


def getHref(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    sel = soup.select("p.title a")
    for s in sel:
        links = 'https://xvideos.com'+s['href']
        title = s['title']

        videoList.append(title)
        videoList.append("")

        linkList.append(links)
        linkList.append("")

def urlTransformer(text):
    if text != "":
        text = str(text).replace(" ","+")
        text = "https://www.xvideos.com/?k="+text
        return text
    else:
        text = "https://www.xvideos.com/"
        return text

#判斷是不是有連結
def judgementLink(number):
    judgement = False
    number = number%2
    if number == 0:
        judgement =True
    return judgement

#毫秒時間轉換時/分/秒
def timeTranslate(time):
    time = int(time/1000)
    minutes, seconds = divmod(time,60)
    hours,minutes = divmod(minutes,60)
    hours = "{:02d}".format(hours)
    minutes = "{:02d}".format(minutes)
    seconds = "{:02d}".format(seconds)
    return hours,minutes,seconds


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
