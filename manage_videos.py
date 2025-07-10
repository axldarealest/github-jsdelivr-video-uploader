#!/usr/bin/env python3
"""
Gestionnaire de vidéos GitHub + jsDelivr
Liste, supprime et gère les vidéos uploadées
"""

import sys
import requests
from datetime import datetime
from config import Config
import pyperclip

class VideoManager:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {self.config.github_token}',
            'User-Agent': 'GitHub-jsDelivr-Video-Manager'
        })

    def list_videos(self):
        """Liste toutes les vidéos uploadées"""
        print("📋 Liste des vidéos uploadées")
        print("=" * 50)
        
        url = f"https://api.github.com/repos/{self.config.github_username}/{self.config.github_repo}/contents/videos"
        
        try:
            response = self.session.get(url)
            if response.status_code == 404:
                print("📁 Aucune vidéo trouvée (dossier videos/ vide)")
                return []
            
            if response.status_code != 200:
                print(f"❌ Erreur API: {response.status_code}")
                return []
            
            videos = response.json()
            
            if not videos:
                print("📁 Aucune vidéo trouvée")
                return []
            
            print(f"📹 {len(videos)} vidéo(s) trouvée(s):\n")
            
            for i, video in enumerate(videos, 1):
                name = video['name']
                size_mb = video['size'] / (1024 * 1024)
                jsdelivr_url = f"https://cdn.jsdelivr.net/gh/{self.config.github_username}/{self.config.github_repo}@main/videos/{name}"
                
                print(f"{i}. 📹 {name}")
                print(f"   📏 Taille: {size_mb:.1f} MB")
                print(f"   🔗 URL: {jsdelivr_url}")
                print(f"   📅 SHA: {video['sha'][:8]}...")
                print()
            
            return videos
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []

    def delete_video(self, filename):
        """Supprime une vidéo"""
        print(f"🗑️ Suppression de {filename}...")
        
        # Récupérer le SHA du fichier
        url = f"https://api.github.com/repos/{self.config.github_username}/{self.config.github_repo}/contents/videos/{filename}"
        
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                print(f"❌ Fichier {filename} non trouvé")
                return False
            
            file_info = response.json()
            sha = file_info['sha']
            
            # Supprimer le fichier
            delete_data = {
                'message': f"Delete video: {filename}",
                'sha': sha,
                'branch': 'main'
            }
            
            delete_response = self.session.delete(url, json=delete_data)
            
            if delete_response.status_code == 200:
                print(f"✅ {filename} supprimé avec succès!")
                return True
            else:
                print(f"❌ Erreur lors de la suppression: {delete_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False

    def get_video_url(self, filename):
        """Génère et copie l'URL jsDelivr d'une vidéo"""
        jsdelivr_url = f"https://cdn.jsdelivr.net/gh/{self.config.github_username}/{self.config.github_repo}@main/videos/{filename}"
        pyperclip.copy(jsdelivr_url)
        print(f"🔗 URL copiée: {jsdelivr_url}")
        return jsdelivr_url

    def interactive_menu(self):
        """Menu interactif"""
        while True:
            print("\n🎥 Gestionnaire de vidéos GitHub + jsDelivr")
            print("=" * 50)
            print("1. 📋 Lister les vidéos")
            print("2. 🔗 Copier URL d'une vidéo")
            print("3. 🗑️ Supprimer une vidéo")
            print("4. ❌ Quitter")
            
            choice = input("\nChoisissez une option (1-4): ").strip()
            
            if choice == '1':
                self.list_videos()
                
            elif choice == '2':
                videos = self.list_videos()
                if videos:
                    try:
                        index = int(input("\nNuméro de la vidéo: ")) - 1
                        if 0 <= index < len(videos):
                            self.get_video_url(videos[index]['name'])
                        else:
                            print("❌ Numéro invalide")
                    except ValueError:
                        print("❌ Veuillez entrer un numéro valide")
                        
            elif choice == '3':
                videos = self.list_videos()
                if videos:
                    try:
                        index = int(input("\nNuméro de la vidéo à supprimer: ")) - 1
                        if 0 <= index < len(videos):
                            filename = videos[index]['name']
                            confirm = input(f"⚠️ Confirmer la suppression de {filename} ? (y/N): ")
                            if confirm.lower() == 'y':
                                self.delete_video(filename)
                        else:
                            print("❌ Numéro invalide")
                    except ValueError:
                        print("❌ Veuillez entrer un numéro valide")
                        
            elif choice == '4':
                print("👋 Au revoir!")
                break
                
            else:
                print("❌ Option invalide")

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        manager = VideoManager()
        
        if command == "list":
            manager.list_videos()
        elif command == "delete" and len(sys.argv) > 2:
            filename = sys.argv[2]
            manager.delete_video(filename)
        elif command == "url" and len(sys.argv) > 2:
            filename = sys.argv[2]
            manager.get_video_url(filename)
        else:
            print("Usage:")
            print("  python manage_videos.py list")
            print("  python manage_videos.py delete <filename>")
            print("  python manage_videos.py url <filename>")
            print("  python manage_videos.py  (mode interactif)")
    else:
        # Mode interactif
        manager = VideoManager()
        manager.interactive_menu()

if __name__ == "__main__":
    main() 