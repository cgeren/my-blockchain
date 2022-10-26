### Header
# Data
# Previous hash
# Merkle root
# Timestamp
# Nonce

from ast import While
from time import time
from hashlib import sha256
from random import getrandbits

class Block:
  def __init__(self, tree, difficulty=0.5, prevHeader=(0<<256)):
    self.data = tree.__str__()
    self.prevHash = sha256(str(prevHeader).encode('ascii')).hexdigest().zfill(64) if prevHeader != (0<<256) else '0'*64
    self.tree = tree
    self.root = tree.root.hash # hexdigest
    self.difficulty = difficulty
    self.nonce, self.time = self.tryNonce()
  
  def tryNonce(self):
    target = self.root
    while True:
      random_bits = getrandbits(256)
      attempt = sha256(str(random_bits).encode('ascii')).hexdigest()
      if (abs(int(target, 16)-int(attempt, 16)) <= (1<<255)*self.difficulty):
        break
    return attempt, time()

  def getHeader(self):
    fullHeader = str(self.prevHash) + str(self.root) + str(self.time) + str(self.difficulty) + str(self.nonce)
    return fullHeader
  
  def print(self):
    all_accounts = self.tree

    print("BEGIN BLOCK\nBEGIN HEADER\n")
    print(str(self.prevHash) + "\n" + "TODO: Merkle Root Hash" + "\n" + str(self.timestamp) + "\n"
          + str(self.difficulty) + "\n" + "TODO: Nonce Value")
    print("END HEADER\n")
    print(all_accounts)

  def __str__(self):
    out = ""
    out += "BEGIN BLOCK\n"
    out += "BEGIN HEADER\n"
    out += self.prevHash + "\n"
    out += self.root + "\n"
    out += str(int(self.time)) + "\n"
    out += str(self.difficulty) + "\n"
    out += self.nonce + "\n"
    out += "END HEADER\n"
    out += self.data + "\n"
    out += "END BLOCK\n"
    return out