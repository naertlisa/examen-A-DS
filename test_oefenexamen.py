from oefenexamen import LinkedList
tasks=LinkedList()
print("===Test:add_task==")
tasks.add_task("Verpakken",30,2)
tasks.add_task("Inspectie",10,1)
tasks.add_task("Transport",45,3)
tasks.display_tasks()

print("\n=== TEST: find_task ===")
found = tasks.find_task("Inspectie")
print("Gevonden taak:", found)

print("\n=== TEST: calculate_total_duration ===")
print("Totale duur:", tasks.calculate_total_duration())

print("\n=== TEST: remove_task ===")
tasks.remove_task("Verpakken")
tasks.display_tasks()

print("\n=== TEST: reorder_tasks_by_priority ===")
tasks.reorder_tasks_by_priority()
tasks.display_tasks()

print("\n=== TEST: reorder_tasks_by_priority_duration ===")
tasks.reorder_tasks_by_priority_duration()
tasks.display_tasks()

print("\n=== TEST: read_tasks_from_csv ===")
new_list = LinkedList()
new_list.read_tasks_from_csv("tasks.csv")
new_list.display_tasks()
