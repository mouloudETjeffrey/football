from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
import math
import strategies4
import strategies1


#___ Creation des des joueurs ___#
j1 = Player("P1",strategies4.Gardien())
j2 = Player("P2",strategies4.Defenseur(1))
j3 = Player("P3",strategies4.Defenseur(2))
j4 = Player("P4",strategies4.Attaquant())

j5 = Player("P5",strategies1.Fonceur())
j6 = Player("P6",strategies1.Fonceur())
j7 = Player("P7",strategies1.Fonceur())
j8 = Player("P8",strategies1.Fonceur())


#___ Creations des equipes ___#
equipe_1 = SoccerTeam("T1",[j1,j2,j3,j4])
equipe_2 = SoccerTeam("T2",[j5,j6,j7,j8])

#___ Creation d'un match ___#
match = Simulation(equipe_1,equipe_2,10000)

#___ Demarrer le match ___#
show_simu(match)