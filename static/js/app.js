/**
 * Be My Code - Konuşma Tabanlı IDE
 * Gemini ile interaktif kod yazma
 */

class BeMyCodeApp {
    constructor() {
        // Bileşenler
        this.editor = new CodeEditor('code-editor');
        this.voice = new VoiceRecognition();
        this.tts = new TextToSpeech();
        
        // Durum
        this.conversationMode = true;
        this.currentPrompt = '';
        
        // UI elemanları
        this.micBtn = document.getElementById('mic-btn');
        this.listeningIndicator = document.getElementById('listening-indicator');
        this.voiceCommandText = document.getElementById('voice-command-text');
        this.statusText = document.getElementById('status-text');
        this.terminalOutput = document.getElementById('terminal-output');
        
        // Başlat
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupVoiceCallbacks();
        
        console.log('✅ Be My Code başlatıldı');
        console.log('Mikrofon butonu:', this.micBtn);
        console.log('Voice Recognition:', this.voice);
        
        // Hoş geldin mesajı
        setTimeout(() => {
            this.speak('Merhaba! Ben Be My Code asistanınızım. Size Python kodu yazmakta yardımcı olacağım.');
            setTimeout(() => this.askForCode(), 3000);
        }, 1000);
    }

    setupEventListeners() {
        console.log('🔧 Event listeners kuruluyor...');
        
        // Mikrofon butonu
        this.micBtn.addEventListener('click', () => {
            console.log('🎤 Mikrofon butonuna tıklandı');
            console.log('Listening durumu:', this.voice.isListening);
            
            if (this.voice.isListening) {
                console.log('Durdurulacak...');
                this.voice.stop();
            } else {
                console.log('Başlatılacak...');
                this.voice.start();
            }
        });
        
        console.log('✅ Mikrofon butonu event listener eklendi');
        
        // Terminal temizle butonu
        const clearTerminalBtn = document.getElementById('clear-terminal-btn');
        if (clearTerminalBtn) {
            clearTerminalBtn.addEventListener('click', () => this.clearTerminal());
            console.log('✅ Terminal temizle butonu eklendi');
        }
        
        // Klavye: Ctrl+M / Cmd+M
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
                e.preventDefault();
                console.log('⌨️ Ctrl+M basıldı');
                this.micBtn.click();
            }
        });
        
        console.log('✅ Tüm event listeners hazır');
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
            this.voiceCommandText.textContent = `❌ ${errorMessage}`;
            
            if (errorCode === 'not-allowed') {
                alert('🎤 Mikrofon İzni Gerekli\n\nTarayıcı ayarlarından mikrofon iznini açın:\n1. Adres çubuğundaki kilit ikonuna tıklayın\n2. Mikrofon iznini "İzin Ver" yapın\n3. Sayfayı yenileyin');
            }
        };

        this.voice.onEnd = () => {
            this.micBtn.classList.remove('active');
            this.listeningIndicator.classList.remove('active');
            this.updateStatus('Hazır', 'success');
        };
    }

    askForCode() {
        if (!this.conversationMode) return;
        
        const prompts = [
            'Ne yazmak istersiniz? Örneğin: değişken oluştur, döngü yaz, fonksiyon tanımla',
            'Başka ne ekleyelim?',
            'Devam edelim mi? Ne yapmak istersiniz?',
            'Bir sonraki adım ne olsun?'
        ];
        
        this.currentPrompt = prompts[Math.floor(Math.random() * prompts.length)];
        
        this.speak(this.currentPrompt);
        this.voiceCommandText.textContent = `🤖 Gemini: "${this.currentPrompt}"`;
        
        // 3 saniye sonra otomatik dinle
        setTimeout(() => {
            if (this.conversationMode) {
                this.voice.start();
            }
        }, 3000);
    }

    async handleUserResponse(userInput) {
        this.updateStatus('Kod üretiliyor...', 'info');
        this.speak('Anlıyorum, kod üretiyorum');
        
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
                
                // Açıklamayı seslendir
                const explanation = data.explanation || 'Kod eklendi';
                this.speak(explanation);
                
                this.updateStatus('Kod yazıldı, çalıştırılıyor...', 'warning');
                
                // Kodu otomatik çalıştır
                await this.runCode();
                
                // 3 saniye sonra tekrar sor
                setTimeout(() => this.askForCode(), 3000);
            } else {
                this.speak('Anlamadım, lütfen tekrar söyler misiniz?');
                setTimeout(() => this.askForCode(), 3000);
            }
        } catch (error) {
            console.error('Hata:', error);
            this.speak('Bir hata oluştu. Tekrar deneyelim.');
            setTimeout(() => this.askForCode(), 3000);
        }
    }

    async runCode() {
        const code = this.editor.getValue();
        
        if (!code.trim()) {
            return;
        }
        
        try {
            const response = await fetch('/api/run_code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            
            const data = await response.json();
            
            if (data.success) {
                if (data.output) {
                    this.appendToTerminal('▶ Çıktı:', 'info');
                    this.appendToTerminal(data.output, 'success');
                    this.speak('Kod başarıyla çalıştı');
                }
                if (data.error) {
                    this.appendToTerminal('⚠ Hata:', 'error');
                    this.appendToTerminal(data.error, 'error');
                    
                    // Gemini'ye hatayı analiz ettir
                    await this.analyzeError(code, data.error);
                }
                
                this.updateStatus('Hazır', 'success');
            } else {
                this.appendToTerminal('❌ Hata:', 'error');
                this.appendToTerminal(data.error, 'error');
                
                // Gemini'ye hatayı analiz ettir
                await this.analyzeError(code, data.error);
            }
        } catch (error) {
            console.error('Çalıştırma hatası:', error);
            this.appendToTerminal('❌ İstek hatası: ' + error.message, 'error');
        }
    }

    async analyzeError(code, errorMessage) {
        this.updateStatus('Gemini hatayı analiz ediyor...', 'warning');
        
        try {
            const response = await fetch('/api/analyze_error', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    code: code,
                    error: errorMessage
                })
            });
            
            const data = await response.json();
            
            if (data.success && data.suggestion) {
                this.appendToTerminal('\n💡 Gemini Önerisi:', 'info');
                this.appendToTerminal(data.suggestion, 'info');
                this.speak(data.suggestion);
            }
        } catch (error) {
            console.error('Hata analizi başarısız:', error);
        }
    }

    speak(text) {
        this.tts.speak(text);
    }

    updateStatus(message, type = 'info') {
        this.statusText.textContent = message;
        this.statusText.className = `status ${type}`;
    }

    appendToTerminal(text, type = 'output') {
        const line = document.createElement('div');
        line.className = `terminal-line ${type}`;
        line.textContent = text;
        this.terminalOutput.appendChild(line);
        this.terminalOutput.scrollTop = this.terminalOutput.scrollHeight;
    }
}

// Uygulama başlat
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BeMyCodeApp();
});
