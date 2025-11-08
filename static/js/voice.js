// Web Speech API - Sesli Komut Tanıma
class VoiceRecognition {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.initialize();
    }

    initialize() {
        console.log('🎤 VoiceRecognition initialize başladı');
        
        // Web Speech API desteği kontrolü
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('❌ Web Speech API desteklenmiyor!');
            this.onError('not-supported', 'Web Speech API desteklenmiyor');
            return;
        }

        console.log('✅ Web Speech API destekleniyor');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        console.log('✅ SpeechRecognition nesnesi oluşturuldu');
        
        // Türkçe dil ayarı
        this.recognition.lang = 'tr-TR';
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.maxAlternatives = 1;

        console.log('✅ SpeechRecognition ayarları yapıldı:', {
            lang: this.recognition.lang,
            continuous: this.recognition.continuous
        });

        // Event listeners
        this.recognition.onstart = () => {
            console.log('🎤 Dinleme BAŞLADI');
            this.isListening = true;
            if (this.onStart) this.onStart();
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('📝 Algılanan metin:', transcript);
            if (this.onResult) this.onResult(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('❌ Ses tanıma hatası:', event.error);
            
            // Hata mesajlarını Türkçe'ye çevir
            const errorMessages = {
                'not-allowed': 'Mikrofon erişimi reddedildi. Tarayıcı ayarlarından mikrofon iznini açın.',
                'no-speech': 'Ses algılanamadı. Lütfen tekrar deneyin.',
                'audio-capture': 'Mikrofon bulunamadı. Mikrofonunuzu kontrol edin.',
                'network': 'Ağ hatası. İnternet bağlantınızı kontrol edin.',
                'not-supported': 'Tarayıcınız sesli komut tanımayı desteklemiyor. Chrome veya Edge kullanın.',
                'aborted': 'Ses tanıma iptal edildi.'
            };
            
            const message = errorMessages[event.error] || `Ses tanıma hatası: ${event.error}`;
            this.onError(event.error, message);
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.onEnd();
        };
    }

    start() {
        console.log('🚀 Voice.start() çağrıldı');
        console.log('Recognition nesnesi:', this.recognition);
        console.log('isListening:', this.isListening);
        
        if (!this.recognition) {
            console.error('❌ Speech Recognition başlatılamadı');
            if (this.onError) {
                this.onError('not-initialized', 'Ses tanıma başlatılamadı');
            }
            return;
        }

        if (this.isListening) {
            console.log('⏹️ Zaten dinleniyor, durduruluyor...');
            this.stop();
            return;
        }

        try {
            console.log('🎤 recognition.start() çağrılıyor...');
            this.recognition.start();
            console.log('✅ recognition.start() başarılı');
        } catch (error) {
            console.error('❌ Mikrofon başlatma hatası:', error);
            if (this.onError) {
                this.onError('start-failed', error.message);
            }
        }
    }

    stop() {
        console.log('⏹️ Voice.stop() çağrıldı');
        if (this.recognition && this.isListening) {
            console.log('🛑 recognition.stop() çağrılıyor...');
            this.recognition.stop();
        }
    }

    // Override edilecek callback'ler
    onStart() {
        console.log('Dinleniyor...');
    }

    onResult(transcript) {
        console.log('Tanınan metin:', transcript);
    }

    onError(errorCode, errorMessage) {
        console.error('Hata:', errorCode, errorMessage);
    }

    onEnd() {
        console.log('Dinleme bitti');
    }
}

// Export
window.VoiceRecognition = VoiceRecognition;
