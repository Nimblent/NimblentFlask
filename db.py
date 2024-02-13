from sqlobject import sqlhub, connectionForURI, SQLObject, StringCol, IntCol, DateTimeCol, BoolCol, ForeignKey, MultipleJoin, RelatedJoin 
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
    courses = RelatedJoin('Course')
    groups = RelatedJoin('GroupTable')
    password = StringCol()

class GroupTable(SQLObject):
    """
    Représente une table de groupe dans la base de données.
    
    Attributes:
        name (str): Le nom du groupe.
        referant (User): L'utilisateur référent du groupe.
        parent (GroupTable): The parent group of the group.
        users (RelatedJoin): The users associated with the group.
        defaultPermission (int): The default permission level for the group.
    """

    name = StringCol()
    referant = ForeignKey('User', default=None)
    parent = ForeignKey('GroupTable', default=None)
    users = RelatedJoin('User')
    defaultPermission = IntCol()

class Course(SQLObject):
    """
    Représente un cours dans la base de données.

    Attributs:
    - start (DateTimeCol): La date et l'heure de début du cours.
    - end (DateTimeCol): La date et l'heure de fin du cours.
    - professors (RelatedJoin): Les professeurs associés à ce cours.
    - group (RelatedJoin): Les groupes associés à ce cours.
    - subject (ForeignKey): La matière associée à ce cours.
    - room (StringCol): La salle où se déroule le cours.
    """

    start = DateTimeCol()
    end = DateTimeCol()
    professors = RelatedJoin('User')
    group = RelatedJoin('GroupTable')
    subject = ForeignKey('Subject')
    room = StringCol()

class Subject(SQLObject):
    """
    Représente un sujet.
    
    Attributes:
        name (str): Le nom du sujet.
    """
    name = StringCol()


School.createTable(ifNotExists=True)
User.createTable(ifNotExists=True)
GroupTable.createTable(ifNotExists=True)
Course.createTable(ifNotExists=True)
Subject.createTable(ifNotExists=True)
