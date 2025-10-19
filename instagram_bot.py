#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Bot - Ana bot sınıfı
SOLID prensiplerine uygun, temiz ve modüler yapı
"""

import json
import os
import random
import time
import logging
from datetime import datetime
from typing import Tuple, Optional

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, TimeoutError as PlaywrightTimeoutError

from config import BotConfig
from database import DatabaseManager

class InstagramAuthManager:
    """Instagram giriş işlemlerini yöneten sınıf"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def save_cookies(self, context: BrowserContext) -> bool:
        """Çerezleri dosyaya kaydet"""
        try:
            cookies = context.cookies()
            with open(self.config.COOKIES_FILE, 'w') as f:
                json.dump(cookies, f)
            self.logger.info("Çerezler kaydedildi")
            return True
        except Exception as e:
            self.logger.error(f"Çerezler kaydedilirken hata: {e}")
            return False
    
    def load_cookies(self, context: BrowserContext) -> bool:
        """Kaydedilmiş çerezleri yükle"""
        if not os.path.exists(self.config.COOKIES_FILE):
            return False
            
        try:
            with open(self.config.COOKIES_FILE, 'r') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            self.logger.info("Kaydedilmiş çerezler yüklendi")
            return True
        except Exception as e:
            self.logger.error(f"Çerezler yüklenirken hata: {e}")
            return False
    
    def login_with_cookies(self, page: Page) -> bool:
        """Çerezler ile giriş yap"""
        try:
            page.goto("https://www.instagram.com/")
            page.wait_for_selector('a[href*="/direct/inbox/"]', timeout=10000)
            self.logger.info("Çerezler ile giriş başarılı")
            return True
        except PlaywrightTimeoutError:
            self.logger.warning("Çerezler geçersiz, normal giriş yapılacak")
            return False
    
    def login_with_credentials(self, page: Page) -> bool:
        """Kullanıcı adı/şifre ile giriş yap"""
        try:
            page.goto("https://www.instagram.com/accounts/login/")
            page.wait_for_selector('input[name="username"]', timeout=10000)
            
            # Kullanıcı adı ve şifre gir
            page.fill('input[name="username"]', self.config.INSTAGRAM_USERNAME)
            time.sleep(random.uniform(1, 2))
            page.fill('input[name="password"]', self.config.INSTAGRAM_PASSWORD)
            time.sleep(random.uniform(1, 2))
            
            # Giriş butonuna tıkla
            page.click('button[type="submit"]')
            
            # Giriş başarılı mı kontrol et
            page.wait_for_selector('a[href*="/direct/inbox/"]', timeout=15000)
            self.logger.info("Giriş başarılı")
            return True
            
        except PlaywrightTimeoutError:
            self.logger.error("Giriş başarısız! Kullanıcı adı/şifre kontrol edin")
            return False
        except Exception as e:
            self.logger.error(f"Giriş sırasında hata: {e}")
            return False
    
    def login(self, page: Page, context: BrowserContext) -> bool:
        """Instagram'a giriş yap"""
        self.logger.info("Instagram'a giriş yapılıyor...")
        
        # Önce çerezleri dene
        if self.load_cookies(context):
            if self.login_with_cookies(page):
                return True
        
        # Normal giriş
        if self.login_with_credentials(page):
            self.save_cookies(context)
            return True
        
        return False

