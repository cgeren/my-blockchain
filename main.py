#import tree
#import node
from random import randint
import sys
import re
import argparse
from hashlib import sha256
from tree import Tree
from block import Block

def main():
    # read in command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--debug', action='store_true')
    parser.add_argument('-B', '--bad', action='store_true')
    parser.add_argument('-F', '--file', nargs='+', type=str)
    args = parser.parse_args()

    # get file names
    #not in requirements. He wants it passed as arguments I believe
    #file_names_list = input("Please enter list of file names separated by spaces (ex. \"X.txt Y.txt Z.txt\"): ")

    list_of_leaf_sets = []
    saveFileName = None
    for filename in args.file:
        saveFileName = filename if saveFileName == None else saveFileName
        # read in.txt
        #Appending a ./code/ since the call is referenced to where the shell script is run
        file = open('./code/'+filename, "r")
        lines = file.readlines()

        # create a node for each line, store in a list
        nodes = []
        for line in lines: # NOTE: Should only really be one line per file, but keeping this just because its how the old code worked

            #PREVIOUSLY SPLIT AND CREATED DICTIONARY for address and balance
            #line = line.split() # split line by space
            #n = {"address": line[0], "balance": int(line[1][:-1])} # :-1 is to ignore null terminator
            
            #Now just inserts literal line to the leaves to append. No dictionary.
            n=line
            nodes.append(n)
        list_of_leaf_sets.append(nodes)

    # create a tree
    
    # optional debug prints
    if args.debug:
        t = Tree(nodes)
        print("[DEBUG] nodes: ", nodes)
        print(t, end="")
    elif args.bad:
        createBadBlocks(saveFileName)
    else:
        #Needs list of leaves in reverse order given from the arguments
        #i.e. Given arguments x.txt, y.txt, z.txt. It should be a leaves list given in the order, z, y, x.
        createRequiredBlocks(list_of_leaf_sets,saveFileName)

def createRequiredBlocks(listOfLeafs, fileName):
    fileName = fileName.split('.')[0] + '.block.out'
    writingBuffer = []
    with open(fileName, 'w') as f:
        previous_header= (0<<256)
        t=None
        block = None
        blockBuffer = []
        t = Tree(listOfLeafs[0])
        block = Block(t, 0.5, previous_header)
        blockBuffer.append(block)
        #print("TESTING IS VALID:  +  " + str(validateMerkleRoot(block)))
        previous_header = block.getHeader()
        writingBuffer.append(block.__str__())
        for leafSet in listOfLeafs[1:]:
            t = Tree(leafSet)
            block = Block(t, 0.5, previous_header)
            previous_header = block.getHeader()
            writingBuffer.append(block.__str__()+'\n')
            blockBuffer.append(block)
        validChain = isValid(blockBuffer)
        writingBuffer.reverse()
        for block in writingBuffer:
            f.write(block)
        if not(validChain):
            f.write("---------INVALID CHAIN----------")
    result = balance(blockBuffer, "344d6cdaDadeA5b9CEcD1EAc9230dD17d25860D4")
    print(result)

def createBadBlocks(fileName):
    fileName = fileName.split('.')[0] + '.block.out'
    writingBuffer = []
    listOfLeafs = [[''.join([str(chr(ord('F')-i))*40, ' ', str(randint(1000, 9999)), '\x00\n']) for i in range(6)] for _ in range(2)]
    print(listOfLeafs)
    with open(fileName, 'w') as f:
        previous_header= (0<<256)
        t=None
        block = None
        blockBuffer = []
        t = Tree(listOfLeafs[0])
        block = Block(t, 0.5, previous_header)
        blockBuffer.append(block)
        previous_header = block.getHeader()
        writingBuffer.append(block.__str__())
        for leafSet in listOfLeafs[1:]:
            t = Tree(leafSet)
            block = Block(t, 0.5, previous_header)
            previous_header = block.getHeader()
            writingBuffer.append(block.__str__()+'\n')
            blockBuffer.append(block)
        validChain = isValid(blockBuffer)
        writingBuffer.reverse()
        for block in writingBuffer:
            f.write(block)
        if not(validChain):
            f.write("---------INVALID CHAIN----------")
    
    

def isValid(blockList):
    currentlyValid = True
    for index in range(len(blockList)-1, 0, -1):
        currentlyValid = validateMerkleRoot(blockList[index])
        currentlyValid = sha256(str(blockList[index-1].getHeader()).encode('ascii')).hexdigest().zfill(64) == blockList[index].prevHash
        if not(bool(currentlyValid)): 
            return currentlyValid
    currentlyValid = validateMerkleRoot(blockList[0])
    currentlyValid = '0'*64 == blockList[0].prevHash
    # check all members in block
    return currentlyValid

def validateMerkleRoot(block_id):
    # check all members in block
    inputArray =block_id.tree.__str__().split('\n')
    #print(inputArray)
    VerificationTree = Tree(inputArray)
    recreatedRoot = sha256(VerificationTree.root.data.encode('ascii')).hexdigest()
    return block_id.root == recreatedRoot

def proveMember(chain, block_index, leaf_index):
    # chain: array of blocks (oldest to newest)
    # block_id: id of block we are trying to validate (0 for first block, 1 for second block, etc...)
    # leaf_index: index of leaf we are verifying in merkle tree

    leafsize = 2 ** chain[block_index].tree.treeHeight
    currentNode = chain[block_index].tree.root
    hasharray = [currentNode.hash]
    while leafsize > 1:
        # find left or right
        if leaf_index < leafsize / 2: # left child
            hasharray.insert(0, currentNode.right.hash)
            hasharray.insert(0, currentNode.left.hash)
            currentNode = currentNode.left
        else: # right child
            hasharray.insert(0, currentNode.left.hash)
            hasharray.insert(0, currentNode.right.hash)
            currentNode = currentNode.right
        # increment variables
        leafsize = leafsize / 2
        leaf_index = leaf_index - leafsize
        if leaf_index < 0:
            leaf_index = 0

    headers = []
    for i in range(block_index, len(chain)):
        headers.append(chain[i].data)

    # DEBUG PRINTS
    #print("--------starting hash--------")
    #print(currentNode.hash)
    #print("--------root--------")
    #print(chain[block_index].root)
    #print("--------tree--------")
    #chain[block_index].tree.print()
    #print("------------")
    #print("-----hash array -------")
    #print(hasharray)
    #print("------------")
    #print("--------headers---------")
    #print(headers)
    #print("---------------")

    return hasharray, headers

def balance(chain, address):
    returnBool = False
    returnArr = [] #return array that will include the balance, and then the proof of membership

    for i in range (len(chain) - 1, -1, -1): #search starting with newest blocks
        if searchForBlock(chain[i], address):#the first instance of the string address being found
            returnBool = True
            correctBlock = chain[i]
            dataString = correctBlock.tree.__str__()
            delimitedDataArr = re.split('\\n|\s', dataString)
            for j in range(len(delimitedDataArr)):
                if delimitedDataArr[j] == address:
                    returnArr.append(delimitedDataArr[j + 1])
                    returnArr.append((j-1)/2)
                    hashArray, _ = proveMember(chain, i, j/2)
                    returnArr += hashArray
                    #returnArr[1....end of proof of membership hashes] must be included in returnArr
                    return returnArr

    return returnBool

def searchForBlock(block, address):
    dataStr = block.tree.__str__()
    delimitedStr = re.split('\\n|\s', dataStr)
    for data in delimitedStr:
        if data == address:
            return True #along with the proof of membership
    return False



if __name__ == "__main__":
    main()
