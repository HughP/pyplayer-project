# -*- coding: utf-8 -*-
import _sqlite3 as sqlite
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import os
import fnmatch
import sys
import shutil
from os.path import getsize
"""AddToCollection(all tags)"""
version = 0.0001


class OhMyGod:
    def __init__(self,drop):
        self.connection = sqlite.Connection('music.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('select name from SQLITE_MASTER where name = "music"')
        if self.cursor.fetchone() is None:
            self.createTableMusic()
            print 'This is first start! Make Library'
        else:
            if (drop):
                print 'Drop table music, but i need backup it'
                shutil.copy('music.db','music-backup.db')
                self.dropTable('music')
                self.createTableMusic()

        self.progress = 0

    def dropTable(self, table):
        self.cursor.execute('drop table '+table)

    def updateTable(self, table, column, value, value_id):
        s = 'update '+table+' set '+column+' = '+value \
        +' where id = '+value_id
        print s
        self.cursor.execute(s)

    def getStr(self):
        self.cursor.execute('select id,artist from music')
        items = self.cursor.fetchall()
        for item in items:
            id = item[0]
            art = item[1]
            print 'ID=',id
            print 'Artist=',art

    def createTableMusic(self):
        self.cursor.execute('create table music (id integer primary key, artist varchar(30),\
                            album varchar(30),title varchar(30),date varchar(15),\
                            genre varchar(20),track varchar(10),path varchar(50),\
                            cover_path varchar(50),play_time varchar(10),file_size varchar(10),\
                            stars varchar(3), plays varchar(10))')

    def createPlaylistTable(self):
        self.cursor.execute('create table playlists (id integer primary key, name varchar(30),\
                            path varchar(30), date varchar(15), plays varchar(10))')

    def CoverFind(self, directory):
        for item in os.listdir(directory):
            if os.path.exists('cover.jpg'):
                return directory + '\\' + item
            if fnmatch.fnmatch(item,'*.jpg'):
                return directory + '\\' + item  #возвращаем первый найденный jpeg

    def S2HMS(self,t):
    # Converts seconds to a string formatted H:mm:ss
        if t > 3600:
            h = int(t/3600)
            r = t-(h*3600)
            m = int(r / 60)
            s = int(r-(m*60))
            return '{0}:{1:02n}:{2:02n}'.format(h,m,s)
        else:
            m = int(t / 60)
            s = int(t-(m*60))
            return '{0}:{1:02n}'.format(m,s)

    def ScanFolders(self, PathCollection):
        fullpath = ''
        cover_path = ''
        PathCollection = unicode(PathCollection,'utf8')

        if os.path.exists(PathCollection):
            print 'Path not exists!'
            for path, files, dirs in os.walk(PathCollection):
                print 'Init scanning in: ',PathCollection
                for name in dirs:
                    if name[-3:] == 'mp3':
                        fullpath = path + '\\' + name
                        print fullpath
                        try:
                            tag_list = []

                            audio = EasyID3(fullpath)
                            info_track = MP3(fullpath)
                            tag_list.append( audio.get('artist','Unknow Artist')[0] )
                            tag_list.append( audio.get('album','Unknow Album')[0] )
                            tag_list.append( audio.get('title',name)[0] )
                            tag_list.append( audio.get('genre','Unknow Genre')[0])
                            tag_list.append( audio.get('date','00.00.2012')[0])
                            tag_list.append( audio.get('tracknumber',"00")[0])
                            tag_list.append( fullpath )
                            tag_list.append( self.CoverFind(path) )
                            tag_list.append( self.S2HMS(info_track.info.length))
                            tag_list.append( getsize(fullpath) )
                            tag_list.append( '0' )#оценка(по умолчанию 0)
                            tag_list.append( '0' )#колчиество проигрываний

                        except ID3NoHeaderError as e:
                            print 'NO TAGS! from file:',fullpath
                            audio.__setitem__('artist','UnknowArtist')
                            audio.__setitem__('album','UnknowAlbum')
                            audio.__setitem__('title', name)
                            audio.save()

                    #   self.CoverFound(path)
                        self.AddToCollection(tag_list)
                        self.progress += 1
                        print self.progress
        print 'End!'

    def AddToCollection(self,tag_list):
        query = u'insert into music (artist,album,title,genre,date,track,path,cover_path,\
        play_time,file_size,stars,plays) values (?,?,?,?,?,?,?,?,?,?,?,?)'
        self.cursor.execute(query,\
        (tag_list[0],tag_list[1],tag_list[2],tag_list[3],tag_list[4],tag_list[5],\
        tag_list[6],tag_list[7],tag_list[8],tag_list[9],tag_list[10],tag_list[11]))
        self.connection.commit()

    def QueryToCollection(self, query):
        listQuery = []
        print query
        self.cursor.execute(unicode(query))
        items = self.cursor.fetchall()
        #for item in items:                  #перебор всех элементов в выдаче
        #    listQuery.append(item[0])

        return items

    def QueryToCollection2(self, query, need_all=False):
        listQuery = []
        print 'Query=',query
        self.cursor.execute(query)
        items = self.cursor.fetchall()
        if need_all:
            return items
        else:
            for item in items:                  #перебор всех элементов в выдаче
                listQuery.append(item[0])
            return listQuery