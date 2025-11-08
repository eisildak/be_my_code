// Ana Uygulama - Be My Code Web IDE
class BeMyCodeApp {
    constructor() {
        // Bileşenleri başlat
        this.editor = new CodeEditor('code-editor');
        this.voice = new VoiceRecognition();
        this.tts = new TextToSpeech();
        
        // Konuşma durumu
        this.conversationMode = true;
        this.waitingForCode = false;
        this.currentPrompt = '';
        
        // UI elemanları
        this.micBtn = document.getElementById('mic-btn');
        this.runBtn = document.getElementById('run-btn');
        this.saveBtn = document.getElementById('save-btn');
        this.newFileBtn = document.getElementById('new-file-btn');
        this.clearTerminalBtn = document.getElementById('clear-terminal-btn');
        this.filenameInput = document.getElementById('filename');
        this.terminalOutput = document.getElementById('terminal-output');
        this.voiceCommandText = document.getElementById('voice-command-text');
        this.statusText = document.getElementById('status-text');
        this.listeningIndicator = document.getElementById('listening-indicator');
        this.autoSpeakCheckbox = document.getElementById('auto-speak');
        this.geminiModeCheckbox = document.getElementById('gemini-mode');
        
        // Event listeners
        this.setupEventListeners();
        this.setupVoiceCallbacks();
        
        // Dosyaları yükle
        this.loadFileList();
        
        // Hoş geldin ve ilk soru
        this.speak('Merhaba! Ben Be My Code asistanınızım. Size Python kodu yazmakta yardımcı olacağım.');
        setTimeout(() => {
            this.askForCode();
        }, 3000);
    }

