#Bonjour moi du futur, j'espere que tout va pour le mieux dans ta vie et que tu as réussi à faire ce que tu veux !
#Ce code est pas très propre mais je suis sur que tu fais beaucoup mieux aujourd'hui ! Si tu es dans le mal, n'oublies pas d'où tu viens.
#Si tu arrives à faire le même jeu dans un autre langage ben gg mais jme demande ce que tu fais de ta vie...

#Je n'ai pas les droits des imgaes de fond et des musiques mais tout le code est de moi ! j'ai aussi dessiné les images des personnages !
#Ce jeu n'est pas fait dans le but d'etre vendu mais à pur but éducatif.


import pygame
import random
import math
import time as tm

def collision(ax, ay, bx, by):
    if level.selectscreen == True or level.endscreen ==  True:
        if int(math.sqrt((ax-bx)**2 + (ay-by)**2)) <= 200 :
            return True
    elif level.levelactuel == "Boss":
        if int(math.sqrt((ax-bx)**2 + (ay-by)**2)) <= 120 : #Vérifie de collision entre 2 objets
            return True
    elif int(math.sqrt((ax-bx)**2 + (ay-by)**2)) <= 60 : #Vérifie de collision entre 2 objets
        return True
    return False

pygame.init()
class Enemi :
    def __init__(self, x, y, vitessex, vitessey, image):
        self.x = x
        self.y = y
        self.vitessex = vitessex
        self.vitessey = vitessey
        self.image = pygame.image.load(image)
        self.going_left = False
        self.nb = 0
        self.mor = pygame.mixer.Sound('tuto/no.wav')
        
        
    def debut(self):
        ecran.blit(self.start,(self.x,self.y))
        
    def draw(self):
        ecran.blit(self.image,(self.x,self.y))
        
    def update(self):
    
        #Avancer horizontalement
        if self.going_left == False:#Vers la droite
            self.x += self.vitessex
            
        else:#Vers la gauche
            self.x -= self.vitessex
            
        #Avancer verticalement+collision mur
        if self.x >= 736:#Collision mur de droite, Descendre
            self.y += self.vitessey
            self.going_left = True
            
        elif self.x <= 0 :#Collision mur de gauche, Descendre
            self.y += self.vitessey
            self.going_left = False
            
        if self.y >= 500:#Défaite
            jeu.loose()
            self.mor.play()
            
    def kill(self):
        self.x = random.randint(0,700)   
        self.y = random.randint(0,50)

class Joueur :
    def __init__(self):
        #Position de base
        self.x = 400
        self.y = 536
        #Load image
        self.image = pygame.image.load("tuto/shrekdraw2.png")
        self.chevalier = pygame.image.load("tuto/shrekarmure.png")
        self.end = pygame.image.load("tuto/hero.png")
    def draw(self):
        #affichage joueur
        if level.levelactuel == "endless":
            ecran.blit(self.end,(self.x,self.y))
        elif level.levelactuel == 3:
            ecran.blit(self.chevalier,(self.x,self.y))
        else:
            ecran.blit(self.image,(self.x,self.y))
        
    def update(self):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            self.mouvement("left")
        if touches[pygame.K_RIGHT]:
            self.mouvement("right")
        
    def mouvement(self, direction):
        if direction == "left":
            if self.x <= 0 :#Limite de Gauche
                self.x = 0
            else :
                self.x -= 10  
        if direction == "right":
            if self.x >= 736 :#Limite de droite
                self.x = 736 
            else :
                self.x += 10
    
player = Joueur()


