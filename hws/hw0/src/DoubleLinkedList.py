import numpy as np

class BiNode():
    def __init__(self, prev, row, col, val, next):
        self.prev = prev
        self.row = row
        self.col = col
        self.val = val
        self.next = next

class DoubleLinkedList():
    def __init__(self, size, values=None):
        self.size = size
        self.create_random_matrix(values)
    
    def create_random_matrix(self, values):
        # get random values & idx
        if values is None:
            idx = [v for v in np.ndindex((self.size,self.size))]
            selection = np.random.choice(len(idx), size=np.random.randint(low=1,high=max(self.size*self.size // 2, 1)), replace=False)
            idx = [idx[i] for i in selection]
            vals = np.random.randint(low=1, high=10, size=(len(idx)))
        else:
            idx = list(values.keys())
            vals = list(values.values())

        arr, head = None, None

        # convert this to a circular double-linked list
        for i, (row,col) in enumerate(idx):
            if arr is None:
                arr = BiNode(None, row, col, vals[i], None)
                arr.prev = arr
                arr.next = arr
                head = arr
            else:
                node = BiNode(None, row, col, vals[i], None)
                head.next = node
                node.prev = head
                node.next = arr
                arr.prev = node
                head = node

        self.head = arr

    def add(self, other):
        values = {}

        if other is None or self.head is None:
            raise ValueError('Error: Empty linked list in summation.')

        head = self.head
        other_head = other.head

        values[head.row, head.col] = head.val

        if (other_head.row, other_head.col) in values:
            values[other_head.row, other_head.col] += other_head.val
        else:
            values[other_head.row, other_head.col] = other_head.val

        head = head.next
        other_head = other_head.next

        # O(n+m), n,m: #nonzeros
        while True:
            if head != self.head:
                if (head.row, head.col) in values:
                    values[head.row, head.col] += head.val
                else:
                    values[head.row, head.col] = head.val

            if other_head != other.head:
                if (other_head.row, other_head.col) in values:
                    values[other_head.row, other_head.col] += other_head.val
                else:
                    values[other_head.row, other_head.col] = other_head.val

            if head != self.head:
                head = head.next

            if other_head != other.head:
                other_head = other_head.next

            if head == self.head and other_head == other.head:
                break
        
        return DoubleLinkedList(self.size, values)

    def scalar_multiply(self, scalar):
        head = self.head
        while True:
            head.val = int(head.val * scalar)

            head = head.next
            if head == self.head:
                break

    def transpose(self):
        head = self.head
        while True:
            tmp = head.col
            head.col = head.row
            head.row = tmp

            head = head.next
            if head == self.head:
                break

    def traverse(self):
        values = np.zeros((self.size, self.size)).astype(np.int64)
        head = self.head

        while True:
            values[head.row, head.col] = head.val

            head = head.next
            if head == self.head:
                break
        
        for (row,col) in np.ndindex((self.size,self.size)):
            print(f'{values[row,col]:3d} ', end='')

            if col == self.size - 1:
                print()