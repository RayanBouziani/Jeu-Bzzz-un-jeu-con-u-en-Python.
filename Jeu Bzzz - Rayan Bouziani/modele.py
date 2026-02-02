import random

NCASES = 16
NFLEURS = 4
NECTAR_INITIAL = 10
MAX_NECTAR = 45
TIME_OUT = 300
COUT_PONTE = 5
TIME_KO = 5

H = 1000
L = 800
PAS = 800 // 16

def creer_grille():
    """
    Initialise la grille de jeu vide avec les ruches dans les coins.

    Paramètres:
        Aucun.

    Retourne:
        list: Une matrice 16x16 représentant le plateau ('R' pour ruche, ' ' pour vide).
    """
    g = [[' ' for _ in range(NCASES)] for _ in range(NCASES)]
    g[0][0] = 'R'
    g[0][NCASES-1] = 'R'
    g[NCASES-1][0] = 'R'
    g[NCASES-1][NCASES-1] = 'R'
    return g

def generateur_fleurs(grille):
    """
    Place les fleurs aléatoirement sur la grille de manière symétrique.

    Paramètres:
        grille (list): La matrice du plateau de jeu.
    Retourne:
        list: La grille modifiée avec les dictionnaires de fleurs.
    """
    cases_dispo_fleurs = []
    for i in range(8):
        for j in range(8):
            cases_dispo_fleurs.append((i,j))
    for i in range(4):
        for j in range(4):
            cases_dispo_fleurs.remove((i,j))
    fleurs = []
    liste_temporaire1 = []
    liste_temporaire2 = []
    for _ in range(4):
        pos_fleur = random.choice(cases_dispo_fleurs)
        cases_dispo_fleurs.remove(pos_fleur)
        fleurs.append([pos_fleur,random.randint(1, MAX_NECTAR)])
    for f in fleurs:
        liste_temporaire1.append([(15-f[0][0],f[0][1]),f[1]])
    for f in liste_temporaire1:
        fleurs.append(f)
    for f in fleurs:
        liste_temporaire2.append([(f[0][0],15-f[0][1]),f[1]])
    for f in liste_temporaire2:
        fleurs.append(f)
    for f in fleurs:
        grille[f[0][0]][f[0][1]] = {"type": 'F', 'nectar': f[1]}
    return grille

def listes_fond():
    """
    Calcule les listes de cases pour l'herbe et les territoires colorés.

    Paramètres:
        Aucun.

    Retourne:
        list : Une liste contenant cinq listes de tuples (x, y) pour l'herbe et les territoires.
    """
    cases_herbe=[]
    territoire_orange=[]
    territoire_bleu=[]
    territoire_rouge=[]
    territoire_jaune=[]
    for i in range(0,16):
        for j in range(0,16):
            cases_herbe.append((i,j))
    for i in range(0,4):
        for j in range(0,4):
            cases_herbe.remove((i,j))
        for j in range(12,15):
            cases_herbe.remove((i,j))
    for i in range(12,15):
        for j in range(0,4):
            cases_herbe.remove((i,j))
        for j in range(12,15):
            cases_herbe.remove((i,j))
    for i in range(0,4):
        for j in range(0,4):
            territoire_bleu.append((i,j))
    for i in range(0,4):
        for j in range(12,16):
            territoire_jaune.append((i,j))
    for i in range(12,16):
        for j in range(0,4):
            territoire_orange.append((i,j))
    for i in range(12,16):
        for j in range(12,16):
            territoire_rouge.append((i,j))
    return [cases_herbe,territoire_bleu,territoire_orange,territoire_rouge,territoire_jaune]

def case_interdites(joueur):
    """
    Calcule la liste des cases appartenant aux territoires des bases adverses.

    Paramètres:
        joueur (int): Le numéro du joueur (1 à 4).

    Retourne:
        list: Une liste de tuples (x, y) correspondant aux cases interdites pour ce joueur.
    """
    l=[]
    for i in range(4):
        if joueur != 1:
            for j in range(4):
                l.append((i,j))
        if joueur != 4:
            for j in range(12,16):
                l.append((i,j))
    for i in range(12,16):
        if joueur != 2:
            for j in range(4):
                l.append((i,j))
        if joueur != 3:
            for j in range(12,16):
                l.append((i,j))
    return l

