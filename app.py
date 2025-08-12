from flask import Flask, request, jsonify
from flask_cors import CORS
import yagmail
import logging
import os

app = Flask(__name__)
CORS(app)

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ===== КОНФИГУРАЦИЯ =====
SMTP_USER = os.getenv('SMTP_USER', 'darkgramnetwork@gmail.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'darkgram1234')  # Замените на реальный пароль
# ========================

def send_email_via_gmail(email, code):
    try:
        # Инициализация Yagmail
        yag = yagmail.SMTP(SMTP_USER, SMTP_PASSWORD)
        
        # Содержимое письма
        contents = [
            f"""
            <div style="font-family: Arial, sans-serif; background-color: #050505; color: #e0e0e0; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ff2a2a; background-color: rgba(10, 2, 2, 0.85);">
                    <h2 style="text-align: center; color: #ff5e00; margin-bottom: 20px;">DarkGram | Подтверждение Email</h2>
                    
                    <p>Ваш код подтверждения для завершения регистрации:</p>
                    
                    <div style="font-size: 2.5rem; letter-spacing: 5px; color: #ff5e00; text-align: center; margin: 30px 0; padding: 10px; background: rgba(0,0,0,0.3); border: 1px solid #ff2a2a;">
                        {code}
                    </div>
                    
                    <p>Введите этот код в форме регистрации для активации вашего аккаунта.</p>
                    
                    <div style="margin-top: 30px; text-align: center; font-size: 0.9rem; opacity: 0.7;">
                        DARKGRAM NETWORK // PROTECTED BY LEVEL 7 ENCRYPTION // 2025
                    </div>
                </div>
            </div>
            """
        ]
        
        # Отправка письма
        yag.send(
            to=email,
            subject='Код подтверждения DarkGram',
            contents=contents
        )
        
        logging.info(f"Письмо отправлено на {email}")
        return True, None
        
    except Exception as e:
        logging.error(f"Ошибка отправки письма: {str(e)}")
        return False, str(e)

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
        if not data:
            return jsonify(success=False, error="Данные не предоставлены"), 400
        
        email = data.get('email')
        code = data.get('code')
        
        if not email or not code:
            return jsonify(success=False, error="Требуется email и код"), 400
        
        # Проверка формата email
        if '@' not in email or '.' not in email:
            return jsonify(success=False, error="Неверный формат email"), 400
        
        # Попытка отправки письма
        success, error = send_email_via_gmail(email, code)
        
        if success:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error=error or "Ошибка отправки письма"), 500
            
    except Exception as e:
        logging.exception("Непредвиденная ошибка:")
        return jsonify(success=False, error="Внутренняя ошибка сервера"), 500

def _corsify_response(response):
    """Добавляет CORS-заголовки к ответу"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    # Запуск с поддержкой HTTPS для совместимости с современными браузерами
    app.run(host='0.0.0.0', port=10000, ssl_context='adhoc')
