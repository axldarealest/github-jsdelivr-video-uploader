# GitHub + jsDelivr Video Uploader - Makefile

.PHONY: help install setup upload list manage clean

help: ## Affiche l'aide
	@echo "🎥 GitHub + jsDelivr Video Uploader"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Installe les dépendances Python
	@echo "📦 Installation des dépendances..."
	pip install -r requirements.txt
	@echo "✅ Dépendances installées!"

setup: install ## Configure l'outil (première utilisation)
	@echo "🛠️ Configuration de l'outil..."
	python setup.py

upload: ## Upload une vidéo (usage: make upload VIDEO=ma_video.mp4)
	@if [ -z "$(VIDEO)" ]; then \
		echo "❌ Usage: make upload VIDEO=chemin/vers/video.mp4"; \
		exit 1; \
	fi
	@echo "📤 Upload de $(VIDEO)..."
	python upload_video.py $(VIDEO)

list: ## Liste toutes les vidéos uploadées
	@echo "📋 Liste des vidéos..."
	python manage_videos.py list

manage: ## Lance le gestionnaire interactif de vidéos
	@echo "🎮 Gestionnaire interactif..."
	python manage_videos.py

web: ## Lance l'interface web
	@echo "🌐 Démarrage de l'interface web..."
	@echo "📱 Disponible sur: http://localhost:8080"
	python3 web_uploader.py

deploy: ## Déploie l'interface web sur GitHub Pages
	@echo "🚀 Déploiement sur GitHub Pages..."
	python deploy_web.py

clean: ## Nettoie les fichiers temporaires
	@echo "🧹 Nettoyage..."
	rm -rf __pycache__/
	rm -rf *.pyc
	rm -rf temp/
	rm -rf .pytest_cache/
	@echo "✅ Nettoyage terminé!"

example: ## Ouvre l'exemple HTML dans le navigateur
	@echo "🌐 Ouverture de example.html..."
	@if command -v open >/dev/null 2>&1; then \
		open example.html; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open example.html; \
	else \
		echo "Ouvrez example.html dans votre navigateur"; \
	fi

# Raccourcis
init: setup ## Alias pour setup

# Commandes utiles pour le développement
dev-install: ## Installation pour développeurs
	pip install -r requirements.txt
	pip install black isort flake8

format: ## Formate le code
	black *.py
	isort *.py

lint: ## Vérifie le code
	flake8 *.py --max-line-length=88 --ignore=E203,W503 