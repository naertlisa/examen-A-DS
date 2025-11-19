from herries_speler import Player

class Pass:
    def __init__(self,sender,receiver,nr_of_times):
        self.sender=sender
        self.receiver=receiver
        self.nr_of_times=nr_of_times

    def get_weight(self):
        return self.nr_of_times
    def get_start(self):
        return self.sender
    def get_end(self):
        return self.receiver

    def __eq__(self,other):
        if isinstance(other,Pass) and self.sender==other.sender and self.receiver==other.receiver:
            return True
        return False

    def __str(self):
        return f"Pass from {self.sender} to {self.receiver}"
def main():
    player1=Player("Eden Hazard",10)
    player2=Player("Moussa Dembele",19)
    player3=Player("Jan Vertonghen",5)
    pass1=Pass(player1,player2,5)
    pass2=Pass(player3,player1,2)
    pass3=Pass(player1,player2,10)
    print(pass1)
    print("pass1==pass3?",pass1==pass3) #test __eq__
    print("pass1=pass2?", pass1==pass2)
    print("Weight of pass1:",pass1.get_weight()) #test get_weight()

if __name__=="__main__":
    main()


