import shared

## Data
raw = shared.read_file('2021/input/day16.txt')

test = ''''''.split('\n')

## Functions
class Bits():
    def __init__(self, hex) -> None:
        self.hex = hex
        self.bin = self.hex_to_bin(hex)
        self.packets = list(self.parse_packets(self.bin))
    
    def hex_to_bin(self, hex):
        lookup = {
            '0':'0000',
            '1':'0001',
            '2':'0010',
            '3':'0011',
            '4':'0100',
            '5':'0101',
            '6':'0110',
            '7':'0111',
            '8':'1000',
            '9':'1001',
            'A':'1010',
            'B':'1011',
            'C':'1100',
            'D':'1101',
            'E':'1110',
            'F':'1111',
            }
        return ''.join([lookup[char] for char in hex])
    
    def parse_packet(self, start=0):
        i = start
        packet = {'start': i}
        packet['version'] = int(self.bin[i:i+3], 2)
        i += 3
        packet['type_id'] = int(self.bin[i:i+3], 2)
        i += 3
        if packet['type_id'] == 4: # literal value
            literal_start = i
            num = self.bin[i+1:i+5]
            while self.bin[i] != '0':
                i += 5
                num += self.bin[i+1:i+5]
            packet['num'] = int(num, 2)
            #i += (i - literal_start) % 4     # Trailing zeros
        else: # operator
            length_type_id = 15 if self.bin[i] == '0' else 11
            i += 1
            packet['length_type_id'] = length_type_id
            packet['length'] = int(self.bin[i:i+length_type_id],2)
            i += length_type_id
            if length_type_id == 15:
                packet['subpackets'] = self.parse_packets(self.bin[i:i+packet['length']])
                i += packet['length']
            else:
                subpackets = []
                for _ in range(packet['length']):
                    subpackets.append(self.parse_packet(start=i))
                    i = subpackets[-1]['end'] + 1
                packet['subpackets'] = subpackets
        packet['end'] = i
        return packet

    def get_version_sum(self):
        out = 0
        for packet in self.packets:
            out += packet['version']
        return out

## Testing
x = Bits('D2FE28')
x.hex
x.bin
x.packets
x.get_version_sum()

x = Bits('620080001611562C8802118E34')
x.hex
x.bin
x.packets
x.get_version_sum()


assert Bits('8A004A801A8002F478').get_version_sum() == 16
assert Bits('620080001611562C8802118E34').get_version_sum() == 23
assert Bits('A0016C880162017C3686B18A3D4780').get_version_sum() == 31

## Solutions