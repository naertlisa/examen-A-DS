class Player:
    def __init__(self, name, number):
        self.name = name         # spelernaam
        self.number = number     # rugnummer

    def __eq__(self, other):
        # True als other een Player is en namen gelijk zijn
        if isinstance(other, Player) and self.name == other.name:
            return True
        return False

    def __lt__(self, other):
        # sorteren op rugnummer, strikt kleiner
        if not isinstance(other, Player):
            return NotImplemented
        elif self.number < other.number:
            return True
        return False

    def __str__(self):
        return f"{self.name} ({self.number})"

def main():
    p1 = Player("Eden Hazard", 10)
    p2=Player("Moussa Dembele",19)
    p3 = Player("Jan Vertonghen", 5)
    spelers=[p1,p2,p3]
    print(p1)
    print("p1==Player('Eden Hazard', 99)?", p1==Player('Eden Hazard', 99)) #== roept __eq__ op
    print("\nGestorteerde lijst:")
    for speler in sorted(spelers): #sorted roept __lt__ op
        print(speler) #roept __str__ op
if __name__ == "__main__":
    main()
