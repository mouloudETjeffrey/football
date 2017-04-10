from soccersimulator import settings,SoccerTeam, Simulation, show_simu, KeyboardStrategy
from soccersimulator import Strategy, SoccerAction, Vector2D, load_jsonz,dump_jsonz,Vector2D
import logging
from arbres_utils import build_apprentissage,affiche_arbre,DTreeStrategy,apprend_arbre,genere_dot
from sklearn.tree 	import export_graphviz
from sklearn.tree import DecisionTreeClassifier
import os.path
from outils import *
from strategies1 import Fonceur

## Strategie aleatoire
class Stop(Strategy):
    def __init__(self):
        super(Stop,self).__init__("Stop")
    def compute_strategy(self,state,id_team,id_player):
        spd = Speed(state,id_team,id_player)
        return SoccerAction(-1*spd.my,Vector2D())

class Tirer(Strategy):
    def __init__(self):
        super(Tirer,self).__init__("Tirer")

    def compute_strategy(self,state,id_team,id_player):
        pos = Position(state,id_team,id_player)
        opt = Option(state,id_team,id_player)
        if opt.has_ball(pos.my):
            return SoccerAction(Vector2D(),opt.shoot_to(pos.adv_goal))
        return SoccerAction(opt.go_to(pos.ball),Vector2D())
        
class Esquiver(Strategy):
    def __init__(self):
        super(Esquiver,self).__init__("Esquiver")

    def compute_strategy(self,state,id_team,id_player):
        pos = Position(state,id_team,id_player)
        opt = Option(state,id_team,id_player)
        if opt.has_ball(pos.my):
            if pos.adv[0].y > pos.my.y:
                return SoccerAction(Vector2D(),opt.shoot_to(pos.adv[0],1,-1*opt.coeff_drible*PI/3))
            return SoccerAction(Vector2D(),opt.shoot_to(pos.adv[0],1,opt.coeff_drible*PI/3))
        return SoccerAction(opt.go_to(pos.ball),Vector2D())
        
class Eloigneur(Strategy):
    def __init__(self):
        super(Eloigneur,self).__init__("Eloigneur")

    def compute_strategy(self,state,id_team,id_player):
        pos = Position(state,id_team,id_player)
        opt = Option(state,id_team,id_player)
        if opt.has_ball(pos.my):
            if pos.adv[0].y > pos.my.y:
                return SoccerAction(Vector2D(),opt.shoot_to(pos.adv[0],1,-1*opt.coeff_drible*PI/3+PI))
            return SoccerAction(Vector2D(),opt.shoot_to(pos.adv[0],1,opt.coeff_drible*PI/3+PI))
        return SoccerAction(opt.go_to(pos.ball),Vector2D())
        
class Defenseur(Strategy):
    def __init__(self):
        super(Defenseur,self).__init__("Defenseur")
    def compute_strategy(self,state,id_team,id_player):
        pos = Position(state,id_team,id_player)
        opt = Option(state,id_team,id_player)
        if opt.has_ball(pos.my):
            return SoccerAction(Vector2D(),opt.shoot_to(pos.adv_goal,1))
        return SoccerAction(Vector2D(10,pos.ball.y%20+35)-pos.my,Vector2D())
        
class Attaquant(Strategy):
    def __init__(self):
        super(Attaquant,self).__init__("Attaquant")
    def compute_strategy(self,state,id_team,id_player):
        pos = Position(state,id_team,id_player)
        opt = Option(state,id_team,id_player)
        if opt.has_ball(pos.my):
            return SoccerAction(Vector2D(),opt.shoot_to(pos.adv_goal,1))
        return SoccerAction(opt.go_to(pos.ball),Vector2D())


#######
## Constructioon des equipes
#######

team1 = SoccerTeam("team1")
strat_j1 = KeyboardStrategy()
strat_j1.add('t',Tirer())
strat_j1.add('a',Attaquant())
strat_j1.add('d',Defenseur())
strat_j1.add('e',Eloigneur())
strat_j1.add('s',Stop())
strat_j1.add('i',Esquiver())
team1.add("Jexp 1",strat_j1)
team2 = SoccerTeam("team2")
team2.add("rien 1", Fonceur())


### Transformation d'un etat en features : state,idt,idp -> R^d
def my_get_features(state,idt,idp):
    """ extraction du vecteur de features d'un etat, ici distance a la balle, distance au but, distance balle but """
    p_pos= state.player_state(idt,idp).position
    f1 = p_pos.distance(state.ball.position)
    f2= p_pos.distance( Vector2D((2-idt)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))
    f3 = state.ball.position.distance(Vector2D((2-idt)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))
    return [f1,f2,f3]


def entrainement(fn):
    simu = Simulation(team1,team2)
    show_simu(simu)
    # recuperation de tous les etats
    training_states = strat_j1.states
    # sauvegarde dans un fichier
    dump_jsonz(training_states,fn)

def apprentissage(fn):
    ### chargement d'un fichier sauvegarder
    states_tuple = load_jsonz(fn)
    ## Apprentissage de l'arbre
    data_train, data_labels = build_apprentissage(states_tuple,my_get_features)
    dt = apprend_arbre(data_train,data_labels,depth=10)
    # Visualisation de l'arbre
    affiche_arbre(dt)
    genere_dot(dt,"test_arbre.dot")
    return dt

def jouer_arbre(dt):
    ####
    # Utilisation de l'arbre
    ###
    dic = {"Attaquant":Attaquant(),"Defenseur":Defenseur(),"Eloigneur":Eloigneur,"Stop":Stop(),"Esquiver":Esquiver(),"Tirer":Tirer()}
    treeStrat1 = DTreeStrategy(dt,dic,my_get_features)
    treeStrat2 = DTreeStrategy(dt,dic,my_get_features)
    team3 = SoccerTeam("Arbre Team")
    team3.add("Joueur 1",treeStrat1)
    team3.add("Joueur 2",treeStrat2)
    simu = Simulation(team2,team3)
    show_simu(simu)

if __name__=="__main__":
    fn = "test_states.jz"
    entrainement(fn)
    dt = apprentissage(fn)
    jouer_arbre(dt)