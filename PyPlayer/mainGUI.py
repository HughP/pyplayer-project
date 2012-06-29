# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon

from ui_mainwindow import Ui_MainWindow
from ui_progresswindow import Ui_progressDialog
from ui_settingswindow import Ui_SettingsWindow
from random import randint

from DBOperation import OhMyGod
import os

version = 0.0005
musicPath = ''
global nameFile
form = None
DEFAULT_COVER = '/icons/nocover.jpg'
CURRENT_PATH_FIELD = 9



class progressWindow(QtGui.QWidget, Ui_progressDialog):
    def __init__(self, windowTitle):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.process)
        self.connect(self.abort, QtCore.SIGNAL("clicked()"),self.closeButton)
        self.setWindowTitle(u'Создаем библиотеку')
        self.movie = QMovie('progress.gif',QByteArray(),self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.anim.setMovie(self.movie)
        self.windowTitle = windowTitle

    ##        self.pro
    def closeButton(self):
        self.close()
    def process(self):
##        self.show()
        global musicPath
        self.movie.start()
        self.db = OhMyGod(self.checkBox.isChecked())
        self.db.ScanFolders(musicPath)
        global form
        form.getArtist()
##------------------------------------------------------------------------------
class settingsWindow(QtGui.QWidget, Ui_SettingsWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.okClick)
        self.toolButton.clicked.connect(self.showDialog)
        global musicPath
        print 'Set',musicPath
        self.lineEdit.setText(musicPath)
##        self.dialog = QtGui.QFileDialog(self,QString('Select path to collection'),QString('c:\\'),'')
        self.dialog = QtGui.QFileDialog()
##        self.dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)

    def showDialog(self):
        self.lineEdit.setText(self.dialog.getExistingDirectory(self,QString(u'Путь к музыке'),
            options=QtGui.QFileDialog.ShowDirsOnly))
##        if (self.dialog.exec_()):
##            print self.dialog.directory().absolutePath()
##            print self.dialog.directory().path()

    def okClick(self):
##        musicPath = self.lineEdit.text()
##        form.writeSettings()
##        print musicPath
        global form
        global musicPath
        musicPath = unicode(str(self.lineEdit.text()))
        print '!!!!',type(musicPath)
        print musicPath
        form.writeSettings()
        self.close()


##------------------------------------------------------------------------------
class TWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle('PyPlayer!')
        #-----------------------------------
        self.m_media = None
        self.currentRow = 0
        self.random = 0
        self.repeat = 0
        self.coverImage.setScaledContents(1)
        #-----------------------------------
        #создаем окно
        self.pro = progressWindow('Pro')
        #self.setW = settingsWindow()
        #self.pro.show()
        #Подключение к коллекции
        self.Coll = OhMyGod(0)
        #Заполняем artistList, albumList, titleList
        self.getArtist()
##        self.getAlbum()

        self.delayedInit()
        #Загружаем настройки
        self.readSettings()
##        self.m_media.pause()
        self.setW = settingsWindow()

        #Подключаем обработчики
        self.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.play)#phononPlay
        self.artistList.itemClicked.connect(self.getAlbum)
        self.albumList.itemClicked.connect(self.getTracks)
        self.titleList.itemClicked.connect(self.getTracksToView)
        self.tableWidget.itemDoubleClicked.connect(self.tableWidgetClick)
        self.playButton.clicked.connect(self.PlayPausePlayer)
        self.stopButton.clicked.connect(self.StopPlayer)
        self.pushButton.clicked.connect(self.playNextTrack)
        self.prevButton.clicked.connect(self.playPrevTrack)
        self.newPlsButton.clicked.connect(self.generateM3U)
        self.clearPlsButton.clicked.connect(self.clearPlaylist)
        self.settingsButton.clicked.connect(self.setW.show)
        self.actionScan.triggered.connect(self.pro.show)
        #показываем фс
        model = QFileSystemModel()
        model.setRootPath('C:\\')
        self.treeView.setModel(model)
        self.loadM3U()

    def closeEvent(self, event):
        self.writeSettings()
    def keyPressEvent(self, e):
        #----CTRL+1,2,3,4,5-------------
        if e.key() == QtCore.Qt.Key_1:
            if (e.modifiers() & QtCore.Qt.CTRL):
                self.updateStars('1')
        if e.key() == QtCore.Qt.Key_2:
            if (e.modifiers() & QtCore.Qt.CTRL):
                self.updateStars('2')
        if e.key() == QtCore.Qt.Key_3:
            if (e.modifiers() & QtCore.Qt.CTRL):
                self.updateStars('3')
        if e.key() == QtCore.Qt.Key_4:
            if (e.modifiers() & QtCore.Qt.CTRL):
                self.updateStars('4')
        if e.key() == QtCore.Qt.Key_5:
            if (e.modifiers() & QtCore.Qt.CTRL):
                self.updateStars('5')
            #оценка 1 звезда
            #update запись в бд

    def tock(self, time):
        time = time/1000
        h = time/3600
        m = (time-3600*h) / 60
        s = (time-3600*h-m*60)
        self.lcdNumber.display('%02d:%02d:%02d'%(h,m,s))

