import heapq

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

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, department1, department2, distance):
        if department1 not in self.graph:
            self.graph[department1] = []
        if department2 not in self.graph:
            self.graph[department2] = []
        edge = Edge(department1, department2, distance)
        self.graph[department1].append(edge)
        self.graph[department2].append(edge)

class HospitalResourceAllocator:
    def __init__(self):
        self.departments = {}
        self.graph = Graph()

    def add_department(self, name, beds, equipment):
        department = Department(name, beds, equipment)
        self.departments[name] = department

    def add_edge(self, department1, department2, distance):
        self.graph.add_edge(self.departments[department1], self.departments[department2], distance)

    def prim_algorithm(self, start_department):
        mst = set()
        visited = set([start_department])
        edges = [
            (edge.distance, edge.department2)
            for edge in self.graph.graph[start_department]
        ]
        heapq.heapify(edges)

        while edges:
            distance, department = heapq.heappop(edges)
            if department not in visited:
                visited.add(department)
                mst.add(department)
                for edge in self.graph.graph[department]:
                    if edge.department2 not in visited:
                        heapq.heappush(edges, (edge.distance, edge.department2))

        return mst

    def allocate_resources(self, start_department):
        mst = self.prim_algorithm(self.departments[start_department])
        total_beds = sum(department.beds for department in mst)
        total_equipment = sum(department.equipment for department in mst)
        return mst, total_beds, total_equipment

def main():
    hospital = HospitalResourceAllocator()

    while True:
        print("1. Add Department")
        print("2. Add Edge")
        print("3. Allocate Resources")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            name = input("Enter department name: ")
            beds = int(input("Enter number of beds: "))
            equipment = int(input("Enter amount of equipment: "))
            hospital.add_department(name, beds, equipment)
        elif choice == 2:
            department1 = input("Enter department 1 name: ")
            department2 = input("Enter department 2 name: ")
            distance = int(input("Enter distance: "))
            hospital.add_edge(department1, department2, distance)
        elif choice == 3:
            start_department = input("Enter start department name: ")
            mst, total_beds, total_equipment = hospital.allocate_resources(start_department)
            print(f"Total Beds Allocated: {total_beds}")
            print(f"Total Equipment Allocated: {total_equipment}")
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()