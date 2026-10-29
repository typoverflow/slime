"""MessageNode.leaves: depth-first leaf order, and no recursion limit on long sessions."""

from __future__ import annotations

import random

from slime.agent.trajectory import MessageNode


def _recursive_leaves(node: MessageNode) -> list[MessageNode]:
    if not node.children:
        return [node]
    return [leaf for c in node.children for leaf in _recursive_leaves(c)]


def test_leaves_keep_depth_first_order():
    rng = random.Random(0)
    root = MessageNode()
    nodes = [root]
    for i in range(300):  # random tree: forks at random depths
        nodes.append(rng.choice(nodes).add_child(MessageNode(role="user", message={"i": i})))
    assert list(root.leaves()) == _recursive_leaves(root)
    assert list(MessageNode().leaves())[0].is_root  # a lone root is its own leaf


def test_leaves_of_a_chain_deeper_than_the_recursion_limit():
    root = node = MessageNode()
    for i in range(5000):  # one node per message: a ~2500-turn agent session
        node = node.add_child(MessageNode(role="assistant" if i % 2 else "user", message={"i": i}))
    assert list(root.leaves()) == [node]
