"""
Be My Code - Ana Pencere
PyQt5 tabanlı ana IDE penceresi
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTextEdit, QTreeView, QFileSystemModel, QPushButton, QLabel,
    QStatusBar, QToolBar, QAction, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDir
from PyQt5.QtGui import QFont, QTextCursor, QIcon

import sys
from io import StringIO
from pathlib import Path

from modules.speech_recognizer import SpeechRecognizer
from modules.text_to_speech_alt import TextToSpeech
from modules.nlp_processor import NLPProcessor
from modules.code_analyzer import CodeAnalyzer
from modules.logger import setup_logger

logger = setup_logger(__name__)


class VoiceThread(QThread):
    """Ses tanıma için ayrı thread"""
    text_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, speech_recognizer):
        super().__init__()
        self.speech_recognizer = speech_recognizer
        self.running = True
    
    def run(self):
        """Thread çalıştır"""
        while self.running:
            try:
                text = self.speech_recognizer.listen_once()
                if text:
                    self.text_received.emit(text)
            except Exception as e:
                logger.error(f"Ses tanıma hatası: {e}")
                self.error_occurred.emit(str(e))
    
    def stop(self):
        """Thread'i durdur"""
        self.running = False


class MainWindow(QMainWindow):
    """Ana IDE penceresi"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Be My Code - Görme Engelli IDE")
        self.setGeometry(100, 100, 1400, 900)
        
        # Bileşenler
        self.speech_recognizer = SpeechRecognizer()
        self.tts = TextToSpeech()
        self.nlp = NLPProcessor()
        self.analyzer = CodeAnalyzer()
        
        # Ses tanıma thread'i
        self.voice_thread = None
        self.voice_active = False
        
        # UI oluştur
        self._create_ui()
        self._create_toolbar()
        self._create_status_bar()
        
        # Workspace ayarla
        self.workspace_path = Path.home() / "BeMyCode_Workspace"
        self.workspace_path.mkdir(exist_ok=True)
        self._setup_file_explorer()
        
        logger.info("MainWindow başlatıldı")
    
    def _create_ui(self):
        """Ana UI bileşenlerini oluştur"""
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Ana layout
        main_layout = QVBoxLayout(central_widget)
        
        # Splitter (dosya gezgini + editor + terminal)
        splitter = QSplitter(Qt.Horizontal)
        
        # Sol panel: Dosya gezgini
        self.file_tree = QTreeView()
        self.file_tree.setMinimumWidth(250)
        splitter.addWidget(self.file_tree)
        
        # Orta panel: Kod editörü
        right_splitter = QSplitter(Qt.Vertical)
        
        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont("Courier New", 14))
        self.code_editor.setPlaceholderText("Kodunuzu buraya yazın veya ses komutu kullanın...")
        right_splitter.addWidget(self.code_editor)
        
        # Alt panel: Terminal
        self.terminal = QTextEdit()
        self.terminal.setFont(QFont("Courier New", 12))
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumHeight(250)
        self.terminal.setPlaceholderText("Program çıktıları burada görünecek...")
        right_splitter.addWidget(self.terminal)
        
        splitter.addWidget(right_splitter)
        
        # Splitter oranları
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        
        main_layout.addWidget(splitter)
    
    def _create_toolbar(self):
        """Toolbar oluştur"""
        toolbar = QToolBar("Ana Toolbar")
        toolbar.setIconSize(toolbar.iconSize() * 1.5)
        self.addToolBar(toolbar)
        
        # Dosya işlemleri
        new_action = QAction("📄 Yeni", self)
        new_action.triggered.connect(self._new_file)
        toolbar.addAction(new_action)
        
        open_action = QAction("📂 Aç", self)
        open_action.triggered.connect(self._open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction("💾 Kaydet", self)
        save_action.triggered.connect(self._save_file)
        save_action.setShortcut("Ctrl+S")
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Mikrofon butonu
        self.mic_button = QAction("🎤 Mikrofon (Ctrl+M)", self)
        self.mic_button.triggered.connect(self._toggle_voice)
        self.mic_button.setShortcut("Ctrl+M")
        toolbar.addAction(self.mic_button)
        
        # Kod okuma
        read_action = QAction("🔊 Kodu Oku (Ctrl+R)", self)
        read_action.triggered.connect(self._read_code)
        read_action.setShortcut("Ctrl+R")
        toolbar.addAction(read_action)
        
        # Satır okuma
        read_line_action = QAction("📖 Satır Oku (Ctrl+L)", self)
        read_line_action.triggered.connect(self._read_current_line)
        read_line_action.setShortcut("Ctrl+L")
        toolbar.addAction(read_line_action)
        
        toolbar.addSeparator()
        
        # Spacer ekle (RUN butonunu sağa itmek için)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        
        # RUN butonu (büyük ve yeşil)
        run_button = QPushButton("▶ ÇALIŞTIR (F5)")
        run_button.setMinimumHeight(50)
        run_button.setMinimumWidth(200)
        run_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        run_button.clicked.connect(self._run_code)
        toolbar.addWidget(run_button)
        
        # Code completion
        suggest_action = QAction("💡 Öneri (Ctrl+Space)", self)
        suggest_action.triggered.connect(self._show_suggestions)
        suggest_action.setShortcut("Ctrl+Space")
        toolbar.addAction(suggest_action)
    
    def _create_status_bar(self):
        """Status bar oluştur"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Hazır - Mikrofon için Ctrl+M'e basın")
    
    def _setup_file_explorer(self):
        """Dosya gezginini ayarla"""
        model = QFileSystemModel()
        model.setRootPath(str(self.workspace_path))
        
        self.file_tree.setModel(model)
        self.file_tree.setRootIndex(model.index(str(self.workspace_path)))
        self.file_tree.setColumnWidth(0, 250)
        
        # Dosya tıklama
        self.file_tree.doubleClicked.connect(self._open_file_from_tree)
    
    def _toggle_voice(self):
        """Ses tanımayı aç/kapat"""
        if not self.voice_active:
            # Mikrofonu aç
            self.voice_active = True
            self.mic_button.setText("🔴 Dinliyor... (Ctrl+M)")
            self.status_bar.showMessage("🎤 Mikrofon aktif - Konuşun...")
            self.tts.speak("Dinliyorum")
            
            # Thread başlat
            self.voice_thread = VoiceThread(self.speech_recognizer)
            self.voice_thread.text_received.connect(self._process_voice_command)
            self.voice_thread.error_occurred.connect(self._voice_error)
            self.voice_thread.start()
        else:
            # Mikrofonu kapat
            self.voice_active = False
            self.mic_button.setText("🎤 Mikrofon (Ctrl+M)")
            self.status_bar.showMessage("Mikrofon kapatıldı")
            self.tts.speak("Mikrofon kapatıldı")
            
            if self.voice_thread:
                self.voice_thread.stop()
                self.voice_thread.wait()
        
        logger.info("Ses tanıma thread'i başlatıldı")
    
    def _process_voice_command(self, text: str):
        """Ses komutunu işle"""
        self.status_bar.showMessage(f"Komut alındı: {text}")
        logger.info(f"Ses komutu: {text}")
        
        # Özel komutlar kontrolü
        text_lower = text.lower()
        
        # Komut listesi sözlüğü (numaralı erişim için)
        command_list = {
            "birinci": "alt_satir",
            "ikinci": "yazdir",
            "üçüncü": "satir_oku",
            "dördüncü": "terminal_oku",
            "beşinci": "komut_listesi"
        }
        
        # Numaralı komut çağrıları (birinci komut, ikinci komut vb.)
        for num, cmd in command_list.items():
            if num in text_lower and "komut" in text_lower:
                logger.info(f"Numaralı komut çağrıldı: {num} -> {cmd}")
                if cmd == "alt_satir":
                    self._move_down_one_line()
                elif cmd == "yazdir":
                    self._run_code()
                elif cmd == "satir_oku":
                    self._read_specific_line(1)
                elif cmd == "terminal_oku":
                    self._read_terminal_output()
                elif cmd == "komut_listesi":
                    self._read_command_list()
                return
        
        # 1- Alt satıra geç
        if any(phrase in text_lower for phrase in ["alt satır", "alt satıra geç", "aşağı", "bir alt"]):
            logger.info(f"ALT SATIR komutu algılandı: {text}")
            self._move_down_one_line()
            return
        
        # 2- Komutu yazdır (terminale yazdır)
        if any(cmd in text_lower for cmd in ["yazdır", "çalıştır", "run", "play", "başlat"]) and "komut" not in text_lower:
            logger.info(f"RUN komutu algılandı: {text}")
            self._run_code()
            return
        
        # 3- X. satırı oku (örn: "1. satırı oku", "birinci satırı oku")
        import re
        line_match = re.search(r'(\d+)\.?\s*satır', text_lower)
        if line_match:
            line_num = int(line_match.group(1))
            logger.info(f"SATIR OKU komutu algılandı: {line_num}. satır")
            self._read_specific_line(line_num)
            return
        
        # 4- Terminal çıktısını oku
        if any(phrase in text_lower for phrase in ["terminal oku", "terminal çıktı", "çıktı oku", "çıktıyı oku"]):
            logger.info(f"TERMINAL OKU komutu algılandı: {text}")
            self._read_terminal_output()
            return
        
        # 5- Sesli komut listesini oku
        if any(phrase in text_lower for phrase in ["komut listesi", "komutları listele", "komutları oku", "yardım"]):
            logger.info(f"KOMUT LİSTESİ komutu algılandı: {text}")
            self._read_command_list()
            return
        
        # "oku" komutu -> Tüm kodu sesli oku
        if "oku" in text_lower and "satır" not in text_lower and "terminal" not in text_lower:
            logger.info(f"OKU komutu algılandı: {text}")
            self._read_code()
            return
        
        # NLP ile koda çevir
        code = self.nlp.process_command(text)
        
        if code:
            # Kodu editöre ekle
            cursor = self.code_editor.textCursor()
            cursor.insertText(code + "\n")
            self.code_editor.setTextCursor(cursor)
            
            # Oluşturulan kodu oku
            self.tts.speak("Kod oluşturuldu")
            
            self.status_bar.showMessage("✅ Kod başarıyla eklendi")
            logger.info(f"Kod eklendi: {code}")
        else:
            # Komut tanınmadıysa, söylenen metni direkt yaz (DİKTE MODU)
            cursor = self.code_editor.textCursor()
            
            # Satır numarasını al (yazmadan önce)
            line_number = cursor.blockNumber() + 1
            
            # Her şeyi direkt yaz (# işareti olmadan)
            cursor.insertText(text + "\n")
            self.tts.speak(f"{line_number}. satıra {text} yazdım")
            logger.info(f"Dikte edildi: {text} (satır: {line_number})")
            
            self.code_editor.setTextCursor(cursor)
            self.status_bar.showMessage(f"✍️ {line_number}. satıra dikte edildi: {text}")
    
    def _read_code(self):
        """Tüm kodu sesli oku"""
        code = self.code_editor.toPlainText()
        if code.strip():
            self.tts.speak("Kodu okuyorum")
            self.tts.speak_code(code, line_by_line=False)
        else:
            self.tts.speak("Editörde kod bulunmuyor")
    
    def _read_current_line(self):
        """Geçerli satırı oku"""
        cursor = self.code_editor.textCursor()
        cursor.select(cursor.LineUnderCursor)
        line = cursor.selectedText()
        
        if line.strip():
            line_number = cursor.blockNumber() + 1
            self.tts.speak(f"Satır {line_number}: {self.tts._code_to_turkish(line)}")
        else:
            self.tts.speak("Satır boş")
    
    def _move_down_one_line(self):
        """İmleci bir alt satıra taşı"""
        cursor = self.code_editor.textCursor()
        cursor.movePosition(cursor.Down)
        self.code_editor.setTextCursor(cursor)
        line_number = cursor.blockNumber() + 1
        self.tts.speak(f"{line_number}. satıra geçtim")
        self.status_bar.showMessage(f"⬇️ {line_number}. satır")
        logger.info(f"Alt satıra geçildi: {line_number}")
    
    def _read_specific_line(self, line_num: int):
        """Belirli bir satırı oku"""
        code = self.code_editor.toPlainText()
        lines = code.split('\n')
        
        if 1 <= line_num <= len(lines):
            line_content = lines[line_num - 1]
            if line_content.strip():
                self.tts.speak(f"{line_num}. satır: {self.tts._code_to_turkish(line_content)}")
            else:
                self.tts.speak(f"{line_num}. satır boş")
        else:
            self.tts.speak(f"{line_num}. satır bulunamadı. Toplam {len(lines)} satır var")
        
        logger.info(f"{line_num}. satır okundu")
    
    def _read_terminal_output(self):
        """Terminal çıktısını oku"""
        output = self.terminal.toPlainText()
        
        if output.strip():
            # ">>> Kod çalıştırılıyor..." gibi sistem mesajlarını temizle
            lines = [line for line in output.split('\n') 
                    if line.strip() and not line.startswith('>>>') and not line.startswith('✅')]
            
            if lines:
                clean_output = '\n'.join(lines)
                self.tts.speak("Terminal çıktısı:")
                self.tts.speak(clean_output)
            else:
                self.tts.speak("Terminal çıktısı boş")
        else:
            self.tts.speak("Terminalde çıktı yok")
        
        logger.info("Terminal çıktısı okundu")
    
    def _read_command_list(self):
        """Sesli komut listesini oku"""
        commands = """
        Sesli Komut Listesi:
        Birinci komut: Bir alt satıra geç.
        İkinci komut: Kodu terminale yazdır.
        Üçüncü komut: Birinci satırı oku.
        Dördüncü komut: Terminal çıktısını oku.
        Beşinci komut: Bu komut listesini oku.
        
        Diğer komutlar:
        Yazdır veya Çalıştır: Kodu çalıştır.
        Oku: Tüm kodu oku.
        1. satırı oku: Belirli bir satırı oku.
        Alt satıra geç: Bir satır aşağı in.
        Terminal oku: Terminal çıktısını oku.
        """
        
        self.tts.speak(commands)
        logger.info("Komut listesi okundu")
    
    def _run_code(self):
        """Kodu çalıştır"""
        code = self.code_editor.toPlainText()
        
        if not code.strip():
            self.tts.speak("Çalıştırılacak kod yok")
            self.status_bar.showMessage("❌ Editörde kod bulunmuyor")
            return
        
        logger.info("Kod çalıştırılıyor...")
        self.status_bar.showMessage("▶️ Kod çalıştırılıyor...")
        
        self.terminal.clear()
        self.terminal.append(">>> Kod çalıştırılıyor...\n")
        self.tts.speak("Kod çalıştırılıyor")
        
        try:
            # stdout'u terminale yönlendir
            import sys
            from io import StringIO
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Kodu çalıştır
            exec_globals = {}
            exec(code, exec_globals)
            
            # Çıktıyı al
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            if output:
                # Terminal'e çıktı yazıldı
                self.terminal.append(output)
                self.terminal.append("\n✅ Kod başarıyla çalıştırıldı")
                self.status_bar.showMessage("✅ Kod başarıyla çalıştırıldı")
                
                # Çıktıyı sesli oku
                self.tts.speak("Kod başarıyla çalıştırıldı. Çıktı:")
                self.tts.speak(output)
                
                logger.info(f"Kod çalıştırıldı. Çıktı: {output[:100]}...")
            else:
                # Çıktı yok
                self.terminal.append("\n✅ Kod başarıyla çalıştırıldı (Çıktı yok)")
                self.status_bar.showMessage("✅ Kod başarıyla çalıştırıldı")
                self.tts.speak("Kod başarıyla çalıştırıldı. Terminale birşey yazdırılmadı")
                logger.info("Kod çalıştırıldı (çıktı yok)")
                
        except Exception as e:
            error_msg = str(e)
            self.terminal.append(f"\n❌ HATA: {error_msg}")
            self.status_bar.showMessage(f"❌ Hata: {error_msg}")
            self.tts.speak(f"Hata oluştu: {error_msg}")
            logger.error(f"Kod çalıştırma hatası: {error_msg}")
    
    def _show_suggestions(self):
        """Kod önerileri göster"""
        cursor = self.code_editor.textCursor()
        cursor.select(cursor.WordUnderCursor)
        word = cursor.selectedText()
        
        suggestions = self.analyzer.get_suggestions(word)
        
        if suggestions:
            self.tts.speak(f"{len(suggestions)} öneri bulundu")
            for i, suggestion in enumerate(suggestions[:5], 1):
                self.tts.speak(f"{i}. {suggestion}")
        else:
            self.tts.speak("Öneri bulunamadı")
    
    def _voice_error(self, error_msg: str):
        """Ses tanıma hatası"""
        self.status_bar.showMessage(f"❌ Ses hatası: {error_msg}")
        logger.error(f"Ses hatası: {error_msg}")
    
    def _new_file(self):
        """Yeni dosya"""
        self.code_editor.clear()
        self.status_bar.showMessage("Yeni dosya oluşturuldu")
        self.tts.speak("Yeni dosya")
    
    def _open_file(self):
        """Dosya aç"""
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Dosya Aç", str(self.workspace_path), "Python Files (*.py);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.code_editor.setPlainText(content)
                    self.status_bar.showMessage(f"Dosya açıldı: {file_path}")
                    self.tts.speak("Dosya açıldı")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya açılamadı: {e}")
    
    def _open_file_from_tree(self, index):
        """Dosya gezgininden dosya aç"""
        model = self.file_tree.model()
        file_path = model.filePath(index)
        
        if Path(file_path).is_file() and file_path.endswith('.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.code_editor.setPlainText(content)
                    self.status_bar.showMessage(f"Dosya açıldı: {file_path}")
                    self.tts.speak("Dosya açıldı")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya açılamadı: {e}")
    
    def _save_file(self):
        """Dosya kaydet"""
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Dosya Kaydet", str(self.workspace_path), "Python Files (*.py);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.code_editor.toPlainText())
                    self.status_bar.showMessage(f"Dosya kaydedildi: {file_path}")
                    self.tts.speak("Dosya kaydedildi")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi: {e}")
    
    def keyPressEvent(self, event):
        """Klavye olaylarını yakala"""
        # F5 tuşu - Kodu çalıştır
        if event.key() == Qt.Key_F5:
            self._run_code()
            event.accept()
            return
        
        # Ctrl+M - Mikrofon
        if event.key() == Qt.Key_M and event.modifiers() == Qt.ControlModifier:
            self._toggle_voice()
            event.accept()
            return
        
        # Ctrl+R - Kodu oku
        if event.key() == Qt.Key_R and event.modifiers() == Qt.ControlModifier:
            self._read_code()
            event.accept()
            return
        
        # Ctrl+L - Satırı oku
        if event.key() == Qt.Key_L and event.modifiers() == Qt.ControlModifier:
            self._read_current_line()
            event.accept()
            return
        
        super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Pencere kapatılırken"""
        if self.voice_thread and self.voice_thread.isRunning():
            self.voice_thread.stop()
            self.voice_thread.wait()
        
        logger.info("Ana pencere kapatılıyor")
        event.accept()
