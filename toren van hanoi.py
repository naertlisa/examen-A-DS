def verplaats(n, start, eind, hulp):
    if n == 1:
        print(f"Schijf 1 van {start} naar {eind}")
        return 1
    else:
        stappen1 = verplaats(n - 1, start, hulp, eind)
        print(f"Schijf {n} van {start} naar {eind}")
        stappen2 = verplaats(n - 1, hulp, eind, start)
        return stappen1 + 1 + stappen2

def hanoi(n):
    totaal = verplaats(n, 'A', 'C', 'B')
    print(f"{totaal} stappen gedaan")
    # geen return: functie geeft None terug (zoals de tests verwachten)
