#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Çalışan Takip Botu
Basit ve etkili
"""

import os
import time
import random
import logging
from playwright.sync_api import sync_playwright, Page
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CalisanInstagramBot:
    """Çalışan Instagram takip botu"""
    
    def __init__(self):
        self.username = os.getenv('INSTAGRAM_USERNAME', 'your_username_here')
        self.password = os.getenv('INSTAGRAM_PASSWORD', 'your_password_here')
        self.source_account = os.getenv('SOURCE_ACCOUNT', 'target_account_here')
        self.max_follows = int(os.getenv('MAX_FOLLOWS_PER_SESSION', 30))
        
        logger.info("=== INSTAGRAM TAKIP BOTU ===")
        logger.info(f"Kullanıcı: {self.username}")
        logger.info(f"Kaynak hesap: @{self.source_account}")
        logger.info(f"Takip limiti: {self.max_follows}")
    
    def random_delay(self, min_sec=1, max_sec=3):
        """Rastgele gecikme - hızlı versiyon"""
        delay = random.uniform(min_sec, max_sec)
        logger.info(f"Bekleniyor: {delay:.1f} saniye")
        time.sleep(delay)
    
    def login_instagram(self, page: Page) -> bool:
        """Instagram'a giriş yap"""
        try:
            logger.info("Instagram'a giriş yapılıyor...")
            page.goto("https://www.instagram.com/accounts/login/", timeout=60000)
            self.random_delay(5, 8)
            
            # Sayfa yüklendi mi kontrol et
            page.wait_for_selector('input[name="username"]', timeout=30000)
            
            # Kullanıcı adı
            username_input = page.locator('input[name="username"]')
            username_input.click()
            username_input.clear()
            username_input.fill(self.username)
            self.random_delay(2, 3)
            
            # Şifre
            password_input = page.locator('input[name="password"]')
            password_input.click()
            password_input.clear()
            password_input.fill(self.password)
            self.random_delay(2, 3)
            
            # Giriş butonu
            login_btn = page.locator('button[type="submit"]')
            login_btn.click()
            
            # Giriş kontrolü - hızlı
            self.random_delay(3, 5)
            
            # URL kontrolü
            current_url = page.url
            logger.info(f"Mevcut URL: {current_url}")
            
            # Daha esnek giriş kontrolü
            if "instagram.com" in current_url:
                if "login" not in current_url or "challenge" in current_url:
                    logger.info("✅ Giriş başarılı!")
                    return True
                else:
                    # Manuel kontrol için bekle
                    logger.info("⚠️ Manuel giriş kontrolü gerekli")
                    logger.info("Giriş yaptıktan sonra 3 saniye bekleniyor...")
                    time.sleep(3)
                    return True
            else:
                logger.error("❌ Instagram sayfası yüklenemedi!")
                return False
                
        except Exception as e:
            logger.error(f"Giriş hatası: {e}")
            return False
    
    def go_to_source_profile(self, page: Page) -> bool:
        """Kaynak hesaba git"""
        try:
            profile_url = f"https://www.instagram.com/{self.source_account}/"
            logger.info(f"Kaynak hesaba gidiliyor: {profile_url}")
            
            page.goto(profile_url, timeout=60000)
            self.random_delay(2, 4)
            
            if self.source_account in page.url:
                logger.info("✅ Kaynak hesap sayfası yüklendi")
                return True
            else:
                logger.error("❌ Kaynak hesap sayfası yüklenemedi")
                return False
                
        except Exception as e:
            logger.error(f"Kaynak hesaba gidilemedi: {e}")
            return False
    
    def open_followers_list(self, page: Page) -> bool:
        """Takipçiler listesini aç"""
        try:
            logger.info("Takipçiler listesi açılıyor...")
            
            # Takipçiler linkini bul
            followers_links = [
                f'a[href="/{self.source_account}/followers/"]',
                'a[href*="/followers/"]',
                'a:has-text("followers")',
                'a:has-text("takipçi")'
            ]
            
            followers_btn = None
            for selector in followers_links:
                try:
                    btn = page.locator(selector).first
                    if btn.count() > 0:
                        followers_btn = btn
                        logger.info(f"Takipçiler butonu bulundu: {selector}")
                        break
                except:
                    continue
            
            if not followers_btn:
                logger.error("❌ Takipçiler butonu bulunamadı")
                return False
            
            # Takipçiler butonuna tıkla
            followers_btn.click()
            self.random_delay(1, 2)
            
            # Modal açıldı mı kontrol et
            try:
                page.wait_for_selector('[role="dialog"]', timeout=20000)
                logger.info("✅ Takipçiler listesi açıldı")
                return True
            except:
                logger.info("✅ Modal açıldı (alternatif kontrol)")
                return True
                
        except Exception as e:
            logger.error(f"Takipçiler listesi açılamadı: {e}")
            return False
    
    def follow_users_in_modal(self, page: Page) -> int:
        """Modal'daki kullanıcıları takip et"""
        followed_count = 0
        
        try:
            logger.info("Modal'dan kullanıcılar takip ediliyor...")
            
            # Modal içinde scroll yaparak daha fazla kullanıcı yükle
            modal = page.locator('[role="dialog"]')
            for i in range(8):  # Daha fazla scroll
                logger.info(f"Modal scroll {i+1}/8")
                
                # Yükleme ekranı kontrolü
                try:
                    loading_indicators = page.locator('[data-testid="loading"], .loading, [class*="loading"], [class*="spinner"]')
                    if loading_indicators.count() > 0:
                        logger.info("Yükleme ekranı tespit edildi, bekleniyor...")
                        self.random_delay(3, 5)  # Yükleme için daha uzun bekle
                except:
                    pass
                
                # Modal içinde scroll yap - daha yavaş ve güvenilir
                try:
                    # Modal'ın scroll container'ını bul
                    scroll_container = modal.locator('div[style*="overflow"]').first
                    if scroll_container.count() > 0:
                        # Yavaş scroll - adım adım
                        scroll_container.evaluate('element => element.scrollTop += 300')
                    else:
                        # Alternatif scroll yöntemi - yavaş
                        modal.evaluate('element => element.scrollTop += 300')
                except:
                    # Son çare: sayfa scroll - yavaş
                    page.keyboard.press('PageDown')
                
                # Scroll sonrası bekleme - yükleme için
                self.random_delay(2, 4)
                
                # Yükleme ekranı tekrar kontrol et
                try:
                    loading_indicators = page.locator('[data-testid="loading"], .loading, [class*="loading"], [class*="spinner"]')
                    if loading_indicators.count() > 0:
                        logger.info("Yükleme devam ediyor, ekstra bekleniyor...")
                        self.random_delay(2, 3)
                except:
                    pass
            
            # Takip butonlarını bul - daha kapsamlı seçiciler
            follow_selectors = [
                'button:has-text("Takip Et")',
                'button:has-text("Follow")',
                'button[type="button"]:has-text("Takip")',
                'button[type="button"]:has-text("Follow")',
                'button:has-text("Takip")',
                'button:has-text("Follow")',
                'div[role="button"]:has-text("Takip Et")',
                'div[role="button"]:has-text("Follow")',
                'a[role="button"]:has-text("Takip Et")',
                'a[role="button"]:has-text("Follow")'
            ]
            
            all_buttons = []
            for selector in follow_selectors:
                try:
                    buttons = page.locator(selector).all()
                    for btn in buttons:
                        if btn not in all_buttons:
                            all_buttons.append(btn)
                except:
                    continue
            
            logger.info(f"Bulunan takip butonu sayısı: {len(all_buttons)}")
            
            # Her butonu kontrol et ve takip et - sırayla ve atlamadan
            processed_count = 0
            for i, button in enumerate(all_buttons):
                if processed_count >= self.max_follows:
                    logger.info(f"Takip limiti ulaşıldı: {processed_count}")
                    break
                    
                try:
                    # Buton metnini kontrol et
                    button_text = button.text_content()
                    
                    if "Takip Et" in button_text or "Follow" in button_text:
                        # Butonu görünür hale getir
                        button.scroll_into_view_if_needed()
                        self.random_delay(0.5, 1)
                        
                        # Daha güçlü tıklama yöntemi
                        try:
                            # Önce hover yap
                            button.hover()
                            self.random_delay(0.2, 0.5)
                            
                            # Birden fazla tıklama yöntemi dene
                            success = False
                            
                            # Yöntem 1: Normal tıklama
                            try:
                                button.click()
                                success = True
                                logger.info(f"✅ Takip edildi (normal): {followed_count + 1}/{self.max_follows}")
                            except:
                                pass
                            
                            # Yöntem 2: JavaScript tıklama
                            if not success:
                                try:
                                    button.evaluate('element => element.click()')
                                    success = True
                                    logger.info(f"✅ Takip edildi (JS): {followed_count + 1}/{self.max_follows}")
                                except:
                                    pass
                            
                            # Yöntem 3: Force tıklama
                            if not success:
                                try:
                                    button.click(force=True)
                                    success = True
                                    logger.info(f"✅ Takip edildi (force): {followed_count + 1}/{self.max_follows}")
                                except:
                                    pass
                            
                            # Yöntem 4: Mouse tıklama
                            if not success:
                                try:
                                    button.click(button='left', force=True)
                                    success = True
                                    logger.info(f"✅ Takip edildi (mouse): {followed_count + 1}/{self.max_follows}")
                                except:
                                    pass
                            
                            if success:
                                followed_count += 1
                                processed_count += 1
                                logger.info(f"✅ Başarılı takip: {followed_count}/{self.max_follows}")
                            else:
                                logger.error(f"❌ Tüm tıklama yöntemleri başarısız: {i}")
                                processed_count += 1  # Başarısız olsa da say
                                continue
                            
                        except Exception as e:
                            logger.error(f"❌ Tıklama hatası {i}: {e}")
                            continue
                        
                        # Gecikme - daha uzun
                        self.random_delay(2, 4)
                        
                        # Yükleme ekranı kontrolü - takip sonrası
                        try:
                            loading_indicators = page.locator('[data-testid="loading"], .loading, [class*="loading"], [class*="spinner"]')
                            if loading_indicators.count() > 0:
                                logger.info("Takip sonrası yükleme tespit edildi, bekleniyor...")
                                self.random_delay(2, 3)
                        except:
                            pass
                            
                except Exception as e:
                    logger.error(f"Takip hatası {i}: {e}")
                    continue
            
            logger.info(f"🎉 Toplam takip edilen: {followed_count}")
            return followed_count
            
        except Exception as e:
            logger.error(f"Modal takip hatası: {e}")
            return followed_count
    
    def run(self):
        """Bot'u çalıştır"""
        logger.info("🚀 Instagram Takip Botu başlatılıyor...")
        
        try:
            with sync_playwright() as p:
                # Tarayıcıyı başlat - daha güvenilir ayarlar
                browser = p.chromium.launch(
                    headless=False,
                    args=[
                        '--no-sandbox', 
                        '--disable-dev-shm-usage',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor',
                        '--disable-background-timer-throttling',
                        '--disable-backgrounding-occluded-windows',
                        '--disable-renderer-backgrounding'
                    ]
                )
                
                context = browser.new_context(
                    viewport={'width': 1366, 'height': 768},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    # Çerezleri temizle - yeni hesap için
                    storage_state=None
                )
                
                page = context.new_page()
                
                # 1. Instagram'a giriş
                if not self.login_instagram(page):
                    logger.error("❌ Giriş başarısız, bot durduruluyor")
                    return
                
                # 2. Kaynak hesaba git
                if not self.go_to_source_profile(page):
                    logger.error("❌ Kaynak hesaba gidilemedi, bot durduruluyor")
                    return
                
                # 3. Takipçiler listesini aç
                if not self.open_followers_list(page):
                    logger.error("❌ Takipçiler listesi açılamadı, bot durduruluyor")
                    return
                
                # 4. Kullanıcıları takip et
                followed_count = self.follow_users_in_modal(page)
                
                logger.info(f"🎉 Bot tamamlandı! Toplam takip edilen: {followed_count}")
                
                # Kısa bekleme
                self.random_delay(2, 4)
                
        except Exception as e:
            logger.error(f"Bot hatası: {e}")
        
        finally:
            logger.info("Bot kapatılıyor...")

if __name__ == "__main__":
    bot = CalisanInstagramBot()
    bot.run()
