from Main.model.searchproblem.search_node import SearchNode
from Main.model.data_structure.stack import Stack


def test_empty_stack():
    stack = Stack()
    assert stack.is_empty()

def test_add_stack():
    stack = Stack()
    node = SearchNode(5, None, None, None)
    assert stack.add(node) == node
    assert not stack.is_empty()

def test_top_stack():
    stack = Stack()
    assert stack.top() is None

    node = SearchNode(5, None, None, None)
    stack.add(node)
    assert stack.top() == node
    assert not stack.is_empty()

def test_pop_stack():
    stack = Stack()
    assert stack.pop() is None

    node = SearchNode(5, None, None, None)
    stack.add(node)
    assert not stack.is_empty()
    assert stack.pop() is node
    assert stack.is_empty()


def test_combined_stack():
    stack = Stack()

    one = SearchNode(1, None, None, None)
    two = SearchNode(2, None, None, None)
    three = SearchNode(3, None, None, None)

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
