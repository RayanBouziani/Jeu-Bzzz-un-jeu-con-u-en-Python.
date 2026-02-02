import modele

def creer_jeu_test():
    return {
        "grille": modele.creer_grille(),
        "tour": 0,
        "joueurs": {
            1: {"stock": 100, "ruche": (0, 0), "abeilles": []},
            2: {"stock": 100, "ruche": (15, 0), "abeilles": []},
            3: {"stock": 100, "ruche": (15, 15), "abeilles": []},
            4: {"stock": 100, "ruche": (0, 15), "abeilles": []}
        }
    }

def test_spawn_abeille():
    print("spawn_abeille", end=" : ")
    j = creer_jeu_test()
    
    # Tout va bien
    modele.spawn_abeille(1, "ouvriere", j)
    assert len(j["joueurs"][1]["abeilles"]) == 1
    assert j["joueurs"][1]["stock"] == 100 - modele.COUT_PONTE
    assert j["joueurs"][1]["abeilles"][0]["type"] == "ouvriere"
    
    # Ruche occupée
    modele.spawn_abeille(1, "bourdon", j)
    assert len(j["joueurs"][1]["abeilles"]) == 1
    assert j["joueurs"][1]["stock"] == 95
    
    # Pas assez d'argent
    j["joueurs"][1]["stock"] = 0
    j["joueurs"][1]["abeilles"][0]["pos"] = (0, 1)
    modele.spawn_abeille(1, "ouvriere", j)
    assert len(j["joueurs"][1]["abeilles"]) == 1
    print("OK")

def test_butiner():
    print("butiner", end=" : ")
    j = creer_jeu_test()
    j["grille"][0][9] = {"type": "F", "nectar": 30}
    abeille = {"pos": (0, 8), "type": "ouvriere", "etat": "ok", "nectar": 0, "temps_ko": 0}
    j["joueurs"][1]["abeilles"].append(abeille)
    
    modele.butiner(1, (0, 8), (0, 9), j)
    
    assert j["joueurs"][1]["abeilles"][0]["nectar"] == 3
    assert j["grille"][0][9]["nectar"] == 27
    print("OK")

def test_decharger_nectar():
    print("decharger_nectar", end=" : ")
    j = creer_jeu_test()
    
    # Doit décharger
    ab1 = {"pos": (0, 1), "type": "ouvriere", "etat": "ok", "nectar": 10}
    j["joueurs"][1]["abeilles"].append(ab1)
    modele.decharger_nectar(1, (0, 1), j)
    assert j["joueurs"][1]["stock"] == 110
    assert j["joueurs"][1]["abeilles"][0]["nectar"] == 0

    # Ne doit pas décharger
    ab2 = {"pos": (10, 10), "type": "ouvriere", "etat": "ok", "nectar": 5}
    j["joueurs"][1]["abeilles"].append(ab2)
    modele.decharger_nectar(1, (10, 10), j)
    assert j["joueurs"][1]["stock"] == 110
    assert j["joueurs"][1]["abeilles"][1]["nectar"] == 5
    print("OK")

def test_deplacer_abeille():
    print("deplacer_abeille", end=" : ")
    j = creer_jeu_test()
    ab = {"pos": (5, 5), "type": "ouvriere", "etat": "ok", "nectar": 0}
    j["joueurs"][1]["abeilles"].append(ab)
    
    # Déplacement valide
    modele.deplacer_abeille(1, (5, 5), (5, 6), j)
    assert j["joueurs"][1]["abeilles"][0]["pos"] == (5, 6)
    
    # Trop loin
    modele.deplacer_abeille(1, (5, 6), (5, 8), j)
    assert j["joueurs"][1]["abeilles"][0]["pos"] == (5, 6)
    
    # Obstacle
    j["joueurs"][2]["abeilles"].append({"pos": (5, 7), "type": "ouvriere", "etat":"ok", "nectar": 0})
    modele.deplacer_abeille(1, (5, 6), (5, 7), j)
    assert j["joueurs"][1]["abeilles"][0]["pos"] == (5, 6)
    
    # Diagonale interdite pour ouvrière
    modele.deplacer_abeille(1, (5, 6), (6, 7), j)
    assert j["joueurs"][1]["abeilles"][0]["pos"] == (5, 6)
    print("OK")

