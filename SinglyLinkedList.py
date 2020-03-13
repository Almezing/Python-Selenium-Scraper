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
        self.nextValue = None

# Linked List class object that'll be used to contain Node objects
class SinglyLinkedList:
    def __init__(self):
        self.headValue = None

sList = SinglyLinkedList()
weekday = ["Monday", "Tueday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday"]

sList.headValue = Node(weekday.pop(0))
sList.headValue.nextValue = Node(weekday.pop(0))
sList.headValue.nextValue.nextValue = Node(weekday.pop(0))

# weekday_Nodes = [Node(item) for item in weekday]

