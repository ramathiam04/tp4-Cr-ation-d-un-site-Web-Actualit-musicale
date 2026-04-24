from app import app, db
from models import Category, Concert, News, User
from datetime import datetime, timedelta

with app.app_context():
    # 1. Nettoyage complet de la base pour repartir de zéro
    db.drop_all()
    db.create_all()

    # 2. Création de l'utilisateur Admin
    test_user = User(username="admin", password="password123", is_admin=True)
    db.session.add(test_user)
    db.session.commit() # On valide l'utilisateur

    # 3. Création des catégories
    cat_rock = Category(name="Rock")
    cat_jazz = Category(name="Jazz")
    cat_electro = Category(name="Electro")
    db.session.add_all([cat_rock, cat_jazz, cat_electro])
    db.session.commit() # On valide pour avoir les IDs des catégories

    # 4. Ajout de tes concerts (Futurs et Passés)
    concerts = [
        # Concerts futurs (Pas d'images ici selon ton souhait)
        Concert(title="Musique a l'honneur", date=datetime(2026, 7, 5), location="Aix-les-Bains", genre="Rock", total_seats=5000),
        Concert(title="Jazz in the town", date=datetime(2026, 6, 25), location="Strasbourg", genre="Jazz", total_seats=2000, review="Superbe acoustique !"),
        Concert(title="Olivia Rodrigo in the town", date=datetime.now() + timedelta(days=30), location="Paris", genre="Rock", total_seats=500),
        
        # Concerts passés AVEC tes images spécifiques
        Concert(
            title="Billie Eillish en feu", 
            date=datetime(2025, 7, 20), 
            location="Paris", 
            genre="Electro", 
            total_seats=10000, 
            review="Une performance légendaire qui a marqué les esprits cette année-là.",
            photos_url="https://karlobag.eu/images/upload/750px-dd2b4.jpg"
        ),
        Concert(
            title="Sienna Spiro Show", 
            date=datetime(2024, 6, 15), 
            location="Los Angeles", 
            genre="Rock", 
            total_seats=8000, 
            review="Une voix pure qui a transporté tout le public.",
            photos_url="https://media.vogue.fr/photos/6916fca8ed1a6fa367ec3f19/master/w_1600%2Cc_limit/2240042379"
        )
    ]
    db.session.add_all(concerts)

    # 5. AJOUT DES ACTUALITÉS (Pour remplir ta page Actualités)
    news_items = [
        News(
            title="Le Rock n'est pas mort", 
            content="Les festivals de cet été affichent complet. Le genre connaît un renouveau historique.", 
            category_id=cat_rock.id
        ),
        News(
            title="Nouveau prodige du Jazz", 
            content="Un jeune pianiste de 19 ans révolutionne la scène Jazz strasbourgeoise.", 
            category_id=cat_jazz.id
        ),
        News(
            title="Daft Punk : La rumeur", 
            content="Des indices laissent présager une collaboration mystère pour la fin d'année.", 
            category_id=cat_electro.id
        )
    ]
    db.session.add_all(news_items)

    # Validation finale
    db.session.commit()
    
    print("--- BASE DE DONNÉES INITIALISÉE ---")
    print("1. Utilisateur 'admin' créé.")
    print("2. Concerts passés (avec images) et futurs ajoutés.")
    print("3. Actualités ajoutées par catégories.")