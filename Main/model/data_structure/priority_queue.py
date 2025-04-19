
"""
I initially wanted to purposely over-engineer an efficient priority queue. Upon some reflection (see bottom), I decided
to implement skew heaps but only realized afterward how slow its decrease-key operation is. So I decided just to go with
a standard, dynamic array-based binary min-heap. It should be extra simple since python lists are dynamic arrays.
The implementation will be based on CLRS
"""
from Main.model.data_structure.frontier import Frontier
from Main.model.searchproblem.search_node import SearchNode


class PriorityQueue(Frontier):
    def __init__(self, search_problem, priority_function):
        """ The input priority_function is the (heuristic) function based on which the priority queue elements will
            be ordered. priority_function(search_problem, node) -> (float|int). """
        self.search_problem = search_problem
        self.f = priority_function # takes parameters: search_problem, node.

        self.heap = []
        # for each node in the heap, store its cost so the cost is only computed once
        self.node_costs = dict()

    def heap_size(self):
        return len(self.heap)

    def is_empty(self):
        return self.heap_size() == 0

    def pop(self):
        """ called "HEAP-EXTRACT-MAX" in CLRS [their example is max-heap, whereas this implementation is a min-heap].
            Returns a Node()"""
        if self.is_empty():
            return None

        min_value = self.heap[0]
        self.node_costs.pop(self.heap[0])
        self.heap[0] = self.heap[-1]
        # below we use list.pop() [and not PriorityQueue.pop()] to remove the tail element in O(1) time
        self.heap.pop()
        self.min_heapify(0)
        return min_value


    def top(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def add(self, node: SearchNode):
        self.heap.append(node)
        self.node_costs[node] = self.f(self.search_problem, node)
        self.heap_decrease_key(self.heap_size()-1, node)

    @staticmethod
    def parent(i):
        return int(i/2)

    @staticmethod
    def left(i):
        """ Given an index corresponding to an element in the heap, return the index of its left child. Does not check
            whether the child is within the heap."""
        return 2 * i + 1

    @staticmethod
    def right(i):
        """ Given an index corresponding to an element in the heap, return the index of its right child. Does not check
            whether the child is within the heap."""
        return 2 * i + 2

    def min_heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        smallest = i
        if l < self.heap_size() and self.cost(l) < self.cost(smallest):
            smallest = l
        if r < self.heap_size() and self.cost(r) < self.cost(smallest):
            smallest = r
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.min_heapify(smallest)

    def heap_decrease_key(self, i, node):
        """ sets the value of the element at index i to key and then makes sures the min-heap property is preserved. """
        cost = self.f(self.search_problem, node)
        if cost > self.cost(i):
            raise ValueError("new key is smaller than current key")
        self.node_costs[self.heap[i]] = cost
        while i > 0 and self.cost(self.parent(i)) > self.cost(i):
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)

    def cost(self, i):
        return self.node_costs[self.heap[i]]



"""
When deciding which data structure to use for my priority queue, my first thought was a min-heap. Quickly afterward I
remembered that Fibonacci heaps had better analytical running time. So I studied them in CLRS. But they seemed quite
complex. In edition 3 CLRS' chapter 19 chapter notes, they acknowledged that Fibonacci heaps had a lot of implementation
complexity, and referred to "relaxed heaps". I studied a bit and learned about the much simpler "skew heap" which has
similar run-time performance in practice. The following skew heap implementation is based on The 1986 article
"Self-Adjusting Heaps" by Sleator and Tarjan: https://www.cs.cmu.edu/~sleator/papers/adjusting-heaps.pdf.

So while Fibonacci heaps have better analytical runtime, in practice they are far more prone to bugs and not even
necessarily faster once constant factors are put into account, due to all the pointers. Skew heap is more practical.
However, I did want to implement my own priority queue (rather than using a python package) just to learn more about
heaps in practice.

class PriorityQueue(Frontier):
    # priority queue based on skew heaps. The priority queue is empty iff self.value = None.
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def is_empty(self):
        return self.value is None

    def pop(self):
        popped_value = self.value
        self.left.meld(self.right)
        return popped_value

    def top(self):
        # the value at the root; the minimum value in the priority queue (heap).
        return self.value

    def add(self, value):
        pushed_item_pq = PriorityQueue(value)
        self.meld(pushed_item_pq)

    def meld(self, other_pq):
        # melds the tree in place, in a top-down fashion.
        if self.is_empty():
            return other_pq
        elif other_pq.is_empty():
            return self

        # make h1 the heap with the lesser root, and h2 the one with the greater root
        h1, h2 = (self, other_pq) if (self.top() < other_pq.top()) else (other_pq, self)
        parent = h1

        while h1 is not None:
            # make h1 the lesser and h2 the greater of the two
            if h1.top() > h2.top():
                h1, h2 = h2, h1
            h1.swap_children()

            # make left child the smallest between h1.left and h2
            if h1.left is not None and h1.left.top() >= h2.top():
                temp = h2
                h2 = h1.left
                h1.left = temp

            parent = h1
            h1 = h1.left
        parent.left = h2


    def swap_children(self):
        # makes the left child the right child and vice versa.
        temp = self.right
        self.right = self.left
        self.left = temp
"""