class Balle:
    def __init__(self):
        self.etat = False
        #Position de base de la balle
        self.y = 1000
        self.x = 1000
        #Load son et image
        self.son = pygame.mixer.Sound('tuto/shrek.wav')
        self.ded = pygame.mixer.Sound('tuto/donkey.wav')
        self.img = pygame.image.load("tuto/vomit.png")
        self.hitcount = 0
        
        
    def update(self,player):
        if self.etat == False:
            touches = pygame.key.get_pressed()
            if touches[pygame.K_SPACE]:#Quand espace est pressé:
                self.etat = True
                #Téléporte la balle sur le joueur
                self.x = player.x
                self.y = player.y
                #Joue un son
                self.son.play()
                
    
    def mouvement(self):
        if self.etat == True:#Déplacement balle
            self.y -= 15
            ecran.blit(self.img,(self.x,self.y))
        if self.y <= 0 :#Collision avec plafond
            self.etat = False
            
    def kill(self):
        
        for i in range (len(level.ennemis)):
            if collision(level.ennemis[i].x,level.ennemis[i].y,balle.x,balle.y) == True:
                if level.selectscreen == True:
                    self.x = -1000      
                    self.y = -1000
                    self.etat = False
                    if level.selectscreen == True:
                        level.selectscreen = False
                        level.levelactuel = "Menu"
                if level.levelactuel == "Boss":
                    self.x = -1000      
                    self.y = -1000
                    self.etat = False
                    self.hitcount += 1
                    if self.hitcount == 10:
                        jeu.score += 1
                else:
                    self.x = -1000      
                    self.y = -1000
                    self.etat = False
                    level.ennemis[i].kill()
                    jeu.score += 1
                self.ded.play()
            
balle = Balle()

class Jeu:
    def __init__(self):
        #Musique
        
        pygame.mixer.music.load('tuto/Background.mp3')
        pygame.mixer.music.play(-1)
        
        #Background load
        #Nom fenetre
        pygame.display.set_caption("Shrouk adventure")
        #Police ecriture(pour le score)
        self.police = pygame.font.Font('tuto/KumbhSans-Regular.ttf', 32)
        self.score = 0
        self.count = 0
        self.lost = False
        self.file = open('tuto/highscore.txt','r')
        readfile = self.file.read()
        self.highscore = [ int(x) for x in readfile.split() ]#Transforme les str du txt en int
        self.file.close()
        self.swamp = pygame.image.load("tuto/swamp.jpg")
        self.fermier = pygame.image.load('tuto/fermierbg.png')
        self.chateau = pygame.image.load('tuto/chateau.jpg')
        self.dragon = pygame.image.load('tuto/chateaudragon.png')
        self.fee = pygame.image.load('tuto/ccompletementrandommaisjaviasriendautre.png')
        
    def hud(self):
        #Score
        message = self.police.render(f"Score : {self.score}", True, (255, 255, 255))
        ecran.blit(message, (0, 0))
        high = self.police.render(f"High score : {sum(self.highscore)}", True, (255, 255, 255))
        ecran.blit(high, (300, 0))
        
        
    def draw(self):#Background affichage
        if level.levelactuel == "Menu" or level.levelactuel =="endscreen" or level.levelactuel == "endless" or level.levelactuel == 1:
            ecran.blit(self.swamp, (0,0))
            
        if level.levelactuel == 2:
            ecran.blit(self.fermier, (0,0))
            
        if level.levelactuel == 3:
            ecran.blit(self.chateau, (0,0))
            
        if level.levelactuel == 4:
            ecran.blit(self.fee, (0,0))
            
        if level.levelactuel == "Boss":
            ecran.blit(self.dragon, (0,0))
            
    def scoreboard(self,count):
        if count == 0:
            if (sum(self.highscore)) < self.score :
                self.file = open('tuto/highscore.txt','w')
                self.file.write(str(self.score))
                self.file.close()
                self.lost = False
        
    def loose(self):#Si ennemis ont gagné
        #Message de fin
        self.scoreboard(self.count)
        self.count += 1
        self.lost = True
        end = self.police.render(f"Vous avez été vaincu !", True, (255, 255, 255))
        ecran.blit(end,(250,300))
        #Retire les ennemis de l'écran
        for i in range(len(level.ennemis)):
            level.ennemis[i].y = 1000
    
                
        
jeu = Jeu()

