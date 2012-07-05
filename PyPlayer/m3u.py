# -*- coding: utf-8 -*-
''' M3U Support Open/Save playlist
'''

import os
from support import *

def saveM3U(lists,filename=u'Pls\main.m3u'):
    fp = file(filename, "w")
    fp.write("#EXTM3U\n")
    for item in lists:
        fp.write('#EXTINF:'+item['length']+','+item['artist']+'-'+item['title']+'\n')
        fp.write(item['path']+'\n')
    fp.close()

def openM3U(filename=u'Pls\main.m3u'):
    """
    Return [{'artist':'Korn','title':'Blind'}]
    lists = loadM3U('korn.m3u')
    for line in lists:
        print 'Artist',line['artist']
        print 'Title',line['title']
        print 'Length',line['length']
        print 'Path', line['path']
    """
    lists = list()
    if os.path.exists(filename):
        fp = file(filename,'r')
        s = fp.readline()
        if s == "#EXTM3U\n":
            lines = fp.readlines()
            lines=iter(lines)
            for s in lines:
                py = 0
                if s[:7] == "#EXTINF":
                    #убираем мусор(#EXTINF:)
                    s = s[8:]
                    length = strToSec(s.split(',')[0])
                    temp = s.split(',')[1]
                    artist = temp.split('-')[0]
                    title = temp.split('-')[1]
                    path = next(lines)
                if s[:10] == '#PyPlayer:':
                    s = s[10:]
                    track = s.split(',')[0]
                    album = s.split(',')[1]
                    date = s.split(',')[2]
                    genre = s.split(',')[3]
                    stars = s.split(',')[4]
                    size = s.split(',')[5]
                    plays = s.split(',')[6]
                    id = s.split(',')[7]
                    py = 1
                #формируем dict и добавляем в список
                d = {'artist':artist,'title':title,'length':length,'path':path,
                     'track':track,'album':album,'date':date,'genre':genre,
                     'stars':stars,'size':size,'plays':plays,'id':id,'py':py}
                lists.append(d)

        fp.close()
    return lists
