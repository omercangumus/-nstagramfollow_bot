#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Bot Configuration
Tüm ayarlar ve sabitler burada tanımlanır
"""

import os
# Ortam değişkenlerini yükle (isteğe bağlı)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

class BotConfig:
    """Bot yapılandırma sınıfı"""
    
    # ========================================
    # AYARLAR - BURAYA KENDİ BİLGİLERİNİZİ YAZIN
    # ========================================
    
    # Instagram hesap bilgileri (BURAYA KENDİ BİLGİLERİNİZİ YAZIN)
    INSTAGRAM_USERNAME = 'your_username_here'  # Kendi Instagram kullanıcı adınızı yazın
    INSTAGRAM_PASSWORD = 'your_password_here'  # Kendi Instagram şifrenizi yazın
    
    # Kaynak hesap (Takipçilerini toplayacağınız hesap)
    SOURCE_ACCOUNT = 'target_account_here'    # Kaynak hesabın kullanıcı adını yazın (@ işareti olmadan)
    
    # Takip limitleri
    MAX_FOLLOWS_PER_SESSION = int(os.getenv('MAX_FOLLOWS_PER_SESSION', 200))
    MAX_FOLLOWS_PER_HOUR = int(os.getenv('MAX_FOLLOWS_PER_HOUR', 50))
    MAX_FOLLOWS_PER_DAY = int(os.getenv('MAX_FOLLOWS_PER_DAY', 150))
    
    # Gecikme ayarları (saniye) - Daha güvenli ayarlar
    MIN_ACTION_DELAY_S = int(os.getenv('MIN_ACTION_DELAY_S', 5))
    MAX_ACTION_DELAY_S = int(os.getenv('MAX_ACTION_DELAY_S', 15))
    SCROLL_DELAY_S = int(os.getenv('SCROLL_DELAY_S', 2))
    PAGE_LOAD_DELAY_S = int(os.getenv('PAGE_LOAD_DELAY_S', 5))
    
    # Blok ayarları
    FOLLOWS_PER_BLOCK = int(os.getenv('FOLLOWS_PER_BLOCK', 10))
    BLOCK_DELAY_MIN_S = int(os.getenv('BLOCK_DELAY_MIN_S', 60))
    BLOCK_DELAY_MAX_S = int(os.getenv('BLOCK_DELAY_MAX_S', 120))
    
    # Dosya yolları
    COOKIES_FILE = 'instagram_cookies.json'
    FOLLOWED_USERS_FILE = 'followed_users.txt'
    LOG_FILE = 'bot.log'
    
    # Tarayıcı ayarları
    BROWSER_HEADLESS = False
    BROWSER_VIEWPORT_WIDTH = 1366
    BROWSER_VIEWPORT_HEIGHT = 768
    
    # Instagram selectors
    FOLLOW_BUTTON_SELECTORS = [
        'button:has-text("Takip Et")',
        'button:has-text("Follow")',
        'button:has-text("Seguir")',
        'button[type="button"]:has-text("Takip")',
        'button[type="button"]:has-text("Follow")',
        'div[role="button"]:has-text("Takip")',
        'div[role="button"]:has-text("Follow")',
        'a[role="button"]:has-text("Takip")',
        'a[role="button"]:has-text("Follow")'
    ]
    
    FOLLOWERS_BUTTON_SELECTORS = [
        'a[href*="/followers/"]',
        'a:has-text("takipçi")',
        'a:has-text("followers")',
        'a:has-text("seguidores")'
    ]
    
    # Takip edilemeyen buton metinleri
    ALREADY_FOLLOWING_KEYWORDS = [
        'takiptesin', 'following', 'siguiendo', 
        'istek gonderildi', 'request sent', 'pending'
    ]
    
    # Takip edilebilir buton metinleri
    FOLLOWABLE_KEYWORDS = [
        'takip et', 'follow', 'seguir', 
        'istek gonder', 'send request'
    ]
