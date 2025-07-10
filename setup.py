#!/usr/bin/env python3
"""
Script de setup pour GitHub + jsDelivr Video Uploader
Configure automatiquement l'environnement
"""

import os
import sys
import shutil
from pathlib import Path

def create_env_file():
    """Crée le fichier .env à partir du template"""
    env_example = "config.env.example"
    env_file = ".env"
    
    if os.path.exists(env_file):
        print("⚠️ Le fichier .env existe déjà.")
        response = input("Voulez-vous le remplacer ? (y/N): ")
        if response.lower() != 'y':
            print("❌ Setup annulé.")
            return False
    
    if not os.path.exists(env_example):
        print(f"❌ Fichier template {env_example} introuvable!")
        return False
    
    # Copier le template
    shutil.copy2(env_example, env_file)
    print(f"✅ Fichier {env_file} créé!")
    
    return True

def get_user_input():
    """Collecte les informations utilisateur"""
    print("\n📋 Configuration de l'outil")
    print("=" * 40)
    
    print("\n1. Token GitHub:")
    print("   → Aller sur: https://github.com/settings/tokens")
    print("   → Cliquer 'Generate new token (classic)'")
    print("   → Cocher 'repo' dans les permissions")
    print("   → Copier le token généré")
    
    github_token = input("\n🔑 Votre token GitHub: ").strip()
    if not github_token:
        print("❌ Token requis!")
        return None
    
    github_username = input("👤 Votre username GitHub: ").strip()
    if not github_username:
        print("❌ Username requis!")
        return None
    
    print(f"\n📁 Repository pour stocker les vidéos")
    print("   (Sera créé automatiquement s'il n'existe pas)")
    github_repo = input("📦 Nom du repository [video-assets]: ").strip()
    if not github_repo:
        github_repo = "video-assets"
    
    return {
        'GITHUB_TOKEN': github_token,
        'GITHUB_USERNAME': github_username,
        'GITHUB_REPO': github_repo
    }

def update_env_file(config):
    """Met à jour le fichier .env avec la configuration"""
    env_content = []
    env_content.append("# Configuration GitHub + jsDelivr Video Uploader")
    env_content.append("# Généré automatiquement par setup.py")
    env_content.append("")
    env_content.append(f"GITHUB_TOKEN={config['GITHUB_TOKEN']}")
    env_content.append(f"GITHUB_USERNAME={config['GITHUB_USERNAME']}")
    env_content.append(f"GITHUB_REPO={config['GITHUB_REPO']}")
    env_content.append("")
    
    with open('.env', 'w') as f:
        f.write('\n'.join(env_content))
    
    print("✅ Configuration sauvegardée dans .env")

def test_configuration():
    """Teste la configuration"""
    print("\n🧪 Test de la configuration...")
    
    try:
        from config import Config
        config = Config()
        config.print_config()
        print("✅ Configuration valide!")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def create_directories():
    """Crée les dossiers nécessaires"""
    directories = ['html_snippets', 'temp']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Dossier {directory}/ créé")

def main():
    print("🎥 Setup GitHub + jsDelivr Video Uploader")
    print("=" * 50)
    
    # Créer le fichier .env
    if not create_env_file():
        return
    
    # Collecter les infos utilisateur
    config = get_user_input()
    if not config:
        return
    
    # Mettre à jour .env
    update_env_file(config)
    
    # Créer les dossiers
    create_directories()
    
    # Tester la configuration
    if test_configuration():
        print("\n🎉 Setup terminé avec succès!")
        print("=" * 50)
        print("💡 Prochaines étapes:")
        print("   1. Installer les dépendances: pip install -r requirements.txt")
        print("   2. Uploader une vidéo: python upload_video.py ma_video.mp4")
        print("   3. Voir example.html pour l'intégration")
    else:
        print("\n❌ Erreur lors du setup")
        print("Vérifiez votre configuration dans .env")

if __name__ == "__main__":
    main() 