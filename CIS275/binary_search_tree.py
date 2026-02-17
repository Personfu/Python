# Binary Search Tree
# CIS 275 — Data Structures | Preston Furulie

class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def insert(root, val):
    if not root:
        return BSTNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

def inorder(root):
    if root:
        inorder(root.left)
        print(root.val, end=" ")
        inorder(root.right)

def search(root, target):
    if not root:
        return False
    if root.val == target:
        return True
    if target < root.val:
        return search(root.left, target)
    return search(root.right, target)


root = None
for v in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, v)
print("In-order:", end=" ")
inorder(root)
print()
print("Search 40:", search(root, 40))
print("Search 99:", search(root, 99))
