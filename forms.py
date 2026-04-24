from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo

# Formulaire pour s'inscrire
class RegistrationForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    confirm_password = PasswordField("Confirmer le mot de passe", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("S'inscrire")

# Formulaire pour se connecter
class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

# Formulaire pour réserver des places
class BookingForm(FlaskForm):
    nombre_places = IntegerField('Nombre de places', validators=[DataRequired()])
    submit = SubmitField('Réserver')

# FORMULAIRE POUR AJOUTER UN CONCERT (C'est ici que manquait l'import)
class ConcertForm(FlaskForm):
    title = StringField('Titre du concert', validators=[DataRequired()])
    date = DateTimeField('Date (AAAA-MM-JJ HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    location = StringField('Lieu', validators=[DataRequired()])
    genre = SelectField('Genre', choices=[('Rock', 'Rock'), ('Jazz', 'Jazz'), ('Electro', 'Electro')], validators=[DataRequired()])
    total_seats = IntegerField('Nombre de places totales', validators=[DataRequired()])
    photos_url = StringField('URL de l\'image (optionnel)')
    review = TextAreaField('Avis du rédacteur (optionnel)')
    submit = SubmitField('Enregistrer le concert')

# FORMULAIRE POUR AJOUTER UNE ACTUALITÉ
class NewsForm(FlaskForm):
    title = StringField('Titre de l\'article', validators=[DataRequired()])
    content = TextAreaField('Contenu de l\'article', validators=[DataRequired()])
    category_id = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Publier l\'article')