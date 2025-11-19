class Batch:
    def __init__(self,quantity,cost_per_unit):
        self.quantity=quantity
        self.cost_per_unit=cost_per_unit

    def __str__(self):
        return f" Batch(quantity={self.quantity}, cost_per_unit={self.cost_per_unit})"

class Product:
    def __init__(self,product_name,batches,holding_cost,stockout_penalty):
        self.product_name=product_name
        self.batches=batches
        self.holding_cost=holding_cost
        self.stockout_penalty=stockout_penalty

    def add_batch(self,quantity,cost_per_unit):
        self.batches.append(Batch(quantity,cost_per_unit)) #Batch(quantity,cost_per_unit) --> maakt een nieuwe batch aan

    def fulfill_demand(self,demand):
        totaal=0
        k=0
        while k<len(self.batches):
            totaal+=self.batches[-1-k].quantity #lifo: eerst wordt laatste batch gebruikt => deze hoeveelheid aan totaal toegevoegd
            k+=1 #daarna gaan we naar de voorlaatste batch ...
            if totaal >= demand: #als vraag door 1 of meerdere batches is vervult, retourneer 0
                return 0
        return (demand-totaal)*self.stockout_penalty #als vraag niet kan worden vervuld, retourneer self.stockout_penalty* aantal producten dat niet kan worden geleverd
    def calculate_holding_cost(self):
        totaal=0
        for i in range(len(self.batches)):
            totaal += self.batches[i].quantity #quantities optellen tot totaal
        return totaal*self.holding_cost

    def __str__(self):
        result = f"Product {self.product_name}:" #starten met beginstring: naam van product
        for batch in self.batches:
            result += f"\n{batch}" #in een lus batches toevoegen aan string => voor elke batch 1 regel
        return result

