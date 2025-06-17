# 📦 OpenFaaS Pipeline - US17

Projet réalisé dans le cadre du TP OpenFaaS - BUT 2 Informatique  
Responsable : US17 (Ewann)

---

## 🧭 Objectif

Mettre en place une chaîne de traitement automatisée via OpenFaaS, composée de trois fonctions serverless connectées par un bus d’événements (NATS), dans le but de :

- Déclencher automatiquement l'import de commandes chaque jour,
- Transformer un fichier CSV via FTP,
- Vérifier le statut des fichiers déposés.

---

## ⚙️ Architecture

.
├── build
│   ├── daily-fetcher
│   ├── file-transformer
│   └── status-checker
├── daily-fetcher
│   ├── handler.py
│   ├── handlerOld - Copie.py:Zone.Identifier
│   ├── requirements.txt
│   └── template
├── deployment
│   ├── cron-config.yml
│   ├── daily-fetcher.yml:Zone.Identifier
│   └── deploy-all.sh
├── file-transformer
│   ├── Data
│   ├── Depot
│   ├── daily-fetcher.yml:Zone.Identifier
│   ├── handler.py
│   └── requirements.txt
├── stack.yml
├── status-checker
│   ├── daily-fetcher.yml:Zone.Identifier
│   ├── handler - Copie.py:Zone.Identifier
│   ├── handler.py
│   └── requirements.txt
├── template
│   ├── dockerfile
│   ├── java11
│   ├── java11-vert-x
│   ├── java17
│   ├── node18
│   ├── node20
│   ├── php7
│   ├── php8
│   ├── python27-flask
│   ├── python3-flask
│   ├── python3-flask-debian
│   ├── python3-http
│   └── python3-http-debian
└── tp-openfaas-pipeline-latest.md

faas-cli up -f stack.yml

echo '{}' | faas-cli invoke daily-fetcher

faas-cli invoke status-checker

