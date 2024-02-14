# on rajoute random
import pyxel, random

# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(128, 128, title="Alien shooter")

# initialisation de l'état du jeu
game_satus = 0     # 0:ecran titre ; 1:jeu ; 2:game over

# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 60
vaisseau_y = 60

# vies, score et temps initial
vies = 3
score = 0
timer = 0

# initialisation des tirs
tirs_liste = []

# initialisation des ennemis
ennemis_liste = []

# initialisation des explosions
explosions_liste = []

# initialisation du bonus
bonus = [random.randint(-8, 120), -16, 1]

# intialisation des étoiles
etoiles_list = []

# initialisation des planetes
planetes_list = []
planetes_dic = {'tree': (0, 0), 'frozen': (16, 0), 'sand': (32, 0), 'river': (0, 16), 'core': (16, 16),
                'station': (32, 16)}

# chargement des ressources
pyxel.load("images.pyxres")

# chargement des records
with open("highscores.txt", "r") as highscores_saved:
    highscores = [int(score) for score in highscores_saved.read().split(",")]

# lancement des musiques
pyxel.playm(0, 0,loop=True)

def Status_update(game_satus):
    """ mise a jour du statut du jeu et inscription des scores si nécéssaire"""
    global vies, timer, highscores
    if game_satus == 0 and pyxel.btnr(pyxel.KEY_SPACE):
        timer = pyxel.frame_count
        pyxel.play(2, 4)
        return 1

    elif game_satus == 1 and (vies < 1 or pyxel.frame_count-timer >= 5400):
        highscores.append(score)
        highscores.sort()
        highscores.pop(0)
        with open("highscores.txt", "w") as highscores_saved:
            highscores_saved.write(','.join([str(score) for score in highscores]))
        pyxel.play(2, 3)
        return 2

    if game_satus == 2 and pyxel.btnr(pyxel.KEY_SPACE):
        pyxel.play(2, 4)
        return 0
    return game_satus

def vaisseau_deplacement(x, y):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 120):
            x = x + 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0):
            x = x - 1
    if pyxel.btn(pyxel.KEY_DOWN):
        if (y < 120):
            y = y + 1
    if pyxel.btn(pyxel.KEY_UP):
        if (y > 0):
            y = y - 1
    return x, y


def tirs_creation(x, y, tirs_liste):
    """création d'un tir avec la barre d'espace"""

    # btnr pour eviter les tirs multiples
    if pyxel.btnr(pyxel.KEY_SPACE):
        tirs_liste.append([x + 3, y - 4])
        pyxel.play(1, 0)
    return tirs_liste


def tirs_deplacement(tirs_liste):
    """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""

    for tir in tirs_liste:
        tir[1] -= 1
        if tir[1] < -8:
            tirs_liste.remove(tir)
    return tirs_liste


def ennemis_creation(ennemis_liste):
    """création aléatoire des ennemis"""

    # un ennemi par seconde
    if (pyxel.frame_count % 30 == 0):
        ennemis_liste.append([random.randint(0, 120), -8])
    return ennemis_liste


def ennemis_deplacement(ennemis_liste):
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

    for ennemi in ennemis_liste:
        ennemi[1] += 1
        if ennemi[1] > 128:
            ennemis_liste.remove(ennemi)
    return ennemis_liste


def vaisseau_suppression(vies):
    """disparition du vaisseau et d'un ennemi si contact"""

    for ennemi in ennemis_liste:
        if ennemi[0] <= vaisseau_x + 8 and ennemi[1] <= vaisseau_y + 8 and ennemi[0] + 8 >= vaisseau_x and ennemi[
            1] + 8 >= vaisseau_y:
            if ennemi in ennemis_liste :
                ennemis_liste.remove(ennemi)
            vies -= 1
            # on ajoute l'explosion
            explosions_creation(vaisseau_x, vaisseau_y)
    return vies


def ennemis_suppression():
    """disparition d'un ennemi et d'un tir si contact"""
    global score
    for ennemi in ennemis_liste:
        for tir in tirs_liste:
            if ennemi[0] <= tir[0] + 1 and ennemi[0] + 8 >= tir[0] and ennemi[1] + 8 >= tir[1]:
                if ennemi in ennemis_liste:
                    ennemis_liste.remove(ennemi)
                if tir in tirs_liste:
                    tirs_liste.remove(tir)
                score += 100
                # on ajoute l'explosion
                explosions_creation(ennemi[0], ennemi[1])