#--------------Инит для плеера--------------------------------------------------
    def delayedInit(self):
        if not self.m_media:
            print 'Player\'s init!'
            self.m_media = Phonon.MediaObject(self)
            self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
            Phonon.createPath(self.m_media, self.audioOutput)
            self.m_media.setTickInterval(100)
            self.m_media.tick.connect(self.tock)
            self.seekSlider.setMediaObject(self.m_media)
            self.volumeSlider.setAudioOutput(self.audioOutput)
            self.m_media.aboutToFinish.connect(self.playNextTrack)

    def PlayPausePlayer(self):
        if (self.m_media.state() == 2):
            self.m_media.pause()
            self.playButton.setIcon(QIcon('Icons\control_play_blue.png'))
        else:
            self.m_media.play()
            self.playButton.setIcon(QIcon('Icons\control_pause_blue.png'))

    def StopPlayer(self):
        self.m_media.stop()


    def play(self, path):
        self.delayedInit()
        if os.path.exists(path):
            print 'Path exists!'
        else:
            print 'Path NOT exists!'
        print path
        self.m_media.setCurrentSource(Phonon.MediaSource(path))
        self.m_media.play()
        #ставим обложку трека
        cover = self.Coll.QueryToCollection('select cover_path from music where id='+self.getID(self.oldRow))
        if cover[0][0] != '':
            self.coverImage.setScaledContents(1)
            self.coverImage.setPixmap(QPixmap(cover[0][0]))

#---------------Сохранение/Загрузка---------------------------------------------
    def writeSettings(self):
        settings = QtCore.QSettings('settings.ini',QtCore.QSettings.IniFormat)
        settings.beginGroup('MainWindow')
        settings.setValue('size',self.size())
        settings.endGroup()
        settings.beginGroup('tableWidget')
        settings.setValue('rowCount', self.tableWidget.rowCount())
        settings.setValue('currentRow',self.tableWidget.currentRow())
        settings.setValue('oldRow', self.oldRow)
        row_str = ''
        for row in xrange(self.tableWidget.rowCount()):
            for col in xrange(self.tableWidget.columnCount()):
                if self.tableWidget.item(row,col) != None:
                    row_str += self.tableWidget.item(row,col).text()+';'
                else:
                    row_str += ';'
            settings.setValue(str(row), unicode(row_str))
            row_str = ''
        settings.endGroup()

        settings.beginGroup('Lists')
        settings.setValue('artistListCurRow',self.artistList.currentRow())
        settings.setValue('albumListCurRow',self.albumList.currentRow())
        settings.setValue('titleListCurRow',self.titleList.currentRow())
        settings.endGroup()

        settings.beginGroup('Player')
        settings.setValue('currentTime',self.m_media.currentTime())
        settings.setValue('currentSource',self.m_media.currentSource().fileName())
        settings.setValue('currentVolume',self.audioOutput.volume())
        settings.setValue('random',self.randomButton.isChecked())
        settings.setValue('repeat',self.repeatButton.isChecked())
        settings.endGroup()

        settings.beginGroup('lcdNumber')
        settings.setValue('displayStr',self.lcdNumber.value())
        settings.endGroup()
        settings.beginGroup('cover')
        #получаем обложку из бд
        print self.oldRow
        self.album = unicode(self.tableWidget.item(self.oldRow,3).text())
        print self.album
        aList = self.Coll.QueryToCollection2('select cover_path from music where album="'\
            +unicode(self.album)+'"')
        if len(aList) > 0:
            settings.setValue('coverImage',aList[0])
        else:
            settings.setValue('coverImage',DEFAULT_COVER)
        settings.endGroup()

        settings.beginGroup('System')
        global musicPath
        settings.setValue('MusicPath',musicPath)
        settings.endGroup()

    def readSettings(self):
        settings = QtCore.QSettings('settings.ini',QtCore.QSettings.IniFormat)
        settings.beginGroup('MainWindow')
        self.resize(settings.value('size',QSize(400,400)).toSize())
        settings.endGroup()
        settings.beginGroup('System')
        global musicPath
        musicPath = settings.value('MusicPath').toString()
        settings.endGroup()
        settings.beginGroup('tableWidget')
        self.oldRow = settings.value('oldRow',0).toInt()[0]
        self.tableWidget.setRowCount( settings.value('rowCount').toInt()[0])
        row_list=[]
        #row_str =''
        for row in xrange(self.tableWidget.rowCount()):
            row_str = unicode( settings.value(str(row),'roy').toString())
            row_list = row_str.split(';')
            for col in xrange(self.tableWidget.columnCount()):
                newItem = QTableWidgetItem(unicode(row_list[col]))
                self.tableWidget.setItem(row,col,newItem)
        settings.endGroup()

        settings.beginGroup('Player')
        print settings.value('currentTime').toInt()[0]
        self.m_media.seek( settings.value('currentTime').toInt()[0])
        self.m_media.setCurrentSource(Phonon.MediaSource(settings.value('currentSource').toString()) )
        self.audioOutput.setVolume( settings.value('currentVolume').toFloat()[0])
        self.randomButton.setChecked(settings.value('random',0).toInt()[0])
        self.repeat = settings.value('repeat',0).toInt()[0]
        settings.endGroup()

        settings.beginGroup('cover')
        s = settings.value('coverImage').toString()
        print 'S = ',s
        self.coverImage.setPixmap(QPixmap(s))
        settings.endGroup()

        settings.beginGroup('Lists')
        self.artistList.setCurrentRow( settings.value('artistListCurRow').toInt()[0] )
        self.albumList.setCurrentRow( settings.value('albumListCurRow').toInt()[0] )
        self.titleList.setCurrentRow( settings.value('titleListCurRow').toInt()[0] )
        settings.endGroup()
