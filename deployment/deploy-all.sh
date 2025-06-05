#!/bin/bash

echo "Déploiement des fonctions OpenFaaS pour DataRetailX"

# Variables
USER_ID=${1:-"US17"}

echo "Déploiement pour l'utilisateur: $USER_ID"

# Mise à jour de l'USER_ID dans les fichiers YAML
sed -i "s/US17/$USER_ID/g" *//*.yml

# Build et déploiement des fonctions
echo "1. Déploiement de daily-fetcher..."
cd daily-fetcher
faas-cli build -f daily-fetcher.yml
faas-cli deploy -f daily-fetcher.yml
cd ..

echo "2. Déploiement de file-transformer..."
cd file-transformer
faas-cli build -f file-transformer.yml
faas-cli deploy -f file-transformer.yml
cd ..

echo "3. Déploiement de status-checker..."
cd status-checker
faas-cli build -f status-checker.yml
faas-cli deploy -f status-checker.yml
cd ..

echo "Déploiement terminé !"
echo "Test de la fonction status-checker:"
curl -X POST http://localhost:8080/function/status-checker

echo -e "\nPour tester manuellement file-transformer:"
echo "curl -X POST http://localhost:8080/function/file-transformer -d '{\"user_id\":\"$USER_ID\"}'"