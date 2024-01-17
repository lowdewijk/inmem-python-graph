from graph.Graph import Edge, Graph, VertexId
import tempfile
import os

def mk_simple_graph() -> Graph:
  g = Graph()
  v1 = g.mk_vertex("v", { "foo": "bar" })
  v2 = g.mk_vertex("v", { "baz": "qux" })
  return g \
    .add_vertices([v1, v2]) \
    .add_edge(g.mk_edge(v1.id, v2.id, "e", { "a": "b" }))

def mk_simple_graph_dup_edge() -> Graph:
  g = mk_simple_graph()
  return g.add_edge(g.mk_edge(VertexId(1), VertexId(2), "e2", { "a": "b" }))

def serder_graph(g: Graph) -> Graph:
  with tempfile.TemporaryDirectory() as tmpdirname:
    filepath = os.path.join(tmpdirname, "graph.pickle")
    g2 = Graph.load(g.save(filepath))
    assert str(g) == str(g2)
  return g2

def test_simplest_graph() -> None:
  g = mk_simple_graph()
  assert len(g.get_vertex_ids()) == 2
  assert len(g.get_edge_ids()) == 1
  v1 = g.get_vertex(VertexId(1))
  v2 = g.get_vertex(VertexId(2))
  assert v1 is not None
  assert v2 is not None
  assert v1.label == "v"
  assert v2.label == "v"
  assert v1.properties == { "foo": "bar" }
  assert v2.properties == { "baz": "qux" }
  e = g.get_edges(v1.id, v2.id)
  assert len(e) == 1
  assert e[0].label == "e"
  assert e[0].properties == { "a": "b"}

def test_simplest_graph_serialization() -> None:
  serder_graph(mk_simple_graph())

def test_graph_eq() -> None:
  assert mk_simple_graph() == mk_simple_graph()
  assert mk_simple_graph() != Graph()
  s = mk_simple_graph()
  s.add_vertex(s.mk_vertex("v", { "foo": "bar" }))
  assert mk_simple_graph() != s
  s = mk_simple_graph()
  v1 = s.get_vertex(VertexId(1))
  assert v1 is not None
  v1.label = "w"
  assert mk_simple_graph() != s

def test_graph_dup_edges() -> None:
  g = mk_simple_graph_dup_edge()

  def test_get_edges(edges: list[Edge]) -> None:
    assert len(edges) == 2
    assert edges[0].label == "e"
    assert edges[1].label == "e2"

  test_get_edges(g.get_edges(VertexId(1), VertexId(2)))
  test_get_edges(g.get_src_edges(VertexId(1)))
  test_get_edges(g.get_dst_edges(VertexId(2)))

def test_graph_dup_edges_serialization() -> None:
    serder_graph(mk_simple_graph_dup_edge())
