import json
import matplotlib.pyplot as plt

class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.generation = None
        self.population = None
        self.scores = None
        self.max_tiles = None
        self.max_dict = None

    def load_data(self):
        with open(self.filename, "r") as file:
            data = json.load(file)
            self.generation = data.get("generation")
            self.population = data.get("population")
            self.scores = data.get("scores")
            self.max_tiles = data.get("max_tiles")
            self.max_dict = data.get("max_dict")

# Przykład użycia:
loader1 = DataLoader("test_random.json")
loader2 = DataLoader("test_no_random.json")
loader1.load_data()
loader2.load_data()

def plot_bar_chart(data):
    labels = list(data.keys())
    values = list(data.values())

    plt.bar(labels, values)
    plt.xlabel("Tiles")
    plt.ylabel("Counts")
    plt.title("Count Tiles per generation")



# plot_bar_chart(loader1.max_dict)
plot_bar_chart(loader2.max_dict)
plt.show()
