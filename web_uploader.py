#!/usr/bin/env python3
"""
Interface Web pour GitHub + jsDelivr Video Uploader
Serveur Flask avec upload par drag & drop
"""

import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import tempfile
from upload_video import VideoUploader
from manage_videos import VideoManager

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'.mp4', '.webm', '.mov', '.avi', '.mkv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Vérifie si le fichier est autorisé"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Page principale avec l'interface d'upload"""
    return render_template('upload.html')

@app.route('/gallery')
def gallery():
    """Page galerie des vidéos uploadées"""
    try:
        manager = VideoManager()
        videos = manager.list_videos()
        
        # Transformer pour le template
        video_list = []
        for video in videos:
            video_list.append({
                'name': video['name'],
                'size_mb': round(video['size'] / (1024 * 1024), 1),
                'url': f"https://cdn.jsdelivr.net/gh/{manager.config.github_username}/{manager.config.github_repo}@main/videos/{video['name']}",
                'sha': video['sha'][:8]
            })
        
        return render_template('gallery.html', videos=video_list)
    except Exception as e:
        return render_template('gallery.html', videos=[], error=str(e))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint pour l'upload de fichiers"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'Format non supporté. Utilisez: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Sauvegarder temporairement
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        # Vérifier la taille
        size_mb = os.path.getsize(temp_path) / (1024 * 1024)
        if size_mb > 50:
            os.remove(temp_path)
            return jsonify({'error': f'Fichier trop volumineux: {size_mb:.1f}MB (max: 50MB)'}), 400
        
        # Générer le filename avant l'upload
        uploader = VideoUploader()
        generated_filename = uploader.generate_filename(temp_path)
        
        # Upload vers GitHub
        success = uploader.upload(temp_path)
        
        # Nettoyer le fichier temporaire
        os.remove(temp_path)
        
        if success:
            # Générer l'URL jsDelivr
            jsdelivr_url = uploader.generate_jsdelivr_url(generated_filename)
            
            return jsonify({
                'success': True,
                'message': 'Vidéo uploadée avec succès!',
                'url': jsdelivr_url,
                'filename': generated_filename,
                'size_mb': size_mb
            })
        else:
            return jsonify({'error': 'Erreur lors de l\'upload vers GitHub'}), 500
            
    except Exception as e:
        # Nettoyer en cas d'erreur
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_video(filename):
    """Supprime une vidéo"""
    try:
        manager = VideoManager()
        success = manager.delete_video(filename)
        
        if success:
            return jsonify({'success': True, 'message': f'{filename} supprimé'})
        else:
            return jsonify({'error': 'Erreur lors de la suppression'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/config')
def config_status():
    """Vérifie le statut de la configuration"""
    try:
        from config import Config
        config = Config()
        return jsonify({
            'configured': True,
            'username': config.github_username,
            'repo': config.github_repo
        })
    except Exception as e:
        return jsonify({
            'configured': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🌐 Démarrage du serveur web...")
    print("📱 Interface disponible sur: http://localhost:5000")
    print("📋 Galerie des vidéos: http://localhost:5000/gallery")
    print("⚙️ Assurez-vous d'avoir configuré votre .env avec setup.py")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 