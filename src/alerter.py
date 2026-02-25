import os
from dotenv import load_dotenv
import smtplib
import email.message


load_dotenv()

EMAIL_USER = os.environ.get('EMAIL')
EMAIL_PASS = os.environ.get('PASS')
EMAIL_TO = os.environ.get('EMAIL_TO')

def send_alert(alerts):
    lines = []
    for _, row in alerts.iterrows():
        emoji = "🔴" if row['variacao_pct'] < 0 else "🟢"
        lines.append(f"{emoji} {row['ticker']}: R$ {row['preco']:.2f} ({row['variacao_pct']:+.2f}%)")

    email_body = "Alerta B3!\n\nAções com variação acima de 5%:\n\n" + "\n".join(lines)
    
    msg = email.message.EmailMessage()
    msg['Subject'] = 'Variacao'
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg.set_content(email_body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


def verify_variation(df):
    alerts = df[df['variacao_pct'].abs() > 5]
    if not alerts.empty:
        send_alert(alerts)

