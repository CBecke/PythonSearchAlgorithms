from Main.search.data_structure.node import Node
from Main.search.data_structure.priority_queue import PriorityQueue
from Main.searchproblem.search_problem import SearchProblem

[one, two, three, four, five, six, seven, nine, ten, fourteen] = [Node(None, None, None, None) for i in range(10)]

def dummy_heuristic(search_problem, node):
    values = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, nine: 9, ten: 10, fourteen: 14 }
    return values[node]

def test_min_heapify_no_change_priority_queue():
    # This heap already fulfills the min-heap property so it should remain the same
    pq = PriorityQueue(SearchProblem, dummy_heuristic)
    original = [one, two, three, six, nine, five, ten, fourteen]
    for node in original:
        pq.node_costs[node] = dummy_heuristic(node, node)

    # PriorityQueue.heap is supposed to be a private attribute, but we here abuse python visibility
    pq.heap = original.copy()

    for i in range(pq.heap_size()):
        pq.min_heapify(i)

    assert original == pq.heap

def test_min_heapify_priority_queue():
    # In this heap, the left child of the root does not fulfill the min-heap property, and therefore min-heapify should
    # change the heap.
    pq = PriorityQueue(SearchProblem, dummy_heuristic)
    faulty_original = [one, seven, three, four, six, nine, four, five, two] # [1, 7, 3, 4, 6, 9, 4, 5, 2]
    for node in faulty_original:
        pq.node_costs[node] = dummy_heuristic(node, node)

    # PriorityQueue.heap is supposed to be a private attribute, but we here abuse python visibility
    pq.heap = faulty_original.copy()

    for i in range(pq.heap_size()):
        pq.min_heapify(i)

    assert faulty_original != pq.heap
    assert pq.heap == [one, four, three, two, six, nine, four, five, seven] #[1, 4, 3, 2, 6, 9, 4, 5, 7]


def test_priority_queue():
    pq = PriorityQueue(SearchProblem, dummy_heuristic)
    assert pq.is_empty()

    pq.add(one)
    assert not pq.is_empty()
    assert pq.heap_size() == 1
    assert pq.top() == one

    pq.add(six)
    pq.add(nine)
    pq.add(three)
    assert pq.heap == [one, three, nine, six]

    assert pq.pop() == one
    assert pq.heap == [three, six, nine]
    assert pq.pop() == three
    assert pq.heap == [six, nine]

    pq.pop()
    pq.pop()
    assert pq.is_empty()


"""
# Test for skew heap
def test_meld_priority_queue():
    # example from figure 4 in https://www.cs.cmu.edu/~sleator/papers/adjusting-heaps.pdf

    ### left heap ###
    # nodes
    thirty_five = PriorityQueue(35)
    thirty_left = PriorityQueue(30)
    twenty = PriorityQueue(20)
    twenty_five = PriorityQueue(25)
    ten = PriorityQueue(10)
    thirteen = PriorityQueue(13)
    sixteen = PriorityQueue(16)
    fifty = PriorityQueue(50)
    one = PriorityQueue(1)

    # edges
    thirty_left.right = thirty_five
    twenty.right = thirty_left
    twenty.left = twenty_five
    ten.right = twenty
    ten.left = thirteen
    thirteen.right = sixteen
    one.right = ten
    one.left = fifty

    ### right heap ###
    # nodes
    five = PriorityQueue(5)
    nineteen = PriorityQueue(19)
    forty = PriorityQueue(40)
    twelve = PriorityQueue(12)
    thirty_right = PriorityQueue(30)
    fourteen = PriorityQueue(14)

    # edges
    twelve.left = thirty_right
    twelve.right = fourteen
    five.right = twelve
    five.left = nineteen
    nineteen.left = forty

    one.meld(five)
    one.meld(PriorityQueue(0))

    assert ((one.left.top(), one.right.top()) == (5, 50) and
             fifty.left is None and fifty.right is None and
            (five.left.top(), five.right.top()) == (10, 19) and
            nineteen.left.top() == 40 and nineteen.right is None and
            forty.left is None and forty.right is None and
            (ten.left.top(), ten.right.top()) == (12, 13) and
            thirteen.left is None and thirteen.right.top() == 16 and
            sixteen.left is None and sixteen.right is None and
            (twelve.left.top(), twelve.right.top()) == (14, 30) and
            thirty_right.left is None and thirty_right.right is None and
            fourteen.left.top() == 20 and fourteen.right is None and
            (twenty.left.top(), twenty.right.top()) == (25, 30) and
            twenty_five.left is None and twenty_five.right is None and
            thirty_left.left is None and thirty_left.right.top() == 35 and
            thirty_five.left is None and thirty_five.right is None)



"""