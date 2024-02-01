# Description: Hash map implementation through open addressing
# Project for datastructures class CS 261

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a new key/value pair must be added.
        """
        while self.table_load() >= .5:  # checks load factor
            self.resize_table(self.get_capacity()*2)  # if load is more or equal than .5, fires resize function

        if self.contains_key(key) is True:  # checks to see if the key is already in the hashmap
            bucket_index = self.probe_find(key)  # gets the index of key
            bucket = self._buckets.get_at_index(bucket_index)  # gets the bucket at key index
            bucket.value = value  # sets bucket to new value
            if bucket.is_tombstone is True:
                bucket.is_tombstone = False
                self._size += 1
            return

        bucket_index = self._hash_function(key) % self.get_capacity()  # to get the bucket associated with the key
        intial_bucket = self._buckets.get_at_index(bucket_index)
        if self._buckets.get_at_index(bucket_index) is None:  # if bucket is empty, then puts key/value
            self._buckets.set_at_index(bucket_index, HashEntry(key, value))
            self._size += 1
        elif intial_bucket.is_tombstone is True:  # if tombstone is true, then puts key/values
            self._buckets.set_at_index(bucket_index, HashEntry(key, value))
            self._size += 1
        else:  # this means bucket is not empty and there is no tombstone
            self.probe_add(key, value)  # This will preform quadratic probing and place entry in next available index

    def probe_add(self, key: str, value: object) -> None:
        """
        A probing method to add a value to the hash map, takes in key/value pair and puts the value in the next open
        slot in the underlying dynamic array
        """
        j = 1  # helps find the next available spot
        exit_condition = 0  # exit condition when exit is not 0
        while exit_condition == 0:
            # finds next bucket according to probe
            bucket_index = (self._hash_function(key) + (j*j)) % self.get_capacity()
            bucket = self._buckets.get_at_index(bucket_index)
            if self._buckets.get_at_index(bucket_index) is None:
                self._buckets.set_at_index(bucket_index, HashEntry(key, value))
                self._size += 1
                exit_condition += 1
            elif bucket.is_tombstone is True:
                self._buckets.set_at_index(bucket_index, HashEntry(key, value))
                self._size += 1
                exit_condition += 1
            else:
                j += 1  # increases counter to find next bucket

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        # each bucket is either filled or empty so just subtract capacity - size
        return self.get_capacity() - self.get_size()

    def resize_table(self, new_capacity: int) -> None:
        """
        changes the capacity of the internal hash table. All existing key/value pairs
        will remain in the new hash map, and all hash table links will be rehashed
        """
        if new_capacity < self._size:  # checks if new capacity is less than current size
            return

        if self._is_prime(new_capacity) is True:  # checks if the new capacity is a prime number
            pass
        else:
            new_capacity = self._next_prime(new_capacity)  # if not then sets it as next prime number

        new_hash = HashMap(new_capacity, self._hash_function)  # creates a new hash map of new capacity

        for i in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(i)
            if bucket is None:
                pass
            elif bucket.is_tombstone is True:
                pass
            else:
                new_hash.put(bucket.key, bucket.value)
        self._capacity = new_hash.get_capacity()
        self._buckets = new_hash.get_buckets()

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        bucket_index = self.probe_find(key)  # runs prob_find which returns the index or None
        if bucket_index is None:
            return None
        bucket = self._buckets.get_at_index(bucket_index)
        if bucket.is_tombstone is True:  # if bucket is a tombstone, then nothing to remove
            return None
        bucket = self._buckets.get_at_index(bucket_index)  # gets the bucket at the index
        return bucket.value  # returns the value of the bucket

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        bucket_index = self.probe_find(key)  # runs prob_find which returns None or the index of the key
        if bucket_index is None:  # if none returns False as key not in hash map
            return False

        return True  # if an index is returned that means the key is in the hash map and returns True

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing
        """
        bucket_index = self.probe_find(key)  # prob_find returns the index of the key or None if key not in hash map

        if bucket_index is None:  # if bucket is empty then nothing to remove
            return
        bucket = self._buckets.get_at_index(bucket_index)
        if bucket.is_tombstone is True:  # if bucket is a tombstone, then nothing to remove
            return
        else:
            bucket = self._buckets.get_at_index(bucket_index)  # gets the bucket at the associated index
            bucket.is_tombstone = True  # sets it tombstone value to true
            self._size -= 1
            return None

    def probe_find(self, key: str):
        """
        A probing method to find the location of the key. returns the bucket index if found, or None if not found
        """
        bucket_index = self._hash_function(key) % self.get_capacity()  # looks at initial bucket index
        bucket = self._buckets.get_at_index(bucket_index)  # gets bucket at first index

        if bucket is None:
            return None
        if bucket.key == key:  # if it is the first index, then returns that bucket index
            return bucket_index
        else:
            j = 1  # helps find the next available spot
            exit_condition = 0  # exit condition when exit is not 0
            while exit_condition == 0:
                # finds next bucket according to probe
                bucket_index = (self._hash_function(key) + (j * j)) % self.get_capacity()
                bucket = self._buckets.get_at_index(bucket_index)
                if bucket is None:  # if the index is None, that means the key is not in the hash map
                    bucket_index = None  # sets bucket index to None
                    exit_condition += 1
                elif bucket.key == key:  # if the index is found fires exit condition
                    exit_condition += 1
                else:
                    j += 1  # increases counter to find next bucket

            return bucket_index

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        new_hash = HashMap(self.get_capacity(), self._hash_function)  # creates an empty hashmap of same length
        self._buckets = new_hash.get_buckets()  # sets current buckets to newly created empty buckets
        self._size = 0  # resets the size counter to 0

    def get_buckets(self):
        """
        returns the buckets object of a hashmap
        """
        new_buckets = self._buckets
        return new_buckets

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map
        """
        tuple_da = DynamicArray()  # creates an empty Dynamic array

        for i in range(self._buckets.length()):  # goes through the length of bucket array
            bucket = self._buckets.get_at_index(i)
            if bucket is None:
                pass
            elif bucket.is_tombstone is True:
                pass
            else:
                tuple_da.append((bucket.key, bucket.value))

        return tuple_da

    def __iter__(self):
        """
        Create iterator for loop
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        try:
            value = self._buckets[self._index]  # gets the value
            # if the value is None or tombstone then keep going until it hits next index with a value
            while value is None or value.is_tombstone is True:
                self._index += 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)