import hashlib
from hashlib import sha256
import re

class Block():
    _difficulty = 2
    _block_number = 0
    _nonce = 0
    _last_value = 0
    _current_value = 0
    _last_hash = 0
    _current_hash = ""


    def init(self,lastNumber, lastValue, currentValue, lastHash):
        self._block_number = lastNumber + 1
        self._last_value = lastValue
        self._current_value = currentValue
        self._last_hash = lastHash
        self.calc_hash()


    def calc_hash(self):
        longString = str(self._block_number)
        longString += str(self._last_value)
        longString += str(self._current_value)
        longString += self._last_hash
        is_valid = False
        zeroString = "0"
        for i in range(0,self._difficulty-1):
            zeroString+="0"
        while is_valid == False:
            secString = str(self._nonce)
            secString+=longString

            if(sha256(secString.encode()).hexdigest()[0:self._difficulty] == zeroString):
                is_valid = True
            else:
                self._nonce = self._nonce + 1
        self._current_hash = sha256(secString.encode()).hexdigest()

    def write_block(self,bn,nonce,lastV,currV,lastH,currH):
            self._block_number = bn
            self._nonce = nonce
            self._last_value = lastV
            self._current_value = currV
            self._last_hash = lastH
            self._current_hash = currH




class Blockchain:
    _chain =  []

    start_block = Block()
    start_block.init(0,0,5,"start")
    _chain[0:] = [start_block]

    dummy = head = start_block

    def add_block(self, currentValue):
        block = Block()
        block.init(self._chain[-1]._block_number,self._chain[-1]._current_value, currentValue,self._chain[-1]._current_hash)
        self._chain.append(block)
        print(len(self._chain))

    def writeBlocks(self):
        file_object = open("outputBV.txt","w")
        for i in self._chain:
            file_object.write("Block Number:   %s \n" % i._block_number)
            file_object.write("Last Value:     %s \n" % i._last_value  )
            file_object.write("Current Value:  %s \n" % i._current_value  )
            file_object.write("Nonce:          %s \n" % i._nonce)
            file_object.write("Last Hash:      %s \n" % i._last_hash  )
            file_object.write("Current Hash:   %s \n" % i._current_hash  )
            file_object.write("_____________________________________\n")
        file_object.write("######")
        file_object.close

    def readBlocks(self, path):
        blocklist = []

        file_object = open(path,"r")

        blocknumber = lastval = currval = nonce = 0
        lasthast = currenthash = ""
        bnTest = lvTest = cvTest = nTest = lhTest = chTest = False

        blockcount = 1
        for line in file_object:
            if line[0:5] == "_____":
                if(bnTest and lvTest and cvTest and nTest and lhTest and chTest):
                    block = Block().write_block(blocknumber,lastval,currval,nonce,lasthash,currenthash)
                    blocklist.append(block)
                    bnTest = lvTest =cvTest = nTest = lhTest = chTest = False
                    blockcount = blockcount + 1
                else :
                    raise ValueError('not all needed Blockentrys found in the %s. Block' % blockcount)

            elif line[0:12] == "Block Number":
                if(bnTest):
                    raise ValueError('wrong Format of read Block. Error BN')
                blocknumber = int(re.findall('\d+',line)[0])
                bnTest = True

            elif line[0:10] == "Last Value":
                if(lvTest):
                    raise ValueError('wrong Format of read Block. Error LV')
                lastval = int(re.findall('\d+',line)[0])
                lvTest = True

            elif line[0:13] == "Current Value":
                if(cvTest):
                    raise ValueError('wrong Format of read Block. Error CV')
                currval = int(re.findall('\d+',line)[0])
                cvTest = True

            elif line[0:5] == "Nonce":
                if(nTest):
                    raise ValueError('Wrong Format of read Block. Error N')
                nonce = int(re.findall('\d+',line)[0])
                nTest = True

            elif line[0:9] == "Last Hash":
                if(lhTest):
                    raise ValueError('Wrong Format of read Block. Error LH')
                lasthash = re.split(' +',line)[2]
                lhTest = True

            elif line[0:12] == "Current Hash":
                if(chTest):
                    raise ValueError('Wrong Format of read Block. Error CH')
                currenthash = re.split(' +',line)[2]
                chTest = True

        self._chain = blocklist
