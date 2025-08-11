from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Загрузка переменных окружения из .env файла

app = Flask(__name__)

# Конфигурация почтового сервера
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SENDER_NAME = os.getenv('SENDER_NAME', 'DarkGram System')

@app.route('/send-verification', methods=['POST'])
def send_verification():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    
    if not email or not code:
        return jsonify({'success': False, 'error': 'Missing email or code'}), 400
    
    try:
        # Создаем сообщение
        msg = MIMEMultipart()
        msg['From'] = f"{SENDER_NAME} <{EMAIL_ADDRESS}>"
        msg['To'] = email
        msg['Subject'] = "Код подтверждения DarkGram"
        
        # HTML версия письма
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #0a0a0a; color: #e0e0e0; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background-color: #1a1a1a; border-radius: 5px; }}
                .header {{ color: #ff2a2a; text-align: center; font-size: 24px; margin-bottom: 20px; }}
                .code {{ font-size: 32px; font-weight: bold; color: #ff5e00; text-align: center; margin: 20px 0; padding: 15px; background-color: #0f0f0f; border-radius: 5px; }}
                .footer {{ margin-top: 30px; text-align: center; color: #888; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">Подтверждение регистрации в DarkGram</div>
                <p>Здравствуйте,</p>
                <p>Для завершения регистрации в системе DarkGram используйте следующий код подтверждения:</p>
                <div class="code">{code}</div>
                <p>Этот код действителен в течение 10 минут. Никому не сообщайте этот код.</p>
                <p>Если вы не запрашивали это подтверждение, проигнорируйте это сообщение.</p>
                <div class="footer">
                    © 2025 DarkGram Network. Все права защищены.<br>
                    Это автоматическое сообщение, пожалуйста, не отвечайте на него.
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Отправка письма
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return jsonify({'success': True}), 200
    
    except Exception as e:
        app.logger.error(f'Ошибка отправки email: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
