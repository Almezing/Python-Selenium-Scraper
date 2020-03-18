"""
Python Quick Reference
https://www.geeksforgeeks.org/search-an-element-in-a-linked-list-iterative-and-recursive/

        Singly Linked List: Not a block of memory of data, but a list of pointers of data in memory

            This data structure consists of Nodes objects. A node can either be a head or a node after the head, and holds 2 properties: a reference or pointer to data and a reference to the next node in the structure. The first node is considered to be the head.

            Because Single Linked List have a single link to the next node,the data structure is only forward traversable. There is not a link to the previous node. A Doubly Linked List, a linked list with a reference to the previous and next node, always one to traverse the structure either way.

"""
# Node class object
# Node objects has an attribute called dataValue that defaults to None
# Else, it's a reference to data when a new Node object is instaniated
# Node object has a nextNode attribute that defaults to None
class Node:
    def __init__(self, dataValue = None):
        # Reference to actual data
        self.dataValue = dataValue
        # Reference to the next Node
        # Initialized as None
        self.nextNode = None


# Linked List class object that'll be used to contain Node objects
class SinglyLinkedList:
    def __init__(self):
        self.headNode = None
    # Prints the contents of the Linked List starting from head
    def print(self):
        temp = self.headNode
        while (temp):
            print(temp.dataValue)
            temp = temp.nextNode

    # Push a new Node at the head of the Linked List
    def push(self, dataValue):
        # Create the new node
        new_Node = Node(dataValue)
        # Make next of the new Node as head
        new_Node.nextNode = self.headNode
        # Move the head to point to the new Node
        self.headNode = new_Node

    # Insert a new Node at give point
    def insertAfter(self, previousNode, dataValue):
        # Check if given previousNode exists
        if previousNode is None:
            print("The given previous node must be in Linked List ")
            return
        # Create Node
        new_Node = Node(dataValue)
        # Make new Node nextNode the same the previousNode nextNode 
        new_Node.nextNode = previousNode.nextNode
        # Make nextNode of previousNode as new Node
        previousNode.next = new_Node

    # Add a new Node at the end of the list
    def append(self, dataValue):
        new_Node = Node(dataValue)
        # If Linked list is empty, make new Node the head
        if self.headNode is None:
            self.headNode = new_Node
            return
        # Get to the last node by checking nextNode is None
        last = self.headNode
        while (last.nextNode):
            last = last.nextNode
        # Add new Node to the list
        last.nextNode = new_Node

    # Delete Node by the first occurrence of key
    def deleteNode(self, key):
        temp = self.headNode
        #If headNode has the key to be deleted
        if temp is not None:
            if temp.dataValue == key:
                self.head = temp.nextNode
                temp = None
                return
        
        # Search for the key to be deleted, keep track of the previousNode
        while (temp is not None):
            if temp.dataValue == key:
                break
            prev = temp
            temp = temp.nextNode
        
        # If key was not found
        if temp == None:
            print("Key not found")
            return
        else:
            # Unlink the node from the list
            prev.nextNode = temp.nextNode
            temp = None
            print("Key deleted")

    # Length of Linked List through iteration
    def length(self):
        count = 0
        temp = self.headNode
        while(temp):
            temp = temp.nextNode
            count += 1
        return count
    # Search list for key (dataValue) through iteration
    def search(self, key):
        temp = self.headNode
        key_bool = False
        while(temp):
            if key == temp.dataValue:
                key_bool = True
                break
            temp = temp.nextNode
        return key_bool
    # Search list for key (dataValue) through recursion 
    def searchRecursive(self, node,key):
        # Base case
        if(not node):
            return False
        if (node.dataValue == key):
            return True
        return self.searchRecursive(node.nextNode, key)

    # Swap nodes given 2 keys
    def swap(self, key1, key2):
        """
        1) x and y may or may not be adjacent.
        2) Either x or y may be a head node.
        3) Either x or y may be last node.
        4) x and/or y may not be present in linked list.

        """

        # Check if the keys are the same
        if key1 == key2:
            return

        # Search for key1 and track the previousNode of key1
        previousKey1 = None
        currentKey1 = self.headNode
        while currentKey1 != None and currentKey1.dataValue != key1:
            previousKey1 = currentKey1
            currentKey1 = currentKey1.nextNode
        
        # Search for key2 and track the previousNode of key2
        previousKey2 = None
        currentKey2 = self.headNode
        while currentKey2 != None and currentKey2.dataValue != key2:
            previousKey2 = currentKey2
            currentKey2 = currentKey2.nextNode
        
        # Check if the keys are found
        if currentKey1 is None or currentKey2 is None:
            return
        
        # Check if key1 is the head
        if previousKey1 != None:
            previousKey1.next = currentKey2
        # Make key2 the head
        else:
            self.headNode = currentKey2

        # Check if key2 is the head
        if previousKey2 != None:
            previousKey2.next = currentKey1
        # Make key1 the head
        else:
            self.headNode = currentKey1

        # Swap the next pointers
        temp = currentKey1.nextNode
        currentKey1.nextNode = currentKey2.nextNode
        currentKey2.nextNode = temp


        # Bug if swapping last 2 nodes

sList = SinglyLinkedList()
weekday = ["Monday", "Tueday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday"]

sList.push(weekday.pop(0))

for day in weekday:
    sList.append(day)
# sList.print()
# print(sList.length())

# print(sList.search("Saturday"))
# print(sList.search("Manday"))


# print(sList.searchRecursive(sList.headNode, "Sturday"))

sList.swap("Monday","Saturday")
sList.print()

"""
Doubly Linked List

Node structure has point to the previous Node
"""

class DoublyNode(Node):
    def __init__(self, dataValue=None):
        super().__init__(dataValue=dataValue)
        self.previousValue = previousValue
        self.nextNode = None


class DoublyLinkedList:
    pass
