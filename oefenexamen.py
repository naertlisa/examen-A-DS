import csv


class Node:
    def __init__(self, task_name, duration, priority):
        self.task_name = task_name  # naam van de taak (string)
        self.duration = duration  # duur van de taak in minuten (int)
        self.priority = priority  # prioriteit (1=hoogste)
        self.next = None  # verwijzen naar volgende node

    def __repr__(self):
        return f"{self.task_name} (duur: {self.duration}, prioriteit: {self.priority})"

class LinkedList:  # hulpsysteem dat eerste element (head) onthoudt en methodes aanbiedt om keten te beheren
    def __init__(self):
        self.head = None

    def add_task(self, task_name, duration, priority):
        new_node = Node(task_name, duration, priority)
        if self.head is None:  # als er nog niets in de lijst zit, wordt dit de eerste node
            self.head = new_node
        else:  # als er al nodes in lijst zitten
            current_node = self.head
            while current_node.next:  # zolang er nog een volgende node bestaat, ga verder
                current_node = current_node.next
            current_node.next = new_node  # hang de nieuwe node eraan

    def remove_task(self, task_name):
        current_node = self.head #begin bij het eerste element
        previous_node = None #houd bij wat vorige node was
        while current_node:
            if current_node.task_name == task_name:
                if previous_node:
                    previous_node.next=current_node.next #sla huidige node (current) over
                else:
                    self.head=current_node.next #als eerste node de juiste is, is er geen vorige node dus verschuif gewoon begin van lijst naar tweede node
                return True #taak gevonden en verwijderd
            previous_node = current_node #schuif previous node 1 stap op
            current_node = current_node.next #schuif current node 1 stap op
        return False #taak niet gevonden

    def display_tasks(self):
        current_node = self.head
        while current_node: #zolang er nog een node bestaat
            print(current_node)
            current_node = current_node.next

    def find_task(self,task_name):
        current_node = self.head
        while current_node: #zolang er nog een node bestaat
            if current_node.task_name == task_name: #als taaknaam van current node = gezochte taak
                return current_node
            current_node=current_node.next
        return None

    def calculate_total_duration(self):
        current_node = self.head
        duration=0
        while current_node: #zolang er nog een node bestaat
            duration+=current_node.duration #tel de duur van current node bij totaal
            current_node = current_node.next #ga naar volgende node
        return duration

    def read_tasks_from_csv(self, file_path):
        with open(file_path,newline='',encoding='utf-8') as csvfile:
            reader=csv.reader(csvfile) #zet elke regel van bestand om in lijst van strings
            next(reader) #sla de eerste regel over (bevat meestal kolomnamen, willen we niet toevoegen als taak)
            for row in reader: #row haalt telkens 1 rijtje op
                task_name,duration,priority=row
                self.add_task(task_name,int(duration),int(priority)) #toeveoegen aan linked list, add_task zorgt ervoor dat er vanzelf node wordt aangemaakt

    def sorted_insert_by_priority(self,head,new_node): #hulpfunctie: voeg node gesorteerd in op basis van prioriteit (kleinste eerst)
        if head is None or new_node.priority < head.priority: #als de lijst leeg is of als de nieuwe node lagere prioriteit heeft dan huidige node
            new_node.next=head #nieuwe node wordt eerste node
            return new_node
        current_node = head #beginnen bij begin van lijst om juiste plek te zoeken
        while current_node.next and current_node.next.priority <= new_node.priority: #zolang er een volgende node bestaat en priority van volgende node <= nieuwe node
            current_node=current_node.next #lopen we verder
        new_node.next=current_node.next #stoppen wanneer je voorbij alle nodes bent met lagere/even prioriteit en precies op node waar new_node achter moet worden geplaatst
        current_node.next=new_node
        return head #omdat hoofd van de lijst niet veranderd is (behalve in eerste geval)

    def sorted_insert_by_priority_duration(self,head, new_node):  # hulpfunctie: voeg node gesorteerd in op basis van prioriteit en duur (bij gelijke prioriteit, kortste duur eerst)
        # we zetten nieuwe node helemaal vooraan als: de lijst leeg is, de nieuwe node betere prioriteit heeft, nieuwe node dezelfde prioriteit maar kortere duur heeft
        if head is None or (new_node.priority < head.priority) or (new_node.priority == head.priority and new_node.duration < head.duration):
            new_node.next = head
            return new_node
        current_node = head  # door de lijst lopen
        # while: stap verder zolang volgende node lagere prioriteit heeft of zelfde prioriteit maar korter of even lang
        while current_node.next and (current_node.next.priority < new_node.priority or (current_node.next.priority == new_node.priority and current_node.next.duration <= new_node.duration)):
            current_node = current_node.next
        new_node.next = current_node.next  # nieuwe node naar volgende laten wijzen
        current_node.next = new_node  # current laten wijzen naar nieuwe node
        return head
    def reorder_tasks_by_priority(self):
        new_head = None #dit wordt de gesorteerde lijst (niet-recursief)
        current_node = self.head #begin bij de eerste node van de oude lijst
        while current_node: #"zolang we nodes hebben in de oude lijst"
            next_node=current_node.next #bewaar volgende node --> want we gaan huidige node losmaken van oude lijst
            current_node.next = None #maak node los --> zit niet maar vast aan oude keten
            new_head=self.sorted_insert_by_priority(new_head, current_node) #plaats node toe op juiste plek in nieuwe lijst(laagste prioriteit eerst)
            current_node = next_node #ga verder met volgende node (doorgaan tot alle nodes verwerkt zijn)
        self.head=new_head #dit is je gelinkte lijst gesorteerd

    def reorder_tasks_by_priority_duration(self):
        new_head = None #beginnen met lege nieuwe gesorteerde lijst
        current_node = self.head #we beginnen bij eerste node van originele lijst
        while current_node: #we gaan door elke node tot het einde
            next_node=current_node.next #onthouden waar volledige ketting verdergaat, want we gaan node losmaken
            current_node.next = None #node losmaken van oorspronkelijke lijst
            new_head= self.sorted_insert_by_priority_duration(new_head, current_node) #node current toevoegen in nieuwe lijst op correcte sorteervolgorde
            current_node=next_node #we gaan verder met volgende node uit oude lijst (next_node bevat volgende wagonnetje)
        self.head=new_head #originele lijst wordt volledig vervangen door de gesorteerde





