from pprint import pprint
from dataclasses import dataclass


"""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
       
    def __str__(self):
        return f"Node(data={self.data})"

class LinkedList:
    def __init__(self):
        self.head = None

if __name__ == "__main__":
    llist = LinkedList()
    
    llist.head = Node(10)
    middle = Node(20)
    last = Node(30)
    
    llist.head.next = middle
    middle.next = last
    
    def printNodes(node):
        while node is not None:
            pprint(node.data)
            pprint(node)
            node  = node.next
    
    printNodes(llist.head)
"""

"""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(seld):
        self.head = None
        
if __name__ == "__main__":
    llist = LinkedList()
    
    llist.head = Node(10)
    middle = Node(20)
    last = Node(30)
    
    llist.head.next = middle
    middle.next = last
    
    def addFirst(self, val):
        newNode = Node(val)
        newNode.next = self.head
        
        self.head = newNode
    
    def printNodes(node):
        while node is not None:
            pprint(node.data)            
            node  = node.next
    
    printNodes(llist.head)
"""

#class 
"""

"""
class Mammal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def eat(self):
        return "Munch munch..."

class Dog(Mammal):
    def __init__(self, name, age):
        super().__init__(name, age)
            



