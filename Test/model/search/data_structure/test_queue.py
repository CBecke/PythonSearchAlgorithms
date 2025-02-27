
from Main.model.search.data_structure.node import Node
from Main.model.search.data_structure.queue import Queue


def test_empty_queue():
    queue = Queue()
    assert queue.is_empty()

def test_add_queue():
    queue = Queue()
    node = Node(5, None, None, None)
    assert queue.add(node) == node
    assert not queue.is_empty()

def test_top_queue():
    queue = Queue()
    assert queue.top() is None

    node = Node(5, None, None, None)
    queue.add(node)
    assert queue.top() == node
    assert not queue.is_empty()

def test_pop_queue():
    queue = Queue()
    assert queue.pop() is None

    node = Node(5, None, None, None)
    queue.add(node)
    assert not queue.is_empty()
    assert queue.pop() is node
    assert queue.is_empty()


def test_combined_queue():
    queue = Queue()

    one = Node(1, None, None, None)
    two = Node(2, None, None, None)
    three = Node(3, None, None, None)

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