class FollowButtonHandler:
    """Takip butonu işlemlerini yöneten sınıf"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def click_follow_button_flexibly(self, button_element) -> Tuple[bool, str]:
        """Esnek takip butonu tıklama fonksiyonu"""
        try:
            button_text = button_element.text_content().strip()
            self.logger.debug(f"Buton metni: '{button_text}'")
            
            # Takip edilebilir mi kontrol et
            if self._is_already_following(button_text):
                self.logger.info(f"Zaten takip ediliyor: {button_text}")
                return False, "already_following"
            
            # Takip edilebilir butonlar
            if self._is_followable(button_text):
                self._perform_follow_click(button_element)
                self.logger.info(f"Başarılı tıklama: {button_text}")
                return True, "success"
            else:
                self.logger.warning(f"Bilinmeyen buton metni: {button_text}")
                return False, "unknown_button"
                
        except Exception as e:
            self.logger.error(f"Tıklama hatası: {e}")
            return False, "error"
    
    def _is_already_following(self, button_text: str) -> bool:
        """Buton zaten takip ediliyor mu?"""
        return any(keyword in button_text.lower() for keyword in self.config.ALREADY_FOLLOWING_KEYWORDS)
    
    def _is_followable(self, button_text: str) -> bool:
        """Buton takip edilebilir mi?"""
        return any(keyword in button_text.lower() for keyword in self.config.FOLLOWABLE_KEYWORDS)
    
    def _perform_follow_click(self, button_element) -> None:
        """Takip butonuna tıkla"""
        try:
            # Butonu görünür hale getir
            button_element.scroll_into_view_if_needed()
            time.sleep(0.5)
            
            # Hover yap
            button_element.hover()
            time.sleep(random.uniform(0.3, 0.8))
            
            # Tıkla
            button_element.click()
            time.sleep(random.uniform(0.5, 1.0))
            
            # Başarılı tıklama kontrolü
            self.logger.debug("Buton tıklandı")
            
        except Exception as e:
            self.logger.error(f"Tıklama hatası: {e}")
            # Alternatif tıklama yöntemi
            try:
                button_element.click(force=True)
                self.logger.info("Zorla tıklama başarılı")
            except Exception as e2:
                self.logger.error(f"Zorla tıklama da başarısız: {e2}")

class InstagramBot:
    """Ana Instagram bot sınıfı"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.database = DatabaseManager(config.FOLLOWED_USERS_FILE)
        self.auth_manager = InstagramAuthManager(config)
        self.follow_handler = FollowButtonHandler(config)
        
        self.follow_count = 0
        self.processed_users = set()
        
        # Daha önce takip edilen kullanıcıları yükle
        self.database.load_followed_users()
    
    def _create_browser(self) -> Tuple[Browser, BrowserContext, Page]:
        """Tarayıcı oluştur"""
        playwright = sync_playwright().start()
        
        browser = playwright.chromium.launch(
            headless=self.config.BROWSER_HEADLESS,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        context = browser.new_context(
            viewport={
                'width': self.config.BROWSER_VIEWPORT_WIDTH, 
                'height': self.config.BROWSER_VIEWPORT_HEIGHT
            },
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        return browser, context, page
    
    def _navigate_to_source_profile(self, page: Page) -> bool:
        """Kaynak hesaba git"""
        try:
            profile_url = f"https://www.instagram.com/{self.config.SOURCE_ACCOUNT}/"
            self.logger.info(f"Kaynak hesaba gidiliyor: {profile_url}")
            page.goto(profile_url)
            page.wait_for_load_state('networkidle', timeout=20000)
            time.sleep(self.config.PAGE_LOAD_DELAY_S)
            
            # Sayfa yüklendi mi kontrol et
            try:
                page.wait_for_selector('h2', timeout=10000)
                self.logger.info("Kaynak hesap sayfası yüklendi")
                return True
            except:
                # Alternatif kontrol
                if "instagram.com" in page.url:
                    self.logger.info("Instagram sayfası yüklendi")
                    return True
                else:
                    self.logger.error("Sayfa yüklenemedi")
                    return False
        except Exception as e:
            self.logger.error(f"Kaynak hesaba gidilemedi: {e}")
            return False
    
    def _open_followers_modal(self, page: Page) -> bool:
        """Takipçiler modal'ını aç"""
        try:
            # Takipçiler butonunu bul
            followers_button = None
            for selector in self.config.FOLLOWERS_BUTTON_SELECTORS:
                try:
                    followers_button = page.locator(selector).first
                    if followers_button.count() > 0:
                        self.logger.info(f"Takipçiler butonu bulundu: {selector}")
                        break
                except:
                    continue
            
            if not followers_button or followers_button.count() == 0:
                self.logger.error("Takipçiler butonu bulunamadı")
                # Alternatif yöntemler dene
                try:
                    # Tüm linkleri kontrol et
                    all_links = page.locator('a').all()
                    for link in all_links:
                        try:
                            href = link.get_attribute('href')
                            if href and 'followers' in href:
                                followers_button = link
                                self.logger.info("Alternatif takipçiler linki bulundu")
                                break
                        except:
                            continue
                except:
                    pass
                
                if not followers_button:
                    self.logger.error("Hiçbir takipçiler butonu bulunamadı")
                    return False
            
            # Takipçiler butonuna tıkla
            self.logger.info("Takipçiler listesi açılıyor...")
            followers_button.click()
            time.sleep(5)  # Daha uzun bekleme
            
            # Modal'ın açılmasını bekle
            try:
                page.wait_for_selector('[role="dialog"]', timeout=15000)
                self.logger.info("Takipçiler listesi açıldı")
                return True
            except:
                # Alternatif modal kontrolü
                try:
                    page.wait_for_selector('div[style*="position: fixed"]', timeout=5000)
                    self.logger.info("Modal alternatif yöntemle açıldı")
                    return True
                except:
                    self.logger.error("Modal açılamadı")
                    return False
            
        except Exception as e:
            self.logger.error(f"Takipçiler modal'ı açılamadı: {e}")
            return False
    
    def _process_visible_users(self, page: Page) -> int:
        """Görünür kullanıcıları işle"""
        user_rows = page.locator('[role="dialog"] div[style*="display: flex"]').all()
        new_users_found = 0
        
        self.logger.info(f"Modal'da {len(user_rows)} kullanıcı satırı bulundu")
        
        for row in user_rows:
            try:
                # Kullanıcı adını bul
                username_link = row.locator('a[href*="/"]').first
                if username_link.count() == 0:
                    continue
                    
                href = username_link.get_attribute('href')
                if not href or '/p/' in href or '/reel/' in href:
                    continue
                    
                username = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                
                # Bu kullanıcıyı daha önce işledik mi?
                if username in self.processed_users or self.database.is_user_followed(username):
                    continue
                    
                # Takip butonunu bul
                follow_button = row.locator('button').first
                if follow_button.count() == 0:
                    continue
                    
                self.logger.info(f"İşleniyor: @{username}")
                
                # Butona tıkla
                success, status = self.follow_handler.click_follow_button_flexibly(follow_button)
                
                if success:
                    self.follow_count += 1
                    self.database.save_followed_user(username)
                    self.logger.info(f"✅ @{username} takip edildi! (Toplam: {self.follow_count})")
                    
                    # Gecikme
                    delay = random.uniform(self.config.MIN_ACTION_DELAY_S, self.config.MAX_ACTION_DELAY_S)
                    self.logger.info(f"Bekleme: {delay:.1f} saniye...")
                    time.sleep(delay)
                    
                elif status == "already_following":
                    self.logger.info(f"⚠️ @{username} zaten takip ediliyor")
                else:
                    self.logger.warning(f"❌ @{username} takip edilemedi")
                    
                # Kullanıcıyı işlenmiş olarak işaretle
                self.processed_users.add(username)
                new_users_found += 1
                
                # Limit kontrolü
                if self.follow_count >= self.config.MAX_FOLLOWS_PER_SESSION:
                    self.logger.info(f"🎯 Takip limiti ulaşıldı: {self.follow_count}")
                    break
                    
            except Exception as e:
                self.logger.error(f"Kullanıcı işlenirken hata: {e}")
                continue
        
        return new_users_found
    
    def _scroll_for_more_users(self, page: Page) -> bool:
        """Yeni kullanıcılar için scroll yap"""
        try:
            self.logger.info("Yeni kullanıcı bulunamadı, scroll yapılıyor...")
            page.evaluate('document.querySelector("[role=\\"dialog\\"]").scrollTop += 1000')
            time.sleep(self.config.SCROLL_DELAY_S)
            return True
        except Exception as e:
            self.logger.error(f"Scroll hatası: {e}")
            return False
    
    def follow_from_list(self, page: Page) -> bool:
        """Takipçi listesinden doğrudan takip etme"""
        self.logger.info(f"@{self.config.SOURCE_ACCOUNT} takipçi listesinden takip başlıyor...")
        
        try:
            # Kaynak hesaba git
            if not self._navigate_to_source_profile(page):
                return False
            
            # Takipçiler modal'ını aç
            if not self._open_followers_modal(page):
                return False
            
            # Ana döngü
            self.logger.info(f"Maksimum {self.config.MAX_FOLLOWS_PER_SESSION} takip yapılacak...")
            
            while self.follow_count < self.config.MAX_FOLLOWS_PER_SESSION:
                new_users_found = self._process_visible_users(page)
                
                if new_users_found == 0:
                    if not self._scroll_for_more_users(page):
                        self.logger.info("Liste sonuna ulaşıldı")
                        break
                else:
                    self.logger.info(f"{new_users_found} yeni kullanıcı işlendi")
            
            self.logger.info(f"Takip işlemi tamamlandı! Toplam: {self.follow_count}")
            
            # Modal'ı kapat
            try:
                page.keyboard.press('Escape')
                time.sleep(1)
            except:
                pass
                
            return True
            
        except Exception as e:
            self.logger.error(f"Takipçi listesi işlenirken hata: {e}")
            return False
    
    def run(self) -> None:
        """Ana bot döngüsü"""
        self.logger.info("Instagram Bot başlatılıyor...")
        self.logger.info(f"Başlangıç zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        browser, context, page = self._create_browser()
        
        try:
            # Giriş yap
            if not self.auth_manager.login(page, context):
                self.logger.error("Giriş başarısız, bot durduruluyor")
                return
            
            # Takipçi listesinden takip et
            self.logger.info("="*50)
            self.logger.info("LİSTE İÇİNDE TAKİP BAŞLIYOR")
            self.logger.info("="*50)
            
            success = self.follow_from_list(page)
            
            if success:
                self.logger.info("Bot başarıyla tamamlandı!")
                self.logger.info(f"Toplam takip edilen: {self.follow_count}")
                self.logger.info(f"Bitiş zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                self.logger.error("Bot tamamlanamadı")
                
        except KeyboardInterrupt:
            self.logger.info("Bot kullanıcı tarafından durduruldu")
        except Exception as e:
            self.logger.error(f"Bot çalışırken hata: {e}")
        finally:
            browser.close()
