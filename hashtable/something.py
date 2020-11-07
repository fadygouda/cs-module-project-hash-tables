class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        # self.next = None

    def __eq__(self, other):
        if isinstance(other, HashTableEntry):
            return self.key == other.key
        return False

    def __repr__(self):
        return f'HashTableEntry({self.key}, {self.value})'


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        currStr = ""
        curr = self.head
        while curr is not None:
            currStr += f'{str(curr.value)} ->'
            curr = curr.next
        return currStr

    # return node w/ value
    # runtime: O(n) where n = number nodes
    def find(self, value):
        curr = self.head
        while curr is not None:
            if curr.value == value:
                return curr
            curr = curr.next
        return None

    # deletes node w/ given value then return that node
    # runtime: O(n) where n = number of nodes
    def delete(self, value):
        curr = self.head

        # special case if we need to delete the head
        if curr.value == value:
            self.head = curr.next
            return curr

        prev = curr
        curr = curr.next

        while curr is not None:
            if curr.value == value:
                prev.next = curr.next
                curr.next = None
                return curr
            else:
                prev = curr
                curr = curr.next

        return None

    # insert node at head of list
    # runtime: O(1)
    def add_to_head(self, node):
        node.next = self.head
        self.head = node

    # overwrite node or insert node at head
    # runtime: O(n)
    def add_to_head_or_overwrite(self, node):
        existingNode = self.find(node.value) # O(n)
        if existingNode != None:
            existingNode.value = node.value
            return False
        else:
            self.add_to_head(node) #O(1)
            return True

    

class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity=MIN_CAPACITY):
        self.capacity = capacity
        self.storage = [None] * capacity
        self.items = 0

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.storage)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # load facter is the number of elements / number of slots
        return self.items / self.get_num_slots()


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        pass


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash_value = 5381
        for x in key:
            hash_value = (( hash_value << 5) + hash_value) + ord(x)
        return hash_value & 0xFFFFFFFF


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.get_num_slots()

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """

        
        
        
        # # check to see if the entry you are placing in the hashtable is none
        # # if it is, create the entry, increment the count of entries

        # if entry is None:
        #     self.storage[index] = HashTableEntry(key, value)
        #     self.items += 1
        #     self.resizeIfNeeded()
        #     return
        # # if there is an entry, check the next to see if the next entry exists and does not match the key. 
        # # if so, point to the next 
        # while entry.next != None and entry.key != key:
        #     entry = entry.next
        # # if the key matches, the value must match (deterministic)
        # # if it doesn't match and the next is empty, create the entry, increment the count of entries
        # if entry.key == key:
        #     entry.value = value
        # else:
        #     entry.next = HashTableEntry(key, value)
        #     self.items += 1
        #     self.resizeIfNeeded()
        # # self.storage[index(key)] = value
        index = self.hash_index(key)
        if self.storage[index] != None:
            linked_list = self.storage[index]
            did_add_new_node = linked_list.add_to_head_or_overwrite(Node(HashTableEntry(key, value)))
            if did_add_new_node:
                self.items += 1
                
            
        else:
            linked_list = LinkedList()
            linked_list.add_to_head(HashTableEntry(key, value))
            self.storage[index] = linked_list
            self.items += 1
        
        if self.get_load_factor() > 0.7:
            self.resize(self.get_num_slots() * 2)
        

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)
        
        # prev_entry = None
        # if entry is not None:
        #     while entry.next != None and entry.key != key:
        #         prev_entry = entry
        #         entry = entry.next
        # if entry.key == key:
        #     if prev_entry is None:
        #         self.storage[index] = entry.next
        #     else:
        #         prev_entry.next = entry.next
        #     self.items -= 1
        #     self.resizeIfNeeded()
        #     return
        if self.storage[index] != None:
            linked_list = self.storage[index]
            did_delete_node = linked_list.delete(HashTableEntry(key, None))
            if did_delete_node != None:
                self.items -= 1
                if self.get_load_factor() < 0.2:
                    self.resize(self.get_num_slots() / 2)
        else:
            print("Warning: node not found")
        
    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # index = self.hash_index(key)
        # entry = self.storage[index]

        # if entry is None:
        #     return None

        # while entry.next != None and entry.key != key:
        #     entry = entry.next
        
        # return entry.value if entry.key == key else None

        index = self.hash_index(key)

        if self.storage[index] != None:
            linked_list = self.storage[index]
            node = linked_list.find(HashTableEntry(key, None)) 
            if node != None:
                return node.value.value
        return None

    def resizeIfNeeded(self):
        if self.get_load_factor() > .7:
            self.resize(self.capacity * 2)

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # oldHashtable = self.storage
        # self.capacity = new_capacity
        # self.storage = [None] * new_capacity

        # for item in oldHashtable:
        #     while item is not None:
        #         key = item.key
        #         value = item.value
        #         index = self.hash_index(key)
        #         entry = self.storage[index]

        #         if entry is None:
        #             self.storage[index] = HashTableEntry(key, value)
        #         else:
        #             while entry.next != None:
        #                 entry = entry.next
        #             entry.next = HashTableEntry(key, value)

        #         item = item.next
        old_hashtable = self.storage
        self.storage = [None] * int(new_capacity)
        self.items = 0

        for element in old_hashtable:
            if element == None:
                continue
            curr_node = element.head
            while curr_node != None:
                temp = curr_node.next
                curr_node.next = None
                index = self.hash_index(curr_node.value.key)

                if self.storage[index] != None:
                    linked_list = self.storage[index]
                    linked_list.insert_at_head(curr_node)
                else:
                    linked_list = LinkedList()
                    linked_list.add_to_head(curr_node)
                    self.storage[index] = linked_list

                curr_node = temp
                self.items += 1 

                




if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
