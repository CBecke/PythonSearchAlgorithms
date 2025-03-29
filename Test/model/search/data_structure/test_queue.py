
from Main.model.searchproblem.search_node import SearchNode
from Main.model.search.data_structure.queue import Queue


def test_empty_queue():
    queue = Queue()
    assert queue.is_empty()

def test_add_queue():
    queue = Queue()
    node = SearchNode(5, None, None, None)
    assert queue.add(node) == node
    assert not queue.is_empty()

def test_top_queue():
    queue = Queue()
    assert queue.top() is None

    node = SearchNode(5, None, None, None)
    queue.add(node)
    assert queue.top() == node
    assert not queue.is_empty()

def test_pop_queue():
    queue = Queue()
    assert queue.pop() is None

    node = SearchNode(5, None, None, None)
    queue.add(node)
    assert not queue.is_empty()
    assert queue.pop() is node
    assert queue.is_empty()


def test_combined_queue():
    queue = Queue()

    one = SearchNode(1, None, None, None)
    two = SearchNode(2, None, None, None)
    three = SearchNode(3, None, None, None)

    assert queue.add(one) == one
    assert queue.add(two) == two
    assert queue.top() == one
    assert queue.add(three) == three
    assert queue.pop() == one
    assert queue.top() == two
    assert queue.pop() == two
    assert not queue.is_empty()
    assert queue.pop() == three
    assert queue.is_empty()
