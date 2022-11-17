# ------------------------------------------------------------------------------
# @author Kaya Unalmis
# python3 balanced_set.py 10000
# ------------------------------------------------------------------------------

from copy import deepcopy

_RED: bool = True
_BLACK: bool = False


class _Node:
    # BST node with color bit
    len: int
    color: bool

    def __init__(self, key, color: bool):
        if key is None:
            raise KeyError
        self.key = key
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
    # number of keys in subtree rooted at h
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
    on_bottom_level: bool = index >= (1 << (fence.bit_length() - 1))
    h = _Node(next(it), _RED if on_bottom_level else _BLACK)
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
#     h = _Node(list[mid], _BLACK)
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


class BalancedSET:
    """The BalancedSET class is an ordered set of distinct keys.

    It requires that the key type implements the < {__lt__} method.

    This implementation uses a left-leaning red-black binary search tree. It
    also uses iteration instead of recursion (wherever it is feasible to do so)
    due to overhead associated with recursion in Python.

    The __init__ method takes time linear in the number of supplied keys.
    The is_empty and __len__ methods take O(1) time. The __iter__ and keys
    methods take O(lg N + M) time, where N is the number of keys in the set, and
    M is the number of keys returned by the iterable.

    The __and__ method takes O(A lg B) time, where A, B are the number
    of keys in the smaller, larger set, respectively. The __or__ method takes
    O(B + A lg B) time. The issubset method takes O(N lg C) time, where C is the
    number of keys in the query set.

    All other methods take O(lg N) time.

    For additional documentation, see
    Section 3.3 of Algorithms, 4th Edition. Addison-Wesley Professional, 2011
    by Robert Sedgewick and Kevin Wayne.

    @author Kaya Unalmis
    """

    def __init__(self, keys=None):
        """
        Makes an empty set if keys is None.
        Otherwise, makes a set containing the pre-sorted keys.

        Takes linear time with zero key compares.

        :param keys:     sorted set of keys
        :raise KeyError: if None is in keys
        """
        if keys is None:
            self._root = None
        else:
            self._root = _make_bst(iter(keys), len(keys), 1)
            if not self.is_empty():
                self._root.color = _BLACK

        assert self._is_redblack_bst()

    def is_empty(self) -> bool:
        """:return: True if this set is empty, False otherwise"""
        return self._root is None

    def __len__(self) -> int:
        """:return: the number of keys in this set"""
        return _len(self._root)

    # --------------------------------------------------------------------------
    # BST search.
    # --------------------------------------------------------------------------

    def __contains__(self, key) -> bool:
        """
        :param key: query key
        :return:    True if this set contains key; False otherwise
        """
        h = self._root
        while h is not None:
            if key < h.key:
                h = h.lt
            elif h.key < key:
                h = h.rt
            else:
                return True

        return False

    # --------------------------------------------------------------------------
    # Red-black tree insertion. (only insert red nodes)
    # --------------------------------------------------------------------------

    def add(self, key):
        """Adds given key to this set.

        :param key:      the key to add
        :raise KeyError: if key is None
        """
        self._root = BalancedSET._add(self._root, key)
        self._root.color = _BLACK
        assert self._is_redblack_bst()

    @staticmethod
    def _add(h: _Node, key) -> _Node:
        # Search for key, grow tree if new.
        if h is None:
            return _Node(key, _RED)

        if key < h.key:
            h.lt = BalancedSET._add(h.lt, key)
        elif h.key < key:
            h.rt = BalancedSET._add(h.rt, key)

        return _balance(h)

    # --------------------------------------------------------------------------
    # Red-black tree deletion. (only delete red nodes)
    # --------------------------------------------------------------------------

    def remove_min(self):
        """Removes the smallest key from this set."""
        if self.is_empty():
            return
        if _is_black(self._root.lt) and _is_black(self._root.rt):
            self._root.color = _RED

        self._root = BalancedSET._remove_min(self._root)
        if not self.is_empty():
            self._root.color = _BLACK

        assert self._is_redblack_bst()

    @staticmethod
    def _remove_min(h: _Node) -> _Node or None:
        # removes the smallest key in subtree rooted at h
        if h.lt is None:
            return None
        if _is_black(h.lt) and _is_black(h.lt.lt):
            h = _move_red_left(h)

        h.lt = BalancedSET._remove_min(h.lt)
        return _balance(h)

    def remove_max(self):
        """Removes the largest key from this set."""
        if self.is_empty():
            return
        if _is_black(self._root.lt) and _is_black(self._root.rt):
            self._root.color = _RED

        self._root = BalancedSET._remove_max(self._root)
        if not self.is_empty():
            self._root.color = _BLACK

        assert self._is_redblack_bst()

    @staticmethod
    def _remove_max(h: _Node) -> _Node or None:
        # remove the largest key in subtree rooted at h
        if _is_red(h.lt):
            h = _rotate_right(h)
        else:
            if h.rt is None:
                return None
            if _is_black(h.rt) and _is_black(h.rt.lt):
                h = _move_red_right(h)

        h.rt = BalancedSET._remove_max(h.rt)
        return _balance(h)

    def remove(self, key):
        """:param key: the key to remove from this set"""
        if self.is_empty():
            return
        if _is_black(self._root.lt) and _is_black(self._root.rt):
            self._root.color = _RED

        self._root = BalancedSET._remove(self._root, key)
        if not self.is_empty():
            self._root.color = _BLACK

        assert self._is_redblack_bst()

    @staticmethod
    def _remove(h: _Node, key) -> _Node or None:
        # remove given key in subtree rooted at h
        if key < h.key:
            if h.lt is None:
                return _balance(h)  # key not in self
            if _is_black(h.lt) and _is_black(h.lt.lt):
                h = _move_red_left(h)

            h.lt = BalancedSET._remove(h.lt, key)
            return _balance(h)

        if _is_red(h.lt):
            h = _rotate_right(h)
        else:
            if h.rt is None:
                return _balance(h) if (key < h.key or h.key < key) else None
            if _is_black(h.rt) and _is_black(h.rt.lt):
                h = _move_red_right(h)
            if not (key < h.key or h.key < key):  # key == h.key
                # replace h with successor and remove successor's old node
                t = h
                h = BalancedSET._min(t.rt)  # successor of t
                h.rt = BalancedSET._remove_min(t.rt)  # remove successor's old node
                h.lt = t.lt
                h.color = t.color  # color should not change
                return _balance(h)

        h.rt = BalancedSET._remove(h.rt, key)
        return _balance(h)

    # --------------------------------------------------------------------------
    # Ordered SET methods.
    # --------------------------------------------------------------------------

    def min(self):
        """:return: the smallest key in this set; None if empty"""
        if self.is_empty():
            return None
        return BalancedSET._min(self._root).key

    @staticmethod
    def _min(h: _Node) -> _Node:
        # min() of subtree rooted at h
        while h.lt is not None:
            h = h.lt
        return h

    def max(self):
        """:return: the largest key in this set; None if empty"""
        if self.is_empty():
            return None
        h = self._root
        while h.rt is not None:
            h = h.rt
        return h.key

    def floor(self, key):
        """
        :param key: query key
        :return:    the largest key in this set less than or equal to
                    key; None if there is no such key
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
        :return:    the smallest key in this set greater than or equal to
                    key; None if there is no such key
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
        :return:    the largest key in this set less than key;
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
        :return:    the smallest key in this set greater than key;
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
        :return:    the number of keys in this set strictly less than key
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
        :return:     The key in this set of specified rank. This key has
                     the property that there are exactly rank keys in this set
                     that are strictly smaller. None if there is no such key.
        """
        if not 0 <= rank < len(self):
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
        """:return: all keys in this set in ascending order"""
        q = []
        BalancedSET._inorder(self._root, q)
        return iter(q)

    @staticmethod
    def _inorder(h: _Node, q: list):
        # populate q[] in subtree rooted at h with keys in order
        if h is None:
            return
        BalancedSET._inorder(h.lt, q)
        q += [h.key]
        BalancedSET._inorder(h.rt, q)

    def keys(self, lo, hi) -> iter:
        """
        :param lo: minimum endpoint (inclusive)
        :param hi: maximum endpoint (inclusive)
        :return:   all keys in this set in range [lo, hi] in ascending order
        """
        q = []
        BalancedSET._keys(self._root, q, lo, hi)
        return iter(q)

    @staticmethod
    def _keys(h: _Node, q: list, lo, hi):
        # populate q[] in subtree rooted at h with keys in [lo, hi]
        if h is None:
            return
        if lo < h.key:
            BalancedSET._keys(h.lt, q, lo, hi)
        if not (h.key < lo or hi < h.key):  # lo <= h.key <= hi
            q += [h.key]
        if h.key < hi:
            BalancedSET._keys(h.rt, q, lo, hi)

    def len(self, lo, hi) -> int:
        """
        :param lo: minimum endpoint (inclusive)
        :param hi: maximum endpoint (inclusive)
        :return:   the number of keys in this set in range [lo, hi]
        """
        if hi < lo:
            return 0
        return self.rank(hi) - self.rank(lo) + (1 if hi in self else 0)

    # --------------------------------------------------------------------------
    # Set methods.
    # --------------------------------------------------------------------------

    def issubset(self, other) -> bool:
        """
        :param other: query set
        :type other:  BalancedSET
        :return:      True if this set is a subset of other; False otherwise
        """
        if len(self) > len(other):
            return False
        for key in self:
            if key not in other:
                return False
        return True

    def __and__(self, other):
        """
        :param other: query set
        :type other:  BalancedSET
        :return:      intersection of this set and other
        :rtype:       BalancedSET
        """
        a, b = (self, other) if len(self) < len(other) else (other, self)
        intersection = BalancedSET()
        for key in a:
            if key in b:
                intersection.add(key)

        assert intersection.issubset(self) and intersection.issubset(other)
        return intersection

    def __or__(self, other):
        """
        :param other: query set
        :type other:  BalancedSET
        :return:      union of this set and other
        :rtype:       BalancedSET
        """
        a, b = (self, other) if len(self) < len(other) else (other, self)
        union = deepcopy(b)
        for key in a:
            union.add(key)

        assert self.issubset(union) and other.issubset(union)
        return union

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

            for key in self:
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
    """Unit tests the BalancedSET data type."""
    import sys

    names = BalancedSET()

    # simple tests
    names.add("Sedgewick")
    names.add("Wayne")
    names.add("Dondero")
    assert "Sedgewick" in names and "Wayne" in names and "Dondero" in names
    assert "Unalmis" not in names

    # Set methods
    wayne = BalancedSET()
    wayne.add("Wayne")
    intersection = wayne & names
    assert "Wayne" in intersection
    union = wayne | names
    assert len(union) == len(names)

    # consistency tests
    n = int(sys.argv[1])
    int_set = BalancedSET(tuple(range(n)))

    lo = int_set.min()
    hi = int_set.max()
    for i, key in enumerate(int_set):
        assert key == i and key in int_set
        # equivalent functions when key in set
        assert key == int_set.floor(key) == int_set.ceiling(key)
        assert int_set.len(lo, key) == i + 1
        assert (
            key == lo
            and int_set.predecessor(key) is None
            or int_set.predecessor(key) == i - 1
        )
        assert (
            key == hi
            and int_set.successor(key) is None
            or int_set.successor(key) == i + 1
        )

    # deletion
    int_set.remove_min()
    int_set.remove_max()
    int_set.remove(-1)  # -1 not in set

    get_min = False
    while not int_set.is_empty():
        key = int_set.min() if get_min else int_set.max()
        int_set.remove(key)
        assert key not in int_set, "Removal failed."
        get_min = not get_min


if __name__ == "__main__":
    main()
