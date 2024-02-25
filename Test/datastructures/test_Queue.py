from Main.datastructures.Queue import Queue


def test_empty():
    queue = Queue()

    assert queue.size == 0

def test_queue():
    queue = Queue([1,2,3])

    assert queue.size == 3

    queue.push(4)
    queue.push(5)

    assert queue.size == 5
    popped = queue.pop()

    assert queue.size == 4
    assert popped == 1

    queue.push(6)

    for i in range(queue.size):
        assert queue.pop() == i + 2
    assert queue.size == 0
