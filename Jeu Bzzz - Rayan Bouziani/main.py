import tkiteasy
import modele


def fond(g,liste):
    """
    Dessine le terrain de jeu (herbe, territoires colorés des bases et ruches).

    Paramètres:
        g (objet): La fenêtre graphique tkiteasy.
    
    Retourne:
        None.
    """
    for i in liste[0]:
        g.afficherImage(i[0]*modele.PAS,i[1]*modele.PAS,"images/terre.png")
    for i in liste[1]:
        g.afficherImage(i[0]*modele.PAS,i[1]*modele.PAS,"images/terrebleu.png")
    for i in liste[2]:
        g.afficherImage(i[0]*modele.PAS,i[1]*modele.PAS,"images/terreorange.png")
    for i in liste[3]:
        g.afficherImage(i[0]*modele.PAS,i[1]*modele.PAS,"images/terrerouge.png")
    for i in liste[4]:
        g.afficherImage(i[0]*modele.PAS,i[1]*modele.PAS,"images/terreblanche.png")

    g.afficherImage(0,15*modele.PAS,"images/rucheblanche.png")
    g.afficherImage(15*modele.PAS,15*modele.PAS,"images/rucherouge.png")
    g.afficherImage(15*modele.PAS,0,"images/rucheorange.png")
    g.afficherImage(0,0,"images/ruchebleu.png")

def afficher_ligne(g):
    """
    Trace le quadrillage noir par-dessus le terrain.

    Paramètres:
        g (objet): La fenêtre graphique.

    Retourne:
        None.
    """
    for x in range(0,modele.L,modele.PAS):
        g.dessinerLigne(x,0,x,modele.H-200,'black')

    for y in range(0,modele.H-200+1,modele.PAS):
        g.dessinerLigne(0,y,modele.L,y,'black')

def afficher_fleurs(g,grille):
    """
    Affiche les images des fleurs sur la grille.

    Paramètres:
        g (objet): La fenêtre graphique.
        grille (list): La matrice du jeu contenant les infos des fleurs.

    Retourne:
        None.
    """
    for i in range(modele.NCASES):
        for j in range(modele.NCASES):
            if type(grille[i][j])==dict:
                g.afficherImage(i*modele.PAS,j*modele.PAS,"images/fleur.png")

def afficher_abeilles(g,dict_jeu,joueur):
    """
    Affiche les abeilles d'un joueur spécifique avec la bonne couleur et état ko.

    Paramètres:
        g (objet): La fenêtre graphique.
        dict_jeu (dict): Le dictionnaire principal du jeu.
        joueur (int): Le numéro du joueur à afficher.

    Retourne:
        None.
    """
    if joueur==1:
        couleur='bleu.png'
    elif joueur==2:
        couleur='orange.png'
    elif joueur==3:
        couleur='rouge.png'
    else:
        couleur='blanc.png'
    for a in dict_jeu["joueurs"][joueur]["abeilles"]:
        if a["type"]=='bourdon':
            g.afficherImage(a["pos"][0]*modele.PAS,a["pos"][1]*modele.PAS,"images/bourdon"+couleur)
        elif a["type"]=='eclaireuse':
            g.afficherImage(a["pos"][0]*modele.PAS,a["pos"][1]*modele.PAS,"images/eclaireuse"+couleur)
        else:
            g.afficherImage(a["pos"][0]*modele.PAS,a["pos"][1]*modele.PAS,"images/ouvriere"+couleur)
        if a["etat"]=="ko":
            g.afficherImage(a["pos"][0]*modele.PAS+1,a["pos"][1]*modele.PAS+1,"images/ko.png")

def nettoyage(g):
    """
    Efface tout le contenu de la fenêtre graphique.

    Paramètres:
        g (objet): La fenêtre graphique.

    Retourne:
        None.
    """
    g.delete("all")

def surbrillance(g,l):
    """
    Affiche un cadre de surbrillance sur les cases listées.

    Paramètres:
        g (objet): La fenêtre graphique.
        l (list): Liste de tuples (x, y) des cases à surligner.

    Retourne:
        None.
    """
    for e in l:
        g.afficherImage(e[0]*modele.PAS+1,e[1]*modele.PAS+1,"images/surbrillance.png")

