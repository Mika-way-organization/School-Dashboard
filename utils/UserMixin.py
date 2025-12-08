"""UserMixin Klasse

Hier wird eine Klasse definiert, die das UserMixin von Flask-Login erweitert.

"""
#Importiere UserMixin von flask_login
from flask_login import UserMixin

#Definiere die User Klasse, die von UserMixin erbt
class User(UserMixin):
    def __init__(self, student):
        self.id = student['uuid']
        self.username = student['username']
        self.role = student['role']
        self.email = student['email']
        self.password = student['password']