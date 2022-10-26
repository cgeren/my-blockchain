from hashlib import sha256 # https://docs.python.org/3/library/hashlib.html


class Node:
    def __init__(self, left=None, right=None, data=''):
        self.left = left
        self.right = right
        self.data = data
        self.hash = sha256(str(data).encode(encoding="ascii")).hexdigest()
        
    def is_child(self) -> bool:
        return not self.left and not self.right
    
    def set_data(self, data):
        if self.is_child():
            self.data = data
            self.hash = sha256(str(data).encode(encoding="ascii")).hexdigest()
        elif self.left and not self.right:
            self.hash = sha256(str(self.left.hash).encode(encoding="ascii")).hexdigest()
        else:
            self.hash = sha256(str(self.left.hash).encode(encoding="ascii")+ str(self.right.hash).encode(encoding="ascii")).hexdigest()
