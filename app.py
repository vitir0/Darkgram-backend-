from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS  # Импорт модуля CORS

app = Flask(__name__)
CORS(app)  # Разрешить все CORS-запросы

# ===== КОНФИГУРАЦИЯ =====
# ЗАМЕНИТЕ ЭТИ ДАННЫЕ НА ВАШИ РЕАЛЬНЫЕ SMTP-НАСТРОЙКИ
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 443
SMTP_USER = "darkgramnetwork@gmail.com"
SMTP_PASSWORD = "darkgram1234"
# ========================

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
            return jsonify({'success': False, 'error': 'Недостаточно данных'}), 400
        
        subject = 'Код подтверждения DarkGram'
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #050505; color: #e0e0e0; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ff2a2a; background-color: rgba(10, 2, 2, 0.85); }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .code {{ font-size: 2.5rem; letter-spacing: 5px; color: #ff5e00; text-align: center; margin: 30px 0; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 0.9rem; opacity: 0.7; }}
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
        
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = email
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [email], msg.as_string())
        
        response = jsonify({'success': True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        response = jsonify({'success': False, 'error': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
