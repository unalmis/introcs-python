# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 balanced_bst.py 10000
# ------------------------------------------------------------------------------

_RED: bool = True
_BLACK: bool = False


class _Node:
    # BST node with color bit
    len: int
    color: bool

    def __init__(self, key, val, color: bool):
        if key is None:
            raise KeyError
        if val is None:
            raise ValueError
        self.key = key
        self.val = val
        self.len = 1  # subtree count
        self.color = color
        self.lt = None  # reference to left child node
        self.rt = None  # reference to right child node

    def flip_colors(self):
        # flip the colors of this node and its two children
        assert (
            self.lt is not None
            and self.rt is not None
            and self.color != self.lt.color
            and self.lt.color == self.rt.color
        )

        self.color = not self.color
        self.lt.color = not self.lt.color
        self.rt.color = not self.rt.color

    def update_len(self):
        # maintain subtree counts
        self.len = _len(self.lt) + 1 + _len(self.rt)


# ------------------------------------------------------------------------------
# Red-black tree helper functions.
# @citation Adapted from: Robert Sedgewick and Kevin Wayne. Algorithms,
# 4th edition. Addison-Wesley Professional, 2011, pp. 433-439, 453-456.
# ------------------------------------------------------------------------------


def _len(h: _Node) -> int:
    # number of entries in subtree rooted at h
    return 0 if h is None else h.len


def _is_red(h: _Node) -> bool:
    # is node h red? (null nodes are black)
    return h is not None and h.color == _RED


def _is_black(h: _Node) -> bool:
    # is node h not red?
    return h is None or h.color == _BLACK


def _rotate_left(h: _Node) -> _Node:
    # make a right-leaning link lean left
    assert h is not None and _is_red(h.rt)

    x = h.rt
    h.rt = x.lt
    x.lt = h
    x.color = h.color
    h.color = _RED
    x.len = h.len
    h.update_len()
    return x


def _rotate_right(h: _Node) -> _Node:
    # make a left-leaning link lean right
    assert h is not None and _is_red(h.lt)

    x = h.lt
    h.lt = x.rt
    x.rt = h
    x.color = h.color
    h.color = _RED
    x.len = h.len
    h.update_len()
    return x


def _move_red_left(h: _Node) -> _Node:
    # move red link to left by coloring h.lt or one of its children red
    assert _is_red(h) and _is_black(h.lt) and _is_black(h.lt.lt)

    h.flip_colors()
    if _is_red(h.rt.lt):  # if now two consecutive red links
        h.rt = _rotate_right(h.rt)
        h = _rotate_left(h)
        h.flip_colors()

    return h


def _move_red_right(h: _Node) -> _Node:
    # move red link to right by coloring h.rt or one of its children red
    assert _is_red(h) and _is_black(h.rt) and _is_black(h.rt.lt)

    h.flip_colors()
    if _is_red(h.lt.lt):  # if now two consecutive red links
        h = _rotate_right(h)
        h.flip_colors()

    return h


def _balance(h: _Node) -> _Node:
    # preserve perfect black balance
    assert h is not None

    if _is_red(h.rt) and _is_black(h.lt):
        h = _rotate_left(h)
    if _is_red(h.lt) and _is_red(h.lt.lt):
        h = _rotate_right(h)
    if _is_red(h.lt) and _is_red(h.rt):
        h.flip_colors()

    h.update_len()
    return h


# ------------------------------------------------------------------------------
# Sorted iterable to left-leaning red-black BST construction.
# ------------------------------------------------------------------------------


def _make_bst(it: iter, fence: int, index: int) -> _Node or None:
    if fence < index:
        return None

    # make complete binary tree
    left = _make_bst(it, fence, index * 2)
    entry = next(it)
    on_bottom_level: bool = index >= (1 << (fence.bit_length() - 1))
    h = _Node(entry[0], entry[1], _RED if on_bottom_level else _BLACK)
    h.lt = left
    h.rt = _make_bst(it, fence, index * 2 + 1)

    # fix-up coloring and size
    if _is_red(h.lt) and _is_red(h.rt):
        h.flip_colors()
    h.update_len()
    return h


