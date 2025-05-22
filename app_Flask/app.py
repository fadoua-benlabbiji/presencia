from datetime import datetime
import sys
import os #make_responce pour envoye des fichier a telecharger 
import pandas as pd #pour creation des tableau excel
from io import BytesIO # type: ignore #pour la cration du fichier excel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask,current_app, request, render_template, redirect,Response,jsonify, url_for, flash, session,make_response # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from werkzeug.security import check_password_hash # type: ignore
from werkzeug.utils import secure_filename
import random
import time
from flask_mail import Mail, Message # type: ignore
from recognition.Reco import encoding, systeme_Recognition,test_camera
import cv2 # type: ignore
app=Flask(__name__)
# Configuration Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'presenciaApp2025@gmail.com'         # ← Ton email
app.config['MAIL_PASSWORD'] = 'xfey cjkq wxvr nlke'   # ← Mot de passe ou mot de passe d'application 
mail = Mail(app)
app.secret_key = "cle_secrete"
# Connexion à MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/pfe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
camera=None
active=False
dernier_noms_detectes = []
# Modèle Admin
class Admin(db.Model):
    __tablename__ = 'admins'  # Nom de la table déjà existante
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(400), nullable=False)  # ← important
class Employes(db.Model):
    __tablename__='employes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    nom_complet = db.Column(db.String(200), nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    poste = db.Column(db.String(50), nullable=True)
    date_embauche = db.Column(db.Date, nullable=True)
    statut = db.Column(db.String(20), nullable=False, default='actif')
    photo = db.Column(db.String(255),default='profil.jpg')  # chemin ou nom de fichier image
def get_infos(nom):
    employe=Employes.query.filter_by(nom_complet=nom).first()
    if employe:
        return  {
            "matricule": employe.matricule,
            "prenom": employe.prenom,
            "nom": employe.nom,
            "poste": employe.poste,
        }
    else:
        return None
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
@app.route('/reconnaissance')
def reconnaissance():
    return render_template('reconnaissance.html')
@app.route('/start')
def start():
    global camera,active
    if not active:
        camera=cv2.VideoCapture(0)
        active=True    
    return redirect(url_for('reconnaissance'))
@app.route('/stop')
def stop():
    global camera, active
    if active and camera is not None:
        camera.release()
        active = False
    return   render_template('reconnaissance.html')
def reconnaissance_facial():
    global camera,active, dernier_noms_detectes
    known_encodings, known_names = encoding()  # type: ignore
    if not active:
        print("Erreur : Impossible d'ouvrir la caméra.")
        return
    while active:
        success, frame = camera.read()
        if not success or frame is None:
            print("Aucune frame capturée.")
            continue
        frame,nom_detecte = systeme_Recognition(frame, known_encodings, known_names)  # type: ignore
        dernier_noms_detectes = nom_detecte
        # Encodage JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Envoi du flux vidéo
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
       # Libération correcte de la caméra
def recon():
     # 0 pour la caméra par défaut

     while True:
        # Capture une image
        success, frame = cap.read()  
        if not success:
            break
        else:
            # Convertit l'image en format JPEG pour l'envoyer au navigateur
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Retourne l'image sous forme de flux
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

     cap.release()  # type: ignore # Libère la caméra lorsque terminé
@app.route('/video_feed')
def video_feed():
    return Response(recon(),mimetype='multipart/x-mixed-replace; boundary=frame')   
@app.route('/video')
def video():
    return Response( reconnaissance_facial(), mimetype='multipart/x-mixed-replace; boundary=frame')
   
@app.route('/Historique')
def Historique():
    return render_template('Historique.html')
@app.route('/oublier')
def oublier():
    return render_template('mot-de-passe.html')
@app.route('/verification-email', methods=['POST'])
def verifier():
    gmail = request.form['email'] #recuperation
    print(f"Email reçu : '{gmail}'")
    gmail = gmail.strip().lower()
    admins=Admin.query.all()
    exist= False
    for admin in admins:
        print("email de la base de donne",admin.email)
        if admin.email.strip().lower() == gmail:
            exist= True
            break
    if exist:
        print("Email trouvé dans la base de données")
        print(sendEmail(gmail))
        return redirect(url_for('envoie'))  # Redirige vers la page d'accueil
    else:
        print("Email non trouvé dans la base de données") # Message d'erreur
        return redirect(url_for('erreur'))
