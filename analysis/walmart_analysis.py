import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
import nltk
import re
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class WalmartRiskAnalyzer:
    def __init__(self, csv_file):
        """Initialize the analyzer with the CSV file"""
        self.df = pd.read_csv(csv_file)
        self.sia = SentimentIntensityAnalyzer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Créer le dossier pour les visualisations
        os.makedirs('visualizations', exist_ok=True)
        
    def preprocess_date(self):
        """Convertir les dates en format datetime"""
        # Extraire la date de la chaîne "Reviewed..."
        self.df['Date'] = self.df['Date'].str.extract(r'Reviewed (.*?), 2023')
        
        # Remplacer les noms de mois par leurs abréviations standard
        month_map = {
            'Sept.': 'Sep',
            'Aug.': 'Aug',
            'July': 'Jul',
            'June': 'Jun',
            'April': 'Apr',
            'March': 'Mar',
            'Feb.': 'Feb',
            'Jan.': 'Jan',
            'Dec.': 'Dec',
            'Nov.': 'Nov',
            'Oct.': 'Oct'
        }
        
        for full, abbr in month_map.items():
            self.df['Date'] = self.df['Date'].str.replace(full, abbr, regex=False)
            
        # Convertir en datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'] + ' 2023', format='%b %d %Y')
        
    def identify_risk_categories(self):
        """Identifier les catégories de risque dans les avis"""
        risk_categories = {
            'delivery': r'delivery|shipping|arrived|late|missing',
            'customer_service': r'customer service|support|representative|phone|call',
            'refund': r'refund|return|money back|charge|payment',
            'account': r'account|login|password|hack|security',
            'scam': r'scam|fraud|fake|third.?party|seller',
            'product_quality': r'quality|defective|broken|damaged|wrong'
        }
        
        for category, pattern in risk_categories.items():
            self.df[f'risk_{category}'] = self.df['Review'].str.contains(
                pattern, case=False, regex=True).astype(int)
            
        # Calculer le score de risque total
        risk_columns = [col for col in self.df.columns if col.startswith('risk_')]
        self.df['total_risk_score'] = self.df[risk_columns].sum(axis=1)
        
    def analyze_sentiment(self):
        """Analyser le sentiment des avis"""
        self.df['sentiment_scores'] = self.df['Review'].apply(
            lambda x: self.sia.polarity_scores(str(x))['compound']
        )
        
        # Catégoriser les sentiments
        self.df['sentiment_category'] = pd.cut(
            self.df['sentiment_scores'],
            bins=[-1, -0.5, -0.1, 0.1, 0.5, 1],
            labels=['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
        )
        
    def generate_risk_report(self):
        """Générer un rapport détaillé des risques"""
        risk_columns = [col for col in self.df.columns if col.startswith('risk_')]
        
        risk_summary = {
            'total_reviews': len(self.df),
            'average_rating': self.df['Rating'].mean(),
            'risk_distribution': {
                col.replace('risk_', ''): self.df[col].mean() * 100 
                for col in risk_columns
            },
            'highest_risk_category': max(
                [(col.replace('risk_', ''), self.df[col].mean()) 
                 for col in risk_columns],
                key=lambda x: x[1]
            )[0],
            'sentiment_distribution': self.df['sentiment_category'].value_counts().to_dict()
        }
        
        return risk_summary
        
    def plot_risk_analysis(self):
        """Générer des visualisations de l'analyse des risques"""
        # 1. Distribution des catégories de risque
        risk_columns = [col for col in self.df.columns if col.startswith('risk_')]
        risk_means = self.df[risk_columns].mean().sort_values(ascending=True)
        
        plt.figure(figsize=(12, 6))
        risk_means.plot(kind='barh')
        plt.title('Distribution of Risk Categories')
        plt.xlabel('Percentage of Reviews')
        plt.tight_layout()
        plt.savefig('visualizations/risk_categories_distribution.png')
        plt.close()
        
        # 2. Évolution temporelle des risques
        plt.figure(figsize=(12, 6))
        self.df.groupby('Date')['total_risk_score'].mean().plot()
        plt.title('Risk Score Evolution Over Time')
        plt.xlabel('Date')
        plt.ylabel('Average Risk Score')
        plt.tight_layout()
        plt.savefig('visualizations/risk_evolution.png')
        plt.close()
        
        # 3. Corrélation entre sentiment et risque
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='sentiment_category', y='total_risk_score', data=self.df)
        plt.title('Risk Score Distribution by Sentiment')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('visualizations/sentiment_risk_correlation.png')
        plt.close()
        
        # 4. Carte de chaleur des corrélations entre risques
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            self.df[[col for col in self.df.columns if col.startswith('risk_')]].corr(),
            annot=True,
            cmap='RdYlBu'
        )
        plt.title('Risk Categories Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('visualizations/risk_correlation_heatmap.png')
        plt.close()
        
        # 5. Nuage de mots des avis à haut risque
        high_risk_text = ' '.join(
            self.df[self.df['total_risk_score'] >= self.df['total_risk_score'].quantile(0.75)]['Review']
        )
        wordcloud = WordCloud(
            width=800, height=400,
            background_color='white',
            max_words=100
        ).generate(high_risk_text)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Most Common Words in High-Risk Reviews')
        plt.tight_layout()
        plt.savefig('visualizations/high_risk_wordcloud.png')
        plt.close()

def main():
    # Initialiser l'analyseur
    analyzer = WalmartRiskAnalyzer('data/Walmart_reviews_data.csv')
    
    # Prétraiter les données
    analyzer.preprocess_date()
    
    # Analyser les risques et sentiments
    analyzer.identify_risk_categories()
    analyzer.analyze_sentiment()
    
    # Générer le rapport
    risk_report = analyzer.generate_risk_report()
    
    # Afficher les résultats
    print("\nWalmart Risk Analysis Report")
    print("===========================")
    print(f"\nTotal Reviews Analyzed: {risk_report['total_reviews']}")
    print(f"Average Rating: {risk_report['average_rating']:.2f}/5")
    
    print("\nRisk Distribution:")
    for category, percentage in risk_report['risk_distribution'].items():
        print(f"- {category.replace('_', ' ').title()}: {percentage:.1f}%")
    
    print(f"\nHighest Risk Category: {risk_report['highest_risk_category'].replace('_', ' ').title()}")
    
    print("\nSentiment Distribution:")
    for sentiment, count in risk_report['sentiment_distribution'].items():
        percentage = (count / risk_report['total_reviews']) * 100
        print(f"- {sentiment}: {percentage:.1f}%")
    
    # Générer les visualisations
    analyzer.plot_risk_analysis()
    print("\nVisualizations have been saved in the 'visualizations' directory.")

if __name__ == "__main__":
    main()
