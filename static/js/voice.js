// Web Speech API - Sesli Komut Tanıma
class VoiceRecognition {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.initialize();
    }

    initialize() {
        // Web Speech API desteği kontrolü
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('Web Speech API desteklenmiyor!');
            this.onError('not-supported');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Türkçe dil ayarı
        this.recognition.lang = 'tr-TR';
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.maxAlternatives = 1;

        // Event listeners
        this.recognition.onstart = () => {
            this.isListening = true;
            this.onStart();
        };

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.onResult(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('Ses tanıma hatası:', event.error);
            
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
        if (!this.recognition) {
            console.error('Speech Recognition başlatılamadı');
            return;
        }

        if (this.isListening) {
            this.stop();
            return;
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Mikrofon başlatma hatası:', error);
        }
    }

    stop() {
        if (this.recognition && this.isListening) {
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