def menu_choix_abeille(g,joueur,donnees_jeu):
    """
    Dessine le menu d'achat d'abeilles (ouvrière, bourdon, éclaireuse).

    Paramètres:
        g (objet): La fenêtre graphique.
        joueur (int): Le numéro du joueur.

    Retourne:
        None.
    """
    g.dessinerRectangle(145,245,510,310,'black')
    g.dessinerRectangle(150,250,500,300,'white')
    g.afficherTexte(f"Joueur {joueur} choisissez votre Abeille !",modele.L//2,290,'black',20)
    g.afficherTexte("Coût : 5 nectars",modele.L//2,335,"black",17)
    g.dessinerRectangle(185,380,120,120,'lightgrey')
    g.afficherImage(185,380,"images/ouvriere_choix.png")
    g.dessinerRectangle(340,380,120,120,'lightgrey')
    g.afficherImage(340,380,"images/bourdon_choix.png")
    g.dessinerRectangle(495,380,120,120,'lightgrey')
    g.afficherImage(495,380,"images/eclaireuse_choix.png")
    if donnees_jeu["tour"]!=0:
        g.dessinerRectangle(605,505,40,40,'lightgrey')
        g.afficherImage(610,510,"images/petite_croix.png")

def choix_abeille(g,joueur,abeilles_a_jouer,donnees_jeu):
    """
    Gère l'interaction (clic) dans le menu d'achat d'abeille.

    Paramètres:
        g (objet): La fenêtre graphique.
        joueur (int): Le numéro du joueur.
        abeilles_a_jouer (list): Liste des abeilles actives ce tour.
        donnees_jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        str: "rejouer" si annulation, sinon None (modifie le jeu).
    """
    choixabeille="vide"
    while choixabeille=="vide":
        clickchoix = g.attendreClic()
        xchoix = clickchoix.x
        ychoix = clickchoix.y
        if 185<=xchoix<=305 and 380<=ychoix<=500:
            choixabeille="ouvriere"
        elif 340<=xchoix<=460 and 380<=ychoix<=500:
            choixabeille="bourdon"
        elif 495<=xchoix<=615 and 380<=ychoix<=500:
            choixabeille="eclaireuse"
        elif 605<=xchoix<=645 and 505<=ychoix<=545 and donnees_jeu["tour"]!=0:
            choixabeille="retour"
    if choixabeille == "retour":
        return "rejouer"
    modele.spawn_abeille(joueur,choixabeille,donnees_jeu)
    abeilles_a_jouer.append(donnees_jeu["joueurs"][joueur]["abeilles"][-1]["pos"])

def menu_butiner_ou_marcher(g):
    """
    Affiche le menu demandant l'action (fleur ou déplacement).

    Paramètres:
        g (objet): La fenêtre graphique.

    Retourne:
        None.
    """
    g.dessinerRectangle(145,205,510,270,'black')
    g.dessinerRectangle(150,210,500,260,'white')
    g.afficherTexte("Voulez-vous butiner ou vous déplacer ?",modele.L//2,250,'black',20)
    g.dessinerRectangle(260,310,120,120,'lightgrey')
    g.afficherImage(265,315,"images/butiner.png")
    g.dessinerRectangle(420,310,120,120,'lightgrey')
    g.afficherImage(425,315,"images/marcher.png")
    g.dessinerRectangle(575,395,60,60,'lightgrey')
    g.afficherImage(580,400,"images/croix.png")


def menu_gagnant(g,donnees_jeu,joueurs,type_v,nb_gagnants):
    """
    Affiche l'écran de fin de partie avec le(s) vainqueur(s).

    Paramètres:
        g (objet): La fenêtre graphique.
        donnees_jeu (dict): Le dictionnaire principal du jeu.
        joueurs (list): Liste des numéros des gagnants.
        type_v (str): Type de victoire (Blitzkrieg ou Nectar).
        nb_gagnants (int): Nombre de gagnants.

    Retourne:
        None.
    """
    g.dessinerRectangle(145,205,510,270,'black')
    g.dessinerRectangle(150,210,500,260,'white')
    if nb_gagnants == 1:
        g.afficherTexte(f"VICTOIRE du joueur {joueurs[0]} !",modele.L//2,250,'black',25)
        g.afficherTexte(f"Victoire par {type_v}",modele.L//2,290,'black',20)
        g.afficherTexte(f"Victoire avec {donnees_jeu["joueurs"][joueurs[0]]["stock"]} points de nectar",modele.L//2,330,'black',20)
    else:
        joueurs_gagnants = str(joueurs[0]) + " "
        for j in joueurs[1:]:
            joueurs_gagnants += f"et {j} "
        g.afficherTexte(f"VICTOIRE des joueurs :",modele.L//2,250,'black',25)
        g.afficherTexte(joueurs_gagnants,modele.L//2,290,'black',25)
        g.afficherTexte(f"Victoire par {type_v}",modele.L//2,330,'black',20)

def choix_butiner_ou_marcher(g):
    """
    Récupère le choix de l'utilisateur dans le menu.

    Paramètres:
        g (objet): La fenêtre graphique.

    Retourne:
        str: 'butiner', 'marcher' ou 'retour'.
    """
    choix="vide"
    while choix=="vide":
        clickchoix = g.attendreClic()
        xchoix = clickchoix.x
        ychoix = clickchoix.y
        if 260<=xchoix<=380 and 310<=ychoix<=430:
            choix="butiner"
        elif 420<=xchoix<=540 and 310<=ychoix<=430:
            choix="marcher"
        elif 575<=xchoix<=635 and 395<=ychoix<=455:
            choix="retour"
    return choix

def afficher_menu_joueur(g,joueur,pos_abeille,donnees_jeu):
    """
    Affiche le menu du joueur en bas : données, tour, bouton fin.

    Paramètres:
        g (objet): La fenêtre graphique.
        joueur (int): Le numéro du joueur.
        pos_abeille (tuple/str): Position de l'abeille sélectionnée ou "aucune".
        donnees_jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None.
    """
    if joueur == 1:
        couleur1 = "LightBlue"
        couleur2 = "blue"
    elif joueur == 2:
        couleur1 = "yellow"
        couleur2 = "DarkOrange3"
    elif joueur == 3:
        couleur1 = "red"
        couleur2 = "black"
    else:
        couleur1 = "LightGrey"
        couleur2 = "grey"
    g.dessinerRectangle(0,modele.H-199,modele.L,199,couleur1)
    g.dessinerRectangle(0,modele.H-199,modele.L,5,couleur2)
    g.dessinerRectangle(modele.L//2-2,modele.H-199,5,199,couleur2)
    g.afficherTexte(f"Joueur {joueur}",200,modele.H-175,couleur2,20)
    g.afficherTexte(f"Stock ruche : {donnees_jeu['joueurs'][joueur]['stock']}",200,modele.H-130,couleur2,18)
    g.afficherTexte(f"Abeille controlée : {pos_abeille}",modele.L-200,modele.H-175,couleur2,20)
    g.afficherTexte(f"Nombre d'abeilles : {len(donnees_jeu['joueurs'][joueur]['abeilles'])}",200,modele.H-90,couleur2,18)
    g.dessinerRectangle(modele.L//2-60,modele.H-55,120,50,couleur2)
    g.dessinerRectangle(modele.L//2-55,modele.H-50,110,40,couleur1)
    g.afficherTexte(f"Tour : {donnees_jeu['tour']}",modele.L//2,modele.H-30,couleur2,18)
    g.dessinerRectangle(modele.L-155,modele.H-55,150,50,couleur2)
    g.dessinerRectangle(modele.L-150,modele.H-50,140,40,couleur1)
    g.afficherTexte(f"Fin de Tour",modele.L-80,modele.H-30,couleur2,18)
    if pos_abeille != "aucune":
        for abeille in donnees_jeu['joueurs'][joueur]['abeilles']:
            if pos_abeille == abeille['pos']:
                g.afficherTexte(f"Type d'abeille : {abeille["type"]}",modele.L-200,modele.H-130,couleur2,18)
                g.afficherTexte(f"Nectar récolté : {abeille["nectar"]}",modele.L-200,modele.H-90,couleur2,18)

def refresh_graphique(g,num_joueur,donnees_jeu):
    """
    Redessine entièrement l'écran (fond, grilles, fleurs, abeilles, menu du joueur).

    Paramètres:
        g (objet): La fenêtre graphique.
        num_joueur (int): Le numéro du joueur.
        donnees_jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None.
    """
    g.delete("all")
    fond(g, modele.listes_fond())
    afficher_menu_joueur(g,num_joueur, "aucune", donnees_jeu)
    afficher_fleurs(g,donnees_jeu["grille"])
    afficher_ligne(g)
    for j in range(1, 5):
        afficher_abeilles(g,donnees_jeu, j)

def traiter_spawn(g, num_joueur, case_clic, donnees_jeu, abeilles_a_jouer):
    """
    Gère la logique d'apparition d'une nouvelle abeille (clic ruche + menu).

    Paramètres:
        g (objet): La fenêtre graphique.
        num_joueur (int): Le numéro du joueur.
        case_clic (tuple): Les coordonnées du clic.
        donnees_jeu (dict): Le dictionnaire principal du jeu.
        abeilles_a_jouer (list): Liste de suivi des abeilles actives et qui n'ont pas encore joué.

    Retourne:
        bool: True si un spawn a eu lieu, False sinon.
    """
    if case_clic != donnees_jeu["joueurs"][num_joueur]["ruche"]:
        return False
    
    if donnees_jeu["joueurs"][num_joueur]["stock"] < 5:
        return False
    
    for a in donnees_jeu["joueurs"][num_joueur]["abeilles"]:
        if a["pos"] == case_clic:
            return False

    menu_choix_abeille(g, num_joueur,donnees_jeu)
    res = choix_abeille(g, num_joueur, abeilles_a_jouer, donnees_jeu)
    if res == "rejouer":
        
        refresh_graphique(g, num_joueur, donnees_jeu)
        return False
    return True

def action_fleur_ou_mouvement(g, num_joueur, abeille, pos_cible, donnees_jeu):
    """
    Gère le choix entre butiner une fleur et se déplacer dessus.

    Paramètres:
        g (objet): La fenêtre graphique.
        num_joueur (int): Le numéro du joueur.
        abeille (dict): L'abeille sélectionnée.
        pos_cible (tuple): La case visée.
        donnees_jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        bool: True si une action a été effectuée, False sinon.
    """
    menu_butiner_ou_marcher(g)
    choix = choix_butiner_ou_marcher(g)
    
    action_faite = False
    if choix == 'butiner':
        modele.butiner(num_joueur, abeille["pos"], pos_cible, donnees_jeu)
        action_faite = True
    elif choix == 'marcher':
        
        if abeille["type"] == "eclaireuse" or (abs(pos_cible[0]-abeille["pos"][0]) + abs(pos_cible[1]-abeille["pos"][1]) == 1):
            for joueur in range(1, 5):
                for a in donnees_jeu["joueurs"][joueur]["abeilles"]:
                    if a["pos"] == pos_cible:
                        return False
            modele.deplacer_abeille(num_joueur, abeille["pos"], pos_cible, donnees_jeu)
            action_faite = True
    
    return action_faite

def traiter_action_abeille(g, num_joueur, abeille, donnees_jeu):
    """
    Gère le second clic après avoir sélectionné une abeille (déplacement/action).

    Paramètres:
        g (objet): La fenêtre graphique.
        num_joueur (int): Le numéro du joueur.
        abeille (dict): L'abeille sélectionnée.
        donnees_jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        str: "fin_tour", "action_faite" ou "rien".
    """
    afficher_menu_joueur(g, num_joueur, abeille["pos"], donnees_jeu)
    surbrillance(g, modele.liste_surbrillance_cases(donnees_jeu, abeille['pos'], num_joueur))
    
    clic2 = g.attendreClic()
    cx2, cy2 = clic2.x // modele.PAS, clic2.y // modele.PAS

    if modele.L-155 <= clic2.x <= modele.L-5 and modele.H-55 <= clic2.y <= modele.H-5: 
        return "fin_tour"
    if clic2.y >= modele.H-199: 
        return "rien" 

    est_fleur = type(donnees_jeu["grille"][cx2][cy2]) == dict and donnees_jeu["grille"][cx2][cy2]["type"] == 'F'
    est_adj = abs(cx2 - abeille['pos'][0]) <= 1 and abs(cy2 - abeille['pos'][1]) <= 1
    if est_fleur and est_adj:
        succes = action_fleur_ou_mouvement(g, num_joueur, abeille, (cx2, cy2), donnees_jeu)
        if succes: 
            modele.decharger_nectar(num_joueur, abeille["pos"], donnees_jeu)
            return "action_faite"

    elif (cx2, cy2) in modele.liste_surbrillance_cases(donnees_jeu, abeille['pos'], num_joueur):
        modele.deplacer_abeille(num_joueur, abeille["pos"], (cx2, cy2), donnees_jeu)
        modele.decharger_nectar(num_joueur, abeille["pos"], donnees_jeu)
        return "action_faite"
    
    return "rien"

def jouer_tour_joueur(g, num_joueur, donnees_jeu):
    """
    Boucle principale gérant le tour complet d'un joueur.

    Paramètres:
        g (objet): La fenêtre graphique.
        num_joueur (int): Le numéro du joueur.
        donnees_jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None.
    """
    peut_spawn = True
    abeilles_a_jouer = []
    for abeille in donnees_jeu["joueurs"][num_joueur]["abeilles"]:
        if abeille["etat"] == "ok":
            abeilles_a_jouer.append(abeille["pos"])
    refresh_graphique(g, num_joueur, donnees_jeu)

    while True:
        if not abeilles_a_jouer and not peut_spawn:
            break
        
        clic = g.attendreClic()
        cx, cy = clic.x // modele.PAS, clic.y // modele.PAS

        if modele.L-155 <= clic.x <= modele.L-5 and modele.H-55 <= clic.y <= modele.H-5: 
            break

        if peut_spawn and traiter_spawn(g, num_joueur, (cx, cy), donnees_jeu, abeilles_a_jouer):
            peut_spawn = False
            refresh_graphique(g, num_joueur, donnees_jeu)
            continue

        abeille = None
        for a in donnees_jeu['joueurs'][num_joueur]['abeilles']:
           
            if a['pos'] == (cx, cy) and a["pos"] in abeilles_a_jouer:
                abeille = a
                break  

        if abeille:
            res = traiter_action_abeille(g, num_joueur, abeille, donnees_jeu)
            
            if res == "fin_tour": 
                break
            
            elif res == "action_faite":
                abeilles_a_jouer.remove((cx, cy)) 
                peut_spawn = False
                refresh_graphique(g, num_joueur, donnees_jeu)
                
            elif res == "rien":
                
                refresh_graphique(g, num_joueur, donnees_jeu)

def phase_initialisation(g, donnees_jeu):
    """
    Lance la séquence de début de partie où chaque joueur choisit son abeille de départ.

    Paramètres:
        g (objet): La fenêtre graphique.
        donnees_jeu (dict): Le dictionnaire principal du jeu.

    Retourne:
        None.
    """
    for i in range(4):
        refresh_graphique(g, i+1, donnees_jeu)
        menu_choix_abeille(g, i+1, donnees_jeu)
        choix_abeille(g, i+1,[] , donnees_jeu)

def verifier_fin_partie(g, donnees_jeu, num_joueur, nb_total_nectar):
    """
    Vérifie si la partie est terminée et affiche l'écran de victoire si nécessaire.

    Paramètres:
        g (objet): La fenêtre graphique.
        donnees_jeu (dict): Le dictionnaire principal du jeu.
        num_joueur (int): Le numéro du joueur.
        nb_total_nectar (int): Le nectar total (pour calcul majorité).

    Retourne:
        bool: True si la partie est finie, False sinon.
    """
    if not modele.continu_partie(donnees_jeu, num_joueur, nb_total_nectar):
        
        gagnants, type_v, nb_g = modele.gagnant(donnees_jeu, num_joueur, nb_total_nectar)
        
       
        menu_gagnant(g, donnees_jeu, gagnants, type_v, nb_g)
        return True 
    return False

def lancer_partie():
    """
    Fonction principale (Main) qui initialise et lance la boucle de jeu.

    Paramètres:
        Aucun.

    Retourne:
        None.
    """
    donnees_jeu = modele.init_jeu()
    g = tkiteasy.ouvrirFenetre(modele.L, modele.H)
    nb_total_nectar = modele.compter_nectar(donnees_jeu) + 4*modele.NECTAR_INITIAL
    
    phase_initialisation(g, donnees_jeu)
    donnees_jeu["tour"] += 1
    partie_en_cours = True
    
    while partie_en_cours:
        for num_joueur in range(1, 5):
            # pour le jour de la soutenance
            '''if num_joueur != 1 and num_joueur != 2:
                donnees_jeu["tour"] += 1
                continue'''
            jouer_tour_joueur(g, num_joueur, donnees_jeu)
            
            
            modele.gestion_combats(num_joueur, donnees_jeu)
            
            if verifier_fin_partie(g, donnees_jeu, num_joueur,nb_total_nectar):
                partie_en_cours = False
                break

            donnees_jeu["tour"] += 1
            modele.enlever_ko(donnees_jeu)

    g.attendreClic()
    g.fermerFenetre()


if __name__ == "__main__":
    lancer_partie()