# see above for a more robust solution
# def _make_bst(list, lo: int, hi: int) -> _Node or None:
#     if hi < lo:
#         return None
#
#     # make (almost) complete binary tree
#     mid = (lo + hi) // 2
#     entry = list[mid]
#     h = _Node(entry[0], entry[1], _BLACK)
#     h.lt = _make_bst(list, lo, mid - 1)
#     h.rt = _make_bst(list, mid + 1, hi)
#
#     # convert to a left-leaning red-black tree
#     if h.lt is None and h.rt is None:
#         h.color = _RED  # color bottom red
#     elif _is_red(h.lt) and _is_black(h.rt):
#         h.lt.color = _BLACK  # fix-up bottom
#     return _balance(h)


# ------------------------------------------------------------------------------


class BalancedBST:
    """The BalancedBST class is an ordered symbol table of key-value pairs.

    It requires that the key type implements the < {__lt__} method.

    A symbol table implements the associative array abstraction:
    when associating a value with a key that is already in the symbol table,
    the convention is to replace the old value with the new value.

    This implementation uses a left-leaning red-black binary search tree. It
    also uses iteration instead of recursion (wherever it is feasible to do so)
    due to overhead associated with recursion in Python.

    The __init__ method takes time linear in the number of supplied keys.
    The is_empty and __len__ methods take O(1) time. The __iter__ and entries
    methods take O(lg N + M) time, where N is the number of entries in the set,
    and M is the number of entries returned by the iterable.

    All other methods take O(lg N) time.

    For additional documentation, see
    Section 3.3 of Algorithms, 4th Edition. Addison-Wesley Professional, 2011
    by Robert Sedgewick and Kevin Wayne.

    @author Kaya Unalmis
    """

    def __init__(self, entries=None):
        """
        Makes an empty symbol table if entries is None.
        Otherwise, makes a symbol table from the keys, and their associated
        values, in the pre-sorted entries. For each entry in entries, keys
        are located at entry[0] and values at entry[1].

        Takes linear time with zero key compares.

        :param entries:    sorted set of keys and their associated values
        :raise KeyError:   if None is a key in entries
        :raise ValueError: if None is a value in entries
        """
        if entries is None:
            self._root = None
        else:
            self._root = _make_bst(iter(entries), len(entries), 1)
            if not self.is_empty():
                self._root.color = _BLACK

        assert self._is_redblack_bst()

    def is_empty(self) -> bool:
        """:return: True if this symbol table is empty, False otherwise"""
        return self._root is None

    def __len__(self) -> int:
        """:return: the number of entries in this symbol table"""
        return _len(self._root)

    # --------------------------------------------------------------------------
    # BST search.
    # --------------------------------------------------------------------------

    def __contains__(self, key) -> bool:
        """
        :param key: query key
        :return:    True if this symbol table contains key; False otherwise
        """
        return self.get(key) is not None

    def __getitem__(self, key):
        """
        :param key: query key
        :return:    the value associated with key; None if no such value
        """
        return self.get(key)

    def get(self, key, default=None):
        """
        :param key:     query key
        :param default: default value to return
        :return:        the value associated with key; default if no such value
        """
        h = self._root
        while h is not None:
            if key < h.key:
                h = h.lt
            elif h.key < key:
                h = h.rt
            else:
                return h.val
        return default

    # --------------------------------------------------------------------------
    # Red-black tree insertion. (only insert red nodes)
    # --------------------------------------------------------------------------

    def __setitem__(self, key, val):
        """Associates given key with given value, overwriting the old value.

        :param key:        the key
        :param val:        the value
        :raise KeyError:   if key is None
        :raise ValueError: if val is None
        """
        self._root = BalancedBST._set(self._root, key, val)
        self._root.color = _BLACK
        assert self._is_redblack_bst()

    @staticmethod
    def _set(h: _Node, key, val) -> _Node:
        # Search for key. Update value if found; grow tree if new.
        if h is None:
            return _Node(key, val, _RED)

        if key < h.key:
            h.lt = BalancedBST._set(h.lt, key, val)
        elif h.key < key:
            h.rt = BalancedBST._set(h.rt, key, val)
        else:
            h.val = val

        return _balance(h)

    # --------------------------------------------------------------------------
    # Red-black tree deletion. (only delete red nodes)
    # --------------------------------------------------------------------------

    def del_min(self):
        """Deletes the smallest key (and its associated value) in this ST."""
        if self.is_empty():
            return
        if _is_black(self._root.lt) and _is_black(self._root.rt):
            self._root.color = _RED

        self._root = BalancedBST._del_min(self._root)
        if not self.is_empty():
            self._root.color = _BLACK

        assert self._is_redblack_bst()

    @staticmethod
    def _del_min(h: _Node) -> _Node or None:
        # delete the smallest key in subtree rooted at h
        if h.lt is None:
            return None
        if _is_black(h.lt) and _is_black(h.lt.lt):
            h = _move_red_left(h)

        h.lt = BalancedBST._del_min(h.lt)
        return _balance(h)

    def del_max(self):
        """Deletes the largest key (and its associated value) in this ST."""
        if self.is_empty():
            return
        if _is_black(self._root.lt) and _is_black(self._root.rt):
            self._root.color = _RED

        self._root = BalancedBST._del_max(self._root)
        if not self.is_empty():
            self._root.color = _BLACK

        assert self._is_redblack_bst()

    @staticmethod
    def _del_max(h: _Node) -> _Node or None:
        # delete the largest key in subtree rooted at h
        if _is_red(h.lt):
            h = _rotate_right(h)
        else:
            if h.rt is None:
                return None
            if _is_black(h.rt) and _is_black(h.rt.lt):
                h = _move_red_right(h)

        h.rt = BalancedBST._del_max(h.rt)
        return _balance(h)

    def __delitem__(self, key):
        """Deletes key (and its associated value) from this ST.

        :param key: the key to delete
        """
        if self.is_empty():
            return
        if _is_black(self._root.lt) and _is_black(self._root.rt):
            self._root.color = _RED

        self._root = BalancedBST._del(self._root, key)
        if not self.is_empty():
            self._root.color = _BLACK

        assert self._is_redblack_bst()

    @staticmethod
    def _del(h: _Node, key) -> _Node or None:
        # delete _Node with the given key in subtree rooted at h
        if key < h.key:
            if h.lt is None:
                return _balance(h)  # key not in self
            if _is_black(h.lt) and _is_black(h.lt.lt):
                h = _move_red_left(h)

            h.lt = BalancedBST._del(h.lt, key)
            return _balance(h)

        if _is_red(h.lt):
            h = _rotate_right(h)
        else:
            if h.rt is None:
                return _balance(h) if (key < h.key or h.key < key) else None
            if _is_black(h.rt) and _is_black(h.rt.lt):
                h = _move_red_right(h)
            if not (key < h.key or h.key < key):  # key == h.key
                # replace h with successor and delete successor's old node
                t = h
                h = BalancedBST._min(t.rt)  # successor of t
                h.rt = BalancedBST._del_min(t.rt)  # delete successor's old node
                h.lt = t.lt
                h.color = t.color  # color should not change
                return _balance(h)

        h.rt = BalancedBST._del(h.rt, key)
        return _balance(h)

    # --------------------------------------------------------------------------
    # Ordered symbol table methods.
    # --------------------------------------------------------------------------

    def min(self):
        """
        :return: the smallest key in this symbol table; None if empty
        """
        if self.is_empty():
            return None
        return BalancedBST._min(self._root).key

    @staticmethod
    def _min(h: _Node) -> _Node:
        # min() of subtree rooted at h
        while h.lt is not None:
            h = h.lt
        return h

    def max(self):
        """
        :return: the largest key in this symbol table; None if empty
        """
        if self.is_empty():
            return None
        h = self._root
        while h.rt is not None:
            h = h.rt
        return h.key

    def floor(self, key):
        """
        :param key: query key
        :return:    the largest key in this symbol table less than or equal
                    to key; None if there is no such key
        """
        champ = None
        h = self._root
        while h is not None:
            if key < h.key:
                h = h.lt
            elif h.key < key:
                champ = h.key
                h = h.rt
            else:
                return h.key
        return champ

    def ceiling(self, key):
        """
        :param key: query key
        :return:    the smallest key in this symbol table greater than or equal
                    to key; None if there is no such key
        """
        champ = None
        h = self._root
        while h is not None:
            if key < h.key:
                champ = h.key
                h = h.lt
            elif h.key < key:
                h = h.rt
            else:
                return h.key
        return champ

    def predecessor(self, key):
        """
        :param key: query key
        :return:    the largest key in this symbol table less than key;
                    None if there is no such key
        """
        champ = None
        h = self._root
        while h is not None:
            # identical to floor() except go left even if equal key found
            if h.key < key:
                champ = h.key
                h = h.rt
            else:
                h = h.lt
        return champ

    def successor(self, key):
        """
        :param key: query key
        :return:    the smallest key in this symbol table greater than key;
                    None if there is no such key
        """
        champ = None
        h = self._root
        while h is not None:
            # identical to ceiling() except go right even if equal key found
            if key < h.key:
                champ = h.key
                h = h.lt
            else:
                h = h.rt
        return champ

    # --------------------------------------------------------------------------
    # Rank and select methods.
    # --------------------------------------------------------------------------

    def rank(self, key) -> int:
        """
        :param key: query key
        :return:    the number of keys in this symbol table less than key
        """
        rank_ = 0
        h = self._root
        while h is not None:
            if key < h.key:
                h = h.lt
            elif h.key < key:
                rank_ += _len(h.lt) + 1
                h = h.rt
            else:
                rank_ += _len(h.lt)
                break
        return rank_

    def select(self, rank: int):
        """
        :param rank: order statistic
        :return:     The key of specified rank.
                     This key has the property that there are exactly rank keys
                     in this symbol table that are strictly smaller.
                     Returns None unless 0 <= rank < len(self).
        """
        if not (0 <= rank < len(self)):
            return None

        h = self._root
        while True:
            assert h is not None
            len_left = _len(h.lt)
            if rank < len_left:
                h = h.lt
            elif len_left < rank:
                rank -= len_left + 1
                h = h.rt
            else:
                return h.key

    # --------------------------------------------------------------------------
    # Range search and range count methods.
    # --------------------------------------------------------------------------

    def __iter__(self) -> iter:
        """:return: all entries in this symbol table in ascending order"""
        q = []
        BalancedBST._inorder(self._root, q)
        return iter(q)

    @staticmethod
    def _inorder(h: _Node, q: list):
        # populate q[] in subtree rooted at h with entries of keys in order
        if h is None:
            return
        BalancedBST._inorder(h.lt, q)
        q += [(h.key, h.val)]
        BalancedBST._inorder(h.rt, q)

    def entries(self, lo, hi) -> iter:
        """
        :param lo: minimum endpoint (inclusive)
        :param hi: maximum endpoint (inclusive)
        :return:   all entries in this symbol table
                   in range [lo, hi] in ascending order
        """
        q = []
        BalancedBST._entries(self._root, q, lo, hi)
        return iter(q)

    @staticmethod
    def _entries(h: _Node, q: list, lo, hi):
        # populate q[] in subtree rooted at h with entries of keys in [lo, hi]
        if h is None:
            return
        if lo < h.key:
            BalancedBST._entries(h.lt, q, lo, hi)
        if not (h.key < lo or hi < h.key):  # lo <= h.key <= hi
            q += [(h.key, h.val)]
        if h.key < hi:
            BalancedBST._entries(h.rt, q, lo, hi)

    def len(self, lo, hi) -> int:
        """
        :param lo: minimum endpoint (inclusive)
        :param hi: maximum endpoint (inclusive)
        :return:   the number of entries in this symbol table in range [lo, hi]
        """
        if hi < lo:
            return 0
        return self.rank(hi) - self.rank(lo) + (1 if hi in self else 0)

    # --------------------------------------------------------------------------
    # Red-black tree integrity tests.
    # @citation Adapted from: algs4.cs.princeton.edu/33balanced/
    # RedBlackBST.java.html. Accessed 2021/05/10.
    # --------------------------------------------------------------------------

    def _is_redblack_bst(self) -> bool:
        """Is this a left-leaning red-black binary search tree?

        :return: True if the integrity test passed; False otherwise
        """
        from math import log2

        def is_bst(h: _Node, lo, hi) -> bool:
            # is tree rooted at h a BST with keys strictly in (lo, hi)?
            if h is None:
                return True
            if not (lo is None or lo < h.key):
                return False
            if not (hi is None or h.key < hi):
                return False
            return is_bst(h.lt, lo, h.key) and is_bst(h.rt, h.key, hi)

        def is23(h: _Node) -> bool:
            # do all red links lean left and are they non-consecutive?
            if h is None:
                return True
            if _is_red(h.rt) or _is_red(h) and _is_red(h.lt):
                return False
            return is23(h.lt) and is23(h.rt)

        def is_balanced(h: _Node) -> bool:
            # is there perfect black balance?
            def balanced(x: _Node, black_: int) -> bool:
                if x is None:
                    return black_ == 0
                if _is_black(x):
                    black_ -= 1
                return balanced(x.lt, black_) and balanced(x.rt, black_)

            root = h
            black = 0
            while h is not None:
                if _is_black(h):
                    black += 1
                h = h.lt
            return balanced(root, black)

        def is_len_consistent(h: _Node) -> bool:
            # are the length fields consistent?
            if h is None:
                return True
            if h.len != _len(h.lt) + 1 + _len(h.rt):
                return False
            return is_len_consistent(h.lt) and is_len_consistent(h.rt)

        def is_rank_consistent() -> bool:
            # are the ranks consistent?
            for rank in range(len(self)):
                if rank != self.rank(self.select(rank)):
                    return False

            for key, val in self:
                itself = self.select(self.rank(key))
                if key < itself or itself < key:  # key != itself
                    return False
            return True

        def height(h: _Node) -> int:
            # returns the height of the subtree rooted at h
            return -1 if h is None else 1 + max(height(h.lt), height(h.rt))

        return (
            _is_black(self._root)
            and is_bst(self._root, None, None)
            and is23(self._root)
            and is_balanced(self._root)
            and is_len_consistent(self._root)
            and is_rank_consistent()
            and height(self._root) <= 2 * log2(len(self) + 1)
        )


