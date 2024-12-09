import heapq
import tkinter as tk
from tkinter import messagebox, simpledialog

class Department:
    def __init__(self, name, beds, equipment):
        self.name = name
        self.beds = beds
        self.equipment = equipment

class Edge:
    def __init__(self, department1, department2, distance):
        self.department1 = department1
        self.department2 = department2
        self.distance = distance

class HospitalResourceAllocator:
    def __init__(self):
        self.departments = []
        self.edges = []

    def add_department(self, name, beds, equipment):
        department = Department(name, beds, equipment)
        self.departments.append(department)

    def add_edge(self, department1, department2, distance):
        edge = Edge(department1, department2, distance)~
        self.edges.append(edge)

    def prim_algorithm(self):
        mst = []
        visited = set()
        start_department = self.departments[0]

        visited.add(start_department)
        priority_queue = [(0, start_department)]

        while priority_queue:
            distance, current_department = heapq.heappop(priority_queue)

            if current_department not in visited:
                visited.add(current_department)
                mst.append(current_department)

                for edge in self.edges:
                    if edge.department1 == current_department and edge.department2 not in visited:
                        heapq.heappush(priority_queue, (edge.distance, edge.department2))
                    elif edge.department2 == current_department and edge.department1 not in visited:
                        heapq.heappush(priority_queue, (edge.distance, edge.department1))

        return mst

    def allocate_resources(self):
        mst = self.prim_algorithm()
        total_beds = sum(department.beds for department in mst)
        total_equipment = sum(department.equipment for department in mst)
        return mst, total_beds, total_equipment

# Tkinter Application
class HospitalResourceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Resource Allocator")
        self.hospital = HospitalResourceAllocator()

        # Create buttons and labels
        self.add_department_button = tk.Button(root, text="Add Department", command=self.add_department)
        self.add_edge_button = tk.Button(root, text="Add Edge", command=self.add_edge)
        self.allocate_resources_button = tk.Button(root, text="Allocate Resources", command=self.allocate_resources)
        self.quit_button = tk.Button(root, text="Quit", command=root.destroy)

        self.departments_label = tk.Label(root, text="Departments:")
        self.departments_listbox = tk.Listbox(root)
        self.edges_label = tk.Label(root, text="Edges:")
        self.edges_listbox = tk.Listbox(root)

        # Place widgets on the grid
        self.add_department_button.grid(row=0, column=0)
        self.add_edge_button.grid(row=0, column=1)
        self.allocate_resources_button.grid(row=0, column=2)
        self.quit_button.grid(row=0, column=3)
        self.departments_label.grid(row=1, column=0)
        self.departments_listbox.grid(row=2, column=0, rowspan=4)
        self.edges_label.grid(row=1, column=1)
        self.edges_listbox.grid(row=2, column=1, rowspan=4)

    def add_department(self):
        name = simpledialog.askstring("Add Department", "Enter department name:")
        beds = int(simpledialog.askstring("Add Department", "Enter number of beds:"))
        equipment = int(simpledialog.askstring("Add Department", "Enter amount of equipment:"))
        if name:
            self.hospital.add_department(name, beds, equipment)
            self.departments_listbox.insert(tk.END, name)

    def add_edge(self):
        department1 = simpledialog.askstring("Add Edge", "Enter department 1 name:")
        department2 = simpledialog.askstring("Add Edge", "Enter department 2 name:")
        distance = int(simpledialog.askstring("Add Edge", "Enter distance:"))
        if department1 and department2:
            self.hospital.add_edge(department1, department2, distance)
            self.edges_listbox.insert(tk.END, f"{department1} <-> {department2} (Distance: {distance})")

    def allocate_resources(self):
        try:
            mst, total_beds, total_equipment = self.hospital.allocate_resources()
            result = "\n".join([f"Allocating {department.beds} beds and {department.equipment} equipment to {department.name}" for department in mst])
            result += f"\nTotal Beds Allocated: {total_beds}\nTotal Equipment Allocated: {total_equipment}"
            messagebox.showinfo("Resource Allocation", result)
        except IndexError:
            messagebox.showwarning("Error", "Add at least one department and edge before allocating resources.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalResourceApp(root)
    root.mainloop()