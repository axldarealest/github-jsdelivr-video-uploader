"""
Configuration pour l'outil GitHub + jsDelivr Video Uploader
"""

import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # Charger les variables d'environnement depuis .env
        load_dotenv()
        
        # Configuration GitHub
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_username = os.getenv('GITHUB_USERNAME')
        self.github_repo = os.getenv('GITHUB_REPO', 'video-assets')
        
        # Validation des paramètres requis
        self.validate_config()
    
    def validate_config(self):
        """Valide que tous les paramètres requis sont présents"""
        if not self.github_token:
            raise ValueError("❌ GITHUB_TOKEN manquant dans .env")
        
        if not self.github_username:
            raise ValueError("❌ GITHUB_USERNAME manquant dans .env")
        
        if not self.github_repo:
            raise ValueError("❌ GITHUB_REPO manquant dans .env")
        
        # Vérifier le format du token
        if not self.github_token.startswith(('ghp_', 'github_pat_')):
            print("⚠️ Attention: Le token GitHub ne semble pas avoir le bon format")
    
    def print_config(self):
        """Affiche la configuration (sans le token pour la sécurité)"""
        print("📋 Configuration actuelle:")
        print(f"   • Username: {self.github_username}")
        print(f"   • Repository: {self.github_repo}")
        print(f"   • Token: {'✅ Configuré' if self.github_token else '❌ Manquant'}")

# Configuration par défaut
DEFAULT_CONFIG = {
    'max_file_size_mb': 50,
    'supported_formats': ['.mp4', '.webm', '.mov', '.avi', '.mkv'],
    'github_branch': 'main',
    'video_folder': 'videos',
    'jsdelivr_base_url': 'https://cdn.jsdelivr.net/gh'
} 