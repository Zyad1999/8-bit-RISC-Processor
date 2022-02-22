from constants import Memonics, Registers, TokenType
import sys

def read_file(file_name):
    source_code = open(file_name, 'r')
    return source_code.read().splitlines()

def write_file(machine_code_list, file_name):
    machine_code = open(file_name + '.hex', 'w')
    machine_code.write('v2.0 raw\n')
    for listitem in machine_code_list:
        machine_code.write('%s\n' % listitem)
    machine_code.close()

def is_address(s):
    return s.startswith('0x')

def is_imm(s):
    return s.startswith('#')

def parse_line(source_code):
    result = list()
    for i in source_code:
        splitted_line = i.split()
        line_list = [''] * 8
        if splitted_line[0] == Memonics.NOP.name:
            line_list[0] = fill_bits(5, hex(Memonics.NOP.value))
            line_list[1] = fill_bits(2, hex(Memonics.NOP.value))
            line_list[2] = fill_bits(1, hex(Memonics.NOP.value))
            line_list[3] = fill_bits(3, hex(Memonics.NOP.value))
            line_list[4] = fill_bits(3, hex(Memonics.NOP.value))
            line_list[5] = fill_bits(2, hex(Memonics.NOP.value))
            line_list[6] = fill_bits(16, hex(Memonics.NOP.value))
            line_list[7] = fill_bits(16, hex(Memonics.NOP.value))
        
        if splitted_line[0] == Memonics.HALT.name:
            line_list[0] = fill_bits(5,hex(Memonics.HALT.value))
            line_list[1] = fill_bits(2, hex(Memonics.NOP.value))
            line_list[2] = fill_bits(1, hex(Memonics.NOP.value))
            line_list[3] = fill_bits(3, hex(Memonics.NOP.value))
            line_list[4] = fill_bits(3, hex(Memonics.NOP.value))
            line_list[5] = fill_bits(2, hex(Memonics.NOP.value))
            line_list[6] = fill_bits(16, hex(Memonics.NOP.value))
            line_list[7] = fill_bits(16, hex(Memonics.NOP.value))
            result.append(line_list)
            break
       
        if splitted_line[0] == Memonics.ADD.name \
           or splitted_line[0] == Memonics.SUB.name \
           or splitted_line[0] == Memonics.MUL.name \
           or splitted_line[0] == Memonics.AND.name \
           or splitted_line[0] == Memonics.OR.name \
           or splitted_line[0] == Memonics.LOAD.name:

            # reg, reg/imm
            line_list[0] = fill_bits(5, hex(Memonics.__getitem__(splitted_line[0]).value)) # Operation
            line_list[2] = fill_bits(1, hex(Memonics.NOP.value))# Destination Type
            line_list[4] = fill_bits(3, hex(Registers.__getitem__(splitted_line[1]).value)) # Destination Register

            if is_imm(splitted_line[2]):
                line_list[1] = fill_bits(2, hex(TokenType.IMMEDIATE.value)) # Source Type
                line_list[6] = splitted_line[2] # Imm Value
                line_list[3] = fill_bits(3, hex(Memonics.NOP.value))
            elif is_address(splitted_line[2]) and splitted_line[0] == Memonics.LOAD.name: # For Load Only
                line_list[1] = fill_bits(2, hex(TokenType.ADDRESS.value)) # Source Type
                line_list[3] = fill_bits(3, hex(Memonics.NOP.value))
                line_list[7] = splitted_line[2] # Address Value
            elif splitted_line[2] in set(item.name for item in Registers): # Source is Register Also
                line_list[1] = fill_bits(2, hex(TokenType.REGISTER.value))
                line_list[3] = fill_bits(3, hex(Registers.__getitem__(splitted_line[2]).value))
            
            line_list[5] = fill_bits(2, hex(Memonics.NOP.value))

        if splitted_line == 2 \
            or splitted_line[0] == Memonics.LSL.name \
            or splitted_line[0] == Memonics.LSR.name \
            or splitted_line[0] == Memonics.COMP.name:

            # Operation REG
            line_list[0] = fill_bits(5,hex(Memonics.__getitem__(splitted_line[0]).value)) # Operation
            line_list[1] = fill_bits(2, hex(Memonics.NOP.value))
            line_list[2] = fill_bits(1, hex(Memonics.NOP.value))
            line_list[3] = fill_bits(3, hex(Memonics.NOP.value))
            line_list[4] = fill_bits(3,hex(Registers.__getitem__(splitted_line[1]).value))
            line_list[5] = fill_bits(2, hex(Memonics.NOP.value))

        if splitted_line[0] == Memonics.STORE.name:
            # STORE ADDRESS REG
            line_list[0] = fill_bits(5, hex(Memonics.__getitem__(splitted_line[0]).value)) # Operation
            line_list[2] = fill_bits(1, hex(TokenType.ADDRESS.value)) # Destination Type
            line_list[1] = fill_bits(2, hex(Memonics.NOP.value))
            line_list[3] = fill_bits(3, hex(Registers.__getitem__(splitted_line[2]).value))
            line_list[4] = fill_bits(3, hex(Memonics.NOP.value))
            line_list[5] = fill_bits(2, hex(Memonics.NOP.value))
            line_list[7] = splitted_line[1]

        if splitted_line[0] == Memonics.MOVE.name:
            # MOVE ADDRESS ADDRESS
            line_list[0] = fill_bits(5, hex(Memonics.__getitem__(splitted_line[0]).value)) # Operation
            line_list[2] = fill_bits(1, hex(TokenType.ADDRESS.value)) # Destination Type
            line_list[1] = line_list[1] = fill_bits(2, hex(TokenType.ADDRESS.value))
            line_list[3] = fill_bits(3, hex(Memonics.NOP.value))
            line_list[4] = fill_bits(3, hex(Memonics.NOP.value))
            line_list[5] = fill_bits(2, hex(Memonics.NOP.value))
            line_list[7] = splitted_line[1] + ',' + splitted_line[2]        
        
        if splitted_line[0].startswith(Memonics.JUMP.name): # Jump and Its variation

            if splitted_line[0].endswith('C'):
                line_list[5] = fill_bits(2, '0x01')
            elif splitted_line[0].endswith('Z'):
                line_list[5] = fill_bits(2, '0x02')
            elif splitted_line[0].endswith('N'):
                line_list[5] = fill_bits(2, '0x03')
            else:
                line_list[5] = fill_bits(2, '0x00')
            line_list[0] = fill_bits(5, hex(Memonics.__getitem__(splitted_line[0][0:4]).value)) # Operation
            for i in range(1, 5):
                line_list[i] = fill_bits(2, '0x00')
            
            line_list[7] = splitted_line[1]
        
        result.append(line_list)
   # print(result)
    return result

