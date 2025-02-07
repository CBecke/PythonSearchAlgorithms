from multiprocessing.context import assert_spawning

from Main.search.data_structure.node import Node
from Main.search.data_structure.stack import Stack


def test_empty_stack():
    stack = Stack()
    assert stack.is_empty()

def test_add_stack():
    stack = Stack()
    node = Node(5, None, None, None)
    assert stack.add(node) == node
    assert not stack.is_empty()

def test_top_stack():
    stack = Stack()
    assert stack.top() is None

    node = Node(5, None, None, None)
    stack.add(node)
    assert stack.top() == node
    assert not stack.is_empty()

def test_pop_stack():
    stack = Stack()
    assert stack.pop() is None

    node = Node(5, None, None, None)
    stack.add(node)
    assert not stack.is_empty()
    assert stack.pop() is node
    assert stack.is_empty()


def test_combined_stack():
    stack = Stack()

    one = Node(1, None, None, None)
    two = Node(2, None, None, None)
    three = Node(3, None, None, None)

    assert stack.add(one) == one
    assert stack.add(two) == two
    assert stack.top() == two
    assert stack.add(three) == three
    assert stack.pop() == three
    assert stack.top() == two
    assert stack.pop() == two
    assert not stack.is_empty()
    assert stack.pop() == one
    assert stack.is_empty()
