import pandas as pd
from walmart_analysis import WalmartRiskAnalyzer
from genai_analysis import GeminiRiskAnalyzer

def main():
    # Charger les données
    df = pd.read_csv('data/Walmart_reviews_data.csv')
    
    print("1. Analyse traditionnelle des risques")
    print("=====================================")
    traditional_analyzer = WalmartRiskAnalyzer('data/Walmart_reviews_data.csv')
    traditional_analyzer.preprocess_date()
    traditional_analyzer.identify_risk_categories()
    traditional_analyzer.analyze_sentiment()
    traditional_analyzer.plot_risk_analysis()
    
    print("\n2. Analyse avancée avec Gemini AI")
    print("==================================")
    genai_analyzer = GeminiRiskAnalyzer(df)
    
    # Analyser un échantillon d'avis
    print("\nAnalyse détaillée d'un échantillon d'avis...")
    batch_analysis = genai_analyzer.analyze_batch(sample_size=5)
    
    if batch_analysis:
        print("\nRésultats de l'analyse par échantillon :")
        print(f"Nombre d'avis analysés : {batch_analysis['total_reviews_analyzed']}")
        print("\nCatégories de risque identifiées :")
        for category in batch_analysis['risk_categories']:
            print(f"- {category}")
        
        print("\nDistribution de la sévérité des risques :")
        for severity, percentage in batch_analysis['severity_distribution'].items():
            print(f"- {severity.title()}: {percentage:.1f}%")
        
        print(f"\nNiveau de risque global : {batch_analysis['overall_risk_level'].title()}")
        
        print("\nRecommandations clés :")
        for rec in batch_analysis['key_recommendations']:
            print(f"- {rec}")
    
    # Générer un rapport complet
    print("\n3. Génération du rapport d'analyse complet")
    print("=========================================")
    report = genai_analyzer.generate_risk_report()
    if report:
        print("\nRapport d'analyse des risques :")
        print(report)

if __name__ == "__main__":
    main()
