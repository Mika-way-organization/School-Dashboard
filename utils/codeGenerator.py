"""Verifizierungs Code Generator

In dieser Datei wird ein sicherer Verifizierungs Code generiert.
Und dann wird diese in die Datanbank gespeichert.

"""


import secrets

class CodeGenerator:
    @staticmethod
    def generate_verification_code():
        return secrets.token_hex(3) # Generiert einen 6-stelligen hexadezimalen Code