def test_case_interdites():
    print("case_interdites", end=" : ")
    # Joueur 1 ne doit pas aller dans les bases des autres
    interdits = modele.case_interdites(1)
    assert (12, 0) in interdits
    assert (15, 14) in interdits
    assert (2, 13) in interdits
    assert (0, 0) not in interdits
    print("OK")

def test_continu_partie():
    print("continu_partie", end=" : ")
    j = creer_jeu_test()
    total_nectar = 200
    j["grille"][5][5] = {"type": "F", "nectar": 10}
    
    # Cas normal
    assert modele.continu_partie(j, 1, total_nectar) == True
    
    # Cas Victoire Blitzkrieg
    j["joueurs"][1]["stock"] = 101
    assert modele.continu_partie(j, 1, total_nectar) == False
    
    # Cas Timeout
    j["joueurs"][1]["stock"] = 10
    j["tour"] = modele.TIME_OUT
    assert modele.continu_partie(j, 1, total_nectar) == False
    print("OK")

def test_gagnant():
    print("gagnant", end=" : ")
    j = creer_jeu_test()
    total = 200
    
    # Test Blitzkrieg
    j["joueurs"][1]["stock"] = 101
    gagnants, type_v, nb = modele.gagnant(j, 1, total)
    assert gagnants == [1]
    assert type_v == "Blitzkrieg"
    
    # Test Victoire aux points
    j["joueurs"][1]["stock"] = 50
    j["joueurs"][2]["stock"] = 80
    j["joueurs"][3]["stock"] = 10
    j["joueurs"][4]["stock"] = 1
    gagnants, type_v, nb = modele.gagnant(j, 1, 1000)
    assert gagnants == [2]
    assert type_v == "plus de nectar"
    print("OK")

def test_combats():
    print("système de combat", end=" : ")
    j = creer_jeu_test()
    
    # J1 (Ouvrière) VS J2 (Bourdon) côte à côte
    # Ouvrière J1 en (5,5)
    ab1 = {"pos": (5, 5), "type": "ouvriere", "etat": "ok", "nectar": 0, "temps_ko":0}
    j["joueurs"][1]["abeilles"].append(ab1)
    # Bourdon J2 en (5,6)
    ab2 = {"pos": (5, 6), "type": "bourdon", "etat": "ok", "nectar": 0, "temps_ko":0}
    j["joueurs"][2]["abeilles"].append(ab2)
    
    # Vérifier qu'init_escarmouches détecte le conflit
    escar = modele.init_escarmouches(1, j)
    # La clé est (Joueur, Pos)
    assert (1, (5, 5)) in escar
    assert (2, (5, 6)) in escar[(1, (5, 5))]
    
    # Vérifier le calcul des forces
    forces = modele.forces_effectives(escar, j)

    cle_ouvriere = (1, (5, 5), '1', '1.0')
    cle_bourdon  = (2, (5, 6), '5', '5.0')
    assert cle_ouvriere in forces
    assert cle_bourdon in forces
    ennemi_de_ouvriere = forces[cle_ouvriere][0]
    ennemi_de_bourdon = forces[cle_bourdon][0]
    assert ennemi_de_ouvriere == (2, (5, 6), '5', '5.0')
    assert ennemi_de_bourdon == (1, (5, 5), '1', '1.0')
    print("OK")

if __name__ == "__main__":
    test_spawn_abeille()
    test_butiner()
    test_decharger_nectar()
    test_deplacer_abeille()
    test_case_interdites()
    test_continu_partie()
    test_gagnant()
    test_combats()
    print("Tous les tests sont passés avec succès !")