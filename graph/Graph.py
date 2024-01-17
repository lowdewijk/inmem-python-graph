import os
from typing import Any, TypeVar, NewType, Tuple
from dataclasses import dataclass
import pickle

VertexId = NewType('VertexId', int)

K = TypeVar('K')
V = TypeVar('V')
def add_to_dict_list(dict: dict[K, list[V]], key: K, value: V) -> None:
  l = dict.get(key, [])
  l.append(value)
  dict[key] = l

@dataclass
class Edge:
  src: VertexId
  dst: VertexId
  label: str
  properties: dict[str, Any] | None = None


@dataclass
class Vertex:
  id: VertexId
  label: str
  properties: dict[str, Any]


@dataclass
class PickleGraph:
  id_seq: VertexId
  vertices: dict[VertexId, Vertex]
  edges: dict[Tuple[VertexId, VertexId], list[Edge]]
  
class Graph():
  id_seq: VertexId = VertexId(0)
  vertices: dict[VertexId, Vertex]
  edges: dict[Tuple[VertexId, VertexId], list[Edge]]
  srcs: dict[VertexId, list[Edge]]
  dsts: dict[VertexId, list[Edge]]

  def __init__(self) -> None:
    self.id_seq = VertexId(0)
    self.vertices = {}
    self.edges = {}
    self.srcs = {}
    self.dsts = {}

  def save(self, filepath: str | os.PathLike) -> str | os.PathLike:
    pg = PickleGraph(self.id_seq, self.vertices, self.edges)
    pickle.dump(pg, open(filepath, "wb"))
    return filepath

  @staticmethod
  def load(filepath: str | os.PathLike) -> "Graph":
    pg = pickle.load(open(filepath, "rb"))
    g = Graph()
    g.vertices = pg.vertices
    g.edges = pg.edges
    g.id_seq = pg.id_seq
    for edges in g.edges.values():
      for e in edges:
        add_to_dict_list(g.srcs, e.src, e)
        add_to_dict_list(g.dsts, e.dst, e)
    return g
    
  def mk_vertex(self, label: str, properties: dict[str, Any]):
    # start at 1, vertexId 0 is reserved for the empty vertex
    self.id_seq = VertexId(self.id_seq + 1) 
    return Vertex(self.id_seq, label, properties)
  
  def add_vertex(self, vertex: Vertex) -> "Graph":
    self.vertices[vertex.id] = vertex
    return self

  def add_vertices(self, vertices: list[Vertex]) -> "Graph":
    for vertex in vertices:
      self.add_vertex(vertex)
    return self

  def mk_edge(self, src: VertexId, dst: VertexId, label: str, properties: dict[str, Any] | None = None):
    return Edge(src, dst, label, properties)
  
  def add_edge(self, e: Edge) -> "Graph":
    if e.src not in self.vertices:
      raise ValueError(f"Cannot add edge. Vertex {e.src} is not in the graph.") 
    if e.dst not in self.vertices:
      raise ValueError(f"Cannot add edge. Vertex {e.dst} is not in the graph.")
    add_to_dict_list(self.edges, (e.src, e.dst), e)
    add_to_dict_list(self.srcs, e.src, e)
    add_to_dict_list(self.dsts, e.dst, e)
    return self
  
  def add_edges(self, edges: list[Edge]) -> "Graph":
    for edge in edges:
      self.add_edge(edge)
    return self

  def get_dst_edges(self, vertexId: VertexId) -> list[Edge]:
    return self.dsts[vertexId]

  def get_src_edges(self, vertexId: VertexId) -> list[Edge]:
    return self.srcs[vertexId]  
  
  def get_vertex_ids(self) -> list[VertexId]:
    return list(self.vertices.keys())
  
  def get_edge_ids(self) -> list[Tuple[VertexId, VertexId]]:
    return list(self.edges.keys())
  
  def get_vertex(self, vertexId: VertexId) -> Vertex | None:
    return self.vertices.get(vertexId)

  def get_edges(self, src: VertexId, dst: VertexId) -> list[Edge]:
    return self.edges.get((src, dst), [])

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Graph):
      return False
    return self.vertices == other.vertices \
        and self.edges == other.edges \
        and self.id_seq == other.id_seq

  def __str__(self) -> str:
    return f"Graph(vertices={self.vertices}, edges={self.edges}, id_seq={self.id_seq})"