import unittest

from btree import BTree, Leaf


class TestLeaf(unittest.TestCase):
    def test_insert(self):
        leaf = Leaf()

        assert leaf.parent is None
        assert leaf.keys == [None, None]
        assert leaf.values == [None, None]

        leaf.insert(5, "world")

        assert leaf.parent is None
        assert leaf.keys == [5, None]
        assert leaf.values == ["world", None]

        leaf.insert(2, "hello")

        assert leaf.parent is None
        assert leaf.keys == [2, 5]
        assert leaf.values == ["hello", "world"]

    def test_split(self):
        leaf = Leaf()

        leaf.insert(5, "world")
        leaf.insert(2, "hello")
        leaf.insert(3, "beautiful")

        assert leaf.parent is not None
        assert leaf.keys == [2, None]
        assert leaf.values == ["hello", None]
        assert leaf.sibling.keys == [3, 5]
        assert leaf.sibling.values == ["beautiful", "world"]
        assert leaf.parent.keys == [3, None]
        assert leaf.parent.children == [leaf, leaf.sibling, None]


class TestBTree(unittest.TestCase):
    def test_insert_and_split(self):
        btree = BTree()

        btree.insert(1, "1")

        assert btree.root.keys == [1, None]

        btree.insert(2, "2")

        assert btree.root.keys == [1, 2]

        btree.insert(3, "3")

        assert btree.root.keys == [2, None]

        leaf1, leaf2, leaf3 = btree.root.children

        assert leaf1.keys == [1, None]
        assert leaf2.keys == [2, 3]
        assert leaf3 is None

        btree.insert(4, "4")

        assert btree.root.keys == [2, 3]

        leaf1, leaf2, leaf3 = btree.root.children

        assert leaf1.keys == [1, None]
        assert leaf2.keys == [2, None]
        assert leaf3.keys == [3, 4]

        btree.insert(5, "5")

        assert btree.root.keys == [3, None]

        node1, node2, node3 = btree.root.children

        assert node1.keys == [2, None]
        assert node2.keys == [3, 4]
        assert node3 is None

        node11, node12, node13 = node1.children
        assert node11.keys == [1, None]
        assert node12 is None
        assert node13 is None

        node21, node22, node23 = node2.children

        assert node21.keys == [2, None]
        assert node22.keys == [3, None]
        assert node23.keys == [4, 5]

    def test_delete_and_merge(self):
        btree = BTree()
        btree.insert(15, "15")
        btree.insert(16, "16")
        btree.insert(20, "20")
        btree.insert(25, "25")

        assert btree.root.keys == [16, 20]

        leaf1, leaf2, leaf3 = btree.root.children

        assert leaf1.keys == [15, None]
        assert leaf2.keys == [16, None]
        assert leaf3.keys == [20, 25]

        btree.delete(16)

        assert btree.root.keys == [16, None]

        leaf1, leaf2, leaf3 = btree.root.children

        assert leaf1.keys == [15, None]
        assert leaf2.keys == [20, 25]
        assert leaf3 is None


if __name__ == "__main__":
    unittest.main()