def spawn_abeille(joueur,type_abeille,jeu):
    """
    Crée une abeille dans la ruche du joueur si le stock et l'espace le permettent.

    Paramètres:
        joueur (int): Le numéro du joueur.
        type_abeille (str): Le type de l'abeille souhaitée ('ouvriere', 'eclaireuse', 'bourdon').
        jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None: Modifie le dictionnaire jeu en place.
    """
    for j in range(1,5):
        for abeille in jeu["joueurs"][j]["abeilles"]:
            if abeille["pos"] == jeu["joueurs"][joueur]["ruche"]:
                return
    if jeu["joueurs"][joueur]["stock"] >= COUT_PONTE:
        jeu["joueurs"][joueur]["stock"] -= COUT_PONTE
        jeu["joueurs"][joueur]["abeilles"].append({"pos": jeu["joueurs"][joueur]["ruche"], 
                                                   "type": type_abeille, 
                                                   "etat": "ok",
                                                   "temps_ko": 0, 
                                                   "nectar": 0 })

def deplacer_abeille(joueur, pos, nouv_pos, jeu):
    """
    Déplace une abeille vers une nouvelle position si le mouvement est valide.

    Paramètres:
        joueur (int): Le numéro du joueur.
        pos (tuple): La position actuelle (x, y).
        nouv_pos (tuple): La position cible (x, y).
        jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None: Modifie la position de l'abeille dans jeu si valide.
    """
    deplacement = True
    if nouv_pos in case_interdites(joueur):
        deplacement = False
    for j in jeu["joueurs"]:
        for abeille in jeu["joueurs"][j]["abeilles"]:
            if abeille["pos"] == nouv_pos:
                deplacement = False
    for abeille in jeu["joueurs"][joueur]["abeilles"]:
        if abeille["pos"] == pos:
            if abeille["etat"] == "ko":
                deplacement = False
    if abs(nouv_pos[0]-pos[0]) > 1 or abs(nouv_pos[1]-pos[1]) > 1:
        deplacement = False 
    for abeille in jeu["joueurs"][joueur]["abeilles"]:
        if abeille["pos"] == pos:
            if abeille["type"] == "bourdon" or abeille["type"] == "ouvriere":
                if nouv_pos[0]-pos[0] != 0 and nouv_pos[1]-pos[1] != 0:
                    deplacement = False
    if deplacement:
        for abeille in jeu["joueurs"][joueur]["abeilles"]:
            if abeille["pos"] == pos:
                abeille["pos"] = nouv_pos



def decharger_nectar(joueur,pos_abeille,jeu):
    """
    Transfère le nectar de l'abeille vers le stock du joueur si elle est dans la zone 4x4 de la ruche.

    Paramètres:
        joueur (int): Le numéro du joueur.
        pos_abeille (tuple): La position de l'abeille.
        jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None: Met à jour le stock du joueur et vide le nectar de l'abeille.
    """
    if abs(pos_abeille[0]-jeu["joueurs"][joueur]["ruche"][0]) <= 3 and abs(pos_abeille[1]-jeu["joueurs"][joueur]["ruche"][1]) <= 3:
        for abeille in jeu["joueurs"][joueur]["abeilles"]:
            if abeille["pos"] == pos_abeille:
                jeu["joueurs"][joueur]["stock"] += abeille["nectar"]
                abeille["nectar"] = 0

