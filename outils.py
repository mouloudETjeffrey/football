from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
import math

GAME_WIDTH = settings.GAME_WIDTH
GAME_HEIGHT = settings.GAME_HEIGHT
PLAYER_RADIUS = settings.PLAYER_RADIUS
BALL_RADIUS = settings.BALL_RADIUS
MAX_GAME_STEPS = settings.MAX_GAME_STEPS
maxPlayerSpeed = settings.maxPlayerSpeed
maxPlayerAcceleration = settings.maxPlayerAcceleration
maxBallAcceleration = settings.maxBallAcceleration
W = GAME_WIDTH
H = GAME_HEIGHT

GOAL = [Vector2D(0,GAME_HEIGHT//2),Vector2D(GAME_WIDTH,GAME_HEIGHT//2)]
PI = math.pi
GAME_GOAL_HEIGHT = 10
ZONE_DEFENSE = [[[(0,3*W//4),(0,3*H//4)],[(0,3*W//4),(H//4,H)]],[[(W//4,W),(0,3*H//4)],[(W//4,W),(H//4,H)]]]
REPOS_DEFENSE = [[Vector2D(W//4,H//4),Vector2D(W//4,3*H//4)],[Vector2D(3*W//4,H//4),Vector2D(3*W//4,3*H//4)]]


class Position:

    def __init__(self,state,idteam,idplayer):
        self.state = state
        self.team = idteam
        self.player = idplayer

    @property
    def my(self):
        return self.state.player_state(self.team,self.player).position

    @property
    def ball(self):
        return self.state.ball.position

    @property
    def my_goal(self):
        return GOAL[self.team-1]

    @property
    def adv_goal(self):
        return GOAL[2-self.team]

    @property
    def middle(self):
        return Vector2D(GAME_WIDTH//2,GAME_HEIGHT//2)

    @property
    def adv(self):
        positions = []
        for i in range(self.state.nb_players(3-self.team)):
            positions.append(self.state.player_state(3-self.team,i).position)
        return positions

    @property
    def fnd(self):
        positions = []
        for i in range(self.state.nb_players(self.team)):
            if i != self.player:
                positions.append(self.state.player_state(self.team,i).position)
        return positions


class Speed:

    def __init__(self,state,idteam,idplayer):
        self.state = state
        self.team = idteam
        self.player = idplayer

    @property
    def my(self):
        return self.state.player_state(self.team,self.player).vitesse

    @property
    def ball(self):
        return self.state.ball.vitesse

    @property
    def adv(self):
        vitesses = []
        for i in range(self.state.nb_players(3-self.team)):
            vitesses.append(self.state.player_state(3-self.team,i).vitesses)
        return vitesses

    @property
    def fnd(self):
        vitesses = []
        for i in range(self.state.nb_players(self.team)):
            if i != self.player:
                vitesses.append(self.state.player_state(self.team,i).vitesses)
        return vitesses


class Option:

    def __init__(self,state,idteam,idplayer):
        self.pos = Position(state,idteam,idplayer)
        self.spd = Speed(state,idteam,idplayer)
        self.team = idteam
        self.player = idplayer
        self.team = idteam 
        
    def has_ball(self,position):
        return (self.pos.ball - position).norm <= (PLAYER_RADIUS + BALL_RADIUS)

    def shoot_to(self,position,norm=None,angle=None):
        vector = position - self.pos.ball
        if norm != None:
            vector = vector.normalize()*norm
        if angle != None:
            vector = Vector2D(angle=vector.angle+angle,norm=vector.norm)
        return vector

    def go_to(self,position,norm=None,angle=None):
        vector = position - self.pos.my
        if norm != None:
            vector = vector.normalize()*norm
        if angle != None:
            vector = Vector2D(angle=vector.angle+angle,norm=vector.norm)
        return vector

    def dist(self,position,liste_positions):
        distances = []
        for pos in liste_positions:
            distances.append((position - pos).norm)
        return min(distances)

    def closer(self,position,liste_positions):
        distance_min = self.dist(position,liste_positions)
        for pos in liste_positions:
            if (position - pos).norm == distance_min:
                return pos
        return None

    @property
    def coeff_drible(self):
        return 3-2*self.pos.team
        
    @property
    def coeff(self):
        if ((spd.my.x < 0) and ((pos.adv[0]-pos.my).x > 0)) or ((spd.my.x > 0) and ((pos.adv[0]-pos.my).x < 0)):
                return -1
        return 1
        
    def balayer(self,valeur,minimum,maximum):
        #return valeur % (maximum-minimum+1) + minimum
        return min(maximum,max(minimum,valeur))
        
    def ma_zone(self,defenseur):
      return ZONE_DEFENSE[self.team-1][defenseur-1]
    
    def appartient(self,position,zone_x,zone_y):
        if (position.x >= zone_x[0] and position.x <= zone_x[1]) and (position.y >= zone_y[0] and position.y <= zone_y[1]):
            return True
        return False
        
    def repos_defense(self,defenseur):
        return REPOS_DEFENSE[self.team-1][defenseur-1]