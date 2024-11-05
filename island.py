import heapq
from collections import deque, defaultdict

class Island:
    def __init__(self, name, population, activities):
        self.name = name
        self.population = population
        self.last_visited = -float('inf')  # Initialize to a very old timestamp
        self.activities = activities

    def __repr__(self):
        return f"Island(name={self.name}, population={self.population})"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

class WeightedGraph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

def optimizeActivities(graph, start, time_budget):
    max_activities = 0
    best_path = []
    counter = 0 
    
    pq = [(0, counter, start, [], 0, set())] 
    counter += 1
    
    while pq:
        current_time, _, current_node, path, activities_count, visited_nodes = heapq.heappop(pq)
        
        if current_time > time_budget:
            continue

        if activities_count > max_activities:
            max_activities = activities_count
            best_path = path

        for neighbor, travel_time in graph.graph[current_node]:
            if neighbor in visited_nodes:
                continue
            
            next_time = current_time + travel_time
            new_activities_count = activities_count
            
            for activity, enjoyment_time in neighbor.activities:
                if next_time + enjoyment_time <= time_budget:
                    next_time += enjoyment_time
                    new_activities_count += 1
            
            new_visited = visited_nodes | {neighbor}  
            new_path = path + [neighbor]  
            
            heapq.heappush(pq, (next_time, counter, neighbor, new_path, new_activities_count, new_visited))
            counter += 1
    
    return best_path, max_activities

'''
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph.graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph.graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances

class CanoeAllocator:
    def __init__(self):
        self.pq = []

    def allocate(self, island, distance):
        heapq.heappush(self.pq, (distance, island))

    def next_island(self):
        if self.pq:
            return heapq.heappop(self.pq)[1]
        return None

class CanoeJourney:
    def __init__(self):
        self.queue = deque()

    def add_canoe(self, canoe_id):
        self.queue.append(canoe_id)

    def next_canoe(self):
        if self.queue:
            return self.queue.popleft()
        return None

class ResourceTracker:
    def __init__(self):
        self.resources = defaultdict(int)

    def set_resources(self, island, amount):
        self.resources[island] = amount

    def update_resources(self, island, amount):
        self.resources[island] -= amount
        if self.resources[island] < 0:
            self.resources[island] = 0

    def get_resources(self, island):
        return self.resources[island]

def distribute_resources(graph, source, resources, canoes, allocator, journey_tracker, resource_tracker):
    distances = dijkstra(graph, source)
    print(f"Starting resource distribution from {source}...")

    for island in resources.keys():
        if island != source:
            allocator.allocate(island, distances[island])

    while any(resource_tracker.get_resources(island) > 0 for island in resources.keys()):
        remaining_resources = [resource_tracker.get_resources(island) for island in resources.keys()]
        print(f"Remaining resources check: {remaining_resources}")

        island = allocator.next_island()
        if not island:
            print("No more islands to allocate to.")
            break
        
        if resource_tracker.get_resources(island) > 0:
            canoe = journey_tracker.next_canoe()
            if canoe:
                print(f"Canoe {canoe} is delivering resources to {island} (Distance: {distances[island]})")
                resource_tracker.update_resources(island, 1)
                print(f"Remaining resources on {island}: {resource_tracker.get_resources(island)}")
                journey_tracker.add_canoe(canoe)
            if resource_tracker.get_resources(island) > 0:
                allocator.allocate(island, distances[island])


island_tahiti = Island("Tahiti", 205980, 10)
island_fiji = Island("Fiji", 902503, 2)
island_samoa = Island("Samoa", 196628, 1)
island_tonga = Island("Tonga", 104494, 19)
island_hawaii = Island("Hawaii", 1453138, 20)
island_niue = Island("Niue", 1600, 40)
island_cook_islands = Island("Cook Islands", 14222, 43)

graph = WeightedGraph()
graph.add_edge('IslandA', 'IslandB', 2)
graph.add_edge('IslandA', 'IslandC', 5)
graph.add_edge('IslandB', 'IslandC', 3)
graph.add_edge('IslandB', 'IslandD', 1)
graph.add_edge('IslandC', 'IslandD', 2)

resources = {'IslandB': 3, 'IslandC': 2, 'IslandD': 4}
canoes = 3

allocator = CanoeAllocator()
journey_tracker = CanoeJourney()
resource_tracker = ResourceTracker()

for island, amount in resources.items():
    resource_tracker.set_resources(island, amount)

for i in range(1, canoes + 1):
    journey_tracker.add_canoe(i)

distribute_resources(graph, 'IslandA', resources, canoes, allocator, journey_tracker, resource_tracker)
'''