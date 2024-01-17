# 126 LOC in-memory Python graph database

Do you think you need a graph database right now?

Maybe you do, maybe you don't. 

As long as your graph:
 * Does not need [durability](https://en.wikipedia.org/wiki/Durability_(database_systems)).
 * Contains less than a few hundred thousands vertices and edges.
 * Does not need require super complicated queries that would require a bunch of indices.

It may just be overkill. Here is a small Python project you can use as a testbed.

# Install and run

```bash
 $ nix develop
 $ pip install -e .
 $ python -m graph 1000000 1000000
```

This will create, save and load a graph of 1m vertices and 1m edges with some random attached to it.

On a my old 2019 MacBook Pro saving and loading a graph that size costs ~20 seconds.