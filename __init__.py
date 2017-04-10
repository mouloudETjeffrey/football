from soccersimulator import SoccerTeam
import strategies1
import strategies2
import math

def get_team(i):
    s = SoccerTeam(name="UPMC")
    if i==1:
        s.add("Ronaldo",strategies1.Dribleur())
    if i==2:
        s.add("Mouloud",strategies2.Attaquant())
        s.add("Jeffrey",strategies2.Defenseur())    
    if i==4:
        s.add("Mouloud",strategies2.Attaquant())
        s.add("Jeffrey",strategies2.Defenseur())
        s.add("Ronaldo",strategies2.Attaquant())
        s.add("Messi",strategies2.Defenseur())
        
    return s
