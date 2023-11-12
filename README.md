# In-Memory B+ Tree Implementation

## Usage

```python
from btree import BTree

btree = BTree()
btree.insert(1, "hello")
btree.insert(99, "world")
btree.insert(50, "beautiful")

assert btree.lookup(99) == "world"
```
