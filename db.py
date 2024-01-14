from sqlobject import sqlhub, connectionForURI, SQLObject, StringCol, IntCol, DateTimeCol, ForeignKey, sqlbuilder
import os

db_filename = os.path.abspath('data.db')
connection_string = f'sqlite:{db_filename}'
sqlhub.processConnection = connectionForURI(connection_string)


class School(SQLObject):
    schoolName = StringCol()
    ogecCode = StringCol()
    password = StringCol()

    def toDict(self):
        return {"id": self.id, "schoolName": self.schoolName, "ogecCode": self.ogecCode, "password": self.password}


School.createTable(ifNotExists=True)