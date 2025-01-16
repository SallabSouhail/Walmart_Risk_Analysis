import csv
import json

# Chemin des fichiers
input_file = 'categorized_products.json'  # Remplacer par le chemin correct
output_file = '../data/product_reviews.csv'

# Charger le fichier JSON
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Extraire les avis pour toutes les catégories
def extract_reviews(data):
    reviews = []
    for category, products in data.items():
        for product_info in products:
            product_name = product_info.get('product', {}).get('name', 'Inconnu')
            customer_reviews = product_info.get('reviews_raw', {}).get('customerReviews', [])

            for review in customer_reviews:
                reviews.append({
                    'Category': category,
                    'Product Name': product_name,
                    'Customer Name': review.get('userNickname', 'Anonymous'),
                    'Rating': review.get('rating', 'N/A'),
                    'Review': review.get('reviewText', 'No Review')
                })
    return reviews

# Écrire les données dans un fichier CSV
def write_to_csv(reviews, output_file):
    with open(output_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Category', 'Product Name', 'Customer Name', 'Rating', 'Review'])
        writer.writeheader()
        writer.writerows(reviews)

# Pipeline principal
def main():
    data = load_data(input_file)
    reviews = extract_reviews(data)
    write_to_csv(reviews, output_file)
    print(f"Les données ont été exportées avec succès dans le fichier {output_file}")

if __name__ == "__main__":
    main()