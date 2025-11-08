// Web Speech API - Text to Speech (Sesli Geri Bildirim)
class TextToSpeech {
    constructor() {
        this.synthesis = window.speechSynthesis;
        this.voice = null;
        this.enabled = true;
        this.loadVoice();
    }

    loadVoice() {
        // Türkçe ses yükle
        const voices = this.synthesis.getVoices();
        
        // Türkçe ses ara (öncelik sırasına göre)
        this.voice = voices.find(v => v.lang === 'tr-TR') ||
                     voices.find(v => v.lang.startsWith('tr')) ||
                     voices[0]; // Yoksa ilk sesi kullan

        // Sesler yüklendiğinde tekrar dene
        if (voices.length === 0) {
            this.synthesis.onvoiceschanged = () => {
                this.loadVoice();
            };
        }
    }

    speak(text, options = {}) {
        if (!this.enabled) return;

        // Önceki konuşmayı durdur
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        
        // Ayarlar
        utterance.voice = this.voice;
        utterance.lang = 'tr-TR';
        utterance.rate = options.rate || 1.0;
        utterance.pitch = options.pitch || 1.0;
        utterance.volume = options.volume || 1.0;

        // Konuş
        this.synthesis.speak(utterance);

        return new Promise((resolve) => {
            utterance.onend = resolve;
        });
    }

    stop() {
        this.synthesis.cancel();
    }

    setEnabled(enabled) {
        this.enabled = enabled;
    }

    isEnabled() {
        return this.enabled;
    }
}

// Export
window.TextToSpeech = TextToSpeech;
