from sqlobject import sqlhub, connectionForURI, SQLObject, StringCol, IntCol, DateTimeCol, BoolCol, ForeignKey, sqlbuilder
import os

db_filename = os.path.abspath('data.db')
connection_string = f'sqlite:{db_filename}'
sqlhub.processConnection = connectionForURI(connection_string)


class School(SQLObject):
    schoolName = StringCol()
    rne = StringCol()
    password = StringCol()

class User(SQLObject):
    username = StringCol()
    firstName = StringCol()
    lastName = StringCol()
    permissions = IntCol()
    is_a_teacher = BoolCol()
    password = StringCol()

class Group(SQLObject):
    name = StringCol()
    referant = StringCol()
    parent = StringCol()
    defaultPermission = StringCol()

class Course(SQLObject):
    start = DateTimeCol()
    end = DateTimeCol()
    professor = StringCol()
    groups = StringCol()
    subject = StringCol()

class Subject(SQLObject):
    name = StringCol()


School.createTable(ifNotExists=True)
User.createTable(ifNotExists=True)
Group.createTable(ifNotExists=True)
Course.createTable(ifNotExists=True)
Subject.createTable(ifNotExists=True)