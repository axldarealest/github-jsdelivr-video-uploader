#!/usr/bin/env python3
"""
GitHub + jsDelivr Video Uploader
Upload rapidement des vidéos sur GitHub et génère les URLs jsDelivr
"""

import os
import sys
import base64
import requests
import hashlib
from pathlib import Path
from datetime import datetime
import pyperclip
from config import Config

class VideoUploader:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {self.config.github_token}',
            'User-Agent': 'GitHub-jsDelivr-Video-Uploader'
        })

    def validate_video(self, video_path):
        """Valide la vidéo (taille, format)"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"❌ Fichier non trouvé: {video_path}")
        
        # Vérifier la taille
        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        if size_mb > 50:
            raise ValueError(f"❌ Fichier trop volumineux: {size_mb:.1f}MB (max: 50MB)")
        
        # Vérifier l'extension
        valid_extensions = {'.mp4', '.webm', '.mov', '.avi', '.mkv'}
        if Path(video_path).suffix.lower() not in valid_extensions:
            raise ValueError(f"❌ Format non supporté. Formats autorisés: {', '.join(valid_extensions)}")
        
        print(f"✅ Vidéo validée: {size_mb:.1f}MB")
        return True

    def generate_filename(self, original_path):
        """Génère un nom de fichier unique"""
        original_name = Path(original_path).stem
        extension = Path(original_path).suffix.lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Hash du fichier pour unicité
        with open(original_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:8]
        
        return f"{original_name}_{timestamp}_{file_hash}{extension}"

    def upload_to_github(self, video_path, filename):
        """Upload la vidéo vers GitHub"""
        print(f"📤 Upload vers GitHub...")
        
        # Lire et encoder le fichier
        with open(video_path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        
        # Préparer la requête
        url = f"https://api.github.com/repos/{self.config.github_username}/{self.config.github_repo}/contents/videos/{filename}"
        
        data = {
            'message': f"Add video: {filename}",
            'content': content,
            'branch': 'main'
        }
        
        # Vérifier si le fichier existe déjà
        try:
            existing = self.session.get(url)
            if existing.status_code == 200:
                data['sha'] = existing.json()['sha']
                print("📝 Fichier existant trouvé, mise à jour...")
        except:
            pass
        
        # Upload
        response = self.session.put(url, json=data)
        
        if response.status_code in [200, 201]:
            print("✅ Upload réussi!")
            return True
        else:
            print(f"❌ Erreur upload: {response.status_code}")
            print(response.text)
            return False

    def generate_jsdelivr_url(self, filename):
        """Génère l'URL jsDelivr"""
        return f"https://cdn.jsdelivr.net/gh/{self.config.github_username}/{self.config.github_repo}@main/videos/{filename}"

    def generate_html_snippet(self, jsdelivr_url, filename):
        """Génère un snippet HTML d'exemple"""
        return f"""
<!-- Background vidéo - {filename} -->
<div class="video-background">
    <video autoplay muted loop playsinline>
        <source src="{jsdelivr_url}" type="video/mp4">
        Votre navigateur ne supporte pas les vidéos HTML5.
    </video>
</div>

<style>
.video-background {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    overflow: hidden;
}}

.video-background video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}
</style>"""

    def upload(self, video_path):
        """Méthode principale d'upload"""
        try:
            print("🎥 GitHub + jsDelivr Video Uploader")
            print("=" * 40)
            
            # Valider la vidéo
            self.validate_video(video_path)
            
            # Générer le nom de fichier
            filename = self.generate_filename(video_path)
            print(f"📁 Nom du fichier: {filename}")
            
            # Upload vers GitHub
            if not self.upload_to_github(video_path, filename):
                return False
            
            # Générer l'URL jsDelivr
            jsdelivr_url = self.generate_jsdelivr_url(filename)
            
            # Copier l'URL dans le presse-papier
            pyperclip.copy(jsdelivr_url)
            
            print("\n🎉 Upload terminé avec succès!")
            print("=" * 40)
            print(f"🔗 URL jsDelivr: {jsdelivr_url}")
            print("📋 URL copiée dans le presse-papier!")
            
            # Générer snippet HTML
            html_snippet = self.generate_html_snippet(jsdelivr_url, filename)
            
            # Sauvegarder le snippet
            snippet_path = f"html_snippets/{filename}.html"
            os.makedirs("html_snippets", exist_ok=True)
            with open(snippet_path, 'w', encoding='utf-8') as f:
                f.write(html_snippet)
            
            print(f"📄 Snippet HTML sauvé: {snippet_path}")
            print("\n⏰ Note: Il peut falloir quelques minutes pour que jsDelivr mette à jour son cache.")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python upload_video.py <chemin_vers_video>")
        print("Exemple: python upload_video.py ./ma_video.mp4")
        sys.exit(1)
    
    video_path = sys.argv[1]
    uploader = VideoUploader()
    
    success = uploader.upload(video_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 