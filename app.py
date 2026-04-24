from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Category, News, Concert, Booking
from forms import BookingForm, RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://musi_user:musi_pass@localhost/musi_actu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ma_cle_secrete_tp_musical_2026'

# Initialisation de la base de données
db.init_app(app)

# --- GESTION DE LA CONNEXION (Flask-Login) ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Injection de variables globales pour tous les templates (comme la météo ou timedelta)
@app.context_processor
def inject_now():
    return {'now': datetime.now(), 'timedelta': timedelta}

# --- ROUTES ---

@app.route('/')
def index():
    recent_news = News.query.order_by(News.date_posted.desc()).limit(3).all()
    upcoming_concerts = Concert.query.filter(Concert.date >= datetime.now()).order_by(Concert.date.asc()).limit(3).all()
    return render_template('index.html', news=recent_news, concerts=upcoming_concerts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(username=form.username.data).first()
        if user_exists:
            flash("Ce nom d'utilisateur est déjà pris.", "danger")
            return redirect(url_for('register'))
        
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Votre compte a été créé avec succès ! Vous pouvez vous connecter.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash(f"Ravi de vous revoir, {user.username} !", "success")
            return redirect(url_for('index'))
        else:
            flash("Identifiants incorrects. Veuillez réessayer.", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for('index'))

@app.route('/concerts', methods=['GET', 'POST'])
def list_concerts():
    form = BookingForm()
    now = datetime.now()
    
    # 1. Traitement de la réservation (POST)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Vous devez être connecté pour réserver des places.", "warning")
            return redirect(url_for('login'))
            
        concert_id = request.form.get('concert_id')
        concert = Concert.query.get(concert_id)
        
        if concert and concert.total_seats >= form.nombre_places.data:
            nouvelle_resa = Booking(
                user_id=current_user.id,
                concert_id=concert_id,
                tickets_count=form.nombre_places.data
            )
            concert.total_seats -= form.nombre_places.data
            db.session.add(nouvelle_resa)
            db.session.commit()
            flash(f"Réservation réussie pour {concert.title} !", "success")
            return redirect(url_for('mes_reservations'))
        else:
            flash("Désolé, il n'y a plus assez de places disponibles.", "danger")

    # 2. Filtrage des concerts (GET)
    lieu = request.args.get('location')
    genre = request.args.get('genre')
    query = Concert.query
    
    if lieu: query = query.filter(Concert.location.contains(lieu))
    if genre: query = query.filter(Concert.genre == genre)
    
    # Séparation À venir / Passés
    upcoming = query.filter(Concert.date >= now).order_by(Concert.date.asc()).all()
    past = query.filter(Concert.date < now).order_by(Concert.date.desc()).all()
    
    return render_template('concerts.html', upcoming=upcoming, past=past, form=form)

@app.route('/actualites')
def list_news():
    category_name = request.args.get('category')
    if category_name:
        categories = Category.query.filter_by(name=category_name).all()
    else:
        categories = Category.query.all()
    return render_template('actualites.html', categories=categories)

@app.route('/mes-reservations')
@login_required
def mes_reservations():
    reservations = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('mes_reservations.html', reservations=reservations)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Accès interdit. Réservé aux administrateurs.", "danger")
        return redirect(url_for('index'))
    concerts = Concert.query.all()
    return render_template('admin.html', concerts=concerts)

@app.route('/admin/concerts', methods=['GET', 'POST'])
@login_required
def admin_concerts():
    if not current_user.is_admin: return redirect(url_for('index'))
    
    form = ConcertForm()
    if form.validate_on_submit():
        new_concert = Concert(
            title=form.title.data,
            date=form.date.data,
            location=form.location.data,
            genre=form.genre.data,
            total_seats=form.total_seats.data,
            photos_url=form.photos_url.data,
            review=form.review.data
        )
        db.session.add(new_concert)
        db.session.commit()
        flash("Concert ajouté !", "success")
        return redirect(url_for('admin_concerts'))
    
    concerts = Concert.query.all()
    return render_template('admin_concerts.html', concerts=concerts, form=form)

@app.route('/admin/actualites', methods=['GET', 'POST'])
@login_required
def admin_news():
    if not current_user.is_admin: return redirect(url_for('index'))
    
    form = NewsForm()
    # On charge les catégories dynamiquement
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        new_item = News(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category_id.data
        )
        db.session.add(new_item)
        db.session.commit()
        flash("Actualité publiée !", "success")
        return redirect(url_for('admin_news'))
    
    news = News.query.all()
    return render_template('admin_news.html', news=news, form=form)

# --- LANCEMENT ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)