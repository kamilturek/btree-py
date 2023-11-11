DEFAULT_ORDER = 3


class BaseNode:
    def __init__(
        self,
        order,
        parent=None,
    ) -> None:
        if order < 2:
            raise ValueError("order must greater than or equal 2")

        self.order = order
        self.parent = parent

    @property
    def max_size(self) -> int:
        return self.order - 1


class Node(BaseNode):
    """Internal node or non-leaf root."""

    def __init__(
        self,
        order=DEFAULT_ORDER,
        parent=None,
    ):
        super().__init__(order=order, parent=parent)

        self.keys = [None] * (order - 1)
        self.children = [None] * order

    def insert(self, key, child):
        """
        Insert child to internal node or non-leaf root. Split node if necessary.

        Returns:
            Node | None: new parent or None if parent not changed
        """
        tmp_keys = self.keys.copy()
        tmp_children = self.children.copy()

        for i, k in enumerate(tmp_keys):
            if k is None:
                tmp_keys[i] = key
                tmp_children[i + 1] = child
                break
            elif key < k:
                tmp_children[i] = child
                break
        else:
            tmp_keys.append(key)
            tmp_children.append(child)

        needs_split = len(tmp_keys) > self.max_size and tmp_keys.count(None) == 0
        if needs_split:
            new_parent = None

            if self.parent is None:
                self.parent = Node(parent=None, order=self.order)
                new_parent = self.parent

            sibling = Node(
                order=self.order,
                parent=self.parent,
            )

            middle = (self.order - 1) // 2

            for i in range(middle + 1):
                sibling.keys[i] = tmp_keys[middle + i]

            for i in range(middle + 2):
                sibling.children[i] = tmp_children[middle + i]

            for i in range(middle):
                self.keys[middle + i] = None

            for i in range(middle + 1):
                self.children[middle + i] = None

            return (
                self.parent.insert(sibling.keys[0], sibling)
                or self.parent.insert(self.keys[middle - 1], self)
                or new_parent
            )
        else:
            self.keys = tmp_keys[: self.max_size]
            self.children = tmp_children[: self.max_size + 1]

            return None


class Leaf(BaseNode):
    def __init__(
        self,
        order=DEFAULT_ORDER,
        parent=None,
        sibling=None,
    ):
        super().__init__(order=order, parent=parent)

        self.sibling = sibling
        self.keys = [None] * (order - 1)
        self.values = [None] * (order - 1)

    def insert(self, key, value):
        """
        Insert value to leaf. Split node if necessary.

        Returns:
            Node | None: new parent or None if parent not changed
        """
        tmp_keys = self.keys.copy()
        tmp_values = self.values.copy()

        for i, k in enumerate(tmp_keys):
            if k is None:
                tmp_keys[i] = key
                tmp_values[i] = value
                break
            elif key < k:
                tmp_keys.insert(i, key)
                tmp_values.insert(i, value)
                break
        else:
            tmp_keys.append(key)
            tmp_values.append(value)

        needs_split = len(tmp_keys) > self.max_size and tmp_keys.count(None) == 0
        if needs_split:
            new_parent = None

            if self.parent is None:
                self.parent = Node(parent=None, order=self.order)
                new_parent = self.parent

            self.sibling = Leaf(
                order=self.order,
                parent=self.parent,
                sibling=self.sibling,
            )

            middle = (self.order - 1) // 2

            for i in range(middle + 1):
                self.sibling.keys[i] = tmp_keys[middle + i]
                self.sibling.values[i] = tmp_values[middle + i]

            for i in range(middle):
                self.keys[middle + i] = None
                self.values[middle + i] = None

            return (
                self.parent.insert(self.sibling.keys[0], self.sibling)
                or self.parent.insert(self.keys[middle - 1], self)
                or new_parent
            )
        else:
            self.keys = tmp_keys[: self.max_size]
            self.values = tmp_values[: self.max_size]

            return None


class BTree:
    def __init__(self):
        self.root = Leaf()

    def insert(self, key, value):
        leaf = self._find_leaf_for(key)

        new_root = leaf.insert(key, value)
        if new_root is not None:
            self.root = new_root

    def _find_leaf_for(self, key):
        node = self.root

        while not isinstance(node, Leaf):
            for i, child in enumerate(node.children):
                last_key = i >= len(node.keys) or node.keys[i] is None
                if last_key or key < node.keys[i]:
                    node = child
                    break

        return node
