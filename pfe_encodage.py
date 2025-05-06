# Importation des bibliothèques nécessaires
import json
import face_recognition  # Pour la détection et la reconnaissance faciale
import cv2  # Pour la capture vidéo et l'affichage des images
import numpy as np  # Pour les opérations mathématiques (calcul des distances)
import os  # Pour parcourir les dossiers
personnes="Personnes"
encodings_dict={}
if not os.path.exists(personnes):
    print("Le dossier spécifié n'existe pas.")
else :
    for  personne in os.listdir(personnes):#parcous des sous dossier
         person_path = os.path.join(personnes, personne)#ecrire le chemin de chaque sous doss
         if os.path.isdir(person_path) :
             person_encodages=[]
             for image in os.listdir(person_path):
                image_path = os.path.join(person_path, image)
                #charger l image et extraire l encodage
                img = face_recognition.load_image_file(image_path)
                encoding=face_recognition.face_encodings(img)
                person_encodages.extend(encoding)
                # Afficher les encodages pour chaque image
               # for encoding in encoding:
                  #  print(f"Encodage du visage pour {personne}, image {image}: {encoding[:5]}...")  # Afficher les 5 premiers éléments
                if person_encodages:
                     mean_encoding = np.mean(person_encodages, axis=0)  # Moyenne des encodages
                     encodings_dict[personne] = mean_encoding.tolist()

             print(f"Vecteur moyen pour {personne} calculé.")
# Sauvegarder les encodages dans un fichier .json
Personnes_ENC = "encodings.json"
with open(Personnes_ENC, "w") as json_file:
    json.dump(encodings_dict, json_file)

print(f"Les encodages ont été sauvegardés dans {Personnes_ENC}")