from herries_speler import Player
from herries_pass import Pass

class PassGraph:
    def __init__(self):
        self.players=[]                         #lijst van player objecten
        self.adj={}                             #dict: key = sender.name, value = lijst van Pass-objecten

    def add_player(self,player):
        if not self.has_player(player):         #speler nog niet aanwezig
            self.players.append(player)         # speler toevoegen aan spelerslijst
            self.adj[player.name]=[]            # voor deze speler een lege pass-lijst aanmaken

    def has_player(self,player):
        if isinstance(player,Player):           # speler is een Player-object?
            for speler in self.players:         # door lijst van spelers lopen
                if speler.name==player.name:    # zelfde naam = zelfde speler
                    return True
            return False

        if isinstance(player,str):
            for speler in self.players:         # speler is een naam (string)?
                if speler.name==player:         # vergelijk naam met speler.name
                    return True
            return False

    def get_player(self,name):
        for player in self.players:             # loop door alle spelerobjecten
            if player.name==name:               # zoek speler op basis van naam
                return player
        return None                             # niet gevonden → None teruggeven

    def add_pass(self,sender: Player ,receiver: Player,times=1):
        if times<=0:                            # negatieve of 0 passes zijn niet logisch
            raise ValueError("times not >0")
        # beide spelers moeten aanwezig zijn in de graaf
        if not self.has_player(sender) or not self.has_player(receiver):
            raise ValueError("sender and receiver not in graph")
        # kijken of pass al bestaat
        for pas in self.adj[sender.name]:       # door lijst uitgaande passes lopen
            if pas.receiver == receiver:        # zelfde ontvanger? zelfde pass
                pas.nr_of_times+=times          # passeer aantal verhogen
                return                          # klaar → niet opnieuw toevoegen
        # bestaat nog niet → nieuwe pass aanmaken
        new_pass=Pass(sender,receiver,times)
        self.adj[sender.name].append(new_pass)   # in adjacency list plaatsen

    def get_pass(self,sender_name:str,receiver_name:str):
        if sender_name not in self.adj:         # geen sender bekend?
            return None                         # door alle passes van deze speler lopen
        for pas in self.adj[sender_name]:       # ontvanger matcht?
            if pas.receiver.name==receiver_name:
                return pas
        return None                             # geen match

    def neighbors(self,sender_name:str):
        if isinstance(sender_name,Player):      # indien Player-object meegegeven
            sender_name=sender_name.name        # naam eruit halen
        return self.adj.get(sender_name,[])     # lijst van passes of lege lijst

    def total_weight(self,subset):
        if subset is None:                      # geen subset meegekregen?
            subset=[player.name for player in self.players] # neem alle spelers
        som=0                                   # totale pass intensiteit
        for player in subset:                   # loop door namen van zenders
            if player not in self.adj:          # geen uitgaande passes → overslaan
                continue
            for pas in self.adj[player]:        # loop door alle passes van deze zender
                if pas.sender.name in subset and pas.receiver.name in subset:
                    som+=pas.nr_of_times        # optellen indien binnen subset
        return som

    def pass_intensity(self,subset:list[str]|None=None) -> float:
        if subset is None:
            subset=[player.name for player in self.players] # standaard: alle spelers
        if len(subset)<2:                       # minder dan 2 spelers → geen intensiteit
            return 0.0
        teller=self.total_weight(subset)        # totaal aantal passes binnen subset
        n=len(subset)
        noemer=n*(n-1)                          # maximaal mogelijke passes (gericht)
        pass_intensity=teller/noemer
        return pass_intensity

    def top_pairs(self,k=5):
        passes=[]                               # lijst voor alle passes
        for player in self.players:
            for pas in self.adj[player.name]:   # alle passes verzamelen
                passes.append(pas)
        sorted_passes=sorted(passes,key=lambda p: p.nr_of_times,reverse=True) # sorteer op aantal keren
        return sorted_passes[:k]                 # top k sterkste passes

    def distribution_from(self,sender_name:str):
        lijst=[]                                 # lijst van (ontvanger, aantal)
        if sender_name not in self.adj:          # zender niet aanwezig?
            return []                            # dan lege lijst
        for pas in self.adj[sender_name]:        # loop door alle passes
            lijst.append((pas.receiver.name, pas.nr_of_times))
        sorted_lijst=sorted(lijst,key=lambda x:x[1],reverse=True) # sorteer op aantal passes (dalend)
        return sorted_lijst



