"""Extensions für die app.py

Hier gibt es Verschiedene Erweiterungen

1. bcrypt
2. csrf
3. mail
4. jwt
5. cors

"""

from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialisierung von Bcrypt für die Passwort-Hashing
# Bcrypt() wird zur sicheren, unwiderruflichen Speicherung (Hashing) von Benutzerpasswörtern genutzt.
bcrypt = Bcrypt()

# Initialisierung von CSRF Schutz
# CSRFProtect() schützt vor Cross-Site Request Forgery (CSRF) bei Formularen und POST-Anfragen.
csrf = CSRFProtect()

# Initialisierung von Mail
# Mail() ermöglicht das einfache Versenden von E-Mails (z.B. für Verifizierung, Passwort-Reset).
mail = Mail()

# Initialisierung JWT Erweiterung
# JWTManager() wird zur Authentifizierung von APIs mittels Token (JSON Web Tokens) verwendet.
jwt = JWTManager()

# Initialisierung CORS
# CORS() steuert, welche externen Frontends (Domains) auf diese API zugreifen dürfen.
cors = CORS()