def explosions_creation(x, y):
    """explosions aux points de collision entre deux objets"""
    explosions_liste.append([x, y, 0])
    pyxel.play(1, 1)


def explosions_animation():
    """animation des explosions"""
    for explosion in explosions_liste:
        explosion[2] += 1
        if explosion[2] == 15:
            explosions_liste.remove(explosion)


def etoiles_creation(etoiles_list):
    color = random.choice([6, 7, 12])
    speed = random.uniform(0.5, 1.5)
    etoiles_list.append([random.randint(0, 120), 0, color, speed])
    return etoiles_list


def etoiles_deplacement(etoiles_list):
    for etoile in etoiles_list:
        etoile[1] += etoile[-1]
        if etoile[1] > 128:
            etoiles_list.remove(etoile)
    return etoiles_list


def planetes_creation(planetes_list):
    if (pyxel.frame_count % 60 == 0):
        planetes = ['tree', 'frozen', 'sand', 'river', 'core', 'station']
        restantes = [rest[2] for rest in planetes_list]
        for test in planetes:
            if test not in restantes:
                planete = test
                speed = random.uniform(0.5, 1.5)
                planetes_list.append([random.randint(-8, 120), -16, planete, speed])
    return planetes_list


def planetes_deplacement(planetes_list):
    for planete in planetes_list:
        planete[1] += planete[-1]
        if planete[1] > 128:
            planetes_list.remove(planete)
    return planetes_list

def bonus_creation(bonus):
    if (pyxel.frame_count % 180 == 0) and bonus[-1]==0:
        bonus = [random.randint(-8, 120), -16, 1]
    return bonus

def bonus_deplacement(bonus):
    if bonus[-1] == 1:
        bonus[1] += 3
        if bonus[1] > 128:
            bonus[-1] = 0
    return bonus

def bonus_recuperation(bonus):
    global vies, score
    if bonus[-1] == 1:
        if bonus[0] <= vaisseau_x + 8 and bonus[1] <= vaisseau_y + 8 and bonus[0] + 8 >= vaisseau_x and bonus[1] + 8 >= vaisseau_y:
            pyxel.play(1, 2)
            bonus = [128, 128, 0]
            if vies < 3:
                vies+=1
            else:
                score += 500
    return bonus

# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global vaisseau_x, vaisseau_y, tirs_liste, ennemis_liste, vies, explosions_liste, etoiles_list, planetes_list, bonus, game_satus, score

    # statut du jeu
    game_satus = Status_update(game_satus)

    if game_satus == 1:
        # mise à jour de la position du vaisseau
        vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)

        # creation des tirs en fonction de la position du vaisseau
        tirs_liste = tirs_creation(vaisseau_x, vaisseau_y, tirs_liste)

        # mise a jour des positions des tirs
        tirs_liste = tirs_deplacement(tirs_liste)

        # creation des ennemis
        ennemis_liste = ennemis_creation(ennemis_liste)

        # mise a jour des positions des ennemis
        ennemis_liste = ennemis_deplacement(ennemis_liste)

        # suppression des ennemis et tirs si contact
        ennemis_suppression()

        # suppression du vaisseau et ennemi si contact
        vies = vaisseau_suppression(vies)

        # evolution de l'animation des explosions
        explosions_animation()

        # Creation d'un bonus si nécéssaire
        bonus = bonus_creation(bonus)

        # déplacement du bonus
        bonus = bonus_deplacement(bonus)

        # suppression du bonus si nécéssaire
        bonus = bonus_recuperation(bonus)

    else:
        # vies et score
        vies = 3
        score = 0

        # initialisation des tirs
        tirs_liste = []

        # initialisation des ennemis
        ennemis_liste = []

        # initialisation des explosions
        explosions_liste = []

        # initialisation du bonus
        bonus = [0]

    # creation des elements du décors
    etoiles_list = etoiles_creation(etoiles_list)
    planetes_list = planetes_creation(planetes_list)

    # mise a jour des positions du décors :
    etoiles_list = etoiles_deplacement(etoiles_list)
    planetes_list = planetes_deplacement(planetes_list)

# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)

    # L'écran titre
    if game_satus == 0:

        # affichage du fond
        for etoile in etoiles_list:
            pyxel.pset(etoile[0], etoile[1], etoile[2])
        for planete in planetes_list:
            pyxel.blt(planete[0], planete[1], 1, planetes_dic[planete[2]][0], planetes_dic[planete[2]][1], 16, 16, 0)

        # affichage du titre
        pyxel.rect(38, 62, 58, 9, 12)
        pyxel.text(40, 64, 'SPACE SHOOTER!', 7)
        pyxel.blt(40, 46, 0, 16, 0, 16, 16, 0)

        # affichage des highscores
        pyxel.rect(38, 73, 58, 37, 5)
        pyxel.text(40, 75, "highscores :", 7)

        pyxel.blt(40, 82, 0, 0, 24, 8, 8, 0)
        pyxel.text(49, 84, "1."+str(highscores[2]), 7)

        pyxel.blt(40, 91, 0, 8, 24, 8, 8, 0)
        pyxel.text(49, 93, "2."+str(highscores[1]), 7)

        pyxel.blt(40, 100, 0, 16, 24, 8, 8, 0)
        pyxel.text(49, 102, "3."+str(highscores[0]), 7)

        # indication au joueur
        pyxel.text(28, 112, 'press space to start', 7)

    # le jeu
    elif game_satus == 1:

        # affichage du fond
        for etoile in etoiles_list:
            pyxel.pset(etoile[0], etoile[1], etoile[2])
        for planete in planetes_list:
            pyxel.blt(planete[0], planete[1], 1, planetes_dic[planete[2]][0], planetes_dic[planete[2]][1], 16, 16, 0)

        # tirs
        for tir in tirs_liste:
            pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8, 0)

        # vaisseau (carre 8x8)
        pyxel.blt(vaisseau_x, vaisseau_y, 0, 0, 0, 8, 8, 0)

        # ennemis
        for ennemi in ennemis_liste:
            pyxel.blt(ennemi[0], ennemi[1], 0, 0, 8, 8, 8, 0)

        # explosions (cercles de plus en plus grands)
        for explosion in explosions_liste:
            pyxel.circb(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3)

        # bonus
        if bonus[-1] == 1:
            pyxel.blt(bonus[0], bonus[1], 0, 8, 8, 8, 8, 0)

        # affichage des vies et du score
        if vies == 3:
            pyxel.blt(5, 3, 0, 0, 16, 8, 8, 0)
        elif vies == 2:
            pyxel.blt(5, 3, 0, 8, 16, 8, 8, 0)
        elif vies == 1:
            pyxel.blt(5, 3, 0, 16, 16, 8, 8, 0)
        pyxel.text(14, 5, str(vies), 7)

        if score >= highscores[2]:
            pyxel.blt(5, 13, 0, 0, 24, 8, 8, 0)
        elif score >= highscores[1]:
            pyxel.blt(5, 13, 0, 8, 24, 8, 8, 0)
        elif score >= highscores[0]:
            pyxel.blt(5, 13, 0, 16, 24, 8, 8, 0)
        else:
            pyxel.blt(5, 13, 0, 24, 24, 8, 8, 0)
        pyxel.text(14, 15 , str(score), 7)

        if 180-(pyxel.frame_count-timer)/30 > 120:
            pyxel.blt(5, 23, 0, 0, 32, 8, 8, 0)
        elif 180-(pyxel.frame_count-timer)/30 > 60:
            pyxel.blt(5, 23, 0, 8, 32, 8, 8, 0)
        elif 180-(pyxel.frame_count-timer)/30 > 10:
            pyxel.blt(5, 23, 0, 16, 32, 8, 8, 0)
        else:
            pyxel.blt(5, 23, 0, 24, 32, 8, 8, 0)
        pyxel.text(14, 25, str(round(180-(pyxel.frame_count-timer)/30)), 7)

    # sinon: GAME OVER
    else:
        pyxel.text(46, 64, 'GAME OVER', 7)

        # affichage des highscores
        pyxel.rect(38, 73, 53, 37, 5)
        pyxel.text(40, 75, "highscores :", 7)

        pyxel.blt(40, 82, 0, 0, 24, 8, 8, 0)
        pyxel.text(49, 84, "1."+str(highscores[2]), 7)

        pyxel.blt(40, 91, 0, 8, 24, 8, 8, 0)
        pyxel.text(49, 93, "2."+str(highscores[1]), 7)

        pyxel.blt(40, 100, 0, 16, 24, 8, 8, 0)
        pyxel.text(49, 102, "3."+str(highscores[0]), 7)
        pyxel.blt(56, 24, 0, 32, 0, 16, 16)

        # indication au joueur
        pyxel.text(26, 112, 'press space to start', 7)

pyxel.run(update, draw)