def butiner(joueur, pos_abeille, pos_fleur, jeu):
    """
    Récolte le nectar d'une fleur vers une abeille selon les capacités de stockage et le type d'abeille.

    Paramètres:
        joueur (int): Le numéro du joueur.
        pos_abeille (tuple): La position de l'abeille.
        pos_fleur (tuple): La position de la fleur.
        jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None: Modifie la quantité de nectar de la fleur et de l'abeille.
    """
    if jeu["grille"][pos_fleur[0]][pos_fleur[1]]["nectar"] > 0:
        for abeille in jeu["joueurs"][joueur]["abeilles"]:
            if abeille["pos"] == pos_abeille:
                if abeille["etat"] == "ok":
                    if abs(pos_fleur[0]-pos_abeille[0]) <= 1 and abs(pos_fleur[1]-pos_abeille[1]) <= 1:
                        if type(jeu["grille"][pos_fleur[0]][pos_fleur[1]]) == dict:
                            if jeu["grille"][pos_fleur[0]][pos_fleur[1]]["nectar"] >= 2/3*MAX_NECTAR:
                                nectar_recolte = min(3,MAX_NECTAR)
                            elif jeu["grille"][pos_fleur[0]][pos_fleur[1]]["nectar"] >= 1/3*MAX_NECTAR and jeu["grille"][pos_fleur[0]][pos_fleur[1]]["nectar"] < 2/3*MAX_NECTAR:
                                nectar_recolte = min(2,MAX_NECTAR)
                            elif jeu["grille"][pos_fleur[0]][pos_fleur[1]]["nectar"] < 1/3*MAX_NECTAR and jeu["grille"][pos_fleur[0]][pos_fleur[1]]["nectar"] > 0:
                                nectar_recolte = 1
                            abeille["nectar"] += nectar_recolte
                            if abeille["type"] == "ouvriere" and abeille["nectar"] > 12:
                                abeille["nectar"] = 12
                            elif abeille["type"] == "eclaireuse" and abeille["nectar"] > 3:
                                abeille["nectar"] = 3
                            elif abeille["type"] == "bourdon" and abeille["nectar"] > 1:
                                abeille["nectar"] = 1
                            jeu["grille"][pos_fleur[0]][pos_fleur[1]]["nectar"] -= nectar_recolte

def compter_nectar(jeu):
    """
    Calcule la quantité totale de nectar restant en jeu (fleurs + abeilles).

    Paramètres:
        jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        int: La somme totale du nectar sur le plateau.
    """
    s=0
    for i in range(NCASES):
        for j in range(NCASES):
            if type(jeu["grille"][i][j]) == dict:
                s+=jeu["grille"][i][j]["nectar"]
    for j in jeu["joueurs"]:
        for abeille in jeu["joueurs"][j]["abeilles"]:
            s+=abeille["nectar"]
    return s

def continu_partie(jeu,joueur,nectartotal):
    """
    Vérifie si la partie doit continuer ou s'arrêter (Blitzkrieg, Timeout, Nectar épuisé).

    Paramètres:
        jeu (dict): Le dictionnaire principal du jeu.
        joueur (int): Le numéro du joueur.
        nectartotal (int): Le nectar total initialement présent (pour calcul majorité).

    Retourne:
        bool: True si la partie continue, False si elle est finie.
    """
    if compter_nectar(jeu)==0:
        return False
    elif jeu["joueurs"][joueur]["stock"] > nectartotal//2:
        return False
    elif jeu["tour"] == TIME_OUT:
        return False
    return True

def liste_surbrillance_cases(jeu,pos,joueur):
    """
    Calcule les cases accessibles ou qui peuvent être butinées pour une abeille donnée.

    Paramètres:
        jeu (dict): Le dictionnaire principal du jeu.
        pos (tuple): La position de l'abeille (x, y).
        joueur (int): Le numéro du joueur.

    Retourne:
        list: Une liste de tuples (x, y) des cases où le déplacement est possible.
    """
    bonne = []
    for i in range(pos[0]-1,pos[0]+2):
        for j in range(pos[1]-1,pos[1]+2):
            if 0 <= i <= 15 and 0 <= j <= 15:
                bonne.append((i,j))
    for abeille in jeu["joueurs"][joueur]["abeilles"]:
        if abeille["pos"] == pos:
            if abeille["type"] != "eclaireuse":
                if pos[0]>0 and pos[1]>0 and type(jeu["grille"][pos[0]-1][pos[1]-1]) != dict:
                    bonne.remove((pos[0]-1,pos[1]-1))
                if pos[0]>0 and pos[1]<15 and type(jeu["grille"][pos[0]-1][pos[1]+1]) != dict:
                    bonne.remove((pos[0]-1,pos[1]+1))
                if pos[0]<15 and pos[1]<15 and type(jeu["grille"][pos[0]+1][pos[1]+1]) != dict:
                    bonne.remove((pos[0]+1,pos[1]+1))
                if pos[0]<15 and pos[1]>0 and type(jeu["grille"][pos[0]+1][pos[1]-1]) != dict:
                    bonne.remove((pos[0]+1,pos[1]-1))
    for n_joueur in range(1,5):
        for abeille in jeu["joueurs"][n_joueur]["abeilles"]:
            if abeille["pos"] in bonne and type(jeu["grille"][abeille["pos"][0]][abeille["pos"][1]]) != dict:
                bonne.remove(abeille["pos"])
    l_cases_interdites = case_interdites(joueur) 
    for t in l_cases_interdites:
        if t in bonne:
            bonne.remove(t)
    return bonne

