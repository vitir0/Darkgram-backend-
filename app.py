from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

app = Flask(__name__)
CORS(app)

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ===== КОНФИГУРАЦИЯ =====
# Используем переменные окружения для безопасности
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.yandex.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
SMTP_USER = os.getenv('SMTP_USER', 'network-testt@yandex.ru')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'valewagjffambxns')
# ========================

def send_email_via_smtp(email, code):
    try:
        # Создаем сообщение
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = email
        msg['Subject'] = 'Код подтверждения DarkGram'
        
        # HTML-содержимое письма
        html = f"""
        <html>
        <head>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    background-color: #050505; 
                    color: #e0e0e0; 
                    margin: 0;
                    padding: 20px;
                }}
                .container {{ 
                    max-width: 600px; 
                    margin: 0 auto; 
                    padding: 20px; 
                    border: 1px solid #ff2a2a; 
                    background-color: rgba(10, 2, 2, 0.85);
                    border-radius: 5px;
                }}
                .header {{ 
                    text-align: center; 
                    margin-bottom: 20px; 
                }}
                .header h2 {{
                    color: #ff5e00;
                    margin-bottom: 10px;
                }}
                .code {{ 
                    font-size: 2.5rem; 
                    letter-spacing: 5px; 
                    color: #ff5e00; 
                    text-align: center; 
                    margin: 30px 0;
                    padding: 15px;
                    background: rgba(0,0,0,0.3);
                    border: 1px solid #ff2a2a;
                    border-radius: 5px;
                }}
                .footer {{ 
                    margin-top: 30px; 
                    text-align: center; 
                    font-size: 0.9rem; 
                    opacity: 0.7; 
                }}
                p {{
                    line-height: 1.6;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>DarkGram | Подтверждение Email</h2>
                </div>
                
                <p>Ваш код подтверждения для завершения регистрации:</p>
                
                <div class="code">{code}</div>
                
                <p>Введите этот код в форме регистрации для активации вашего аккаунта.</p>
                
                <div class="footer">
                    DARKGRAM NETWORK // PROTECTED BY LEVEL 7 ENCRYPTION // 2025
                </div>
            </div>
        </body>
        </html>
        """
        
        # Прикрепляем HTML к письму
        msg.attach(MIMEText(html, 'html'))
        
        # Создаем SMTP соединение
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # Шифруем соединение
        
        # Аутентификация
        server.login(SMTP_USER, SMTP_PASSWORD)
        
        # Отправка письма
        server.sendmail(SMTP_USER, email, msg.as_string())
        server.quit()
        
        logging.info(f"Email sent to {email}")
        return True, None
        
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"SMTP Authentication Error: {e}")
        return False, "Неверные учетные данные SMTP. Проверьте логин/пароль."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP Error: {e}")
        return False, f"Ошибка SMTP: {str(e)}"
    except Exception as e:
        logging.error(f"General Error: {str(e)}")
        return False, f"Общая ошибка: {str(e)}"

@app.route('/send-verification', methods=['POST', 'OPTIONS'])
def send_verification():
    if request.method == 'OPTIONS':
        # Предварительный запрос CORS
        response = jsonify({'status': 'preflight'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
        
    try:
        data = request.json
        email = data.get('email')
        code = data.get('code')
        
        if not email or not code:
            return jsonify(success=False, error="Требуется email и код"), 400
        
        # Проверка формата email
        if '@' not in email or '.' not in email:
            return jsonify(success=False, error="Неверный формат email"), 400
        
        # Отправка письма
        success, error = send_email_via_smtp(email, code)
        
        if success:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, error=error), 500
            
    except Exception as e:
        logging.exception("Unexpected error:")
        return jsonify(success=False, error="Internal server error"), 500

if __name__ == '__main__':
    # Для локального тестирования
    app.run(host='0.0.0.0', port=10000)
