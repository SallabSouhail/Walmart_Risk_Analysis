import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('product_reviews.csv')  # Remplacez par le chemin de votre fichier

# Ajouter une colonne d'étiquette basée sur la condition
df["label"] = df["Rating"].apply(lambda x: 1 if x > 3 else 0)

# Sauvegarder le DataFrame avec les étiquettes dans un nouveau fichier CSV
df.to_csv('product_reviews.csv', index=False)

print("Fichier étiqueté sauvegardé avec succès !")
