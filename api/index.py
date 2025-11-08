"""
Be My Code - Web IDE (Vercel Serverless Compatible)
Flask web application - Simplified for serverless deployment
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Modülleri ekle (api klasöründen)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from modules.nlp_processor import NLPProcessor
    from modules.code_analyzer import CodeAnalyzer
    from modules.logger import setup_logger
    
    logger = setup_logger()
    nlp = NLPProcessor()
    analyzer = CodeAnalyzer()
except Exception as e:
    print(f"Module import error: {e}")
    # Fallback: basit NLP
    class SimpleNLP:
        def process_command(self, command, context=""):
            return None
    nlp = SimpleNLP()
    analyzer = None
    
    import logging
    logger = logging.getLogger(__name__)

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'be_my_code_secret_key_2025')

# Workspace dizini
WORKSPACE_DIR = Path('/tmp') / "BeMyCode_Workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/generate_conversation_code', methods=['POST'])
def generate_conversation_code():
    """Konuşma tabanlı kod üretimi - Gemini sürekli konuşarak yönlendirir"""
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')
        context = data.get('context', '')
        prompt = data.get('prompt', '')
        
        if not user_input:
            return jsonify({'success': False, 'error': 'Kullanıcı girişi boş'})
        
        # Gemini'ye özel prompt
        conversation_prompt = f"""Kullanıcı sana şunu söyledi: "{user_input}"
Sen ona şu soruyu sormuştun: "{prompt}"

Şimdi:
1. Kullanıcının isteğini anla
2. Python kodu üret (sadece kod, yorum satırı yok)
3. Kısa bir açıklama cümlesi oluştur (Türkçe, konuşma dilinde)

Mevcut kod:
{context}

Yanıt formatı:
CODE: [Python kodu buraya]
EXPLANATION: [Türkçe açıklama buraya, örnek: "Tamam, değişken oluşturdum" veya "Döngü eklendi"]
"""
        
        # Gemini ile kod üret
        if nlp.gemini:
            try:
                response = nlp.gemini.generate_content(conversation_prompt)
                response_text = response.text
                
                # CODE ve EXPLANATION kısımlarını ayır
                code_part = ''
                explanation_part = ''
                
                if 'CODE:' in response_text and 'EXPLANATION:' in response_text:
                    parts = response_text.split('EXPLANATION:')
                    code_part = parts[0].replace('CODE:', '').strip()
                    explanation_part = parts[1].strip()
                    
                    # Kod bloğu temizle
                    if '```python' in code_part:
                        code_part = code_part.split('```python')[1].split('```')[0].strip()
                    elif '```' in code_part:
                        code_part = code_part.split('```')[1].split('```')[0].strip()
                else:
                    # Fallback: tüm yanıtı kod olarak al
                    code_part = response_text.strip()
                    explanation_part = "Kod eklendi"
                
                return jsonify({
                    'success': True,
                    'code': code_part,
                    'explanation': explanation_part
                })
            except Exception as e:
                print(f"Gemini hatası: {e}")
                return jsonify({
                    'success': False,
                    'error': f'Gemini hatası: {str(e)}'
                })
        else:
            return jsonify({
                'success': False,
                'error': 'Gemini mevcut değil'
            })
            
    except Exception as e:
        print(f"Genel hata: {e}")
        return jsonify({'success': False, 'error': str(e)})

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
            ['python3', temp_file],
            capture_output=True,
            text=True,
            timeout=5  # Vercel timeout limiti
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
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        return jsonify({
            'success': False,
            'error': 'Kod 5 saniyede tamamlanamadı (Vercel timeout)'
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

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'gemini_available': nlp.gemini is not None if hasattr(nlp, 'gemini') else False
    })

# Vercel için
app = app

if __name__ == '__main__':
    print("🚀 Be My Code Web IDE başlatılıyor...")
    print(f"📁 Workspace: {WORKSPACE_DIR}")
    print("🌐 Tarayıcınızda açın: http://localhost:5001")
    print("\n✨ Gemini AI entegrasyonu aktif!")
    print("\n📚 TÜBİTAK 2209-A Projesi")
    print("👨‍💻 Proje Sahibi: Erol Işıldak")
    print("👩‍🏫 Danışman: Öğr. Gör. Gülsüm KEMERLİ")
    print("🤝 Proje Ortağı: Harun Efe Akkan")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
