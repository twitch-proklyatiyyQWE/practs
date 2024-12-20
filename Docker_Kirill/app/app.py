from flask import Flask, render_template, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs('/data/images', exist_ok=True)

@app.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory('/data/images', filename)

if not os.path.exists('/data/info.txt'):
    with open('/data/info.txt', 'w', encoding='utf-8') as f:
        f.write('Начальная информация')

if not os.path.exists('/data/last_update.txt'):
    with open('/data/last_update.txt', 'w', encoding='utf-8') as f:
        f.write('Не обновлялось')

@app.route('/')
def index():
    try:
        with open('/data/last_update.txt', 'r', encoding='utf-8') as f:
            update_time = f.read().strip()
    except:
        update_time = "Не обновлялось"
        with open('/data/last_update.txt', 'w', encoding='utf-8') as f:
            f.write(update_time)

    try:
        with open('/data/info.txt', 'r', encoding='utf-8') as f:
            info = f.read().strip()
    except:
        info = "Начальная информация"
        with open('/data/info.txt', 'w', encoding='utf-8') as f:
            f.write(info)
    
    image_path = '/data/images'
    images = [f for f in os.listdir(image_path) if f.endswith(('.jpg', '.png', '.gif'))]
    current_image = images[0] if images else 'default.jpg'
    
    return render_template('index.html', 
                         info=info,
                         image=current_image,
                         last_update=update_time)

@app.route('/update_info', methods=['POST'])
def update_info():
    new_info = request.form.get('info')
    
    with open('/data/info.txt', 'w', encoding='utf-8') as f:
        f.write(new_info)
    
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open('/data/last_update.txt', 'w', encoding='utf-8') as f:
        f.write(f"Текст обновлен: {current_time}")
    
    return {'status': 'success'}

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return {'status': 'error', 'message': 'Нет файла'}
    
    file = request.files['image']
    if file.filename == '':
        return {'status': 'error', 'message': 'Файл не выбран'}
    
    if file:
        os.makedirs('/data/images', exist_ok=True)
        
        for old_file in os.listdir('/data/images'):
            os.remove(os.path.join('/data/images', old_file))
        
        filename = secure_filename(file.filename)
        file.save(os.path.join('/data/images', filename))
        
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        with open('/data/last_update.txt', 'w', encoding='utf-8') as f:
            f.write(f"Изображение обновлено: {current_time}")
        
        return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)