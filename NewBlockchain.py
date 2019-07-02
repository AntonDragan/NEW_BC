import hashlib
from hashlib import sha256
import random
from BCRoot import Blockchain

BC = Blockchain()


for i in range(1,10):
    BC.add_block(random.randint(1,1000))

BC.writeBlocks()
