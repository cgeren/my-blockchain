# merkle tree
from math import log, ceil
from node import Node

class Tree:

# constructor
#   empty tree
  def __init__(self, leaves):
    self.__height = ceil(log(len(leaves),2))
    self.print_list = []
    self.treeHeight = ceil(log(len(leaves),2))
    self.root, _ = self.makeNode(leaves,self.treeHeight)
    return

  def makeNode(self, leaves, currentHeight): #-> Node, leaf 
    if currentHeight > 0:
      leftNode, leaves = self.makeNode(leaves, currentHeight-1)
      rightNode = None
      if (len(leaves) != 0):
        rightNode, leaves = self.makeNode(leaves, currentHeight-1)
      currentNode = Node(leftNode, rightNode)
      currentNode.set_data(None) #Should not have to provide if hashing. 
      return currentNode, leaves
    else:
      newLeaf = Node(left=None, right=None, data=leaves[0])
      del leaves[0]
      return newLeaf, leaves

  def print(self):
    print(self.__str__())
    return

  def __str__(self):
    self.print_list.append("")
    self.print_helper(self.root, 0)
    finalString = ""
    for line in self.print_list:
      finalString = finalString + line
    self.print_list = []
    return finalString
    

  def print_helper(self, node, height):
    #if height > len(self.print_list) - 1:
      #self.print_list.append("")
    if self.__height == height:
      self.print_list[0] += (node.data)

    #try: OLD USED WITH DICTIONARY IN MAIN.PY
    #  self.print_list[height] += (node.data["address"][:3]) + "\t"
    #except:
    #  self.print_list[height] += (node.data[:3]) + "\t"\

    if node.left:
      self.print_helper(node.left, height + 1)
    if node.right:
      self.print_helper(node.right, height + 1)
