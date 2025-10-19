#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Güvenli Takip Botu
Daha yavaş ve güvenli çalışır
"""

import os
import time
import random
import logging
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class GuvenliInstagramBot:
    """Güvenli Instagram takip botu"""
    
    def __init__(self):
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.source_account = os.getenv('SOURCE_ACCOUNT', 'target_account_here')
        self.max_follows = int(os.getenv('MAX_FOLLOWS_PER_SESSION', 50))  # Daha az takip
        
        # Güvenli gecikme ayarları
        self.min_delay = 8   # Minimum 8 saniye
        self.max_delay = 25  # Maximum 25 saniye
        self.scroll_delay = 3  # Scroll gecikmesi
        
        logger.info("Güvenli Instagram Bot başlatıldı")
        logger.info(f"Kullanıcı: {self.username}")
        logger.info(f"Kaynak hesap: @{self.source_account}")
        logger.info(f"Takip limiti: {self.max_follows}")
        logger.info(f"Gecikme: {self.min_delay}-{self.max_delay} saniye")
    
    def random_delay(self, min_seconds=None, max_seconds=None):
        """Rastgele gecikme"""
        if min_seconds is None:
            min_seconds = self.min_delay
        if max_seconds is None:
            max_seconds = self.max_delay
        
        delay = random.uniform(min_seconds, max_seconds)
        logger.info(f"Bekleniyor: {delay:.1f} saniye")
        time.sleep(delay)
    
    def login_to_instagram(self, page: Page) -> bool:
        """Instagram'a giriş yap"""
        try:
            logger.info("Instagram'a giriş yapılıyor...")
            page.goto("https://www.instagram.com/accounts/login/")
            self.random_delay(3, 5)
            
            # Kullanıcı adı gir
            username_input = page.locator('input[name="username"]')
            username_input.fill(self.username)
            self.random_delay(1, 2)
            
            # Şifre gir
            password_input = page.locator('input[name="password"]')
            password_input.fill(self.password)
            self.random_delay(1, 2)
            
            # Giriş butonuna tıkla
            login_button = page.locator('button[type="submit"]')
            login_button.click()
            
            # Giriş başarılı mı kontrol et
            self.random_delay(5, 8)
            
            if "instagram.com" in page.url and "login" not in page.url:
                logger.info("Giriş başarılı!")
                return True
            else:
                logger.error("Giriş başarısız!")
                return False
                
        except Exception as e:
            logger.error(f"Giriş hatası: {e}")
            return False
    
    def navigate_to_source(self, page: Page) -> bool:
        """Kaynak hesaba git"""
        try:
            profile_url = f"https://www.instagram.com/{self.source_account}/"
            logger.info(f"Kaynak hesaba gidiliyor: {profile_url}")
            
            page.goto(profile_url)
            self.random_delay(5, 8)
            
            # Sayfa yüklendi mi kontrol et
            if self.source_account in page.url:
                logger.info("Kaynak hesap sayfası yüklendi")
                return True
            else:
                logger.error("Kaynak hesap sayfası yüklenemedi")
                return False
                
        except Exception as e:
            logger.error(f"Kaynak hesaba gidilemedi: {e}")
            return False
    
    def open_followers_modal(self, page: Page) -> bool:
        """Takipçiler modal'ını aç"""
        try:
            logger.info("Takipçiler listesi açılıyor...")
            
            # Takipçiler linkini bul ve tıkla
            followers_link = page.locator(f'a[href="/{self.source_account}/followers/"]')
            if followers_link.count() > 0:
                followers_link.click()
                self.random_delay(3, 5)
                logger.info("Takipçiler listesi açıldı")
                return True
            else:
                logger.error("Takipçiler linki bulunamadı")
                return False
                
        except Exception as e:
            logger.error(f"Takipçiler modal'ı açılamadı: {e}")
            return False
    
    def follow_users_from_modal(self, page: Page) -> int:
        """Modal'dan kullanıcıları takip et"""
        followed_count = 0
        
        try:
            logger.info("Modal'dan kullanıcılar takip ediliyor...")
            
            # Scroll yaparak daha fazla kullanıcı yükle
            for scroll in range(5):  # 5 kez scroll
                logger.info(f"Scroll {scroll + 1}/5")
                page.keyboard.press('End')
                self.random_delay(2, 4)
            
            # Takip butonlarını bul
            follow_buttons = page.locator('button:has-text("Takip Et"), button:has-text("Follow")')
            button_count = follow_buttons.count()
            logger.info(f"Bulunan takip butonu sayısı: {button_count}")
            
            # Her butonu kontrol et ve takip et
            for i in range(min(button_count, self.max_follows)):
                try:
                    button = follow_buttons.nth(i)
                    button_text = button.text_content()
                    
                    if "Takip Et" in button_text or "Follow" in button_text:
                        # Butonu görünür hale getir
                        button.scroll_into_view_if_needed()
                        self.random_delay(1, 2)
                        
                        # Tıkla
                        button.click()
                        followed_count += 1
                        logger.info(f"Takip edildi: {i + 1}/{self.max_follows}")
                        
                        # Gecikme
                        self.random_delay()
                        
                        # Limit kontrolü
                        if followed_count >= self.max_follows:
                            logger.info(f"Takip limiti ulaşıldı: {followed_count}")
                            break
                            
                except Exception as e:
                    logger.error(f"Takip hatası {i}: {e}")
                    continue
            
            logger.info(f"Toplam takip edilen: {followed_count}")
            return followed_count
            
        except Exception as e:
            logger.error(f"Modal takip hatası: {e}")
            return followed_count
    
    def run(self):
        """Bot'u çalıştır"""
        logger.info("Güvenli Instagram Bot başlatılıyor...")
        
        try:
            with sync_playwright() as p:
                # Tarayıcıyı başlat
                browser = p.chromium.launch(
                    headless=False,  # Görünür mod
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                
                context = browser.new_context(
                    viewport={'width': 1366, 'height': 768},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                
                page = context.new_page()
                
                # Instagram'a giriş
                if not self.login_to_instagram(page):
                    logger.error("Giriş başarısız, bot durduruluyor")
                    return
                
                # Kaynak hesaba git
                if not self.navigate_to_source(page):
                    logger.error("Kaynak hesaba gidilemedi, bot durduruluyor")
                    return
                
                # Takipçiler modal'ını aç
                if not self.open_followers_modal(page):
                    logger.error("Takipçiler modal'ı açılamadı, bot durduruluyor")
                    return
                
                # Kullanıcıları takip et
                followed_count = self.follow_users_from_modal(page)
                
                logger.info(f"Bot tamamlandı! Toplam takip edilen: {followed_count}")
                
                # Kısa bekleme
                self.random_delay(5, 10)
                
        except Exception as e:
            logger.error(f"Bot hatası: {e}")
        
        finally:
            logger.info("Bot kapatılıyor...")

if __name__ == "__main__":
    bot = GuvenliInstagramBot()
    bot.run()
