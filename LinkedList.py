"""
Python Quick Reference

        Singly Linked List: Not a block of memory of data, but a list of pointers of data in memeory

            This data structure consists of Nodes objects. A node can either be a head or a node after the head, and holds 2 properties: a reference or pointer to data and a reference to the next node in the structure. The first node is considered to be the head.

            Because Single Linked List have a single link to the next node,the data structure is only forward traversable. There is not a link to the previous node. A Doubly Linked List, a linked list with a reference to the previous and next node, always one to travese the structure either way.

"""
# Node class object 
# Node objects has an attribute called dataValue that defaults to None
# Else, it's a reference to data when a new Node object is instaniated
# Node object has a nextValue attribute that defaults to None
class Node:
    def __init__(self, dataValue = None):
        # Reference to actual data
        self.dataValue = dataValue
        # Reference to the next Node
        # Initialized as None
        self.nextValue = None

# Linked List class object that'll be used to contain Node objects
class SinglyLinkedList:
    def __init__(self):
        self.headValue = None
    # Prints the contents of the Linked List starting from head
    def print(self):
        temp = self.headValue
        while (temp):
            print(temp.dataValue)
            temp = temp.nextValue

    # Push a new Node at the head of the Linked List
    def push(self, dataValue):
        # Create the new node
        new_Node = Node(dataValue)
        # Make next of the new Node as head
        new_Node.nextValue = self.headValue
        # Move the head to point to the new Node
        self.headValue = new_Node

    # Insert a new Node at give point
    def insertAfter(self, previousNode, dataValue):
        # Check if given previousNode exists
        if previousNode is None:
            print("The given previous node must be in Linked List ")
            return
        # Create Node
        new_Node = Node(dataValue)
        # Make new Node nextValue the same the preivousNode nextValue 
        new_Node.nextValue = previousNode.nextValue
        # Make nextValue of preivousNode as new Node
        previousNode.next = new_Node

    # Add a new Node at the end of the list
    def append(self, dataValue):
        new_Node = Node(dataValue)
        # If Linked list is empty, make new Node the head
        if self.headValue is None:
            self.headValue = new_Node
            return
        # Get to the last node by checking nextValue is None
        last = self.headValue
        while (last.nextValue):
            last = last.nextValue
        # Add new Node to the list
        last.nextValue = new_Node

    # Delete Node by the first occurance of key
    def deleteNode(self, key):
        temp = self.headValue
        #If headValue has the key to be deleted
        if temp is not None:
            if temp.dataValue == key:
                self.head = temp.nextValue
                temp = None
                return
        
        # Search for the key to be deleted, keep track of the previousNode
        while (temp is not None):
            if temp.dataValue == key:
                break
            prev = temp
            temp = temp.nextValue
        
        # If key was not found
        if temp == None:
            print("Key not found")
            return
        else:
            # Unlink the node from the list
            prev.nextValue = temp.nextValue
            temp = None
            print("Key deleted")

sList = SinglyLinkedList()
weekday = ["Monday", "Tueday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday"]

sList.push(weekday.pop(0))

for day in weekday:
    sList.append(day)

print("New Head of Linked List")
sList.print()

sList.deleteNode("Saturday")
sList.print()

"""
Doubly Linked List

Node structure has point to the previous Node
"""

class DoublyNode(Node):
    def __init__(self, dataValue=None):
        super().__init__(dataValue=dataValue)
        self.previousValue = previousValue
        self.nextValue = None


class DoublyLinkedList:
    pass
