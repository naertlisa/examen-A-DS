from herries_speler import *
from herries_pass import *
class PassGraph:
    def __init__(self, path_naam = None):
        self.players = []
        self.adj = {}

        if path_naam is not None:
            self.load_from_text(path_naam)

    def add_player(self, player: Player):
        if not self.has_player(player):
            self.players.append(player)
            self.adj[player.name] = []

    def has_player(self, player):
        if isinstance(player, Player):
            for pl in self.players:
                if pl.name == player.name:
                    return True
            return False
        if isinstance(player, str):
            for pl in self.players:
                if pl.name == player:
                    return True
            return False

    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def add_pass(self, sender: Player, receiver: Player, times = 1):
        if times <= 0:
            raise ValueError("times not > 0")
        if not self.has_player(sender) or not self.has_player(receiver):
            raise ValueError("sender and receiver not in graph")

        for pas in self.adj[sender.name]:
            if pas.receiver == receiver:
                pas.nr_times += times
                return
        new_pass = Pass(sender, receiver, times)
        self.adj[sender.name].append(new_pass)

    def get_pass(self, sender_name: str, receiver_name: str):
        if sender_name not in self.adj:
            return None

        for pas in self.adj[sender_name]:
            if pas.receiver.name == receiver_name:
                return pas
        return None

    def neighbors(self, sender_name: str):
        if isinstance(sender_name, Player):
            sender_name = sender_name.name
        return self.adj.get(sender_name, [])


    def total_weight(self, subset: list[str]):
        if subset is None:
            subset = [player.name for player in self.players]
        som = 0
        for player in subset:
            if player not in self.adj:
                continue
            for pas in self.adj[player]:
                if pas.sender.name in subset and pas.receiver.name in subset:
                    som += pas.nr_times
        return som

    def pass_intensity(self, subset: list[str] | None = None) -> float:
        if subset is None:
            subset = [player.name for player in self.players]

        if len(subset) < 2:
            return 0.0

        teller = self.total_weight(subset)
        n = len(subset)
        noemer = n*(n-1)
        pass_intensity = teller / noemer

        return pass_intensity

    def top_pairs(self, k=5):
        passes = []
        for player in self.players:
            for pas in self.adj[player.name]:
                passes.append((pas, pas.nr_times))
        sorted_passes = sorted(passes, key=lambda x: x[1], reverse=True)
        return sorted_passes[:k]

    def distribution_from(self, sender_name:str):
        lijst = []
        for pas in self.adj[sender_name]:
            lijst.append((pas.receiver.name, pas.nr_times))
        sorted_lijst = sorted(lijst, key=lambda x: x[1], reverse=True)
        return sorted_lijst

    def players_list(self):
        players = self.players.copy()
        return players

    def passes(self):
        passes = []
        for player in self.players:
            for pas in self.adj[player.name]:
                passes.append(pas)
        return passes

    def load_from_text(self, path_naam):
        section = None
        file = open(path_naam, 'r')
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                section = line
                continue

            if section == "[PLAYERS]":
                try:
                    name, number = line.split(";")
                    name = name.strip()
                    number = int(number.strip())
                    self.add_player(Player(name, number))
                except:
                    raise ValueError(f"Wrong player data: {line}")
            elif section == "[PASSES]":
                try:
                    names, pas = line.split(":")
                    names = names.strip()
                    pas = int(pas.strip())
                    sender_name, receiver_name = names.split("->")
                    sender_name = sender_name.strip()
                    sender = self.get_player(sender_name)
                    receiver_name = receiver_name.strip()
                    receiver = self.get_player(receiver_name)
                    if sender not in self.players or receiver not in self.players:
                        raise ValueError(f"Pass refers to unknown player: {line}")
                    self.add_pass(sender, receiver, pas)
                except:
                    raise ValueError(f"Wrong pass data: {line}")
            else:
                raise ValueError(f"Wrong section: {section}")
        file.close()

    def save_to_txt(self, path):
        file = open(path, "w")
        file.write("[PLAYERS]\n")
        for player in self.players:
            file.write(f"{player.name};{player.number}\n")
        file.write("[PASSES]\n")
        for player in self.players:
            for pas in self.adj[player.name]:
                file.write(f"{pas.sender.name} -> {pas.receiver.name} : {pas.nr_times}\n")

def main():
    graph = PassGraph()
    speler1 = Player("Vanaken", 20)
    speler2 = Player("Forbs", 30)
    speler3 = Player("Mechele", 15)
    speler4 = Player("Mignolet", 11)

    graph.add_player(speler1)
    graph.add_player(speler2)
    graph.add_player(speler3)
    graph.add_player(speler4)

    graph.add_pass(speler1, speler2, 3)
    graph.add_pass(speler1, speler2, 2)
    graph.add_pass(speler2, speler3, 4)
    graph.add_pass(speler3, speler4, 1)

    graph.save_to_txt("team.txt")

    graph2 = PassGraph("team.txt")

    print([player.name for player in graph2.players_list()])
    for pas in graph.passes():
        print(pas)

if __name__ == "_main_":
    main()

