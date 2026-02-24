import os
from dotenv import load_dotenv
import smtplib
import email.message
from collector import get_data
from transformer import transform_data

load_dotenv()

EMAIL_USER = os.environ.get('EMAIL')
EMAIL_PASS = os.environ.get('PASS')
EMAIL_TO = os.environ.get('EMAIL_TO')

def send_alert(alerts):
    email_body = f"Alerta B3!\n\nAções com variação acima de 5%:\n\n{alerts.to_string(index=False)}"

    msg = email.message.EmailMessage()
    msg['Subject'] = 'Variacao'
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg.set_content(email_body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


def verify_variation(df):
    alerts = df[df['variacao_pct'].abs() > 0.1]
    if not alerts.empty:
        send_alert(alerts)

if __name__== '__main__':

    df = transform_data(get_data())
    verify_variation(df)      