# ------------------------------------------------------------------------------


def main():
    """Unit tests the BalancedBST data type."""
    import sys

    names = BalancedBST()

    # simple tests
    names["Sedgewick"] = "Bob"
    names["Wayne"] = "Kevin"
    names["Dondero"] = "Bob"
    assert "Dondero" in names and "Unalmis" not in names
    assert names["Sedgewick"] == "Bob"
    assert names["Wayne"] == "Kevin"
    assert names["Dondero"] == "Bob"
    assert names.get("Unalmis", "Kaya") == "Kaya"

    # consistency tests
    n = int(sys.argv[1])
    entries = tuple((i, 1) for i in range(n))
    st = BalancedBST(entries)

    lo = st.min()
    hi = st.max()
    for i, e in enumerate(st):
        key, val = e
        assert key == i and st[key] == val
        # equivalent functions when key in symbol table
        assert key == st.floor(key) == st.ceiling(key)
        assert st.len(lo, key) == i + 1
        assert key == lo and st.predecessor(key) is None or st.predecessor(key) == i - 1
        assert key == hi and st.successor(key) is None or st.successor(key) == i + 1

    # deletion
    st.del_min()
    st.del_max()
    del st[-1]  # -1 not in symbol table

    get_min = False
    while not st.is_empty():
        key = st.min() if get_min else st.max()
        del st[key]
        assert key not in st, "Deletion failed."
        get_min = not get_min


if __name__ == "__main__":
    main()
