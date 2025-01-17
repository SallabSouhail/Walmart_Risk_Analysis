# Analyse des Risques Walmart avec Web Scraping et IA Générative

Ce projet combine le web scraping, l'analyse de données traditionnelle et l'IA générative pour analyser les risques liés aux avis clients de Walmart.

## 📊 Structure du Projet

```
PROJET_SCRAPING/
├── data/
│   └── Walmart_reviews_data.csv     # Données des avis clients
├── scrapers/
│   └── walmart.py                   # Script de scraping
├── analysis/
│   ├── walmart_analysis.py          # Analyse traditionnelle
│   ├── genai_analysis.py           # Analyse avec Gemini AI
│   ├── risk.py                     # Fonctions d'analyse des risques
│   └── run_analysis.py             # Script principal d'analyse
├── visualizations/                  # Graphiques et visualisations
├── requirements.txt                 # Dépendances du projet
└── .env                            # Variables d'environnement
```

## 🚀 Fonctionnalités

### 1. Web Scraping
- Collecte automatisée des avis clients Walmart
- Extraction des informations clés : note, texte, date, localisation
- Gestion des erreurs et des timeouts
- Respect des limites de taux de requêtes

### 2. Analyse Traditionnelle
- Prétraitement des données
- Analyse des sentiments avec NLTK VADER
- Identification des catégories de risque
- Visualisations :
  - Distribution des notes
  - Évolution temporelle des risques
  - Corrélations entre risques
  - Nuage de mots des avis négatifs

### 3. Analyse avec IA Générative
- Intégration de Google Gemini AI
- Analyse détaillée des risques par avis
- Génération de recommandations
- Rapport d'analyse global

## 📈 Résultats Clés

### Catégories de Risque Identifiées
- Service client (60% des avis)
- Problèmes de livraison (50%)
- Problèmes de remboursement (50%)
- Qualité des produits (20%)
- Sécurité des comptes (20%)
- Arnaques (10%)

### Analyse des Sentiments
- 50% très négatifs
- 30% très positifs
- 10% négatifs
- 10% neutres

## 🛠️ Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
cd PROJET_SCRAPING
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
- Créer un fichier `.env`
- Ajouter les clés API :
  ```
  GEMINI_API_KEY=votre_clé_gemini
  SCRAPINGBEE_API_KEY=votre_clé_scrapingbee
  ```

## 📝 Utilisation

### Scraping des Données
```bash
python scrapers/walmart.py
```

### Analyse Complète
```bash
python analysis/run_analysis.py
```

## 📊 Visualisations

Les visualisations sont générées dans le dossier `visualizations/` :
- `risk_categories_distribution.png` : Distribution des catégories de risque
- `risk_evolution.png` : Évolution temporelle des risques
- `sentiment_risk_correlation.png` : Corrélation sentiment-risque
- `risk_correlation_heatmap.png` : Carte de chaleur des corrélations

## 🔍 Conclusions et Recommandations

1. **Priorités Immédiates**
   - Amélioration du service client
   - Optimisation des processus de livraison
   - Renforcement des procédures de remboursement

2. **Actions à Moyen Terme**
   - Contrôle qualité des produits
   - Sécurisation des comptes clients
   - Vérification des vendeurs tiers

3. **Stratégies à Long Terme**
   - Mise en place d'un système de détection précoce des risques
   - Formation continue des employés
   - Amélioration de l'expérience client globale

## 📚 Technologies Utilisées

- **Web Scraping** : BeautifulSoup, ScrapingBee
- **Analyse de Données** : Pandas, NumPy
- **NLP** : NLTK, VADER
- **Visualisation** : Matplotlib, Seaborn, WordCloud
- **IA Générative** : Google Gemini AI
- **Autres** : Python-dotenv, JSON

## 👥 Contribution

- [**ANTOINE Ahehehinnou Matial**](https://github.com/antoineahehehinnou)
- [**NOAM Haythem**](https://github.com/noamgates)
- [**SALLAB Souhail**](https://github.com/SallabSouhail)
