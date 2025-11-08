# Be My Code - Vercel Deployment

## 🚀 Vercel'de Deploy Etme

### 1. Vercel CLI Kurulumu (Opsiyonel)

```bash
npm install -g vercel
```

### 2. Vercel Dashboard ile Deploy

1. **https://vercel.com** adresine gidin
2. GitHub hesabınızla giriş yapın
3. "New Project" butonuna tıklayın
4. `eisildak/be_my_code` repository'sini seçin
5. "Import" butonuna tıklayın

### 3. Environment Variables Ayarlama

**Environment Variables** bölümünde:

- **Name:** `GEMINI_API_KEY`
- **Value:** `AIzaSyCMAcbLrhsR8EqUfOgr7SmKTvPTeQU0ZkQ`

### 4. Build Settings

Vercel otomatik olarak `vercel.json` dosyasını algılayacak.

### 5. Deploy

"Deploy" butonuna tıklayın!

## 📝 Notlar

- ✅ HTTPS otomatik olarak aktif (mikrofon çalışacak!)
- ✅ Ücretsiz SSL sertifikası
- ✅ Global CDN
- ⚠️ Serverless functions cold start olabilir (ilk yükleme yavaş)

## 🌐 Deploy Sonrası

Deploy tamamlandığında şu şekilde bir URL alacaksınız:
- `https://be-my-code.vercel.app`
- veya `https://be-my-code-eisildak.vercel.app`

## 🎤 Mikrofon İzni

HTTPS sayesinde mikrofon izni sorunsuz çalışacak!

## 🔄 Güncelleme

Git'e push yaptığınızda otomatik deploy olacak:

```bash
git add .
git commit -m "Update"
git push
```

Vercel otomatik olarak deploy edecek! 🚀
