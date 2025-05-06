from flask import Flask, request, render_template, redirect, url_for, flash, session # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from werkzeug.security import check_password_hash # type: ignore
app=Flask(__name__)
app.secret_key = "cle_secrete"
# Connexion à MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/pfe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle Admin
class Admin(db.Model):
    __tablename__ = 'admins'  # Nom de la table déjà existante
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

@app.route("/")
def home():
    return render_template('home.html',show_login_popup=False) 
@app.route('/login', methods=['POST'])
def login():
        utilisateur = request.form['username']
        mot_de_passe = request.form['password']

        # Vérification simple
        user = Admin.query.filter_by(username=utilisateur).first()
        if user and check_password_hash(user.password, mot_de_passe):
           return render_template('home.html', success=True)
        else:
           flash("Nom ou mot de passe incorrect", "danger")
        # On indique à la page qu’il faut ouvrir la pop-up
           return render_template('home.html', show_login_popup=True)

@app.route('/deconnexion')
def deconnexion():
    return render_template ('home.html')
@app.route('/principale')
def principale():
    return render_template ('acceuil.html')
@app.route('/test')
def test():
    return render_template ('test.html')
@app.route('/Admin')
def admin():
    return render_template ('Admin.html')
@app.route('/acceuil')
def acceuil():
    return render_template ('acceuil.html')
if __name__ == '__main__':
    app.run(debug=True)