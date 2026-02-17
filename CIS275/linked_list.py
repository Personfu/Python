# ============================================================
# Linked List — Complete Implementation
# CIS 275 — Data Structures | Preston Furulie
# ============================================================
# Covers: singly linked list (prepend, append, insert, delete,
# search, reverse, length, get nth, detect cycle), doubly
# linked list, and complexity analysis.
# ============================================================


class Node:
    """A single node in a singly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class SinglyLinkedList:
    """Full singly linked list with all standard operations.

    Time Complexities:
        prepend:    O(1)
        append:     O(n)  — must traverse to the end
        insert_at:  O(n)  — must traverse to position
        delete:     O(n)  — must find the node
        search:     O(n)  — linear scan
        reverse:    O(n)  — single pass
        get_at:     O(n)  — traverse to index
        length:     O(n)  — count all nodes
    """

    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    # ── Insertion Operations ────────────────────────────────

    def prepend(self, data):
        """Insert at the beginning — O(1)."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def append(self, data):
        """Insert at the end — O(n)."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def insert_at(self, index, data):
        """Insert at a specific index — O(n).
        Index 0 = prepend, index >= length = append."""
        if index <= 0:
            self.prepend(data)
            return
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            if current is None:
                break
            current = current.next
        if current is None:
            self.append(data)
        else:
            new_node.next = current.next
            current.next = new_node

    def insert_sorted(self, data):
        """Insert into a sorted list maintaining sort order — O(n)."""
        new_node = Node(data)
        if not self.head or data <= self.head.data:
            new_node.next = self.head
            self.head = new_node
            return
        current = self.head
        while current.next and current.next.data < data:
            current = current.next
        new_node.next = current.next
        current.next = new_node

    # ── Deletion Operations ─────────────────────────────────

    def delete_first(self):
        """Remove and return the first element — O(1)."""
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        return data

    def delete_last(self):
        """Remove and return the last element — O(n)."""
        if not self.head:
            return None
        if not self.head.next:
            data = self.head.data
            self.head = None
            return data
        current = self.head
        while current.next.next:
            current = current.next
        data = current.next.data
        current.next = None
        return data

    def delete_value(self, data):
        """Delete the first occurrence of a value — O(n).
        Returns True if found and deleted, False otherwise."""
        if not self.head:
            return False
        if self.head.data == data:
            self.head = self.head.next
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def delete_at(self, index):
        """Delete node at a specific index — O(n)."""
        if not self.head or index < 0:
            return None
        if index == 0:
            return self.delete_first()
        current = self.head
        for _ in range(index - 1):
            if current.next is None:
                return None
            current = current.next
        if current.next is None:
            return None
        data = current.next.data
        current.next = current.next.next
        return data

    # ── Search & Access ─────────────────────────────────────

    def search(self, data):
        """Find the index of a value — O(n). Returns -1 if not found."""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def contains(self, data):
        """Check if a value exists — O(n)."""
        return self.search(data) != -1

    def get_at(self, index):
        """Get value at index — O(n). Returns None if out of bounds."""
        current = self.head
        for _ in range(index):
            if current is None:
                return None
            current = current.next
        return current.data if current else None

    # ── Utility Operations ──────────────────────────────────

    def length(self):
        """Count all nodes — O(n)."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def reverse(self):
        """Reverse the list in-place — O(n), O(1) space.
        Uses three-pointer technique: prev, current, next."""
        prev = None
        current = self.head
        while current:
            next_node = current.next   # save next
            current.next = prev        # reverse link
            prev = current             # advance prev
            current = next_node        # advance current
        self.head = prev

    def to_list(self):
        """Convert to a Python list for easy viewing."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def find_middle(self):
        """Find middle node using slow/fast pointer technique — O(n).
        Slow moves 1 step, fast moves 2 steps. When fast reaches end,
        slow is at the middle."""
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow.data if slow else None

    def has_cycle(self):
        """Detect if the list has a cycle using Floyd's algorithm.
        Two pointers: if they ever meet, there's a cycle."""
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def remove_duplicates(self):
        """Remove duplicate values from a sorted list — O(n)."""
        current = self.head
        while current and current.next:
            if current.data == current.next.data:
                current.next = current.next.next
            else:
                current = current.next

    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " → ".join(elements) + " → None"

    def __len__(self):
        return self.length()

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next


# ── Doubly Linked List ──────────────────────────────────────

class DNode:
    """Node with both next and prev pointers."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Doubly linked list with O(1) append via tail pointer."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        """Append to end — O(1) with tail pointer."""
        new_node = DNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def prepend(self, data):
        """Insert at beginning — O(1)."""
        new_node = DNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def delete_value(self, data):
        """Delete first occurrence — O(n)."""
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def forward(self):
        """Traverse forward."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def backward(self):
        """Traverse backward."""
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result

    def __len__(self):
        return self._size


# ── Demonstrations ──────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  LINKED LIST — CIS 275 | Preston Furulie")
    print("=" * 60)

    # --- Singly Linked List ---
    print("\n--- Singly Linked List ---")
    ll = SinglyLinkedList()

    for val in [10, 20, 30, 40, 50]:
        ll.append(val)
    print(f"  Built:      {ll}")

    ll.prepend(5)
    print(f"  Prepend 5:  {ll}")

    ll.insert_at(3, 25)
    print(f"  Insert 25 at index 3: {ll}")

    ll.delete_value(30)
    print(f"  Delete 30:  {ll}")

    print(f"  Length:     {ll.length()}")
    print(f"  Search 40: index {ll.search(40)}")
    print(f"  Middle:    {ll.find_middle()}")
    print(f"  Has cycle: {ll.has_cycle()}")

    ll.reverse()
    print(f"  Reversed:  {ll}")

    print(f"\n  Iterate with for loop:")
    for val in ll:
        print(f"    {val}")

    # --- Sorted Insert ---
    print("\n--- Sorted Linked List ---")
    sorted_ll = SinglyLinkedList()
    for val in [30, 10, 50, 20, 40, 20]:
        sorted_ll.insert_sorted(val)
    print(f"  Sorted: {sorted_ll}")
    sorted_ll.remove_duplicates()
    print(f"  No dups: {sorted_ll}")

    # --- Doubly Linked List ---
    print("\n--- Doubly Linked List ---")
    dll = DoublyLinkedList()
    for val in [1, 2, 3, 4, 5]:
        dll.append(val)
    print(f"  Forward:  {dll.forward()}")
    print(f"  Backward: {dll.backward()}")
    dll.delete_value(3)
    print(f"  Delete 3: {dll.forward()}")
    print(f"  Size:     {len(dll)}")
