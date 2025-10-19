# Instagram Follow Bot

An intelligent Instagram automation bot for following users with human-like behavior and security features.

## ⚠️ Important Warnings

- This bot is for educational purposes only
- Use in compliance with Instagram's terms of service
- Excessive use may result in account suspension
- Use at your own risk

## 🚀 Features

- **Secure Login**: Safe Instagram authentication with cookie management
- **Smart Following**: Human-like behavior with random delays
- **Auto Target Collection**: Automatically scrapes followers from source accounts
- **Loading Detection**: Waits for loading screens to complete
- **Multiple Click Methods**: Various button clicking strategies
- **Error Handling**: Robust error management and recovery
- **Rate Limiting**: Built-in delays to avoid detection
- **Logging**: Comprehensive activity logging

## 📋 Installation

### Prerequisites
- Python 3.8 or higher
- Windows/Linux/macOS

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/omercangumus/instagramfollow_bot.git
cd instagramfollow_bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
playwright install chromium
```

3. **Configure your settings:**
   - Copy `env.example` to `.env`
   - Edit `.env` with your Instagram credentials

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# Instagram Account Information
INSTAGRAM_USERNAME=your_username_here
INSTAGRAM_PASSWORD=your_password_here

# Target Account Settings
SOURCE_ACCOUNT=target_account_here
MAX_FOLLOWS_PER_SESSION=30

# Delay Settings (seconds)
MIN_ACTION_DELAY_S=5
MAX_ACTION_DELAY_S=15
SCROLL_DELAY_S=2
PAGE_LOAD_DELAY_S=5

# Block Settings
FOLLOWS_PER_BLOCK=10
BLOCK_DELAY_MIN_S=60
BLOCK_DELAY_MAX_S=120
```

## 🚀 Usage

### Quick Start
```bash
python calisan_bot.py
```

### Available Scripts
- `calisan_bot.py` - Main bot (recommended)
- `guvenli_bot.py` - Slower, more secure version
- `main.py` - Alternative entry point

### Windows Users
Double-click `calisan_calistir.bat` for easy execution.

## 🛡️ Security Features

- **Environment Variables**: Sensitive data stored in `.env` file
- **Git Protection**: `.gitignore` prevents accidental credential commits
- **Cookie Management**: Secure session handling
- **Rate Limiting**: Built-in delays to avoid detection
- **Error Recovery**: Automatic retry mechanisms

## 📝 How It Works

1. **Login**: Authenticates with Instagram using credentials
2. **Target Selection**: Navigates to source account
3. **Follower Collection**: Opens followers modal and scrolls to load users
4. **Smart Following**: Follows users with human-like delays
5. **Progress Tracking**: Logs all activities and saves progress

## 🔧 Development

### Project Structure
```
instagramfollow_bot/
├── calisan_bot.py          # Main bot implementation
├── config.py               # Configuration settings
├── database.py             # Data persistence
├── instagram_bot.py         # Core bot logic
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env                    # Your credentials (not in git)
└── README.md              # This file
```

### Key Components
- **BotConfig**: Centralized configuration management
- **DatabaseManager**: Handles followed users tracking
- **InstagramBot**: Core automation logic
- **Error Handling**: Comprehensive error management

## 📊 Performance

- **Speed**: 1-3 second delays between actions
- **Reliability**: Multiple click methods for better success rate
- **Safety**: Built-in rate limiting and error recovery
- **Logging**: Detailed activity tracking

## 🛠️ Troubleshooting

### Common Issues
1. **Login Failed**: Check credentials in `.env` file
2. **Button Not Found**: Instagram may have updated their interface
3. **Rate Limited**: Increase delays in configuration
4. **Browser Issues**: Ensure Playwright is properly installed

### Debug Mode
Enable detailed logging by modifying the logging level in the bot files.

## 📄 License

This project is for educational purposes only. Commercial use is prohibited.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

# Instagram Takip Botu

Instagram'da otomatik takip işlemleri yapmak için geliştirilmiş akıllı bir Python botu.

## ⚠️ Önemli Uyarılar

- Bu bot sadece eğitim amaçlıdır
- Instagram'ın hizmet şartlarına uygun kullanın
- Aşırı kullanım hesabınızın kapatılmasına neden olabilir
- Kendi sorumluluğunuzda kullanın

## 🚀 Özellikler

- **Güvenli Giriş**: Çerez yönetimi ile güvenli Instagram kimlik doğrulama
- **Akıllı Takip**: Rastgele gecikmeler ile insan benzeri davranış
- **Otomatik Hedef Toplama**: Kaynak hesaplardan otomatik takipçi toplama
- **Yükleme Algılama**: Yükleme ekranlarının tamamlanmasını bekler
- **Çoklu Tıklama**: Çeşitli buton tıklama stratejileri
- **Hata Yönetimi**: Güçlü hata yönetimi ve kurtarma
- **Hız Sınırlama**: Tespit edilmeyi önlemek için yerleşik gecikmeler
- **Loglama**: Kapsamlı aktivite loglama

