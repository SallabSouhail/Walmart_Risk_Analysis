import json
import os

# Fonction pour catégoriser un produit en fonction de son nom ou d'autres critères
def categorize_product(product: dict) -> str:
    categories = {
        "electronics": ["laptop", "macbook", "phone", "tablet", "headphones", "tv"],
        "beauty": ["moisturizing", "lotion", "skincare", "beauty", "makeup"],
        "furniture": ["chair", "table", "sofa", "furniture", "bed", "couch"],
        "clothing": ["shirt", "pants", "dress", "jacket", "jeans"],
        "kitchen": [
            "air fryer", "oven", "microwave", "steamer", "deep fryer", "stove", "grill",
            "plancha", "wok", "mixer", "blender", "food processor", "mincer", "grater",
            "mandoline", "juicer", "peeler", "whisk", "rolling pin", "pan", "pot", "casserole",
            "roasting pan", "baking tin", "baking tray", "grill pan", "plate", "bowl", "glass",
            "cup", "carafe", "bread basket", "airtight container", "spice rack", "knife block",
            "chopping board", "wooden spoon", "spatula", "tongs", "ladle", "skimmer", "pastry brush",
            "meat tongs", "pepper mill", "salt mill", "garlic press", "zester", "pizza cutter",
            "bottle opener", "wine opener"
        ]
    }

    # Vérification du nom du produit
    product_name = product.get("name", "").lower()
    
    # Vérification du type de produit
    for category, keywords in categories.items():
        if any(keyword in product_name for keyword in keywords):
            return category
    
    return "other"  # Si aucun mot-clé n'est trouvé, on place le produit dans "other"

# Fonction principale pour charger le fichier JSON brut et appliquer la catégorisation
def categorize_products(input_file: str, output_file: str):
    # Charger les données JSON
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    categorized_data = {"electronics": [], "beauty": [], "furniture": [], "clothing": [], "kitchen": [], "other": []}

    # Parcours des produits
    for product_data in data:
        product = product_data.get("product", {})
        category = categorize_product(product)  # Déterminer la catégorie
        categorized_data[category].append(product_data)  # Ajouter le produit à la catégorie correspondante

    # Sauvegarder les données catégorisées dans un nouveau fichier JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(categorized_data, f, indent=2, ensure_ascii=False)

    print(f"Data categorized and saved to {output_file}")

# Exemple d'utilisation
input_file = "walmart_products_with_reviews.json"  # Fichier d'entrée (fichier brut JSON)
output_file = "categorized_products.json"  # Fichier de sortie pour les produits catégorisés

categorize_products(input_file, output_file)
