def update_json_data():
    import json
    import face_recognition  # type: ignore
    import os

    base_dir = os.path.abspath(os.path.dirname(__file__))  # Dossier actuel
    personnes = os.path.join(base_dir, 'Personnes')
    json_path = os.path.join(base_dir, "encodages.json")

    # Charger les encodages déjà existants s'ils existent
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            try:
                encodings_dict = json.load(f)
            except json.JSONDecodeError:
                encodings_dict = {}
    else:
        encodings_dict = {}

    if not os.path.exists(personnes):
        print("Le dossier spécifié n'existe pas.")
        return

    for personne in os.listdir(personnes):
        person_path = os.path.join(personnes, personne)
        if os.path.isdir(person_path):
            person_encodages = []
            for image in os.listdir(person_path):
                image_path = os.path.join(person_path, image)
                img = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(img, model="cnn")
                person_encodages.extend(encoding)

            if person_encodages:
                liste_encodages = [enc.tolist() for enc in person_encodages]

                # Ajouter ou mettre à jour les encodages existants sans écraser
                if personne in encodings_dict:
                    encodings_dict[personne].extend(liste_encodages)
                else:
                    encodings_dict[personne] = liste_encodages
            else:
                print(f"Aucun encodage valide pour {personne}, dossier ignoré.")

    # Sauvegarder les encodages mis à jour dans le fichier JSON
    print(f"Écriture dans le fichier : {json_path}")
    with open(json_path, "w") as json_file:
        json.dump(encodings_dict, json_file, indent=4)
    print(f"Les encodages ont été sauvegardés dans {json_path}")
