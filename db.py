from sqlobject import sqlhub, connectionForURI, SQLObject, StringCol, IntCol, DateTimeCol, BoolCol, ForeignKey, sqlbuilder, MultipleJoin
import os

db_filename = os.path.abspath('data.db')
connection_string = f'sqlite:{db_filename}'
sqlhub.processConnection = connectionForURI(connection_string)


class School(SQLObject):
    """
    Représente une école dans la base de données.

    Attribus:
        schoolName (str): Le nom de l'école.
        rne (str): Le numéro RNE de l'école.
        password (str): Le mot de passe de l'école.
    """
    schoolName = StringCol()
    rne = StringCol()
    password = StringCol()

class User(SQLObject):
    """
    Représente un utilisateur (étudiant/professeur/membre du personnel administratif).
    
    Attributs:
        - username: Nom d'utilisateur de l'utilisateur (type: str)
        - firstName: Prénom de l'utilisateur (type: str)
        - lastName: Nom de famille de l'utilisateur (type: str)
        - permissions: Niveau de permissions de l'utilisateur (type: int)
        - is_a_teacher: Indique si l'utilisateur est un enseignant (type: bool)
        - password: Mot de passe de l'utilisateur (type: str)
    """

    username = StringCol()
    firstName = StringCol()
    lastName = StringCol()
    permissions = IntCol()
    is_a_teacher = BoolCol()
    password = StringCol()

class Group(SQLObject):
    name = StringCol()
    referant = ForeignKey('User', default=None)
    parent = ForeignKey('Group', default=None)
    defaultPermission = IntCol()

class Course(SQLObject):
    start = DateTimeCol()
    end = DateTimeCol()
    professor = MultipleJoin('User')
    groups = MultipleJoin('Group')
    subject = ForeignKey('Subject')
    room = StringCol()

class Subject(SQLObject):
    name = StringCol()


School.createTable(ifNotExists=True)
User.createTable(ifNotExists=True)
Group.createTable(ifNotExists=True)
Course.createTable(ifNotExists=True)
Subject.createTable(ifNotExists=True)
