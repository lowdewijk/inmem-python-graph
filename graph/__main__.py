import random
import time
from tqdm import tqdm
from typing import Any
from graph.Graph import Graph, VertexId
import sys

def mk_random_vertex_properties() -> dict[str, Any]:
  dict = { 
    "first": "John",
    "last": "Doe",
    "age": 42,
    "address": {
      "street": "Main Street",
      "number": 123,
      "city": "New York"
    },
    "phone": [
      "+1-123-456-7890",
      "+1-098-765-4321"
    ],
    "email": "john@doe.com",
    "isAlive": True,
    "height_cm": 180.5,
    "favorite_colors": ["red", "blue", "green"],
    "favorite_foods": ["pizza", "hamburger", "sushi"],
  }
  return dict

def main(vertex_count: int, edge_count: int) -> None:
  g = Graph()

  print(f"Adding {vertex_count} vertices (with a bunch of properties)...")
  tic = time.perf_counter()
  for _ in tqdm(range(vertex_count)):
    v = g.mk_vertex("v", mk_random_vertex_properties())
    g.add_vertex(v)
  toc = time.perf_counter()
  print(f"Added {vertex_count} vertices in {toc - tic:0.4f} seconds")

  print(f"Adding {edge_count} edges (without properties)...")
  tic = time.perf_counter()
  for _ in tqdm(range(edge_count)):
    src = VertexId(random.randint(1, vertex_count))
    dst = VertexId(random.randint(1, vertex_count))
    g.add_edge(g.mk_edge(src, dst, "e"))
  toc = time.perf_counter()
  print(f"Added {edge_count} edges in {toc - tic:0.4f} seconds")

  print(f"Saving graph...")
  tic = time.perf_counter()
  g.save("graph.pickle")
  toc = time.perf_counter()
  print(f"Saved graph in {toc - tic:0.4f} seconds")

  print(f"Loading graph...")
  tic = time.perf_counter()
  g = Graph.load("graph.pickle")
  toc = time.perf_counter()
  print(f"Loaded graph in {toc - tic:0.4f} seconds")

if __name__ == "__main__":
  main(int(sys.argv[1]), int(sys.argv[2]))