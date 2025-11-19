from vorig_examen_ADS_oef1 import Product
import random

class Inventory_Manager:
    def __init__(self):
        self.woordenboek = {} #{product_name: product_object}

    def add_product(self, product_name, holding_cost,stockout_penalty):
        if product_name in self.woordenboek:
            return f"Product {product_name} already exists."
        else:
            self.woordenboek[product_name] = Product(product_name, [], holding_cost, stockout_penalty)  #nieuw product aanmaken, batches start als lege lijst

    def restock_product(self, product_name, quantity,cost_per_unit):
        if product_name not in self.woordenboek:
            return f"Product {product_name} not found."
        else:
            self.woordenboek[product_name].add_batch(quantity,cost_per_unit) #nieuwe batch toevoegen,lifo stock

    def simulate_demand(self,min_demand,max_demand):
        vragenboek={} #{product_name:vraag}
        for product in self.woordenboek:
            demand=random.randint(min_demand,max_demand)
            vragenboek[product]=demand
        return vragenboek #return alle vragen

    def simulate_day(self,demand):
        stockoutkost=0 #totale stockout penalty voor deze dag
        aanhoudkost=0  #totale holdingcost voor deze dag
        for product in demand:
            vraag=demand[product] #gevraagde hoeveelheid
            produkt=self.woordenboek[product] #het productobject
            totaal=0

            for batch in produkt.batches:
                totaal+=batch.quantity #totale voorraad= som van alle batch quantities
            if totaal>=vraag: #voldoende voorraad --> holding cost voor overschot
                holding_cost=produkt.holding_cost
                aanhoudkost+=(totaal-vraag)*holding_cost
            else: #onvoldoende voorraad --> stockout penalty voor tekort
                stockout=produkt.stockout_penalty
                stockoutkost+=(vraag-totaal)*stockout
        return aanhoudkost,stockoutkost

    def save_to_csv(self,filename):
        output=open(filename,"w") #bestand openen in schrijfmodus
        resultaat="" #startstring is lege string
        for product in self.woordenboek: #elke product-batch opschrijven als 1 regel
            for batch in self.woordenboek[product].batches:
                resultaat+=f"{product},{batch.quantity},{batch.cost_per_unit}\n"
        resultaat=resultaat.strip('\n') #laatste nieuwe lijn verwijderen
        output.write(resultaat)
        output.close()

    def load_from_csv(self,filename):
        output=open(filename,"r") #bestand openen in leesmodus
        for line in output:
            product_name,quantity,cost_per_unit=line.strip().split(",") #regel splitsen in 3 waarden
            quantity=int(quantity)
            cost_per_unit=float(cost_per_unit)
            if product_name not in self.woordenboek: #product nog niet in voorraad --> eerst toevoegen
                self.add_product(product_name,quantity,cost_per_unit)
            self.restock_product(product_name,quantity,cost_per_unit) #batch toevoegen aan product

    def print_inventory(self):
        resultaat="Current Inventory:\n"
        for product in self.woordenboek: #voor elk product tonene welke batches erin zitten
            resultaat+=f"Product {product}:\n"
            for batch in self.woordenboek[product].batches:
                resultaat+=f"\t{batch}\n" #batch-object heeft eigen __str__()
            resultaat+="\n"
        return resultaat

def main():
    # 1. Maak een nieuwe Inventory Manager aan
    manager = Inventory_Manager()

    # 2. Voeg twee producten toe aan het systeem
    # add_product(product_name, holding_cost, stockout_penalty)
    manager.add_product("Widget", 0.5, 10)
    manager.add_product("Gadget", 1.0, 8)

    # 3. Voeg batches toe aan deze producten (restock)
    # restock_product(name, quantity, cost_per_unit)
    manager.restock_product("Widget", 100, 2.5)
    manager.restock_product("Widget", 50, 2.0)
    manager.restock_product("Gadget", 70, 3.0)

    # 4. Toon de voorraad voor alle producten
    print(manager.print_inventory())

    # 5. Simuleer een willekeurige vraag voor elk product
    # simulate_demand(min, max) → dictionary {product_name : demand}
    demand = manager.simulate_demand(0, 20)
    print("Simulated demand:", demand)

    # 6. Simuleer 1 dag en bereken holding_cost + stockout_cost
    holding, stockout = manager.simulate_day(demand)
    print("Total holding cost:", holding)
    print("Total stockout penalty:", stockout)

    # 7. Sla de voorraad op in een CSV-bestand
    manager.save_to_csv("inventory.csv")

    # 8. Test: laad terug in uit CSV (optioneel)
    print("\nLoading inventory from CSV again:")
    manager2 = Inventory_Manager()
    manager2.load_from_csv("inventory.csv")
    print(manager2.print_inventory())


# Verplicht: enkel uitvoeren als dit bestand direct wordt gerund
if __name__ == "__main__":
    main()









