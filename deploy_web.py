#!/usr/bin/env python3
"""
Script de déploiement pour l'interface web GitHub + jsDelivr
Déploie automatiquement sur GitHub Pages
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from config import Config

class WebDeployer:
    def __init__(self):
        try:
            self.config = Config()
        except Exception as e:
            print(f"❌ Erreur de configuration: {e}")
            print("Exécutez 'python setup.py' d'abord")
            sys.exit(1)
    
    def create_static_html(self):
        """Crée une version statique de l'interface web"""
        print("📄 Génération de l'interface web statique...")
        
        # Template HTML principal
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎥 Video Uploader - GitHub + jsDelivr</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            padding: 2rem;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            margin-bottom: 3rem;
            color: white;
        }}

        .header h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}

        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }}

        .info-box {{
            background: rgba(102, 126, 234, 0.1);
            border-radius: 15px;
            padding: 1.5rem;
            border-left: 4px solid #667eea;
        }}

        .info-box h3 {{
            margin-bottom: 1rem;
            color: #667eea;
        }}

        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            margin: 0.5rem;
        }}

        .btn-primary {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }}

        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }}

        .repo-info {{
            background: rgba(0, 184, 148, 0.1);
            border-radius: 10px;
            padding: 1rem;
            margin: 2rem 0;
            border-left: 4px solid #00b894;
        }}

        .footer {{
            text-align: center;
            padding: 2rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 3rem;
        }}

        .code-block {{
            background: #2d3748;
            color: #e2e8f0;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            font-family: monospace;
            text-align: left;
            overflow-x: auto;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .card {{
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎥 Video Uploader</h1>
            <p>GitHub + jsDelivr • Upload gratuit et rapide</p>
        </div>

        <div class="card">
            <h2>🎯 Repository configuré</h2>
            
            <div class="repo-info">
                <strong>📦 Repository:</strong> {self.config.github_username}/{self.config.github_repo}<br>
                <strong>🌐 Base URL:</strong> https://cdn.jsdelivr.net/gh/{self.config.github_username}/{self.config.github_repo}@main/videos/
            </div>

            <div class="info-grid">
                <div class="info-box">
                    <h3>📤 Upload Local</h3>
                    <p>Utilisez les scripts Python pour uploader vos vidéos depuis votre ordinateur.</p>
                    <div class="code-block">
python upload_video.py ma_video.mp4
# ou
make upload VIDEO=ma_video.mp4
                    </div>
                </div>

                <div class="info-box">
                    <h3>🌐 Interface Web</h3>
                    <p>Lancez l'interface web locale pour une expérience moderne avec drag & drop.</p>
                    <div class="code-block">
python web_uploader.py
# ou
make web
                    </div>
                </div>

                <div class="info-box">
                    <h3>📋 Gestion</h3>
                    <p>Gérez vos vidéos avec l'interface interactive.</p>
                    <div class="code-block">
python manage_videos.py
# ou
make manage
                    </div>
                </div>

                <div class="info-box">
                    <h3>🎬 Utilisation</h3>
                    <p>Intégrez vos vidéos dans vos projets web.</p>
                    <div class="code-block">
&lt;video autoplay muted loop&gt;
  &lt;source src="https://cdn.jsdelivr.net/gh/{self.config.github_username}/{self.config.github_repo}@main/videos/VIDEO.mp4"&gt;
&lt;/video&gt;
                    </div>
                </div>
            </div>

            <div style="margin-top: 2rem;">
                <a href="https://github.com/{self.config.github_username}/{self.config.github_repo}" class="btn btn-primary" target="_blank">
                    📦 Voir le repository
                </a>
                <a href="https://github.com/{self.config.github_username}/{self.config.github_repo}/tree/main/videos" class="btn btn-primary" target="_blank">
                    📁 Dossier videos
                </a>
            </div>
        </div>

        <div class="footer">
            <p>Made with ❤️ • Hébergement gratuit via GitHub + jsDelivr</p>
        </div>
    </div>
</body>
</html>"""
        
        # Créer le dossier docs pour GitHub Pages
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)
        
        # Sauvegarder le fichier HTML
        index_path = docs_dir / "index.html"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Interface statique créée: {index_path}")
        return index_path

    def setup_github_pages(self):
        """Configure GitHub Pages"""
        print("⚙️ Configuration de GitHub Pages...")
        
        # Vérifier si on est dans un repo git
        if not os.path.exists('.git'):
            print("❌ Pas un repository git. Initialisation...")
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/{self.config.github_username}/{self.config.github_repo}.git'])
        
        # Créer ou mettre à jour .gitignore pour inclure docs/
        gitignore_path = Path('.gitignore')
        gitignore_content = gitignore_path.read_text() if gitignore_path.exists() else ""
        
        if 'docs/' not in gitignore_content:
            with open(gitignore_path, 'a') as f:
                f.write('\n# GitHub Pages (ne pas ignorer)\n!docs/\n')
        
        try:
            # Ajouter et commiter
            subprocess.run(['git', 'add', 'docs/', '.gitignore'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Add GitHub Pages interface'], check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            
            print("✅ Code poussé vers GitHub")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Erreur git: {e}")
            print("Vous pouvez pousser manuellement avec:")
            print("git add docs/ .gitignore")
            print("git commit -m 'Add GitHub Pages interface'")
            print("git push origin main")

    def create_github_pages_config(self):
        """Crée la configuration GitHub Pages"""
        docs_dir = Path("docs")
        
        # Créer _config.yml pour Jekyll
        config_content = """title: "Video Uploader"
description: "GitHub + jsDelivr Video Uploader Interface"
theme: minima
plugins:
  - jekyll-feed
"""
        
        with open(docs_dir / "_config.yml", 'w') as f:
            f.write(config_content)
        
        print("✅ Configuration Jekyll créée")

    def deploy(self):
        """Déploie l'interface web"""
        print("🚀 Déploiement de l'interface web...")
        print("=" * 50)
        
        # Créer l'interface statique
        self.create_static_html()
        
        # Créer la config Jekyll
        self.create_github_pages_config()
        
        # Setup GitHub Pages
        self.setup_github_pages()
        
        # Instructions finales
        pages_url = f"https://{self.config.github_username}.github.io/{self.config.github_repo}"
        
        print("\n🎉 Déploiement terminé!")
        print("=" * 50)
        print(f"🌐 URL GitHub Pages: {pages_url}")
        print("\n📋 Prochaines étapes:")
        print("1. Aller sur https://github.com/{}/{}/settings/pages".format(
            self.config.github_username, self.config.github_repo
        ))
        print("2. Dans 'Source', sélectionner 'Deploy from a branch'")
        print("3. Choisir 'main' et '/docs'")
        print("4. Cliquer 'Save'")
        print("\n⏰ L'interface sera disponible dans 1-2 minutes à:")
        print(f"   {pages_url}")

def main():
    print("🚀 GitHub Pages Deployer")
    print("=" * 40)
    
    deployer = WebDeployer()
    deployer.deploy()

if __name__ == "__main__":
    main() 