def gagnant(jeu,num_joueur,nb_total_nectar):
    """
    Détermine le ou les gagnants et le type de victoire.

    Paramètres:
        jeu (dict): Le dictionnaire principal du jeu.
        num_joueur (int): Le numéro du joueur qui vient de jouer.
        nb_total_nectar (int): Le nectar total de référence.

    Retourne:
        tuple: ([liste_gagnants], "type_victoire", nb_gagnants).
    """
    if jeu["joueurs"][num_joueur]["stock"] > nb_total_nectar//2:
        rep = [num_joueur]
        nb_gagnants = 1
        type_v = "Blitzkrieg"
    else:
        rep = []
        type_v = "plus de nectar"
        max_nectar = 0
        for j in range(1,5):
            if jeu["joueurs"][j]["stock"] > max_nectar :
                rep = [j]
                max_nectar = jeu["joueurs"][j]["stock"]
            elif jeu["joueurs"][j]["stock"] == max_nectar :
                rep.append(j)
        nb_gagnants = len(rep)
    return (rep,type_v,nb_gagnants)

def init_escarmouches(joueur,jeu):
    """
    Repère les abeilles en situation de combat (adjacentes à des ennemis).

    Paramètres:
        joueur (int): Le numéro du joueur.
        jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        dict: Un dictionnaire liant chaque abeille à ses adversaires directs.
    """
    escarmouches = {}
    for abeille in jeu["joueurs"][joueur]["abeilles"]:
        if abeille["etat"] == "ok":
            escarmouches[(joueur,abeille["pos"])] = []
            for j in jeu["joueurs"]:
                if j != joueur:
                    for abeille_adverse in jeu["joueurs"][j]["abeilles"]:
                        if abs(abeille_adverse["pos"][0]-abeille["pos"][0]) <= 1 and abs(abeille_adverse["pos"][1]-abeille["pos"][1]) <= 1 and abeille_adverse["etat"] == "ok":
                            escarmouches[(joueur,abeille["pos"])].append((j,abeille_adverse["pos"]))
    abeilles_opps = []
    for cle in escarmouches:
        for abeille in escarmouches[cle]:
            if abeille not in abeilles_opps:
                abeilles_opps.append(abeille)
    for abeille_ennemi in abeilles_opps:
        escarmouches[abeille_ennemi] = []
        for abeille in jeu["joueurs"][joueur]["abeilles"]:
            if abs(abeille_ennemi[1][0]-abeille["pos"][0]) <= 1 and abs(abeille_ennemi[1][1]-abeille["pos"][1]) <= 1 and abeille["etat"] == "ok":
                escarmouches[abeille_ennemi].append((joueur,abeille["pos"]))
    supp_cles = []
    for cle in escarmouches:
        if escarmouches[cle] == []:
            supp_cles.append(cle)
    for cle in supp_cles:
        escarmouches.pop(cle)
    return escarmouches

