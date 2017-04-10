from soccersimulator.strategies  import Strategy
from soccersimulator.mdpsoccer import SoccerAction, PlayerState
from soccersimulator.utils import Vector2D
from tools import Strats, Action

class Solo(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Solo")
    def compute_strategy (self, state, id_team, id_player):
        tools=Strats(state,id_team,id_player)
        if tools.coups_denvoi:
            return tools.fonce
        return tools.solo


class Attaquant(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaquant")
    def compute_strategy (self, state, id_team, id_player):
        tools=Strats(state,id_team,id_player)
        if tools.coups_denvoi:
            return tools.fonce
        return tools.attaquant
        
class Defenceur(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defenseur")
    def compute_strategy (self, state, id_team, id_player):
        tools = Strats(state,id_team,id_player)
        return tools.defenseur
    
        
class Fonceur(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")
    def compute_strategy (self, state, id_team, id_player):
        tools = Strats(state,id_team,id_player)
        return tools.fonce


class Dribbleur(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Dribbleur")
    def compute_strategy (self, state, id_team, id_player):
        tools = Action(state,id_team,id_player)
        if PlayerState.can_shoot :
            return tools.aller(tools.ball_position)+tools.dribble
        return SoccerAction(Vector2D(),Vector2D()) 
        
