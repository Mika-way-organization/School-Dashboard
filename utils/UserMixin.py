"""UserMixin Klasse

Hier wird eine Klasse definiert, die das UserMixin von Flask-Login erweitert.

"""
#Importiere UserMixin von flask_login
from flask_login import UserMixin

#Definiere die User Klasse, die von UserMixin erbt
class User(UserMixin):
    def __init__(self, user):
        self.id = user['uuid']
        self.username = user['username']
        self.role = user['role']
        self.email = user['email']
        self.password = user['password']