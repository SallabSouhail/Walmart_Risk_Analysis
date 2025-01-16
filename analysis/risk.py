import json
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class RiskAnalyzer:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        self.risk_categories = {
            'product_quality': ['defective', 'broken', 'quality', 'damaged'],
            'delivery': ['late', 'delay', 'shipping', 'delivery'],
            'customer_service': ['rude', 'unhelpful', 'support', 'service'],
            'stock': ['unavailable', 'out of stock', 'inventory'],
            'price': ['expensive', 'overpriced', 'cost']
        }
    
    def categorize_risk(self, text):
        """Categorize the risk based on keywords"""
        text = text.lower()
        risks = []
        
        for category, keywords in self.risk_categories.items():
            if any(keyword in text for keyword in keywords):
                risks.append(category)
                
        return risks if risks else ['uncategorized']
    
    def analyze_reviews_with_ai(self, reviews, max_samples=100):
        """Use Google's Gemini to analyze reviews and identify risks"""
        if len(reviews) > max_samples:
            reviews = reviews[:max_samples]
        
        analysis_results = []
        
        for review in reviews:
            prompt = f"""Analyze this customer review and identify potential CRM risks:
            Review: {review['text']}
            
            Please identify:
            1. Main issues mentioned
            2. Risk severity (low/medium/high)
            3. Suggested mitigation strategies"""
            
            try:
                response = self.model.generate_content(prompt)
                
                analysis_results.append({
                    'review_id': review.get('id', 'unknown'),
                    'analysis': response.text,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"Error analyzing review: {str(e)}")
                
        return analysis_results
    
    def generate_risk_report(self, reviews):
        """Generate a comprehensive risk report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_reviews': len(reviews),
            'risk_categories': {},
            'high_priority_issues': []
        }
        
        # Risk categorization
        all_risks = []
        for review in reviews:
            risks = self.categorize_risk(review['text'])
            all_risks.extend(risks)
        
        # Count risks
        risk_counts = {}
        for risk in all_risks:
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        report['risk_categories'] = risk_counts
        
        # Analyze high priority reviews with AI
        negative_reviews = [
            review for review in reviews 
            if any(negative in review['text'].lower() 
                  for negative in ['bad', 'terrible', 'awful', 'worst', 'poor'])
        ]
        if negative_reviews:
            report['high_priority_issues'] = self.analyze_reviews_with_ai(negative_reviews[:10])
        
        return report

if __name__ == "__main__":
    # Example usage
    analyzer = RiskAnalyzer()
    
    # Example reviews
    reviews = [
        {"id": 1, "text": "The delivery was very late and the product was damaged"},
        {"id": 2, "text": "Great service and product quality"},
    ]
    
    # Generate risk report
    risk_report = analyzer.generate_risk_report(reviews)
    
    # Save report
    with open('data/risk_report.json', 'w') as f:
        json.dump(risk_report, f, indent=4)