def forces_effectives(escarmouches, jeu):
    """
    Calcule la force effective de chaque abeille impliquée dans une escarmouche.

    Paramètres:
        escarmouches (dict): Le dictionnaire des combats en cours.
        jeu (dict): Le dictionnaire principal du jeu.
    Retourne:
        dict: Le dictionnaire escarmouches enrichi avec les valeurs de force.
    """
    l = []
    for abeille in escarmouches:
        for abeilles_joueur in jeu["joueurs"][abeille[0]]["abeilles"]:
            if abeilles_joueur["pos"] == abeille[1]:
                if abeilles_joueur["type"] == "eclaireuse" or abeilles_joueur["type"] == "ouvriere":
                    force_abeille = 1
                else:
                    force_abeille = 5
                force_effective = force_abeille / len(escarmouches[abeille])
                
        l.append((abeille+(str(force_abeille),str(force_effective)),abeille))
    for e in l:
        escarmouches[e[0]] = escarmouches.pop(e[1])
    for lst in escarmouches.values():
        for i in range(len(lst)):
            abeille_test = lst[i]
            for cle in escarmouches:
                if abeille_test[1] == cle[1]:
                    lst[i] = abeille_test + (cle[2], cle[3])
                    break
    return escarmouches

def escarmouches(escarmouches, jeu):
    """
    Résout les combats aléatoirement selon les probabilités calculées.

    Paramètres:
        escarmouches (dict): Le dictionnaire des combats avec forces.
        jeu (dict): Le dictionnaire principal du jeu.
    Retourne:
        None: Modifie l'état des abeilles perdantes en "ko" ainsi que leur stock de nectar et leur nombre de tours ko.
    """
    for abeille in escarmouches:
        somme_forces_effectives_opposees = 0
        for abeille_opposee in escarmouches[abeille]:
            somme_forces_effectives_opposees += float(abeille_opposee[3])
        proba_esquive = float(abeille[2]) / (float(abeille[2]) + somme_forces_effectives_opposees)
        nb = random.random()
        if nb > proba_esquive:
            for abeilles_joueur in jeu["joueurs"][abeille[0]]["abeilles"]:
                if abeilles_joueur["pos"] == abeille[1]:
                    abeilles_joueur["etat"] = "ko"
                    abeilles_joueur["temps_ko"] = TIME_KO*4 #*2 , pour le jour de la soutenance
                    abeilles_joueur["nectar"] = 0

def gestion_combats(num_joueur, jeu):
    """
    Orchestre toute la logique de combat à la fin d'un tour.

    Paramètres:
        num_joueur (int): Le numéro du joueur qui vient de finir son tour.
        jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None: Modifie les données des abeilles ko.
    """
    escar_init = init_escarmouches(num_joueur, jeu)
    forces = forces_effectives(escar_init, jeu)
    escarmouches(forces, jeu)

def enlever_ko(jeu):
    """
    Décrémente le temps de KO des abeilles et les réactive si le temps est écoulé.

    Paramètres:
        jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None: Modifie l'état "ko" -> "ok" si l'abeille a fini son temps de ko.
    """
    for joueur in jeu["joueurs"]:
        for abeille in jeu["joueurs"][joueur]["abeilles"]:
            if abeille["etat"] == "ko":
                abeille["temps_ko"] -= 1
                if abeille["temps_ko"] < 0:
                    abeille["etat"] = "ok"
                    abeille["temps_ko"] = 0

def init_jeu():
    """
    Initialise toute la structure de données pour une nouvelle partie.

    Paramètres:
        Aucun.

    Retourne:
        dict: Le dictionnaire 'jeu' complet contenant grille, tour et joueurs.
    """
    jeu = {
        "grille": generateur_fleurs(creer_grille()),
        "tour": 0,
        "joueurs": {
            1: {"stock": NECTAR_INITIAL, "ruche": (0, 0), "abeilles": []},
            2: {"stock": NECTAR_INITIAL, "ruche": (NCASES-1, 0), "abeilles": []},
            3: {"stock": NECTAR_INITIAL, "ruche": (NCASES-1, NCASES-1), "abeilles": []},
            4: {"stock": NECTAR_INITIAL, "ruche": (0, NCASES-1), "abeilles": []}
        }
    }
    return jeu