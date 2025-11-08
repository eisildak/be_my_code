// CodeMirror Editör Yönetimi
class CodeEditor {
    constructor(textareaId) {
        this.editor = CodeMirror.fromTextArea(document.getElementById(textareaId), {
            mode: 'python',
            theme: 'monokai',
            lineNumbers: true,
            indentUnit: 4,
            indentWithTabs: false,
            lineWrapping: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            extraKeys: {
                'Tab': (cm) => cm.execCommand('indentMore'),
                'Shift-Tab': (cm) => cm.execCommand('indentLess'),
                'Ctrl-/': (cm) => this.toggleComment(cm),
                'Cmd-/': (cm) => this.toggleComment(cm)
            }
        });

        this.currentFile = 'untitled.py';
    }

    getValue() {
        return this.editor.getValue();
    }

    setValue(code) {
        this.editor.setValue(code);
    }

    appendCode(code) {
        const cursor = this.editor.getCursor();
        this.editor.replaceRange(code + '\n', cursor);
        
        // Cursor'u yeni kodun sonuna taşı
        const newCursor = {
            line: cursor.line + code.split('\n').length,
            ch: 0
        };
        this.editor.setCursor(newCursor);
    }

    insertAtCursor(text) {
        this.editor.replaceSelection(text);
    }

    getContext(lines = 5) {
        // Son N satırı al (context için)
        const cursor = this.editor.getCursor();
        const startLine = Math.max(0, cursor.line - lines);
        const context = this.editor.getRange(
            { line: startLine, ch: 0 },
            cursor
        );
        return context;
    }

    getLine(lineNumber) {
        return this.editor.getLine(lineNumber - 1); // 0-indexed
    }

    moveCursorDown() {
        const cursor = this.editor.getCursor();
        this.editor.setCursor({ line: cursor.line + 1, ch: 0 });
    }

    toggleComment(cm) {
        const from = cm.getCursor('start');
        const to = cm.getCursor('end');
        const lines = [];
        
        for (let i = from.line; i <= to.line; i++) {
            lines.push(cm.getLine(i));
        }

        // Tümü comment mi kontrol et
        const allCommented = lines.every(line => line.trim().startsWith('#'));

        // Toggle
        for (let i = from.line; i <= to.line; i++) {
            const line = cm.getLine(i);
            if (allCommented) {
                // Comment'i kaldır
                const newLine = line.replace(/^\s*#\s?/, '');
                cm.replaceRange(newLine, { line: i, ch: 0 }, { line: i, ch: line.length });
            } else {
                // Comment ekle
                cm.replaceRange('# ' + line, { line: i, ch: 0 }, { line: i, ch: line.length });
            }
        }
    }

    focus() {
        this.editor.focus();
    }

    refresh() {
        this.editor.refresh();
    }
}

// Export
window.CodeEditor = CodeEditor;
