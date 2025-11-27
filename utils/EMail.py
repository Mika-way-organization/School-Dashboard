"""EMailService

In dieser Datei werden Funktionen zum Senden von E-Mails bereitgestellt.

"""

from flask_mail import Message

from app import mail


# EMailService Klasse zum Senden von Verifizierungs-E-Mails
class EmailService:
    # Senden der Verifizierungs-E-Mail
    @staticmethod
    def send_verify_email(email_adress, code):
        msg = Message(
            subject="Verifizierungs Code",
            recipients=[email_adress],
            html=f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verifizierungscode</title>
        </head>
        
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #f8f9fa; /* Bootstrap Light Text */ margin: 0; padding: 0; background-color: #212529;">
            
            <div style="max-width: 600px; margin: 20px auto; padding: 25px; 
                        background-color: #343a40; /* Bootstrap Dark Hintergrund */ 
                        border-radius: 0.5rem; /* Bootstrap Card Border-Radius */ 
                        border: 1px solid #495057; /* Bootstrap Border Color */
                        box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.5);">
                
                <h1 style="color: #007bff; /* Bootstrap Primary Color */ 
                           font-size: 24px; 
                           border-bottom: 1px solid #495057; /* Dezente Trennlinie */
                           padding-bottom: 15px; margin-bottom: 20px;">
                    Schul-Dashboard: Identitätsbestätigung
                </h1>
                
                <p style="font-size: 16px; color: #f8f9fa;">
                    Herzlich Willkommen auf der Schul-Dashboard Website.
                </p>
                <p style="font-size: 16px; color: #f8f9fa;">
                    Sie haben die Verifizierung Ihrer E-Mail-Adresse angefordert. Bitte verwenden Sie diesen Code:
                </p>

                <div style="background-color: #28a745; /* Bootstrap Success Green */
                            color: #fff; /* Weisser Text auf Grün */
                            padding: 20px; 
                            border-radius: 0.25rem; 
                            text-align: center; 
                            font-size: 32px; 
                            font-weight: bold; 
                            margin: 25px 0;
                            letter-spacing: 4px;">
                    {code}
                </div>

                <p style="font-size: 16px; color: #ffc107; /* Bootstrap Warning Yellow */ font-weight: bold;">
                    Dieser Code ist nur <b>10 Minuten</b> lang gültig.
                </p>
                
                <p style="font-size: 16px; color: #f8f9fa;">
                    Bitte geben Sie ihn jetzt auf der Verifizierungsseite ein, um den Vorgang abzuschließen.
                </p>

                <p style="margin-top: 40px; font-size: 12px; color: #adb5bd; /* Bootstrap Secondary Color */ 
                           border-top: 1px solid #495057; 
                           padding-top: 15px;">
                    <strong>Sicherheitshinweis:</strong> Wenn Sie diese Aktion nicht angefordert haben, müssen Sie nichts weiter unternehmen. Bitte teilen Sie diesen Code niemals mit Dritten.
                </p>

                <p style="font-size: 14px; color: #f8f9fa; margin-top: 20px;">
                    Vielen Dank,<br>
                    Ihr **Schul-Dashboard Team**
                </p>
            </div>
        </body>
        </html>
"""
        )
        mail.send(msg)
        print(f"E-Mail an {email_adress} erfolgreich gesendet.")
