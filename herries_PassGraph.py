from herries_speler import Player
from herries_pass import Pass

class PassGraph:
    def __init__(self):
        self.players=[] #lijst van player objecten
        self.adj={} #dict: key = sender.name, value = lijst van Pass-objecten

    def add_player(self,player):
        if not self.has_player(player):
            self.players.append(player)
            self.adj[player.name]=[]

    def has_player(self,player):
        if isinstance(player,Player):
            for speler in self.players:
                if speler.name==player.name:
                    return True
            return False

        if isinstance(player,str):
            for speler in self.players:
                if speler.name==player:
                    return True
            return False

    def get_player(self,name):
        for player in self.players:
            if player.name==name:
                return player
        return None

    def add_pass(self,sender: Player ,receiver: Player,times=1):
        if times<=0:
            raise ValueError("times not >0")
        if not self.has_player(sender) or not self.has_player(receiver):
            raise ValueError("sender and receiver not in graph")
        for pas in self.adj[sender.name]:
            if pas.receiver == receiver:
                pas.nr_of_times+=times
                return
        new_pass=Pass(sender,receiver,times)
        self.adj[sender.name].append(new_pass)

    def get_pass(self,sender_name:str,receiver_name:str):
        if sender_name not in self.adj:
            return None
        for pas in self.adj[sender_name]:
            if pas.receiver.name==receiver_name:
                return pas
        return None
    def neighbors(self,sender_name:str):
        if isinstance(sender_name,Player):
            sender_name=sender_name.name
        return self.adj.get(sender_name,[])

    def total_weight(self,subset):
        if subset is None:
            subset=[player.name for player in self.players]
        som=0
        for player in subset:
            if player not in self.adj:
                continue
            for pas in self.adj[player]:
                if pas.sender.name in subset and pas.receiver.name in subset:
                    som+=pas.nr_of_times
        return som

    def pass_intensity(self,subset:list[str]|None=None) -> float:
        if subset is None:
            subset=[player.name for player in self.players]
        if len(subset)<2:
            return 0.0
        teller=self.total_weight(subset)
        n=len(subset)
        noemer=n*(n-1)
        pass_intensity=teller/noemer
        return pass_intensity

    def top_pairs(self,k=5):
        passes=[]
        for player in self.players:
            for pas in self.adj[player.name]:
                passes.append(pas)
        sorted_passes=sorted(passes,key=lambda p: p.nr_of_times,reverse=True)
        return sorted_passes[:k]

    def distribution_from(self,sender_name:str):
        lijst=[]
        if sender_name not in self.adj:
            return []
        for pas in self.adj[sender_name]:
            lijst.append((pas.receiver.name, pas.nr_of_times))
        sorted_lijst=sorted(lijst,key=lambda x:x[1],reverse=True)
        return sorted_lijst



