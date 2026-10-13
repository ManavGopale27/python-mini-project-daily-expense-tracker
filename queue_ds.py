# queue_ds.py
# Contains the custom linked-list Queue  (Custom Data Structure requirement)

class Node:
    """
    A single node for the linked list.
    Holds the data and a pointer to the next node.
    """

    def __init__(self, data):
        self.data = data
        self.next = None   # points to the next Node


class CustomQueue:
    """
    A basic Queue implemented using a singly linked list.
    enqueue() adds to the rear, dequeue() removes from the front.
    This is FIFO (First In, First Out).
    We are NOT using Python's built-in list or queue module.
    """

    def __init__(self):
        self.front = None   # points to the first node
        self.rear  = None   # points to the last node
        self.size  = 0

    def enqueue(self, item):
        # Create a new node with the given item
        new_node = Node(item)

        # If queue is empty, front and rear both point to new node
        if self.rear is None:
            self.front = new_node
            self.rear  = new_node
        else:
            # Attach new node at the end and move rear forward
            self.rear.next = new_node
            self.rear      = new_node

        self.size += 1

    def dequeue(self):
        # If queue is empty, nothing to remove
        if self.front is None:
            return None

        # Save the data from the front node
        removed_data = self.front.data

        # Move front one step forward
        self.front = self.front.next

        # If front became None, queue is empty so reset rear too
        if self.front is None:
            self.rear = None

        self.size -= 1
        return removed_data

    def is_empty(self):
        return self.size == 0