#-------------------------------------------------------------------------------


    def showSplash(self,splash):
        splash.showMessage('Loadng')
        QtGui.qApp.processEvents()

    def showProgress(self):
        progressWindow = QtGui.QWidget(self)
##        progressWindow.setWindowFlags(QtCore.Qt.SubWindow)
        progressWindow.setWindowTitle('Progress...')
        progressWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        progressWindow.resize(200,90)
        progressWindow.show()


    def getArtist(self):
        self.artistList.clear()
        aList = self.Coll.QueryToCollection2('select distinct artist from music')
        for item in aList:
            self.artistList.addItem(item)

    def getAlbum(self):
        self.artist = self.artistList.currentItem().text()
        self.albumList.clear()
        aList = self.Coll.QueryToCollection2('select distinct album from music where artist="'+unicode(self.artist)+'"')
        for item in aList:
            self.albumList.addItem(item)

    def getTracks(self):
        self.album = self.albumList.currentItem().text()
        self.titleList.clear()
        aList = self.Coll.QueryToCollection2('select title from music where album="'\
            +str(self.album)+'" and artist="'+unicode(self.artist)+'"')
        for item in aList:
            self.titleList.addItem(item)

    def getTracksToView(self):
        #запоминаем текущую строчку
        curRow = self.tableWidget.rowCount()
        #создаем новую строчку
        self.tableWidget.setRowCount(curRow+1)
        #берем из списка title потом по нему достаем ID и по
        #нему уже получаем все остальное
        self.title = self.titleList.currentItem().text()
        #находим нужный ID
        id = self.Coll.QueryToCollection('select id from music where title="'\
            +unicode(self.title)+'"')
        #нужные поля
        fields = 'track,title,artist,album,play_time,date,genre,stars,\
        file_size,path,plays,id'
        item = self.Coll.QueryToCollection('select '+fields+' from music where id='+str(id[0][0]))
        #заполняем одну строчку таблицы
        for i in xrange(12):
            newItem = QTableWidgetItem(str(item[0][i]))
            self.tableWidget.setItem(curRow,i,newItem)

    def playNextTrack(self):
        #УБИРАЕМ иконку "воспроизведения"
        self.tableWidget.item(self.oldRow,0).setIcon(QIcon(QPixmap('')))
        #разруливаем random
        if not self.randomButton.isChecked():
            path = self.tableWidget.item(self.oldRow+1,CURRENT_PATH_FIELD).text()
            if self.repeatButton.isChecked():
                if (self.tableWidget.rowCount()-1 == self.oldRow+1):
                    path = self.tableWidget.item(0,CURRENT_PATH_FIELD).text()
            #СТАВИМ иконку "воспроизведения"
            self.tableWidget.item(self.oldRow+1,0).setIcon(QIcon(QPixmap('Icons/select_play.png')))
            self.oldRow += 1
        else:
            rand_value = randint(0,self.tableWidget.rowCount()-1)
            path = self.tableWidget.item(rand_value,CURRENT_PATH_FIELD).text()
            #СТАВИМ иконку "воспроизведения"
            self.tableWidget.item(rand_value,0).setIcon(QIcon(QPixmap('Icons/select_play.png')))
            self.oldRow = rand_value
        self.play(path)
        self.updatePlays()

    def playPrevTrack(self):
        #убираем иконку "воспроизведения"
        self.tableWidget.item(self.oldRow,0).setIcon(QIcon(QPixmap('')))
        #разруливаем рандом
        if not self.randomButton.isChecked():
            path = self.tableWidget.item(self.oldRow-1,CURRENT_PATH_FIELD).text()
            #ставим иконку "воспроизведения"
            self.tableWidget.item(self.oldRow-1,0).setIcon(QIcon(QPixmap('Icons/select_play.png')))
            self.oldRow -= 1
        else:
            rand_value = randint(0,self.tableWidget.rowCount()-1)
            path = self.tableWidget.item(rand_value,CURRENT_PATH_FIELD).text()
            #ставим иконку "воспроизведения"
            self.tableWidget.item(rand_value,0).setIcon(QIcon(QPixmap('Icons/select_play.png')))
            self.oldRow = rand_value
        self.play(path)
        self.updatePlays()

    def tableWidgetClick(self):
        ##запоминаем текущую строку
        self.oldRow = self.tableWidget.currentRow()
        #убираем иконку "воспроизведения"
        self.tableWidget.item(self.oldRow,0).setIcon(QIcon(QPixmap('')))
        #получаем название трека из таблицы и по нему делаем запрос->получаем полный путь
        path = self.tableWidget.item(self.oldRow,CURRENT_PATH_FIELD).text()
        #проигрываем указанный путь
        self.play(path)

        #обновляем проигрывания
        self.updatePlays()

        #ставим иконку "воспроизведения"
        self.tableWidget.item(self.oldRow,0).setIcon(QIcon(QPixmap('Icons/select_play.png')))

    def updatePlays(self):
        value = int(self.tableWidget.item(self.oldRow,10).text()) + 1
        self.Coll.updateTable('music','plays',str(value),self.getID(self.oldRow))
        self.tableWidget.item(self.oldRow,10).setText(str(value))

    def updateStars(self, star):
        self.Coll.updateTable('music','stars',star,self.getID(self.oldRow))
        self.tableWidget.item(self.oldRow, 7).setText(star)


    def generateM3U(self,filename=u'Pls/main.m3u'):
        #колонки: название - 1; артист - 2; длина - 4; путь - 8;
        fp = file(filename, "w")
        fp.write("#EXTM3U\n")
        for row in xrange(self.tableWidget.rowCount()):
##            str1 += self.tableWidget.item(row,col).text()
            #получаем данные для формрования m3u
            title = self.tableWidget.item(row,1).text()
            artist = self.tableWidget.item(row,2).text()
            track_length = self.tableWidget.item(row,4).text()
            full_path = self.tableWidget.item(row,8).text()
            #формируем m3u плейлист
            fp.write("#EXTINF" + ":" + track_length + "," +\
                             artist + " - " + title + "\n")
            fp.write(full_path + "\n")
        fp.close()

    def loadM3U(self, filename=u'Pls/main.m3u'):
        pass


    def clearPlaylist(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    def getID(self,row):
        return str(self.tableWidget.item(row,11).text())


def main():
    app = QtGui.QApplication(sys.argv)
    #Подключаем стили css
    #app.setStyleSheet(open("style.css","r").read())
    global form

    splash = QtGui.QSplashScreen(QtGui.QPixmap('splash.png'))
    splash.show()
    QtGui.qApp.processEvents()
    form = TWindow()

    form.showSplash(splash)
    form.show()

    splash.finish(form)
    app.exec_()

if __name__ == "__main__":
    main()