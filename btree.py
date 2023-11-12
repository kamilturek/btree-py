DEFAULT_ORDER = 3


class BaseNode:
    def __init__(
        self,
        order,
        parent=None,
        sibling=None,
    ) -> None:
        if order < 2:
            raise ValueError("order must greater than or equal 2")

        self.order = order
        self.parent = parent
        self.sibling = sibling

    @property
    def max_size(self):
        return self.order - 1

    @property
    def keys_occupancy(self):
        return sum(k is not None for k in self.keys)


class Node(BaseNode):
    """Internal node or non-leaf root."""

    def __init__(
        self,
        order=DEFAULT_ORDER,
        parent=None,
        sibling=None,
    ):
        super().__init__(order=order, parent=parent, sibling=sibling)

        self.keys = [None] * (order - 1)
        self.children = [None] * order

    def __repr__(self):
        return f"Internal: [{', '.join(str(k) for k in self.keys)}]"

    @property
    def children_occupancy(self):
        return sum(c is not None for c in self.children)

    def _insert(self, key, child):
        """
        Insert child to internal node or non-leaf root. Split node if necessary.

        Should not be used directly.

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

            self.sibling = Node(
                order=self.order,
                parent=self.parent,
                sibling=self.sibling,
            )

            middle = (self.order - 1) // 2

            # Copy second half of the node
            self.sibling.keys[: middle + 1] = tmp_keys[middle:]
            self.sibling.children[: middle + 2] = tmp_children[middle:]

            # Haven't tested it properly.
            self.keys[:middle] = tmp_keys[:middle]
            self.children[:middle] = tmp_children[:middle]

            for child in self.sibling.children:
                child.parent = self.sibling

            # Erase second half of the node
            for i in range(middle):
                self.keys[middle + i] = None

            for i in range(middle + 1):
                self.children[middle + i] = None

            # Return new parent if created
            return (
                self.parent._insert(self.sibling.keys[0], self.sibling)
                or self.parent._insert(self.keys[middle - 1], self)
                or new_parent
            )
        else:
            self.keys = tmp_keys[: self.max_size]
            self.children = tmp_children[: self.max_size + 1]

            return None

    def _delete(self, key):
        """
        Delete key and child following it. Merge with sibling if possible.

        Should not be used directly.
        """
        for i, k in enumerate(self.keys):
            if key == k:
                is_last_key = i + 1 == len(self.keys) or self.keys[i + 1] is None
                assert is_last_key, "Only last key from internal node can be deleted"

                self.keys[i] = None
                self.children[i + 1] = None
                break

        # Haven't tested it properly.
        has_sibling = self.sibling is not None
        if has_sibling:
            keys_occupancy = self.keys_occupancy
            sibling_keys_occupancy = self.sibling.keys_occupancy

            children_occupancy = self.children_occupancy
            sibling_children_occupancy = self.children_occupancy

            can_merge = (
                keys_occupancy + sibling_keys_occupancy <= self.max_size
                and children_occupancy + sibling_children_occupancy <= self.max_size + 1
            )
            if can_merge:
                self.keys[keys_occupancy:sibling_keys_occupancy] = self.sibling.keys[
                    :sibling_keys_occupancy
                ]
                self.children[
                    children_occupancy:sibling_children_occupancy
                ] = self.sibling.children[:sibling_children_occupancy]
                self.parent._delete(self.sibling.keys[0])


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

    def __repr__(self):
        content = [f"{k}/{v}" for k, v in zip(self.keys, self.values)]
        return f"[{', '.join(content)}]"

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

            # Move second half of the node
            self.sibling.keys[: middle + 1] = tmp_keys[middle:]
            self.sibling.values[: middle + 1] = tmp_values[middle:]
            self.keys[:middle] = tmp_keys[:middle]
            self.values[:middle] = tmp_values[:middle]

            # Erase second half of the node
            for i in range(middle):
                self.keys[middle + i] = None
                self.values[middle + i] = None

            # Return new parent if created
            return (
                self.parent._insert(self.sibling.keys[0], self.sibling)
                or self.parent._insert(self.keys[middle - 1], self)
                or new_parent
            )
        else:
            self.keys = tmp_keys[: self.max_size]
            self.values = tmp_values[: self.max_size]

            return None

    def delete(self, key):
        for i, k in enumerate(self.keys):
            if k == key:
                # Shift and delete
                self.keys[i:] = self.keys[i + 1 :]
                self.values[i:] = self.values[i + 1 :]
                self.keys[-1] = None
                self.values[-1] = None
                break

        # Only right sibling is considered.
        # Merge could probably happen with left sibling too.
        has_sibling = self.sibling is not None
        if has_sibling:
            occupancy = self.keys_occupancy
            sibling_occupancy = self.sibling.keys_occupancy

            can_merge = occupancy + sibling_occupancy <= self.max_size
            if can_merge:
                self.keys[occupancy:sibling_occupancy] = self.sibling.keys[
                    :sibling_occupancy
                ]
                self.values[occupancy:sibling_occupancy] = self.sibling.values[
                    :sibling_occupancy
                ]
                self.parent._delete(self.sibling.keys[0])


class BTree:
    def __init__(self):
        self.root = Leaf()

    def _target_leaf(self, key):
        node = self.root

        while not isinstance(node, Leaf):
            for i, child in enumerate(node.children):
                last_key = i >= len(node.keys) or node.keys[i] is None
                if last_key or key < node.keys[i]:
                    node = child
                    break

        return node

    def insert(self, key, value):
        leaf = self._target_leaf(key)

        new_root = leaf.insert(key, value)
        if new_root is not None:
            self.root = new_root

    def delete(self, key):
        leaf = self._target_leaf(key)
        leaf.delete(key)

    def lookup(self, key):
        leaf = self._target_leaf(key)

        for k, v in zip(leaf.keys, leaf.values):
            if k == key:
                return v

        raise KeyError(key)