## 📋 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- Windows/Linux/macOS

### Kurulum Adımları

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/omercangumus/instagramfollow_bot.git
cd instagramfollow_bot
```

2. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
playwright install chromium
```

3. **Ayarlarınızı yapılandırın:**
   - `env.example` dosyasını `.env` olarak kopyalayın
   - `.env` dosyasını Instagram bilgilerinizle düzenleyin

## ⚙️ Yapılandırma

Aşağıdaki değişkenlerle bir `.env` dosyası oluşturun:

```env
# Instagram Hesap Bilgileri
INSTAGRAM_USERNAME=your_username_here
INSTAGRAM_PASSWORD=your_password_here

# Hedef Hesap Ayarları
SOURCE_ACCOUNT=target_account_here
MAX_FOLLOWS_PER_SESSION=30

# Gecikme Ayarları (saniye)
MIN_ACTION_DELAY_S=5
MAX_ACTION_DELAY_S=15
SCROLL_DELAY_S=2
PAGE_LOAD_DELAY_S=5

# Blok Ayarları
FOLLOWS_PER_BLOCK=10
BLOCK_DELAY_MIN_S=60
BLOCK_DELAY_MAX_S=120
```

## 🚀 Kullanım

### Hızlı Başlangıç
```bash
python calisan_bot.py
```

### Mevcut Scriptler
- `calisan_bot.py` - Ana bot (önerilen)
- `guvenli_bot.py` - Daha yavaş, güvenli versiyon
- `main.py` - Alternatif giriş noktası

### Windows Kullanıcıları
Kolay çalıştırma için `calisan_calistir.bat` dosyasına çift tıklayın.

## 🛡️ Güvenlik Özellikleri

- **Ortam Değişkenleri**: Hassas veriler `.env` dosyasında saklanır
- **Git Koruması**: `.gitignore` yanlışlıkla kimlik bilgisi commit'lerini önler
- **Çerez Yönetimi**: Güvenli oturum işleme
- **Hız Sınırlama**: Tespit edilmeyi önlemek için yerleşik gecikmeler
- **Hata Kurtarma**: Otomatik yeniden deneme mekanizmaları

## 📝 Nasıl Çalışır

1. **Giriş**: Kimlik bilgileri ile Instagram'a kimlik doğrulama
2. **Hedef Seçimi**: Kaynak hesaba gider
3. **Takipçi Toplama**: Takipçiler modal'ını açar ve kullanıcıları yüklemek için scroll yapar
4. **Akıllı Takip**: İnsan benzeri gecikmeler ile kullanıcıları takip eder
5. **İlerleme Takibi**: Tüm aktiviteleri loglar ve ilerlemeyi kaydeder

## 🔧 Geliştirme

### Proje Yapısı
```
instagramfollow_bot/
├── calisan_bot.py          # Ana bot implementasyonu
├── config.py               # Yapılandırma ayarları
├── database.py             # Veri kalıcılığı
├── instagram_bot.py         # Temel bot mantığı
├── main.py                 # Giriş noktası
├── requirements.txt        # Bağımlılıklar
├── .env                    # Kimlik bilgileriniz (git'te değil)
└── README.md              # Bu dosya
```

### Ana Bileşenler
- **BotConfig**: Merkezi yapılandırma yönetimi
- **DatabaseManager**: Takip edilen kullanıcıları takip eder
- **InstagramBot**: Temel otomasyon mantığı
- **Hata Yönetimi**: Kapsamlı hata yönetimi

## 📊 Performans

- **Hız**: Aksiyonlar arası 1-3 saniye gecikme
- **Güvenilirlik**: Daha iyi başarı oranı için çoklu tıklama yöntemleri
- **Güvenlik**: Yerleşik hız sınırlama ve hata kurtarma
- **Loglama**: Detaylı aktivite takibi

## 🛠️ Sorun Giderme

### Yaygın Sorunlar
1. **Giriş Başarısız**: `.env` dosyasındaki kimlik bilgilerini kontrol edin
2. **Buton Bulunamadı**: Instagram arayüzlerini güncellemiş olabilir
3. **Hız Sınırlandı**: Yapılandırmada gecikmeleri artırın
4. **Tarayıcı Sorunları**: Playwright'ın düzgün yüklendiğinden emin olun

### Hata Ayıklama Modu
Bot dosyalarındaki loglama seviyesini değiştirerek detaylı loglama etkinleştirin.

## 📄 Lisans

Bu proje sadece eğitim amaçlıdır. Ticari kullanım yasaktır.

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Özellik dalı oluşturun
3. Değişikliklerinizi yapın
4. Kapsamlı test edin
5. Pull request gönderin

## 📞 Destek

Sorunlar ve sorular için lütfen GitHub'da issue açın.