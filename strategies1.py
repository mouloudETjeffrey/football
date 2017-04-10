from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from outils import*
import math


class Fonceur(Strategy):

    def __init__(self):
        Strategy.__init__(self,"Fonceur")

    def compute_strategy(self,state,id_team,id_player):
        pos = Position(state,id_team,id_player)
        opt = Option(state,id_team,id_player)

        if opt.has_ball(pos.my):
            return SoccerAction(Vector2D(),opt.shoot_to(pos.adv_goal))
        else:
            return SoccerAction(opt.go_to(pos.ball),Vector2D())


class Dribleur(Strategy):

    def __init__(self,disTire=20,rayDrib=40,rayPred=10,coefPred=8,angDrib=PI/4):
        Strategy.__init__(self,"Dribleur")
        self.disTire = disTire
        self.rayDrib = rayDrib
        self.rayPred = rayPred
        self.coefPred = coefPred
        self.angDrib = angDrib

    def compute_strategy(self,state,id_team,id_player):
        
        pos = Position(state,id_team,id_player)
        spd = Speed(state,id_team,id_player)
        opt = Option(state,id_team,id_player)

        if opt.has_ball(pos.my):
            if opt.dist(pos.my,[pos.adv_goal]) < self.disTire or opt.has_ball(pos.adv[0]):
                return SoccerAction(Vector2D(),opt.shoot_to(pos.adv_goal))
            else:
                if opt.dist(pos.my,pos.adv) > self.rayDrib or opt.dist(pos.my,[pos.adv_goal]) < opt.dist(pos.adv_goal,pos.adv):
                    return SoccerAction(Vector2D(),opt.shoot_to(pos.adv_goal,1))
                else:
                    if pos.my.y > pos.adv[0].y:
                        return SoccerAction(Vector2D(),opt.shoot_to(pos.adv[0],1,opt.coeff_drible*self.angDrib))
                    else:
                        return SoccerAction(Vector2D(),opt.shoot_to(pos.adv[0],1,opt.coeff_drible*(-1)*self.angDrib))
        else:
            if opt.dist(pos.my,[pos.ball]) < opt.dist(pos.ball,pos.adv):
                if opt.dist(pos.my,[pos.ball]) > self.rayPred:
                    return SoccerAction(opt.go_to(pos.ball)+spd.ball*self.coefPred,Vector2D())
                else:
                    return SoccerAction(opt.go_to(pos.ball),Vector2D())
            else:
                if opt.dist(pos.my,[pos.my_goal]) == 0:
                    return SoccerAction((-1)*spd.my,Vector2D())
                else:
                    return SoccerAction(opt.go_to(pos.my_goal),Vector2D())