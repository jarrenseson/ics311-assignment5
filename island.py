import heapq
from collections import deque, defaultdict

class Island:
    def __init__(self, name, population, activityTime):
        self.name = name
        self.population = population
        self.last_visited = -float('inf')  # Initialize to a very old timestamp
        self.activityTime = activityTime

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

def optimizeActivities(graph, start):
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
