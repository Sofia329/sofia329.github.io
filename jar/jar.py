class Jar:

    def __init__(self, capacity=12):
        if not isinstance (capacity, int) or capacity < 0:
            raise ValueError("Capacity should be an integer and shld be >= 0")
        self._capacity = capacity
        self._size = 0


    def __str__(self):
        return"🍪" * self._size

    def deposit(self, n):
        if (self._size + n) > self._capacity:
            raise ValueError("Reached max capacity")
        self._size +=n

    def withdraw(self, n):
        if (self._size - n) < 0:
            raise ValueError ("Not enought cookies")
        self._size -=n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
