"""
Be My Code - Web IDE
Flask web application entry point
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Modülleri ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modules.nlp_processor import NLPProcessor
from modules.code_analyzer import CodeAnalyzer
from modules.logger import setup_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'be_my_code_secret_key_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

logger = setup_logger()
nlp = NLPProcessor()
analyzer = CodeAnalyzer()

# Workspace dizini
WORKSPACE_DIR = Path.home() / "BeMyCode_Workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/process_command', methods=['POST'])
def process_command():
    """Sesli komutu işle"""
    data = request.json
    command = data.get('command', '')
    context = data.get('context', '')
    
    logger.info(f"Komut alındı: {command}")
    
    # NLP ile işle
    code = nlp.process_command(command, context)
    
    if code:
        return jsonify({
            'success': True,
            'code': code,
            'message': 'Kod oluşturuldu'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Komut anlaşılamadı, dikteye geçiliyor'
        })

@app.route('/api/run_code', methods=['POST'])
def run_code():
    """Python kodunu çalıştır"""
    data = request.json
    code = data.get('code', '')
    
    if not code.strip():
        return jsonify({
            'success': False,
            'error': 'Kod boş'
        })
    
    # Geçici dosyaya yaz ve çalıştır
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Çalıştır
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Geçici dosyayı sil
        os.unlink(temp_file)
        
        return jsonify({
            'success': True,
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode
        })
        
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return jsonify({
            'success': False,
            'error': 'Kod 10 saniyede tamamlanamadı (timeout)'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/analyze_code', methods=['POST'])
def analyze_code():
    """Kodu analiz et"""
    data = request.json
    code = data.get('code', '')
    
    if not code.strip():
        return jsonify({'suggestions': []})
    
    # Analiz yap
    suggestions = analyzer.get_suggestions(code)
    
    return jsonify({
        'suggestions': suggestions
    })

@app.route('/api/save_file', methods=['POST'])
def save_file():
    """Dosyayı kaydet"""
    data = request.json
    filename = data.get('filename', 'untitled.py')
    code = data.get('code', '')
    
    # Güvenlik: sadece .py uzantılı dosyalar
    if not filename.endswith('.py'):
        filename += '.py'
    
    # Workspace'e kaydet
    filepath = WORKSPACE_DIR / filename
    
    try:
        filepath.write_text(code, encoding='utf-8')
        logger.info(f"Dosya kaydedildi: {filepath}")
        
        return jsonify({
            'success': True,
            'message': f'{filename} kaydedildi',
            'path': str(filepath)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/load_file', methods=['POST'])
def load_file():
    """Dosyayı yükle"""
    data = request.json
    filename = data.get('filename', '')
    
    filepath = WORKSPACE_DIR / filename
    
    if not filepath.exists():
        return jsonify({
            'success': False,
            'error': 'Dosya bulunamadı'
        })
    
    try:
        code = filepath.read_text(encoding='utf-8')
        return jsonify({
            'success': True,
            'code': code,
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/list_files', methods=['GET'])
def list_files():
    """Workspace dosyalarını listele"""
    try:
        files = [f.name for f in WORKSPACE_DIR.glob('*.py')]
        return jsonify({
            'success': True,
            'files': sorted(files)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Client bağlandı"""
    logger.info("Client bağlandı")
    emit('connected', {'message': 'Be My Code IDE\'ye hoş geldiniz!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Client bağlantısı kesildi"""
    logger.info("Client bağlantısı kesildi")

@socketio.on('voice_command')
def handle_voice_command(data):
    """Sesli komut geldi"""
    command = data.get('command', '')
    context = data.get('context', '')
    
    logger.info(f"WebSocket sesli komut: {command}")
    
    # İşle
    code = nlp.process_command(command, context)
    
    if code:
        emit('code_generated', {
            'code': code,
            'command': command
        })
    else:
        emit('dictation_mode', {
            'text': command
        })

if __name__ == '__main__':
    print("🚀 Be My Code Web IDE başlatılıyor...")
    print(f"📁 Workspace: {WORKSPACE_DIR}")
    print("🌐 Tarayıcınızda açın: http://localhost:5001")
    print("🎤 Mikrofon erişimi için HTTPS gerekebilir (production)")
    print("\n✨ Gemini AI entegrasyonu aktif!")
    print("\n📚 TÜBİTAK 2209-A Projesi")
    print("👨‍💻 Proje Sahibi: Erol Işıldak")
    print("👩‍🏫 Danışman: Öğr. Gör. Gülsüm KEMERLİ")
    print("🤝 Proje Ortağı: Harun Efe Akkan")
    
    # Development modda çalıştır
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
