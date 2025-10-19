#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Bot - Ana program
Temiz, modüler ve profesyonel yapı
"""

import logging
import sys
from datetime import datetime

from config import BotConfig
from instagram_bot import InstagramBot

def setup_logging() -> None:
    """Logging yapılandırması"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main() -> None:
    """Ana fonksiyon"""
    try:
        # Logging'i yapılandır
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # Yapılandırmayı yükle
        config = BotConfig()
        
        # Bot'u başlat
        logger.info("="*60)
        logger.info("INSTAGRAM OPTIMIZED TAKIP BOTU")
        logger.info("="*60)
        logger.info(f"Kullanıcı: {config.INSTAGRAM_USERNAME}")
        logger.info(f"Kaynak hesap: @{config.SOURCE_ACCOUNT}")
        logger.info(f"Takip limiti: {config.MAX_FOLLOWS_PER_SESSION}")
        logger.info(f"Gecikme: {config.MIN_ACTION_DELAY_S}-{config.MAX_ACTION_DELAY_S} saniye")
        logger.info("="*60)
        
        bot = InstagramBot(config)
        bot.run()
        
    except Exception as e:
        logging.error(f"Program başlatılırken hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()