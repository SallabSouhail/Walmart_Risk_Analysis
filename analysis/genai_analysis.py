import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import json

# Charger les variables d'environnement
load_dotenv()

# Configurer l'API Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

class GeminiRiskAnalyzer:
    def __init__(self, reviews_df):
        """Initialiser l'analyseur avec un DataFrame de reviews"""
        self.df = reviews_df
        
    def analyze_review_risks(self, review_text):
        """Analyser les risques d'un avis spécifique avec Gemini"""
        prompt = f"""Analyze this Walmart customer review and identify specific risks. Focus on customer service, product quality, delivery, security/fraud, and technical issues.

Review: {review_text}

Provide a concise analysis following this EXACT format (keep the exact keys, just fill in the values):
CATEGORIES: [list key risk categories, comma-separated]
SEVERITY: [high, medium, or low]
ISSUES: [list main issues identified, comma-separated]
IMPACT: [brief description of customer and business impact]
ACTIONS: [list recommended actions, comma-separated]"""
        
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Parser la réponse structurée
            result = {}
            current_key = None
            current_value = []
            
            for line in text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                if ':' in line:
                    # Sauvegarder la valeur précédente
                    if current_key:
                        result[current_key.lower()] = ', '.join(current_value) if current_value else ''
                    
                    # Nouvelle clé
                    key, value = line.split(':', 1)
                    current_key = key.strip()
                    current_value = [value.strip()]
                else:
                    # Continuation de la valeur précédente
                    current_value.append(line.strip())
            
            # Sauvegarder la dernière valeur
            if current_key:
                result[current_key.lower()] = ', '.join(current_value) if current_value else ''
            
            return result
        except Exception as e:
            print(f"Error analyzing review: {e}")
            return None
    
    def analyze_batch(self, sample_size=10):
        """Analyser un échantillon d'avis pour obtenir une vue d'ensemble des risques"""
        # Prendre un échantillon aléatoire d'avis
        sample = self.df.sample(n=min(sample_size, len(self.df)))
        
        all_risks = []
        for _, row in sample.iterrows():
            risk_analysis = self.analyze_review_risks(row['Review'])
            if risk_analysis:
                all_risks.append(risk_analysis)
        
        return self.aggregate_risk_analysis(all_risks)
    
    def aggregate_risk_analysis(self, risk_analyses):
        """Agréger les analyses de risques pour obtenir une vue d'ensemble"""
        if not risk_analyses:
            return None
            
        # Collecter toutes les catégories de risque uniques
        all_categories = set()
        for analysis in risk_analyses:
            all_categories.update(analysis.get('categories', []))
            
        # Calculer la distribution des niveaux de sévérité
        severity_counts = {
            'high': 0,
            'medium': 0,
            'low': 0
        }
        for analysis in risk_analyses:
            severity = analysis.get('severity', '').lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
                
        # Collecter toutes les recommandations uniques
        all_recommendations = set()
        for analysis in risk_analyses:
            all_recommendations.update(analysis.get('actions', []))
        
        # Créer le rapport agrégé
        return {
            'total_reviews_analyzed': len(risk_analyses),
            'risk_categories': list(all_categories),
            'severity_distribution': {
                k: v/len(risk_analyses)*100 for k, v in severity_counts.items()
            },
            'key_recommendations': list(all_recommendations),
            'overall_risk_level': max(severity_counts.items(), key=lambda x: x[1])[0]
        }
    
    def generate_risk_report(self):
        """Générer un rapport complet d'analyse des risques"""
        prompt = f"""Based on the following summary statistics from Walmart customer reviews:
        - Average Rating: {self.df['Rating'].mean():.2f}
        - Total Reviews: {len(self.df)}
        - Negative Reviews: {len(self.df[self.df['Rating'] <= 2])}
        
        Generate a comprehensive risk analysis report focusing on:
        1. Major risk areas
        2. Potential business impact
        3. Customer satisfaction trends
        4. Recommended mitigation strategies
        
        Format the response as a detailed markdown report.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating report: {e}")
            return None
