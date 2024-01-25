from sqlobject import sqlhub, connectionForURI, SQLObject, StringCol, IntCol, DateTimeCol, ForeignKey, sqlbuilder
import os

db_filename = os.path.abspath('data.db')
connection_string = f'sqlite:{db_filename}'
sqlhub.processConnection = connectionForURI(connection_string)


class School(SQLObject):
    schoolName = StringCol()
    rne = StringCol()
    password = StringCol()

    def toDict(self):
        return {"id": self.id, "schoolName": self.schoolName, "rne": self.rne, "password": self.password}

class Students(SQLObject):
    username = StringCol()
    firstName = StringCol()
    lastName = StringCol()
    level = StringCol()
    password = StringCol()

    def toDict(self):
        return {"id": id, "username": self.username, "firstName": self.firstName, "lastName": self.lastName, "level": self.level, "password": self.password}

class Teachers(SQLObject):
    username = StringCol()
    firstName = StringCol()
    lastName = StringCol()
    password = StringCol()

    def toDict(self):
        return {"id": id, "username": self.username, "firstName": self.firstName, "lastName": self.lastName, "password": self.password}


School.createTable(ifNotExists=True)
Students.createTable(ifNotExists=True)
Teachers.createTable(ifNotExists=True)