    setupEventListeners() {
        // Mikrofon butonu
        this.micBtn.addEventListener('click', () => {
            if (this.voice.isListening) {
                this.voice.stop();
            } else {
                this.voice.start();
            }
        });
        
        // Klavye kısayolları
        document.addEventListener('keydown', (e) => {
            // Ctrl+M veya Cmd+M - Mikrofon
            if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
                e.preventDefault();
                this.micBtn.click();
            }
            
            // F5 - Kodu çalıştır (kod düzenleyicide değilse)
            if (e.key === 'F5' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                this.runCode();
            }
        });
    }

    setupVoiceCallbacks() {
        this.voice.onStart = () => {
            this.micBtn.classList.add('active');
            this.listeningIndicator.classList.add('active');
            this.updateStatus('Dinleniyor...', 'warning');
        };

        this.voice.onResult = (transcript) => {
            this.voiceCommandText.textContent = `📝 "${transcript}"`;
            this.handleUserResponse(transcript);
        };

        this.voice.onError = (errorCode, errorMessage) => {
            this.updateStatus('Ses hatası', 'error');
            this.voiceCommandText.textContent = `❌ ${errorMessage || 'Ses tanıma hatası'}`;
            
            // Kullanıcıya bilgi ver
            if (errorCode === 'not-allowed') {
                alert('🎤 Mikrofon İzni Gerekli\n\nTarayıcı ayarlarından mikrofon iznini açın:\n1. Adres çubuğundaki kilit ikonuna tıklayın\n2. Mikrofon iznini "İzin Ver" olarak değiştirin\n3. Sayfayı yenileyin');
            } else if (errorCode === 'not-supported') {
                alert('⚠️ Tarayıcı Desteği Yok\n\nChrome, Edge veya Safari tarayıcısı kullanmanız gerekiyor.');
            }
        };

        this.voice.onEnd = () => {
            this.micBtn.classList.remove('active');
            this.listeningIndicator.classList.remove('active');
            this.updateStatus('Hazır', 'success');
        };
    }

    askForCode() {
        const prompts = [
            'Ne yazmak istersiniz? Örneğin: değişken oluştur, döngü yaz, fonksiyon tanımla...',
            'Başka ne ekleyelim?',
            'Devam edelim mi? Ne yazmak istersiniz?',
            'Bir sonraki adım ne olsun?'
        ];
        
        const prompt = prompts[Math.floor(Math.random() * prompts.length)];
        this.currentPrompt = prompt;
        
        this.speak(prompt);
        this.voiceCommandText.textContent = `🤖 Gemini: "${prompt}"`;
        
        // 3 saniye sonra otomatik dinlemeye başla
        setTimeout(() => {
            if (this.conversationMode) {
                this.voice.start();
            }
        }, 3000);
    }

    async handleUserResponse(userInput) {
        this.updateStatus('Kod üretiliyor...', 'info');
        this.speak('Anlıyorum, kod üretiyorum...');
        
        try {
            const context = this.editor.getContext();
            const response = await fetch('/api/generate_conversation_code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    user_input: userInput,
                    context: context,
                    prompt: this.currentPrompt
                })
            });
            
            const data = await response.json();
            
            if (data.success && data.code) {
                // Kodu editöre ekle
                this.editor.appendCode(data.code);
                
                // Gemini'nin açıklamasını seslendir
                const explanation = data.explanation || 'Kod eklendi';
                this.speak(explanation);
                
                this.updateStatus('Kod eklendi', 'success');
                
                // 3 saniye sonra tekrar sor
                setTimeout(() => {
                    this.askForCode();
                }, 4000);
            } else {
                this.speak('Anlamadım, lütfen tekrar söyler misiniz?');
                setTimeout(() => {
                    this.askForCode();
                }, 3000);
            }
        } catch (error) {
            console.error('Kod üretme hatası:', error);
            this.speak('Bir hata oluştu. Tekrar deneyelim.');
            setTimeout(() => {
                this.askForCode();
            }, 3000);
        }
    }

    async processVoiceCommand(command) {
        this.updateStatus('Komut işleniyor...', 'info');
        
        // Komutları kontrol et
        const lowerCommand = command.toLowerCase();
        
        // Özel komutlar
        if (this.handleSpecialCommands(lowerCommand)) {
            return;
        }
        
        // Numaralı komutlar
        if (this.handleNumberedCommands(lowerCommand)) {
            return;
        }
        
        // Backend'e gönder
        try {
            const context = this.editor.getContext();
            const response = await fetch('/api/process_command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command, context })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Kod oluşturuldu
                this.editor.appendCode(data.code);
                const lineCount = data.code.split('\n').length;
                this.speak(`${lineCount} satır kod eklendi`);
                this.updateStatus('Kod eklendi', 'success');
            } else {
                // Dikteye geç
                this.editor.insertAtCursor(command + ' ');
                this.speak(`Yazdırıldı: ${command}`);
                this.updateStatus('Dikteye yazıldı', 'info');
            }
        } catch (error) {
            console.error('Komut işleme hatası:', error);
            this.updateStatus('Hata oluştu', 'error');
            this.speak('Bir hata oluştu');
        }
    }

    handleSpecialCommands(command) {
        if (command.includes('çalıştır') || command.includes('yazdır') || command.includes('run')) {
            this.runCode();
            return true;
        }
        
        if (command.includes('kaydet') || command.includes('save')) {
            this.saveFile();
            return true;
        }
        
        if (command.includes('terminal') && command.includes('oku')) {
            this.readTerminal();
            return true;
        }
        
        if (command.includes('komut listesi')) {
            this.readCommandList();
            return true;
        }
        
        return false;
    }

    handleNumberedCommands(command) {
        const commandMap = {
            'birinci': () => this.editor.moveCursorDown(),
            'ikinci': () => this.runCode(),
            'üçüncü': () => this.readLine(1),
            'dördüncü': () => this.readTerminal(),
            'beşinci': () => this.readCommandList()
        };
        
        for (const [key, action] of Object.entries(commandMap)) {
            if (command.includes(key)) {
                action();
                return true;
            }
        }
        
        return false;
    }

    async runCode() {
        const code = this.editor.getValue();
        
        if (!code.trim()) {
            this.speak('Kod boş');
            return;
        }
        
        this.updateStatus('Kod çalıştırılıyor...', 'info');
        this.speak('Kod çalıştırılıyor');
        this.clearTerminal();
        
        // Konuşma modunu geçici olarak durdur
        const wasConversing = this.conversationMode;
        this.conversationMode = false;
        
        try {
            const response = await fetch('/api/run_code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            
            const data = await response.json();
            
            if (data.success) {
                if (data.output) {
                    this.appendToTerminal(data.output, 'success');
                    this.speak('Kod başarıyla çalıştırıldı. Terminal çıktısı hazır.');
                }
                if (data.error) {
                    this.appendToTerminal(data.error, 'error');
                }
                
                this.updateStatus('Kod çalıştırıldı', 'success');
            } else {
                this.appendToTerminal(data.error, 'error');
                this.updateStatus('Hata oluştu', 'error');
                this.speak('Kod çalıştırırken hata oluştu');
            }
        } catch (error) {
            console.error('Çalıştırma hatası:', error);
            this.appendToTerminal('İstek hatası: ' + error.message, 'error');
            this.speak('Bir hata oluştu');
        } finally {
            // Konuşma modunu geri aç
            if (wasConversing) {
                setTimeout(() => {
                    this.conversationMode = true;
                    this.askForCode();
                }, 3000);
            }
        }
    }

    async saveFile() {
        const filename = this.filenameInput.value || 'untitled.py';
        const code = this.editor.getValue();
        
        this.updateStatus('Dosya kaydediliyor...', 'info');
        
        try {
            const response = await fetch('/api/save_file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename, code })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateStatus('Kaydedildi: ' + filename, 'success');
                this.speak(`${filename} kaydedildi`);
                this.loadFileList();
            } else {
                this.updateStatus('Kayıt hatası', 'error');
                this.speak('Dosya kaydedilemedi');
            }
        } catch (error) {
            console.error('Kaydetme hatası:', error);
            this.speak('Kaydetme hatası');
        }
    }

    async loadFile(filename) {
        try {
            const response = await fetch('/api/load_file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.editor.setValue(data.code);
                this.filenameInput.value = filename;
                this.updateStatus('Yüklendi: ' + filename, 'success');
                this.speak(`${filename} yüklendi`);
            }
        } catch (error) {
            console.error('Dosya yükleme hatası:', error);
        }
    }

    async loadFileList() {
        try {
            const response = await fetch('/api/list_files');
            const data = await response.json();
            
            if (data.success) {
                const fileList = document.getElementById('file-list');
                fileList.innerHTML = '';
                
                data.files.forEach(file => {
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.textContent = '📄 ' + file;
                    fileItem.addEventListener('click', () => this.loadFile(file));
                    fileList.appendChild(fileItem);
                });
            }
        } catch (error) {
            console.error('Dosya listesi yükleme hatası:', error);
        }
    }

    newFile() {
        this.editor.setValue('');
        this.filenameInput.value = 'untitled.py';
        this.clearTerminal();
        this.speak('Yeni dosya oluşturuldu');
    }

    clearTerminal() {
        this.terminalOutput.innerHTML = '';
    }

    appendToTerminal(text, type = 'normal') {
        const line = document.createElement('div');
        line.className = 'terminal-' + type;
        line.textContent = text;
        this.terminalOutput.appendChild(line);
        this.terminalOutput.scrollTop = this.terminalOutput.scrollHeight;
    }

    readTerminal() {
        const text = this.terminalOutput.textContent || 'Terminal boş';
        this.speak(text);
    }

    readLine(lineNumber) {
        const line = this.editor.getLine(lineNumber);
        if (line) {
            this.speak(`${lineNumber}. satır: ${line}`);
        } else {
            this.speak(`${lineNumber}. satır boş`);
        }
    }

    readCommandList() {
        const commands = [
            'Birinci komut: Alt satıra geç',
            'İkinci komut: Kodu çalıştır',
            'Üçüncü komut: Birinci satırı oku',
            'Dördüncü komut: Terminal çıktısını oku',
            'Beşinci komut: Komut listesini oku'
        ].join('. ');
        
        this.speak(commands);
    }

    speak(text) {
        if (this.tts.isEnabled()) {
            this.tts.speak(text);
        }
    }

    updateStatus(text, type = 'info') {
        this.statusText.textContent = text;
        const indicator = document.getElementById('status-indicator');
        
        // Renk
        indicator.style.background = {
            'success': '#4CAF50',
            'error': '#f44336',
            'warning': '#ff9800',
            'info': '#2196F3'
        }[type] || '#2196F3';
    }
}

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BeMyCodeApp();
});
