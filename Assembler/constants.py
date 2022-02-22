from enum import Enum

class AddressesConstants(Enum):
    START_PROGRAM = 0x0000
    END_PROGRAM = 0x2000
    START_DATA = 0x2000
    END_DATA = 0x1FFF


class Memonics(Enum):
    NOP = 0x00
    ADD = 0x01
    SUB = 0x02
    MUL = 0x03
    AND = 0x04
    OR = 0x05
    LSR = 0x06
    LSL = 0x07
    COMP = 0x08
    JUMP = 0x0f
    LOAD = 0x10
    STORE = 0x11
    MOVE = 0x12
    HALT = 0x1F

class TokenType(Enum):
    REGISTER = 0
    IMMEDIATE = 2
    ADDRESS = 1

class Registers(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7


class Line():
    def __init__(self, line) -> None:
        self.line = line
        self.address = ""
        self.imm = ""
        self.src_reg = ""
        self.dest_reg = ""
        self.memonic = ""
        self.source_type = ""
        self.dest_type = ""
        self.condition = ""
        self.result = []
    def parse_line(self):
        splitted_arr = self.line.split()
        self.memonic = Memonics.__getitem__(splitted_arr[0].upper()).value
        
        rr = set(item.name for item in Registers)
        
        # Destination Check
        if (not self.is_address(splitted_arr[1])) and (not self.is_imm(splitted_arr[1])) and (splitted_arr[1].upper() in rr):
            self.dest_type = "0"
            self.dest_reg = Registers.__getitem__(splitted_arr[1].upper()).value
        elif self.is_address(splitted_arr[1]) and (not self.is_imm(splitted_arr[2])) and (not splitted_arr[1].upper() in rr): 
            # dest is memory
            self.dest_type = "1"
            self.address = splitted_arr[1]
        
        # Source Check
        if not self.is_address(splitted_arr[2]) and not self.is_imm(splitted_arr[2]) and splitted_arr[2].upper() in rr:
            self.source_type = "0"
            self.src_reg = Registers.__getitem__(splitted_arr[2].upper()).value
        elif self.is_address(splitted_arr[2]) and not self.is_imm(splitted_arr[2]) and not splitted_arr[2].upper() in rr: 
            # src is memory
            self.source_type = "1"
            self.address = splitted_arr[2]
        elif not self.is_address(splitted_arr[2]) and self.is_imm(splitted_arr[2]) and not splitted_arr[2].upper() in rr: 
            # src is memory
            self.source_type = "2"
            self.imm = splitted_arr[2]

    
    def is_address(s):
        return s.startswith('0x')
   
    def is_imm(s):
        return s.startswith('#')
   
    def get_dict(self):
        self.parse_line()
        return {'memonic': self.memonic, 'address': self.address, 'imm': self.imm, 'registers': self.registers}

    def get_result(self):
        self.parse_line()
        self.result.append(self.memonic, self.source_type, self.dest_type, self.src_reg, self.dest_reg)
        return self.result



