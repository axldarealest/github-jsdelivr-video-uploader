# 🎥 GitHub + jsDelivr Video Uploader

Un outil simple pour uploader rapidement des vidéos sur GitHub et les servir via jsDelivr comme background vidéo.

## ✨ Fonctionnalités

- Upload automatique vers GitHub via API
- Génération automatique de l'URL jsDelivr
- Vérification de la taille (< 50MB)
- Support des formats vidéo courants (mp4, webm, mov)
- Exemple d'intégration HTML inclus

## 🚀 Installation rapide

1. **Cloner ce repo** :
```bash
git clone <votre-repo>
cd github-jsdelivr-video-uploader
```

2. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Configuration automatique** :
```bash
python setup.py
```
   Le script va vous guider pour créer votre token GitHub et configurer l'outil.

## ⚡ Démarrage ultra-rapide

```bash
# Avec Make (recommandé)
make setup                    # Configuration automatique
make web                      # Interface web (http://localhost:5000)
make upload VIDEO=video.mp4   # Upload d'une vidéo
make list                     # Liste des vidéos
make manage                   # Gestionnaire interactif

# Ou manuellement
python setup.py              # Configuration
python web_uploader.py       # Interface web
python upload_video.py ma_video.mp4   # Upload
python manage_videos.py      # Gestion
```

## 📝 Configuration

Éditer le fichier `.env` :
```env
GITHUB_TOKEN=ghp_votre_token_ici
GITHUB_USERNAME=votre_username
GITHUB_REPO=nom_du_repo_pour_les_videos
```

## 🎬 Utilisation

```bash
python upload_video.py chemin/vers/votre/video.mp4
```

L'outil va :
1. ✅ Vérifier que la vidéo fait < 50MB
2. 📤 Upload vers GitHub
3. 🔗 Générer l'URL jsDelivr
4. 📋 Copier l'URL dans le presse-papier

## 🌐 Utilisation sur votre site

```html
<!-- Background vidéo responsive -->
<div class="video-background">
    <video autoplay muted loop>
        <source src="https://cdn.jsdelivr.net/gh/username/repo@main/videos/ma-video.mp4" type="video/mp4">
    </video>
</div>
```

## 📁 Structure du projet

```
├── upload_video.py      # Script principal d'upload
├── web_uploader.py      # Serveur web Flask
├── manage_videos.py     # Gestion des vidéos (liste, suppression)
├── deploy_web.py        # Déploiement GitHub Pages
├── setup.py            # Configuration automatique
├── config.py           # Gestion de la configuration
├── templates/          # Templates HTML pour l'interface web
│   ├── base.html       # Template de base
│   ├── upload.html     # Page d'upload
│   └── gallery.html    # Galerie des vidéos
├── example.html        # Exemple d'utilisation complète
├── requirements.txt    # Dépendances Python
├── config.env.example  # Template de configuration
├── Makefile           # Commandes simplifiées
├── .gitignore         # Fichiers à ignorer
└── README.md          # Documentation
```

## 🛠️ Scripts disponibles

- **`setup.py`** : Configuration automatique interactive
- **`web_uploader.py`** : 🌐 Interface web moderne avec drag & drop
- **`upload_video.py`** : Upload de vidéos vers GitHub + jsDelivr  
- **`manage_videos.py`** : Gestion des vidéos (liste, suppression, URLs)
- **`deploy_web.py`** : 🚀 Déploiement automatique sur GitHub Pages

## 🌐 Interface Web

L'outil inclut une interface web moderne avec :

✨ **Upload par drag & drop**  
✨ **Barre de progression en temps réel**  
✨ **Galerie avec prévisualisation**  
✨ **Gestion complète des vidéos**  
✨ **Copie automatique des URLs**  
✨ **Design responsive**  

```bash
make web
# ou
python web_uploader.py
```

Accédez à http://localhost:5000 pour une expérience ultra-simple !

### 🌍 Déploiement Public

Déployez votre interface sur GitHub Pages en une commande :

```bash
make deploy
# ou
python deploy_web.py
```

Votre interface sera disponible publiquement à `https://username.github.io/repo-name` !

## 🎯 Exemple complet

Voir `example.html` pour un exemple complet d'intégration avec CSS et HTML.

## ⚠️ Limitations

- Taille max : 50MB par vidéo
- Rate limit GitHub API : 5000 requêtes/heure
- jsDelivr cache : ~24h pour les mises à jour 