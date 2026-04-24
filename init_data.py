from app import app, db
from models import Category, Concert
from datetime import datetime, timedelta

with app.app_context():
    # 1. Ajout des catégories demandées
    c1 = Category(name="Rock")
    c2 = Category(name="Jazz")
    c3 = Category(name="Electro")
    db.session.add_all([c1, c2, c3])
    
    # 2. Ajout de concerts (un futur et un passé)
    # Concert à venir (Source 15)
    concert_futur = Concert(
        title="Musilac 2024",
        date=datetime.now() + timedelta(days=30),
        location="Aix-les-Bains",
        genre="Rock",
        total_seats=500
    )
    # Concert passé avec avis (Source 17)
    concert_passe = Concert(
        title="Jazz à Vienne",
        date=datetime.now() - timedelta(days=10),
        location="Vienne",
        genre="Jazz",
        total_seats=200,
        review="Une performance acoustique incroyable dans le théâtre antique.",
        photos_url="https://placehold.co/600x400?text=Photo+Concert+Jazz"
    )
    
    db.session.add_all([concert_futur, concert_passe])
    db.session.commit()
    print("Données de test insérées avec succès !")