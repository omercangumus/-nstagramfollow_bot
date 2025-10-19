#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager
Takip edilen kullanıcıları yönetir
"""

import os
import logging
from typing import Set, List
from pathlib import Path

class DatabaseManager:
    """Takip edilen kullanıcıları yöneten sınıf"""
    
    def __init__(self, followed_users_file: str):
        self.followed_users_file = followed_users_file
        self.followed_users: Set[str] = set()
        self.logger = logging.getLogger(__name__)
        
    def load_followed_users(self) -> Set[str]:
        """Daha önce takip edilen kullanıcıları yükle"""
        if not os.path.exists(self.followed_users_file):
            self.logger.info(f"Takip edilen kullanıcılar dosyası bulunamadı: {self.followed_users_file}")
            return set()
            
        try:
            with open(self.followed_users_file, 'r', encoding='utf-8') as f:
                users = {line.strip() for line in f if line.strip()}
            self.followed_users = users
            self.logger.info(f"{len(users)} daha önce takip edilen kullanıcı yüklendi")
            return users
        except Exception as e:
            self.logger.error(f"Takip edilen kullanıcılar yüklenirken hata: {e}")
            return set()
    
    def save_followed_user(self, username: str) -> bool:
        """Takip edilen kullanıcıyı kaydet"""
        try:
            with open(self.followed_users_file, 'a', encoding='utf-8') as f:
                f.write(f"{username}\n")
            self.followed_users.add(username)
            self.logger.info(f"Kullanıcı kaydedildi: {username}")
            return True
        except Exception as e:
            self.logger.error(f"Kullanıcı kaydedilirken hata: {e}")
            return False
    
    def is_user_followed(self, username: str) -> bool:
        """Kullanıcı daha önce takip edilmiş mi?"""
        return username in self.followed_users
    
    def get_followed_count(self) -> int:
        """Toplam takip edilen kullanıcı sayısı"""
        return len(self.followed_users)
