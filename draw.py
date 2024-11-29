"""
    @author: Stagnant09
    @github: https://github.com/Stagnant09
"""

import random, time, math

class Club:
    def __init__(self, name, pot):
        self.name = name
        self.pot = pot # 1, 2, 3 or 4
        self.opponents = [] # each opponent labeled as a tuple of (opp, home/away, pot)
    def __str__(self):
        return self.name
    def add_opponent(self, opp, home_away, pot):
        self.opponents.append((opp, home_away, pot))
    def get_opponents(self, home_only=False, away_only=False, pot=None):
        if home_only and away_only:
            raise ValueError("Cannot specify both home_only and away_only")
        # Single iteration, applying all conditions at once
        return [opp for opp, home_away, pot_ in self.opponents
                if (not home_only or home_away == "home") and
                (not away_only or home_away == "away") and
                (pot is None or pot_ == pot)]

class Draw:
    def __init__(self, teams_1, teams_2, teams_3, teams_4):
        self.pot_1 = teams_1
        self.pot_2 = teams_2
        self.pot_3 = teams_3
        self.pot_4 = teams_4
        self.all_ = teams_1 + teams_2 + teams_3 + teams_4
        self.pots = [self.pot_1, self.pot_2, self.pot_3, self.pot_4]
        self.teams = self.all_[::]
        self.matches = [] # Stored as tuples (home_club, away_club)
    def _handle_pot(self, pot, opponent_pot, num_matches):
        for club in pot:
            picked_ground = random.choice(["home", "away"])
            for _ in range(num_matches):
                if len(club.get_opponents()) == 8 or (len(club.get_opponents(home_only=True, pot=opponent_pot[0].pot)) > 0 and picked_ground == "home") or (len(club.get_opponents(away_only=True, pot=opponent_pot[0].pot)) > 0 and picked_ground == "away") or len(club.get_opponents(pot=opponent_pot[0].pot)) > 1:
                    already_picked_opponent = None
                    if picked_ground == "home":
                        already_picked_opponent = club.get_opponents(home_only=True, pot=opponent_pot[0].pot)[0]
                    elif picked_ground == "away":
                        already_picked_opponent = club.get_opponents(away_only=True, pot=opponent_pot[0].pot)[0]
                    print(f"{club} of pot {pot[0].pot} is already matched with an opponent from pot {opponent_pot[0].pot}, {picked_ground} ({already_picked_opponent.name}).")
                    continue
                valid_clubs = [potential_club for potential_club in opponent_pot 
                                if len(potential_club.get_opponents(pot=pot[0].pot)) <= 1 
                                and potential_club != club 
                                and club not in potential_club.get_opponents(pot=pot[0].pot)
                                and len(potential_club.get_opponents()) < 8
                                and ((len(potential_club.get_opponents(home_only=True, away_only=False, pot=pot[0].pot)) < 1 and picked_ground == "away") or (len(potential_club.get_opponents(away_only=True, home_only=False, pot=pot[0].pot)) < 1 and picked_ground == "home"))]
                if valid_clubs:
                    picked_club = random.choice(valid_clubs)
                else:
                    # No valid club is found
                    print(f"{club} of pot {pot[0].pot} cannot find a valid opponent of pot {opponent_pot[0].pot} to match with, {picked_ground}.")
                    picked_ground = "away" if picked_ground == "home" else "home"
                    continue
                # Each club has 1 home match and 1 away match with one and one club from pot 2 respectively
                club.add_opponent(picked_club, picked_ground, opponent_pot[0].pot)
                picked_club.add_opponent(club, "away" if picked_ground == "home" else "home", pot[0].pot)
                if picked_ground == "home":
                    self.matches.append((club, picked_club))
                else:
                    self.matches.append((picked_club, club))
                print(f"{club} vs {picked_club} ({picked_ground})")
                picked_ground = "away" if picked_ground == "home" else "home"
    def execute_draw(self):
        self.matches = []
        # Each pot has 9 clubs, creating a total of 36 clubs
        # Each club (of any of the pots) has 8 opponents, 4 at home, and 4 away and 2 from each pot (including its own)
        random.shuffle(self.pot_1)
        random.shuffle(self.pot_2)
        random.shuffle(self.pot_3)
        random.shuffle(self.pot_4)
        self._handle_pot(self.pot_1, self.pot_1, 2)
        self._handle_pot(self.pot_1, self.pot_2, 2)
        self._handle_pot(self.pot_1, self.pot_3, 2)
        self._handle_pot(self.pot_1, self.pot_4, 2)
        random.shuffle(self.pot_2)
        random.shuffle(self.pot_3)
        random.shuffle(self.pot_4)
        self._handle_pot(self.pot_2, self.pot_2, 2)
        self._handle_pot(self.pot_2, self.pot_3, 2)
        self._handle_pot(self.pot_2, self.pot_4, 2)
        random.shuffle(self.pot_3)
        random.shuffle(self.pot_4)
        self._handle_pot(self.pot_3, self.pot_3, 2)
        self._handle_pot(self.pot_3, self.pot_4, 2)
        random.shuffle(self.pot_4)
        self._handle_pot(self.pot_4, self.pot_4, 2)
    def get_matches(self, club=None, pot=None):
        if club:
            return [match for match in self.matches if (club == match[0].name or club == match[1].name)]
        elif pot:
            return [match for match in self.matches if pot in [match[0].pot, match[1].pot]]
        else:
            return self.matches


def draw_valid(draw):
    # Each club must have 8 opponents
    valid = True
    for club in draw.all_:
        if len(club.get_opponents()) != 8:
            print(f"{club} has {len(club.get_opponents())} opponents")
            valid = False
    return valid


POT1_ = [Club("Real Madrid", 1), Club("Manchester City", 1), Club("Bayern Munich", 1), Club("Paris-Saint Germain", 1), Club("Liverpool", 1), Club("Inter Milan", 1), Club("Borussia Dortmund", 1), Club("RB Leipzig", 1), Club("Barcelona", 1)]
POT2_ = [Club("Bayer Leverkusen", 2), Club("Juventus", 2), Club("Atletico Madrid", 2), Club("Benfica", 2), Club("Atalanta", 2), Club("Arsenal", 2), Club("Club Brugge", 2), Club("Shakhtar Donetsk", 2), Club("AC Milan", 2)]
POT3_ = [Club("Feyenoord", 3), Club("Sporting CP", 3), Club("PSV Eindhoven", 3), Club("Dinamo Zagreb", 3), Club("Red Bull Salzburg", 3), Club("Lille", 3), Club("Red Star Belgrade", 3), Club("Young Boys", 3), Club("Celtic", 3)]
POT4_ = [Club("Slovan Bratislava", 4), Club("Monaco", 4), Club("Sparta Prague", 4), Club("Aston Villa", 4), Club("Bologna", 4), Club("Girona", 4), Club("VfB Stuttgart", 4), Club("Sturm Graz", 4), Club("Brest", 4)]
draw = Draw(POT1_, POT2_, POT3_, POT4_)
draw.execute_draw()
"""seed = 37
while not draw_valid(draw):
    draw = Draw(POT1_, POT2_, POT3_, POT4_)
    seed = (5*seed + 3)%29
    random.seed(seed)
    draw.execute_draw()"""
for club in draw.all_:
    print(f"{club} has {len(club.get_opponents())} opponents: {", ".join([opp.name for opp in club.get_opponents()])}, facing {len(club.get_opponents(home_only=True))} at home and {len(club.get_opponents(away_only=True))} away")