def generer_code():
    return str(random.randint(100000,999999))
@app.route('/erreur')
def erreur():
    return render_template('erreur.html')
@app.route('/test1')
def test1():
    return render_template('test1.html')
@app.route('/envoie')
def envoie():
    return render_template('login.html')
# Fonction pour envoyer un email
def sendEmail(destinataire):
    msg = Message(subject='Code de vérification pour la réinitialisation de mot de passe',
                  recipients=[destinataire], sender=('PRESENCIA','presenciApp2025@gmail.com'))
    msg.html ="""
       <p>Bonjour,<br>
       Vous avez demandé à réinitialiser votre mot de passe<br>
       Voici votre code de vérification : <strong>123456</strong><br>
       Veuillez ne pas le partager avec qui que ce soit.<br>
       Si vous n’êtes pas à l’origine de cette demande, vous pouvez ignorer cet e-mail en toute sécurité.<br>
       cordialement,<br>
       L’équipe PRESENCIA<p>
         """
   
    try:
        mail.send(msg)
        return 'Email envoyé avec succès !'
    except Exception as e:
        return f'Échec de l’envoi : {str(e)}'
@app.route('/Employes')
def employes():
    employes=Employes.query.all()
    return render_template('Employes.html',employes=employes)
@app.route('/supprimer/<matricule>', methods=['GET'])
def supprimer(matricule):
    emp = Employes.query.filter_by(matricule=matricule).first()
    if emp:
        db.session.delete(emp)
        db.session.commit()
    return redirect('/Employes')
@app.route('/editer/<matricule>', methods=['GET', 'POST'])
def editer_emp(matricule):
    # ton code ici
    pass
@app.route('/export_excel')
def export_excel():
    employes = Employes.query.all()
    data = []
    for emp in employes:
        data.append({
            'Matricule': emp.matricule,
            'Nom': emp.nom,
            'Prénom': emp.prenom,
            'Email': emp.email,
            'Téléphone': emp.telephone,
            'Poste': emp.poste,
            'Date Embauche': emp.date_embauche.strftime('%Y-%m-%d') if emp.date_embauche else '',
            'Statut': emp.statut
        })
    dataPandas=pd.DataFrame(data)
    # cration de fichier excel
    output=BytesIO()
    with pd.ExcelWriter(output,engine='openpyxl') as writer:
        dataPandas.to_excel(writer, index=False, sheet_name='Employes')
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=employes.xlsx'
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    return response
@app.route('/modifier_emp', methods=['POST'])
def modifier_emp():
    matricule = request.form['matricule']
    print("Matricule reçu :", matricule) 
    employe = Employes.query.filter_by(matricule=matricule).first()
    if employe:
        employe.nom = request.form['nom']
        employe.prenom = request.form['prenom']
        employe.email = request.form['email']
        employe.telephone = request.form['telephone']
        employe.poste = request.form['poste']
        employe.date_embauche = datetime.strptime(request.form['date_embauche'], '%Y-%m-%d')
        employe.statut = request.form['statut']
        photo = request.files.get('photo')
        if photo and photo.filename != '':
            # Sécuriser le nom de fichier
            filename = secure_filename(photo.filename)
            uniqfilename =employe.nom+"_"+employe.prenom+"_"+filename
            upload_path = os.path.join(current_app.root_path, 'static', 'images', uniqfilename)
            photo.save(upload_path)
            employe.photo = uniqfilename
        db.session.commit()
        return redirect(url_for('employes'))  # adapte selon ta route principale
    else:
        return "Employé non trouvé", 404
@app.route('/employe_infos')
def employe_infos():
    global dernier_noms_detectes
    if dernier_noms_detectes:
        nom = dernier_noms_detectes[0]
        print("Nom utilisé pour la recherche:", nom)
        infos = get_infos(nom)
        print("Infos trouvées:", infos)
        if infos and active:
            return jsonify(infos)
    return jsonify({"nom": "Inconnu", "prenom": "Inconnu", "matricule": "Inconnu", "poste": "Inconnu"})
if __name__ == '__main__':
 
    app.run(debug=True)