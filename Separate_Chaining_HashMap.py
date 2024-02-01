# Description: Hash map implementation through chaining and using linked lists
# Project for datastructures class CS 261

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        This method updates the key/value pair in the hash map.  If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a new key/value pair must be added.
        """
        if self.table_load() >= 1:
            self.resize_table(self.get_capacity()*2)
        bucket_index = self._hash_function(key) % self.get_capacity()  # to get the bucket associated with the key
        SLL = self._buckets.get_at_index(bucket_index)  # gets the linkedlist at the bucket index
        if SLL.contains(key) is None:  # checks to see if the key is not already in the linkedlist
            SLL.insert(key, value)
            self._size += 1  # increases the size of the map as a key/value is added
        else:
            node = SLL.contains(key)  # the value of the key at the specified node
        # if the value of the current key is different from the value being put into the map, then update value in LL
            if node.value != value:
                node.value = value

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        counter = 0

        for i in range(self._buckets.length()):  # goes through the length of the hashmap array
            SLL = self._buckets.get_at_index(i)  # gets the linked list at each bucket
            if SLL.length() == 0:  # if the linked list is empty, increases counter as bucket is empty
                counter += 1
            else:
                pass  # if there are values in linked list then passes
        return counter

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self.get_size() / self.get_capacity()

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

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table.
        """

        if new_capacity < 1:  # make sure the new capacity is greater than 1
            return

        if self._is_prime(new_capacity) is True:  # checks to see if the new_capacity is a prime number
            pass
        else:
            new_capacity = self._next_prime(new_capacity)  # if not then sets it as next prime number
        if new_capacity == 2:
            pass
        # ******* Hello TA! - just some explaining, because I can not seem to think of a way to get resize(2) to work...
        # I know the problem with the resize function is if resize(2) is given then when new_hash is created the
        # new_hash gets a capacity of 3 because self_capacity = next_prime_number(capacity) so it always becomes 3
        # and if the capacity is 1 then it becomes 3 as well since the next_prime function increments by capacity + 2
        new_hash = HashMap(new_capacity, self._hash_function)  # creates a new hash map of new capacity
        key_values = self.get_keys_and_values()  # gets the key and values of the old (current) hash map

        for i in range(key_values.length()):  # goes through key/value DA
            key, value = key_values.pop()  # gets the key and value from each tuple
            new_hash.put(key, value)  # rehashes the key/value into new hash map with new capacity
        self._buckets = new_hash.get_buckets()  # replaces the buckets of current hashmap with new temp hashmap
        self._capacity = new_hash.get_capacity()  # updates the capacity

    def get(self, key: str):
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        bucket_index = self._hash_function(key) % self.get_capacity()
        SLL = self._buckets.get_at_index(bucket_index)  # gets the linkedlist at the bucket index
        if SLL.contains(key) is None:  # checks to see if the key is not already in the linkedlist
            return None
        else:
            node = SLL.contains(key)
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        bucket_index = self._hash_function(key) % self.get_capacity()
        SLL = self._buckets.get_at_index(bucket_index)  # gets the linkedlist at the bucket index
        if SLL.contains(key) is None:  # checks to see if the key is not already in the linkedlist
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing.
        """
        bucket_index = self._hash_function(key) % self.get_capacity()
        SLL = self._buckets.get_at_index(bucket_index)  # gets the linkedlist at the bucket index
        if SLL.contains(key) is None:  # checks to see if the key is not already in the linkedlist
            return
        else:
            SLL.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        """

        tuple_da = DynamicArray()  # creates an empty Dynamic array

        for i in range(self._buckets.length()):  # goes through the length of bucket array
            SLL = self._buckets.get_at_index(i)  # grabs the SLL at the specific bucket
            for i in SLL:  # goes through each key/value pair in the SLL
                tuple_da.append((i.key, i.value))  # adds each key/value pair as a tuple in the tuple_da
        return tuple_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    receives a dynamic array (that is not guaranteed to be sorted). This function will return a tuple containing,
    in this order, a dynamic array comprising the mode (most occurring) value/s of the array, and an integer that
    represents the highest frequency (how many times the mode value(s) appear).
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    for i in range(da.length()):
        if map.contains_key(da.get_at_index(i)) is True:
            map.put(da.get_at_index(i), map.get(da.get_at_index(i))+1)
        else:
            map.put(da.get_at_index(i), 1)
    new_da = DynamicArray()
    frequency = 0
    for i in range(map.get_capacity()):
        SLL = map.get_buckets().get_at_index(i)
        for i in SLL:  # goes through each node in the SLL
            if i.value > frequency:  # if the value (frequency counter) of the node is higher than current freq
                new_da = DynamicArray()  # empties the new_da
                new_da.append(i.key)  # adds the key to DA
                frequency = i.value  # sets new top frequency of occurrences of specific key
            elif i.value == frequency:  # if the key has the same amount of occurrences as the current mode
                new_da.append(i.key)  # adds to DA
            else:
                pass
    return (new_da, frequency)

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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(2)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(2)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")