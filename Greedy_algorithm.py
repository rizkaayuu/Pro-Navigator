import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import PriorityQueue
import tkinter as tk
from tkinter import ttk, messagebox

class CityNotFoundError(Exception):
    def __init__(self, city):
        self.message = f"{city} tidak ditemukan."
        super().__init__(self.message)

class PathNotFoundError(Exception):
    def __init__(self, info):
        self.message = f"Jalur antara {info} tidak ditemukan di peta. Coba lagi!!."
        super().__init__(self.message)

def build_graph(path):
    try:
        Map = {}
        with open(path, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) 
            for row in csv_reader:
                city1 = row[0].strip().lower()
                city2 = row[1].strip().lower()
                distance = int(row[2])

                if city1 not in Map:
                    Map[city1] = {}
                if city2 not in Map:
                    Map[city2] = {}

                Map[city1][city2] = distance
                Map[city2][city1] = distance

        return Map
    except FileNotFoundError:
        messagebox.showerror("Error", "File tidak ditemukan.")
        raise

def greedy_shortest_path(graph, start, goal):
    start = start.lower()
    goal = goal.lower()

    if start not in graph:
        raise CityNotFoundError(start)
    if goal not in graph:
        raise CityNotFoundError(goal)

    visited = set()  
    path = [start]   
    total_cost = 0   
    
    current = start
    while current != goal:
        visited.add(current)
        
        neighbors = graph[current].items()
        next_node, min_cost = None, float('inf')
        for neighbor, cost in neighbors:
            if neighbor not in visited and cost < min_cost:
                next_node, min_cost = neighbor, cost
        
        if next_node is None:
            raise PathNotFoundError(f"{start} ke {goal}")
        
        path.append(next_node)
        total_cost += min_cost
        current = next_node
    
    return total_cost, path

def visualize_graph(graph, path=[], start=None, goal=None):
    G = nx.Graph()
    for city in graph:
        for neighbor in graph[city]:
            G.add_edge(city, neighbor, weight=graph[city][neighbor])

    pos = nx.spring_layout(G, seed=42)  
    weights = nx.get_edge_attributes(G, 'weight')

    start = start.lower() if start else None
    goal = goal.lower() if goal else None

    node_colors = []
    for node in G.nodes:
        if node == start:
            node_colors.append("blue")  
        elif node == goal:
            node_colors.append("red")  
        else:
            node_colors.append("skyblue")  

    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(
        G, pos, with_labels=True, ax=ax, 
        node_size=150, node_color=node_colors, 
        font_size=10, font_weight='bold'
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, ax=ax)

    if path:
        edge_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color='r', width=2, ax=ax)
    if goal:
        goal_pos = pos[goal]  
        ax.plot(
            goal_pos[0], goal_pos[1], 
            marker="o", markersize=15, color="red", 
            markeredgecolor="black", markeredgewidth=1
        )
        ax.annotate("📍", (goal_pos[0], goal_pos[1]), fontsize=14, ha='center')

    ax.set_title("Graf Jaringan Kota")
    return fig


def show_graph(fig):
    for widget in graph_frame.winfo_children():
        widget.destroy() 

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def find_path():
    start_city = start_entry.get().strip().lower()  
    end_city = end_entry.get().strip().lower()      

    try:
        distance, road_way = greedy_shortest_path(graph, start_city, end_city)
        formatted_route = '\n'.join([' → '.join(road_way[i:i+4]) for i in range(0, len(road_way), 4)])

        result_label_distance.config(text=f"{distance} Km", fg='red', font=('Arial', 17))
        result_label_distance_title.config(text="Jarak minimal yang Anda tempuh adalah", font=('Arial', 12))
        
        result_label_route.config(text=f"Dengan rute tercepat yang dilalui: \n{formatted_route}", font=('Arial', 12))

        fig = visualize_graph(graph, road_way, start=start_city, goal=end_city)

        show_graph(fig)

    except CityNotFoundError as e:
        messagebox.showerror("Error", str(e))
    except PathNotFoundError as e:
        messagebox.showerror("Error", str(e))



def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Pencarian Jalur Terpendek dengan Algoritma Greedy")

root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

try:
    graph = build_graph("kota_jatimm.csv")
except FileNotFoundError:
    exit()  

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame = tk.Frame(main_frame)
input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

graph_frame = tk.Frame(main_frame)
graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

welcome_label = tk.Label(input_frame, text="Selamat datang di Greedy Pro Navigator!\nPencarian rute tercepat berbasis algoritma Greedy", font=('Arial', 15), justify=tk.LEFT)
welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

tk.Label(input_frame, text="Kota Asal  :", font=('Arial', 12)).grid(row=1, column=0 , padx=10, pady=10, sticky=tk.W)
start_entry = tk.Entry(input_frame, width=30, font=('Arial', 12))
start_entry.grid(row=1, column=1, padx=20, pady=10, sticky=tk.W+tk.E)

tk.Label(input_frame, text="Kota Tujuan  :",font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
end_entry = tk.Entry(input_frame, width=30, font=('Arial', 12))
end_entry.grid(row=2, column=1, padx=20, pady=10, sticky=tk.W+tk.E)

search_button = tk.Button(input_frame, text="Cari Jalur", font=('Arial', 11), command=find_path)
search_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label_distance_title = tk.Label(input_frame, text="", font=('Arial', 12, 'bold'))
result_label_distance_title.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
result_label_distance = tk.Label(input_frame, text="", font=('Arial', 16, 'bold'), fg='red')
result_label_distance.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
result_label_route = tk.Label(input_frame, text="", font=('Arial', 12))
result_label_route.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

fig = visualize_graph(graph)
show_graph(fig)

root.mainloop()