class Level:
    def __init__ (self):
        self.selectscreen = True
        self.ennemis = []
        self.levelactuel = "start"
        self.endscreen = False
        
    def select_screen(self):
        if self.selectscreen == True:
            #Tutoriel ecrit
            tuto_start = jeu.police.render("Tire sur le bouton start pour commencer !", True, (255, 255, 0))
            tuto_deplacement = jeu.police.render("Déplacement : Flèches directionnelles", True, (0, 255, 255))
            tuto_tire = jeu.police.render("Tir : Barre espace", True, (255, 0, 255))
            ecran.blit(tuto_start,(125,50))
            ecran.blit(tuto_deplacement,(150,100))
            ecran.blit(tuto_tire,(275,150))
        elif self.levelactuel == "endscreen":
            end = jeu.police.render("Bravo vous avez vaincu tous les ennemis de Shrouk !", True, (255, 255, 0))
            encouragement = jeu.police.render("Mais le combat ne prend pas fin...", True, (0, 255, 255))
            tire = jeu.police.render("Tirez sur le bouton pour continuer le combat", True, (255, 0, 255))
            ecran.blit(end,(15,50))
            ecran.blit(encouragement,(175,100))
            ecran.blit(tire,(85,150))
            
    def creation_ennemi(self, nb, vitessex, vitessey, image):
        self.ennemis = []
        if self.selectscreen == True  :
            self.ennemis.append(Enemi(300,200,vitessex, vitessey, image))
            
        elif self.endscreen == True :
            self.ennemis.append(Enemi(300,200,vitessex, vitessey, image))
            
        else:
            for i in range (0,nb):
                self.ennemis.append(Enemi(random.randint(0,700),random.randint(0,100),vitessex, vitessey, image))
            
    def deplacement(self):
        for i in range(len(self.ennemis)):
            self.ennemis[i].draw()
            self.ennemis[i].update()
            
    def passage_level(self):
        if jeu.score == 0 and self.levelactuel == "start":
            self.level(0)
            self.levelactuel = "Menu"
        if jeu.score == 1 and self.levelactuel == "Menu":
            self.level(1)
            self.levelactuel = 1
        elif jeu.score == 10 and self.levelactuel == 1:
            self.level(2)
            self.levelactuel = 2
        elif jeu.score == 20 and self.levelactuel == 2:
            self.level(3)
            self.levelactuel = 3
        elif jeu.score == 30 and self.levelactuel == 3:
            self.level(4)
            self.levelactuel = 4
        elif jeu.score == 40 and self.levelactuel == 4:
            self.level(5)
            self.levelactuel = "Boss"
        elif jeu.score == 41 and self.levelactuel == "Boss":
            self.endscreen = True
            self.level(6)
            self.levelactuel = "endscreen"
        elif jeu.score == 42 and self.levelactuel == "endscreen":
            self.endscreen = False
            self.level(7)
            self.levelactuel = "endless"
        
            
        levelencours = jeu.police.render(f"Level : {self.levelactuel}", True, (255, 255, 255))
        ecran.blit(levelencours,(600,0))
        
        
        self.deplacement()
            
    def level(self,level):
        if level == 0:
            self.creation_ennemi(1, 0, 0, 'tuto/startbutton.png')
            
        elif level == 1:
            self.creation_ennemi(5, 6, 20, 'tuto/donkeydraw.png')

        elif level == 2:
            self.creation_ennemi(10, 10, 50, 'tuto/farmer.png')

        elif level == 3:
            self.creation_ennemi(15, 14, 80, 'tuto/chevalier.png')
 
        elif level == 4:
            self.creation_ennemi(20, 16, 110,'tuto/fairy.png')

        elif level == 5:
            self.creation_ennemi(1, 10, 140,'tuto/dragon.png')
            
        elif level == 6:
            self.creation_ennemi(1,0,0,'tuto/startbutton.png')
            
        elif level == 7:
            self.creation_ennemi(10,14,50,'tuto/donkeydraw.png')
    
level = Level()

ecran = pygame.display.set_mode((800,600))
continuer = True
last_tick = 0
while continuer:
    tick = tm.time()
    elapsed_time = tick - last_tick
    if elapsed_time >= 1/60:
        
        ecran.fill((0, 0, 0))
        
            
        #Parametre jeu
        jeu.draw()
        jeu.hud()
        
        #Level
        level.select_screen()
        level.passage_level()
        
        #Parametre joueur
        player.update()
        player.draw()
        
        #Parametre balle
        balle.update(player)
        balle.mouvement()
        balle.kill()
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#Quitter le jeu
                continuer = False
        
        
        last_tick = tick
        
    
    
        
    
    
pygame.quit()

