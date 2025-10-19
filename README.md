# Instagram Takip Botu

Bu proje, Instagram'da otomatik takip işlemleri yapmak için geliştirilmiş bir Python botudur.

## ⚠️ Önemli Uyarılar

- Bu bot sadece eğitim amaçlıdır
- Instagram'ın hizmet şartlarına uygun kullanın
- Aşırı kullanım hesabınızın kapatılmasına neden olabilir
- Kendi sorumluluğunuzda kullanın

## 🚀 Özellikler

- Güvenli Instagram girişi
- Otomatik takipçi toplama
- Akıllı gecikme sistemi
- Yükleme ekranı bekleme
- Çoklu tıklama yöntemleri
- Hata yönetimi

## 📋 Kurulum

1. **Gereksinimler:**
```bash
pip install -r requirements.txt
playwright install chromium
```

2. **Yapılandırma:**
- `.env` dosyasını düzenleyin
- Kendi Instagram bilgilerinizi girin

3. **Çalıştırma:**
```bash
python calisan_bot.py
```

## ⚙️ Yapılandırma

`.env` dosyasında aşağıdaki değişkenleri ayarlayın:

```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
SOURCE_ACCOUNT=target_account
MAX_FOLLOWS_PER_SESSION=30
```

## 🛡️ Güvenlik

- Kişisel bilgilerinizi asla paylaşmayın
- `.env` dosyasını git'e pushlamayın
- Düzenli olarak şifrenizi değiştirin

## 📝 Kullanım

1. Bot'u çalıştırın
2. Instagram'a giriş yapın
3. Bot otomatik olarak takip işlemlerini başlatır

## 🔧 Geliştirme

Bu proje Python 3.8+ ve Playwright kullanılarak geliştirilmiştir.

## 📄 Lisans

Bu proje eğitim amaçlıdır. Ticari kullanım yasaktır.
