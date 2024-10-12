from fastapi import FastAPI, HTTPException, Query
import uvicorn

app = FastAPI()

envoiCouleur = ""
countdownResetEnvoiCouleur: int
countdownResetEnvoiArriveeRobot: int
GIJoesauves = 0
GIJoecaptures = 0
arriveeRobot23: bool

# Fonction pour le robot 1
# Envoie la couleur du GI Joe trouvé à l'API
@app.get("/api/data/receptionCouleurGIJoe")
def send_data_couleur(couleurGIJoe: str = Query(...)):
    global envoiCouleur
    global countdownResetEnvoiCouleur

    if(couleurGIJoe == "bleu"):
        print(f"Réception de l'info de la détection d'un G.I. Joe bleu de Robot 1")
        envoiCouleur = "bleu"
        countdownResetEnvoiCouleur = 1

    elif(couleurGIJoe == "rouge"):
        print(f"Réception de l'info de la détection d'un G.I. Joe rouge de Robot 1")
        envoiCouleur = "rouge"
        countdownResetEnvoiCouleur = 1

# Fonction pour le robot 1
# Récupère l'info de l'arrivée de Robot 2 ou Robot 3 à leur base respective
@app.post("/api/data/receptionArriveeRobot23")
def get_data_arrivee():
    global arriveeRobot23

    if(arriveeRobot23):
        print(f"Envoi de l'ordre de repartir à Robot 1")
        arriveeRobot23 = False
        return "OK"

# Fonction pour les robots 2 et 3
# Récupère la couleur du GI Joe depuis l'API
@app.post("/api/data/envoiCouleurGIJoe")
def get_data_couleur():
    global envoiCouleur
    global countdownResetEnvoiCouleur

    if(envoiCouleur == "bleu"):
        print(f"Envoi de l'info de la détection d'un G.I. Joe bleu aux Robots 2 et 3")

        if(countdownResetEnvoiCouleur > 0):
            countdownResetEnvoiCouleur = countdownResetEnvoiCouleur - 1
        else:
            envoiCouleur = ""
            countdownResetEnvoiCouleur = 1

        return "bleu"
    elif(envoiCouleur == "rouge"):
        print(f"Envoi de l'info de la détection d'un G.I. Joe rouge aux Robots 2 et 3")

        if(countdownResetEnvoiCouleur > 0):
            countdownResetEnvoiCouleur = countdownResetEnvoiCouleur - 1
        else:
            envoiCouleur = ""
            countdownResetEnvoiCouleur = 1

        return "rouge"
    else:
        print(f"envoiCouleur n'a pas la bonne valeur ou vide")

# Fonction pour les robots 2 et 3
# Indique qu'ils sont retournés à leur base avec le GI Joe
@app.get("/api/data/envoiArriveeRobot23")
def send_data_arrivee(idRobot: int = Query(...)):
    global arriveeRobot23
    global GIJoecaptures
    global GIJoesauves

    if(idRobot == 2):
        print(f"Réception de l'arrivée de Robot 2 à sa base")
        GIJoesauves = GIJoesauves + 1
    elif(idRobot == 3):
        print(f"Réception de l'arrivée de Robot 3 à sa base")
        GIJoecaptures = GIJoecaptures + 1
    arriveeRobot23 = True

# Fonction pour l'interface
# Renvoie le nombre de GI Joe capturés
@app.post("/api/data/receptionGIJoeCaptures")
def get_data_gijoe_captures():
    return GIJoecaptures

# Fonction pour l'interface
# Renvoie le nombre de GI Joe sauvés
@app.post("/api/data/receptionGIJoeSauves")
def get_data_gijoe_sauves():
    return GIJoesauves

# Fonction pour l'interface
# Réinitialise le nombre de Gi Joe sauvés et capturés
@app.get("/api/data/rebootNbGIJoe")
def reboot_nb_gi_joe():
    global GIJoecaptures
    global GIJoesauves
    GIJoecaptures = 0
    GIJoesauves = 0

# Fonction autres
# Réinitialise le couleur du GI Joe
@app.get("/api/data/rebootCouleurGIJoe")
def reboot_couleur_gi_joe():
    global envoiCouleur
    envoiCouleur = ""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)