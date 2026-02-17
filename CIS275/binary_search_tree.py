# ============================================================
# Binary Search Tree — Complete Implementation
# CIS 275 — Data Structures | Preston Furulie
# ============================================================
# Covers: insert, search, delete (3 cases), all traversals
# (in-order, pre-order, post-order, level-order), height,
# min/max, successor, validation, and balancing analysis.
# ============================================================

from collections import deque


class BSTNode:
    """A node in a Binary Search Tree."""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.count = 1   # handle duplicates by counting


class BinarySearchTree:
    """Full BST implementation.

    BST Property: For every node N:
        - All values in N.left < N.val
        - All values in N.right >= N.val

    Average complexities (balanced):
        insert:  O(log n)
        search:  O(log n)
        delete:  O(log n)
    Worst case (degenerate/skewed): O(n) for all operations
    """

    def __init__(self):
        self.root = None
        self._size = 0

    # ── Insertion ───────────────────────────────────────────

    def insert(self, val):
        """Insert a value into the BST."""
        self.root = self._insert(self.root, val)
        self._size += 1

    def _insert(self, node, val):
        """Recursive insert. Navigate left/right based on comparison."""
        if node is None:
            return BSTNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        else:
            node.count += 1  # duplicate: increment count
        return node

    # ── Search ──────────────────────────────────────────────

    def search(self, val):
        """Search for a value. Returns True/False."""
        return self._search(self.root, val)

    def _search(self, node, val):
        if node is None:
            return False
        if val == node.val:
            return True
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    # ── Deletion (3 Cases) ──────────────────────────────────

    def delete(self, val):
        """Delete a value from the BST.

        Three cases:
        1. Leaf node: simply remove it
        2. One child: replace node with its child
        3. Two children: replace with in-order successor (smallest
           value in right subtree), then delete the successor
        """
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if node is None:
            return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Found the node to delete
            if node.count > 1:
                node.count -= 1
                return node
            # Case 1 & 2: No child or one child
            if node.left is None:
                self._size -= 1
                return node.right
            if node.right is None:
                self._size -= 1
                return node.left
            # Case 3: Two children — find in-order successor
            successor = self._find_min_node(node.right)
            node.val = successor.val
            node.count = successor.count
            successor.count = 1
            node.right = self._delete(node.right, successor.val)
        return node

    # ── Min / Max ───────────────────────────────────────────

    def find_min(self):
        """Find the minimum value (leftmost node)."""
        if not self.root:
            return None
        return self._find_min_node(self.root).val

    def _find_min_node(self, node):
        while node.left:
            node = node.left
        return node

    def find_max(self):
        """Find the maximum value (rightmost node)."""
        if not self.root:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.val

    # ── Traversals ──────────────────────────────────────────

    def inorder(self):
        """In-order: Left → Node → Right (sorted ascending)."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.extend([node.val] * node.count)
            self._inorder(node.right, result)

    def preorder(self):
        """Pre-order: Node → Left → Right (useful for copying trees)."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.extend([node.val] * node.count)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        """Post-order: Left → Right → Node (useful for deletion)."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.extend([node.val] * node.count)

    def level_order(self):
        """Level-order (BFS): traverse level by level using a queue."""
        if not self.root:
            return []
        result = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            result.extend([node.val] * node.count)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    # ── Tree Properties ─────────────────────────────────────

    def height(self):
        """Height: longest path from root to a leaf."""
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1  # empty tree has height -1
        left_h = self._height(node.left)
        right_h = self._height(node.right)
        return 1 + max(left_h, right_h)

    def is_balanced(self):
        """Check if tree is balanced (height difference <= 1 at every node)."""
        return self._check_balanced(self.root) != -1

    def _check_balanced(self, node):
        if node is None:
            return 0
        left = self._check_balanced(node.left)
        if left == -1:
            return -1
        right = self._check_balanced(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    def is_valid_bst(self):
        """Validate BST property: left < node < right for all nodes."""
        return self._validate(self.root, float("-inf"), float("inf"))

    def _validate(self, node, low, high):
        if node is None:
            return True
        if node.val <= low or node.val >= high:
            return False
        return (self._validate(node.left, low, node.val) and
                self._validate(node.right, node.val, high))

    def count_nodes(self):
        """Count total values stored (including duplicates)."""
        return self._count(self.root)

    def _count(self, node):
        if node is None:
            return 0
        return node.count + self._count(node.left) + self._count(node.right)

    # ── Visualization ───────────────────────────────────────

    def print_tree(self):
        """Print a visual representation of the tree."""
        lines = []
        self._build_lines(self.root, lines, "", True)
        return "\n".join(lines)

    def _build_lines(self, node, lines, prefix, is_last):
        if node is not None:
            connector = "└── " if is_last else "├── "
            label = f"{node.val}" + (f"(x{node.count})" if node.count > 1 else "")
            lines.append(prefix + connector + label)
            new_prefix = prefix + ("    " if is_last else "│   ")
            children = []
            if node.left:
                children.append(("L", node.left))
            if node.right:
                children.append(("R", node.right))
            for i, (side, child) in enumerate(children):
                self._build_lines(child, lines, new_prefix, i == len(children) - 1)

    def __len__(self):
        return self._size

    def __contains__(self, val):
        return self.search(val)


# ── Demonstrations ──────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  BINARY SEARCH TREE — CIS 275 | Preston Furulie")
    print("=" * 60)

    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for v in values:
        bst.insert(v)

    print(f"\n  Inserted: {values}")
    print(f"\n  Tree structure:")
    print(bst.print_tree())

    print(f"\n  In-order (sorted):  {bst.inorder()}")
    print(f"  Pre-order:          {bst.preorder()}")
    print(f"  Post-order:         {bst.postorder()}")
    print(f"  Level-order (BFS):  {bst.level_order()}")

    print(f"\n  Height:    {bst.height()}")
    print(f"  Min:       {bst.find_min()}")
    print(f"  Max:       {bst.find_max()}")
    print(f"  Nodes:     {bst.count_nodes()}")
    print(f"  Valid BST: {bst.is_valid_bst()}")
    print(f"  Balanced:  {bst.is_balanced()}")

    print(f"\n  Search 40: {bst.search(40)}")
    print(f"  Search 99: {bst.search(99)}")
    print(f"  45 in bst: {45 in bst}")

    print(f"\n  Delete 20 (leaf):")
    bst.delete(20)
    print(f"  In-order: {bst.inorder()}")

    print(f"\n  Delete 30 (two children):")
    bst.delete(30)
    print(f"  In-order: {bst.inorder()}")

    print(f"\n  Final tree:")
    print(bst.print_tree())
