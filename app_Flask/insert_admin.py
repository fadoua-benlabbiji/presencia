from werkzeug.security import generate_password_hash # type: ignore
from app import db, Admin, app
def ajouter_admin(username, mot_de_passe,email):
    with app.app_context():
        mot_de_passe_hash = generate_password_hash(mot_de_passe)
        admin = Admin(username=username, password=mot_de_passe_hash,email=email)
        db.session.add(admin)
        db.session.commit()
if __name__ == '__main__':
   username = input("Entrez le nom d'utilisateur : ")
   mot_de_passe = input("Entrez le mot de passe : ")
   email = input("Entrez l'email : ")
   ajouter_admin(username, mot_de_passe,email)