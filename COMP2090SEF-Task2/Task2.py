"""Advanced Study: Binary Tree & Shell Sort (Independent Test Cases)"""
import time, random
from typing import List, Generator

# ===================== 1. Pure Binary Tree (BT) + Test Cases =====================
class BinaryTreeNode:
    def __init__(self, val): self.val, self.left, self.right = val, None, None

# Binary Tree core operations (explicit BT functions, not just BST sort)
def build_bt(arr: List[int]) -> BinaryTreeNode:
    """Build a binary tree from list (level-order)"""
    if not arr: return None
    root = BinaryTreeNode(arr[0])
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if arr[i] is not None:
            node.left = BinaryTreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = BinaryTreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root

def traverse_bt(root: BinaryTreeNode, type="inorder") -> List[int]:
    """BT traversal: inorder/preorder/postorder"""
    res = []
    def dfs(node):
        if not node: return
        if type == "preorder": res.append(node.val)
        dfs(node.left)
        if type == "inorder": res.append(node.val)
        dfs(node.right)
        if type == "postorder": res.append(node.val)
    dfs(root)
    return res

def test_binary_tree():
    """Independent test cases for PURE Binary Tree (not just BST)"""
    print("="*65)
    print("          Advanced Study: Binary Tree Test Cases          ")
    print("="*65)
    # BT test cases (level-order input: None = empty child)
    test_cases = [
        ("Basic BT (level-order: 1,2,3,4,None,5)", [1,2,3,4,None,5]),
        ("Empty BT", []),
        ("Single node BT", [42]),
        ("BT with only left children", [10,20,None,30,None,40])
    ]
    
    for i, (name, data) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {name}")
        print(f"  Input (level-order): {data}")
        root = build_bt(data)
        # Test all traversals
        pre = traverse_bt(root, "preorder")
        ino = traverse_bt(root, "inorder")
        post = traverse_bt(root, "postorder")
        print(f"  Preorder:  {pre}")
        print(f"  Inorder:   {ino}")
        print(f"  Postorder: {post}")
    print("\n" + "-"*65 + "\n")

# ===================== 2. Shell Sort + Independent Test Cases =====================
def shell_sort(arr: List[int], gap_type="original") -> List[int]:
    def get_gaps(n: int) -> Generator[int, None, None]:
        if gap_type == "original":
            gap = n//2
            while gap>0: yield gap; gap//=2
        elif gap_type == "hibbard":
            k=1
            while (1<<k)-1 <n: k+=1
            while k>=1: yield (1<<k)-1; k-=1
        elif gap_type == "knuth":
            g,k=[],1
            while (3**k-1)//2 <=n: g.append((3**k-1)//2);k+=1
            for x in reversed(g): yield x
    n, arr = len(arr), arr.copy()
    if n<=1: return arr
    for gap in get_gaps(n):
        for i in range(gap, n):
            t,j = arr[i],i
            while j>=gap and arr[j-gap]>t:
                arr[j] = arr[j-gap]; j-=gap
            arr[j] = t
    return arr

def test_shell_sort():
    """Independent test cases for Shell Sort"""
    print("="*65)
    print("          Advanced Study: Shell Sort Test Cases          ")
    print("="*65)
    cases = [
        ("Basic random nums", [64,34,25,12,22,11,90,5]),
        ("Empty list", []),
        ("Single element", [42]),
        ("Duplicate elements", [5,3,8,5,1,8,2])
    ]
    gaps = ["original", "hibbard", "knuth"]
    for i, (name, data) in enumerate(cases,1):
        print(f"\nTest Case {i}: {name}")
        print(f"  Input:  {data}")
        for g in gaps:
            s = time.perf_counter()
            out = shell_sort(data, g)
            print(f"  [{g}] Output: {out} | Time: {time.perf_counter()-s:.6f}s")
    print("\n" + "-"*65 + "\n")

# Run all independent test cases
if __name__ == "__main__":
    test_binary_tree()  # First: Pure Binary Tree tests
    test_shell_sort()   # Second: Shell Sort tests
    print("✅ All test cases completed!")