from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from outils import*
import math


class Gardien(Strategy):
    
    def __init__(self):
        Strategy.__init__(self,"Gardien")
        
    def compute_strategy(self,state,id_team,id_player):
        
        pos = Position(state,id_team,id_player)
        spd = Speed(state,id_team,id_player)
        opt = Option(state,id_team,id_player) 
        
        if opt.has_ball(pos.my):
            return SoccerAction(Vector2D(),opt.shoot_to(pos.fnd[2],maxBallAcceleration))
        else:
            d = opt.dist(pos.my,[pos.ball])
            if d < 20:
                if d > 10:
                    return SoccerAction(opt.go_to(pos.ball+10*spd.ball),Vector2D())
                else:
                    return SoccerAction(opt.go_to(pos.ball),Vector2D())
            else:
                return SoccerAction(opt.go_to(Vector2D(pos.my_goal.x+opt.coeff_drible*2,opt.balayer(pos.ball.y,40,50))),Vector2D())
        

class Attaquant(Strategy):
    
    def __init__(self):
        Strategy.__init__(self,"Attaquant")
        
    def compute_strategy(self,state,id_team,id_player):
        
        pos = Position(state,id_team,id_player)
        spd = Speed(state,id_team,id_player)
        opt = Option(state,id_team,id_player)
        
        if opt.has_ball(pos.my):
            if (pos.my - pos.adv_goal).norm < 20:
                return SoccerAction(Vector2D(),opt.shoot_to(pos.adv_goal))
            else:
                p = opt.closer(pos.my,pos.adv)
                d = opt.dist(pos.my,pos.adv)
                if d < 30 and opt.dist(pos.adv_goal,[pos.my]) > opt.dist(pos.adv_goal,[p]):
                    if pos.my.y > p.y:
                        return SoccerAction(Vector2D(),opt.shoot_to(p,1,opt.coeff_drible*PI/4))
                    else:
                        return SoccerAction(Vector2D(),opt.shoot_to(p,1,opt.coeff_drible*(-1)*PI/4))
                else:
                    return SoccerAction(Vector2D(),opt.go_to(pos.adv_goal,1))
        else:
            if (Vector2D(pos.ball.x,0) - Vector2D(pos.adv_goal.x,0)).norm < (Vector2D(pos.middle.x+(-1)*opt.coeff_drible*W//4,0) - Vector2D(pos.adv_goal.x,0)).norm:
                if (pos.my - pos.ball).norm < opt.closer(pos.ball,pos.adv):
                    if (pos.my - pos.ball).norm < 10:
                        return SoccerAction(opt.go_to(pos.ball),Vector2D())
                    else:
                        return SoccerAction(opt.go_to(pos.ball+spd.ball*10),Vector2D())
                else:
                    return SoccerAction(opt.go_to(Vector2D(pos.middle.x,opt.balayer(pos.ball.y,0,90))),Vector2D())
            else:
                return SoccerAction(opt.go_to(Vector2D(pos.middle.x,opt.balayer(pos.ball.y,0,90))),Vector2D())
                
                

class Defenseur(Strategy):
    
    def __init__(self,defenseur):
        Strategy.__init__(self,"Defenseur")
        self.defenseur = defenseur
        
    def compute_strategy(self,state,id_team,id_player):
        
        pos = Position(state,id_team,id_player)
        opt = Option(state,id_team,id_player)
        
        if opt.has_ball(pos.my):
            return SoccerAction(Vector2D(),opt.shoot_to(pos.fnd[2],maxBallAcceleration))
        else:
            x,y = opt.ma_zone(self.defenseur)
            if opt.appartient(pos.my,x,y):
                return SoccerAction(opt.go_to(pos.ball),Vector2D())
            else:
                return SoccerAction(opt.go_to(opt.repos_defense(self.defenseur)),Vector2D())