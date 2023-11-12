import unittest

from btree import BTree, Leaf


class TestLeaf(unittest.TestCase):
    def test_insert(self):
        leaf = Leaf()

        self.assertIsNone(leaf.parent)
        self.assertEqual(leaf.keys, [None, None])
        self.assertEqual(leaf.values, [None, None])

        leaf.insert(5, "world")

        self.assertIsNone(leaf.parent)
        self.assertEqual(leaf.keys, [5, None])
        self.assertEqual(leaf.values, ["world", None])

        leaf.insert(2, "hello")

        self.assertIsNone(leaf.parent)
        self.assertEqual(leaf.keys, [2, 5])
        self.assertEqual(leaf.values, ["hello", "world"])

    def test_split(self):
        leaf = Leaf()
        leaf.insert(5, "world")
        leaf.insert(2, "hello")
        leaf.insert(3, "beautiful")

        self.assertIsNotNone(leaf.parent)
        self.assertEqual(leaf.keys, [2, None])
        self.assertEqual(leaf.values, ["hello", None])
        self.assertEqual(leaf.sibling.keys, [3, 5])
        self.assertEqual(leaf.sibling.values, ["beautiful", "world"])
        self.assertEqual(leaf.parent.keys, [3, None])
        self.assertEqual(leaf.parent.children, [leaf, leaf.sibling, None])


class TestBTree(unittest.TestCase):
    def test_insert_and_split_1(self):
        btree = BTree()
        btree.insert(1, "1")

        self.assertEqual(btree.root.keys, [1, None])

        btree.insert(2, "2")

        self.assertEqual(btree.root.keys, [1, 2])

        btree.insert(3, "3")

        self.assertEqual(btree.root.keys, [2, None])

        leaf1, leaf2, leaf3 = btree.root.children

        self.assertEqual(leaf1.keys, [1, None])
        self.assertEqual(leaf2.keys, [2, 3])
        self.assertIsNone(leaf3)

        btree.insert(4, "4")

        self.assertEqual(btree.root.keys, [2, 3])

        leaf1, leaf2, leaf3 = btree.root.children

        self.assertEqual(leaf1.keys, [1, None])
        self.assertEqual(leaf2.keys, [2, None])
        self.assertEqual(leaf3.keys, [3, 4])

        btree.insert(5, "5")

        self.assertEqual(btree.root.keys, [3, None])

        node1, node2, node3 = btree.root.children

        self.assertEqual(node1.keys, [2, None])
        self.assertEqual(node2.keys, [3, 4])
        self.assertIsNone(node3)

        node11, node12, node13 = node1.children

        self.assertEqual(node11.keys, [1, None])
        self.assertIsNone(node12)
        self.assertIsNone(node13)

        node21, node22, node23 = node2.children

        self.assertEqual(node21.keys, [2, None])
        self.assertEqual(node22.keys, [3, None])
        self.assertEqual(node23.keys, [4, 5])

    def test_insert_and_split_2(self):
        btree = BTree()

        btree.insert(15, "Alice")
        btree.insert(16, "Bob")
        btree.insert(20, "Charlie")
        btree.insert(25, "Darius")

        self.assertEqual(btree.root.keys, [16, 20])

        leaf1, leaf2, leaf3 = btree.root.children

        self.assertEqual(leaf1.keys, [15, None])
        self.assertEqual(leaf1.values, ["Alice", None])
        self.assertEqual(leaf2.keys, [16, None])
        self.assertEqual(leaf2.values, ["Bob", None])
        self.assertEqual(leaf3.keys, [20, 25])
        self.assertEqual(leaf3.values, ["Charlie", "Darius"])

        btree.insert(30, "Elizabeth")

        self.assertEqual(btree.root.keys, [20, None])

        node1, node2, node3 = btree.root.children

        self.assertEqual(node1.keys, [16, None])
        self.assertEqual(node2.keys, [20, 25])
        self.assertIsNone(node3)

        node11, node12, node13 = node1.children
        node21, node22, node23 = node2.children

        self.assertEqual(node11.keys, [15, None])
        self.assertEqual(node11.values, ["Alice", None])
        self.assertIsNone(node12)
        self.assertIsNone(node13)
        self.assertEqual(node21.keys, [16, None])
        self.assertEqual(node21.values, ["Bob", None])
        self.assertEqual(node22.keys, [20, None])
        self.assertEqual(node22.values, ["Charlie", None])
        self.assertEqual(node23.keys, [25, 30])
        self.assertEqual(node23.values, ["Darius", "Elizabeth"])

    def test_delete_and_merge(self):
        btree = BTree()
        btree.insert(15, "15")
        btree.insert(16, "16")
        btree.insert(20, "20")
        btree.insert(25, "25")

        self.assertEqual(btree.root.keys, [16, 20])

        leaf1, leaf2, leaf3 = btree.root.children

        self.assertEqual(leaf1.keys, [15, None])
        self.assertEqual(leaf2.keys, [16, None])
        self.assertEqual(leaf3.keys, [20, 25])

        btree.delete(16)

        self.assertEqual(btree.root.keys, [16, None])

        leaf1, leaf2, leaf3 = btree.root.children

        self.assertEqual(leaf1.keys, [15, None])
        self.assertEqual(leaf2.keys, [20, 25])
        self.assertIsNone(leaf3)

    def test_lookup_1(self):
        btree = BTree()

        btree.insert(10, "Alice")
        btree.insert(15, "Bob")
        btree.insert(20, "Charlie")
        btree.insert(25, "Darius")
        btree.insert(30, "Elizabeth")
        btree.insert(35, "Frank")

        self.assertEqual(btree.lookup(35), "Frank")

    def test_lookup_2(self):
        btree = BTree()

        btree.insert(35, "Frank")
        btree.insert(30, "Elizabeth")
        btree.insert(25, "Darius")
        btree.insert(20, "Charlie")
        btree.insert(15, "Bob")
        btree.insert(10, "Alice")

        self.assertEqual(btree.lookup(35), "Frank")


if __name__ == "__main__":
    unittest.main()
