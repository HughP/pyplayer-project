def getTracksToView(self):
    curRow = self.tableWidget.rowCount()
    print 'curRow = ',curRow
    self.tableWidget.setRowCount(curRow+1)

    curCol = 0
    self.title = self.titleList.currentItem().text()

    aList = self.Coll.QueryToCollection('select track from music where title="'\
                                        +unicode(self.title)+'"')
    print aList[0]
    newItem = QTableWidgetItem(aList[0])
    self.tableWidget.setItem(curRow,curCol,newItem)

    curCol+=1
    newItem = QTableWidgetItem(self.title)
    self.tableWidget.setItem(curRow,curCol,newItem)

    curCol+=1
    aList = self.Coll.QueryToCollection('select artist from music where title="'\
                                        +unicode(self.title)+'"')
    print aList[0]
    newItem = QTableWidgetItem(aList[0])
    self.tableWidget.setItem(curRow,curCol,newItem)

    curCol+=1
    aList = self.Coll.QueryToCollection('select album from music where title="'\
                                        +unicode(self.title)+'"')
    print aList[0]
    newItem = QTableWidgetItem(aList[0])
    self.tableWidget.setItem(curRow,curCol,newItem)

    curCol+=1
    aList = self.Coll.QueryToCollection('select play_time from music where title="'\
                                        +unicode(self.title)+'"')
    print aList[0]
    newItem = QTableWidgetItem(aList[0])
    self.tableWidget.setItem(curRow,curCol,newItem)

    curCol+=1
    aList = self.Coll.QueryToCollection('select date from music where title="'\
                                        +unicode(self.title)+'"')
    print aList[0]
    newItem = QTableWidgetItem(aList[0])
    self.tableWidget.setItem(curRow,curCol,newItem)

    curCol+=1
    aList = self.Coll.QueryToCollection('select genre from music where title="'\
                                        +unicode(self.title)+'"')
    print aList[0]
    newItem = QTableWidgetItem(aList[0])
    self.tableWidget.setItem(curRow,curCol,newItem)


    curCol+=1
    aList = self.Coll.QueryToCollection('select file_size from music where title="'\
                                        +unicode(self.title)+'"')
    newItem = QTableWidgetItem(aList[0])
    self.tableWidget.setItem(curRow,curCol,newItem)

    curCol+=1
    aList = self.Coll.QueryToCollection('select path from music where title="'\
                                        +unicode(self.title)+'"')
    print aList[0]
    newItem = QTableWidgetItem(aList[0])
    self.tableWidget.setItem(curRow,curCol,newItem)

def QueryToCollection(self, query):
    listQuery = []
    self.cursor.execute(query)
    items = self.cursor.fetchall()
    for item in items:                  #перебор всех элементов в выдаче
        listQuery.append(item[0])

    return listQuery

    """ i = 0
    newItem = QTableWidgetItem(item[0][0])
    self.tableWidget.setItem(curRow,i,newItem)

    i+=1
    newItem = QTableWidgetItem(item[0][1])
    self.tableWidget.setItem(curRow,i,newItem)

    i+=1
    newItem = QTableWidgetItem(item[0][1])
    self.tableWidget.setItem(curRow,i,newItem)"""