def fill_bits(n, value):
    return str(bin(int(value, 16)))[2:].zfill(n)

def extract_instruction(ins_list):
    final_res = []
    for i in ins_list:
        m = ''.join(i[0:6])
        m_hex = hex(int(m,2))[2:]
       
        if len(m_hex) > 2:
            m_hex_x = "0x{:04x}".format(int(m_hex, 16))[2:]
            final_res.append(m_hex_x[0:2])
            final_res.append(m_hex_x[2:])
        else:
            final_res.append(m_hex)
       
        if i[6] != '':
            imm_value = "0x{:02x}".format(int(i[6][3:], 16))[2:]
            final_res.append(imm_value[0:2])

        if i[7] != '':
            addr_val = i[7].split(',')
            
            dest_addr_hex = hex(int(addr_val[0][2:], 16))[2:]
            dest_addr = "0x{:04x}".format(int(dest_addr_hex, 16))[2:]
            final_res.append(dest_addr[0:2])
            final_res.append(dest_addr[2:])                   
        
            if len(addr_val) > 2:
                src_addr_hex = hex(int(addr_val[1][2:], 16))[2:]
                src_addr = "0x{:04x}".format(int(src_addr_hex, 16))[2:]
                final_res.append(src_addr[0:2])
                final_res.append(src_addr[2:])

            
    return final_res



if __name__ == "__main__":
    file_name = str(sys.argv[1])
    source_code = read_file(file_name)
    write_file(extract_instruction(parse_line(source_code)), file_name.split('.')[0])
