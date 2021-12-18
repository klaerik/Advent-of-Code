import shared

## Data
raw = 'E20D41802B2984BD00540010F82D09E35880350D61A41D3004E5611E585F40159ED7AD7C90CF6BD6BE49C802DEB00525272CC1927752698693DA7C70029C0081002140096028C5400F6023C9C00D601ED88070070030005C2201448400E400F40400C400A50801E20004C1000809D14700B67676EE661137ADC64FF2BBAD745B3F2D69026335E92A0053533D78932A9DFE23AC7858C028920A973785338832CFA200F47C81D2BBBC7F9A9E1802FE00ACBA44F4D1E775DDC19C8054D93B7E72DBE7006AA200C41A8510980010D8731720CB80132918319804738AB3A8D3E773C4A4015A498E680292B1852E753E2B29D97F0DE6008CB3D4D031802D2853400D24DEAE0137AB8210051D24EB600844B95C56781B3004F002B99D8F635379EDE273AF26972D4A5610BA51004C12D1E25D802F32313239377B37100105343327E8031802B801AA00021D07231C2F10076184668693AC6600BCD83E8025231D752E5ADE311008A4EA092754596C6789727F069F99A4645008247D2579388DCF53558AE4B76B257200AAB80107947E94789FE76E36402868803F0D62743F00043A1646288800084C3F8971308032996A2BD8023292DF8BE467BB3790047F2572EF004A699E6164C013A007C62848DE91CC6DB459B6B40087E530AB31EE633BD23180393CBF36333038E011CBCE73C6FB098F4956112C98864EA1C2801D2D0F319802D60088002190620E479100622E4358952D84510074C0188CF0923410021F1CE1146E3006E3FC578EE600A4B6C4B002449C97E92449C97E92459796EB4FF874400A9A16100A26CEA6D0E5E5EC8841C9B8FE37109C99818023A00A4FD8BA531586BB8B1DC9AE080293B6972B7FA444285CC00AE492BC910C1697B5BDD8425409700562F471201186C0120004322B42489A200D4138A71AA796D00374978FE07B2314E99BFB6E909678A0'

## Functions
def hex_to_bin(hex):
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
    
def parse_packet(bin, start=0):
    i = start
    packet = {'start': i}
    packet['version'] = int(bin[i:i+3], 2)
    i += 3
    packet['type_id'] = int(bin[i:i+3], 2)
    i += 3
    if packet['type_id'] == 4: # literal value
        num = bin[i+1:i+5]
        while bin[i] != '0':
            i += 5
            num += bin[i+1:i+5]
        packet['num'] = int(num, 2)
        i += 5
    else: # operator
        packet['length_type_id'] = 15 if bin[i] == '0' else 11
        i += 1
        packet['length'] = int(bin[i:i+packet['length_type_id']],2)
        i += packet['length_type_id']
        subpackets = []
        if packet['length_type_id'] == 15:
            stop = i+packet['length']
            while i < stop:
                subpackets.append(parse_packet(bin, start=i))
                i = subpackets[-1]['end']
        else:
            for _ in range(packet['length']):
                subpackets.append(parse_packet(bin, start=i))
                i = subpackets[-1]['end']
        packet['subpackets'] = subpackets
    packet['end'] = i
    return packet
    
def collect_packets(bin):
    packets = []
    i = 0
    while not packets or packets[-1]['end'] < len(bin) - 11:
        packets.append(parse_packet(start=i))
        i = packets[-1]['end'] + 1
        print(i, packets[-1])
    return packets

def get_version_sum(packet):
    out = 0
    out += packet['version']
    if 'subpackets' in packet:
        for subpacket in packet['subpackets']:
            out += get_version_sum(subpacket)
    return out

def decode_bits(packet):
    typ = packet['type_id']
    if typ == 4:
        return packet['num']
    else:
        vals = [decode_bits(subpacket) for subpacket in packet['subpackets']]
    if typ == 0:
        return sum(vals)
    elif typ == 1:
        out = 1
        for val in vals:
            out *= val
        return out
    elif typ == 2:
        return min(vals)
    elif typ == 3:
        return max(vals)
    elif typ == 5:
        return 1 if vals[0] > vals[1] else 0
    elif typ == 6:
        return 1 if vals[0] < vals[1] else 0
    elif typ == 7:
        return 1 if vals[0] == vals[1] else 0
    else:
        return 'Not found'

def solve(raw):
    bin = hex_to_bin(raw)
    packets = parse_packet(bin)
    return get_version_sum(packets)

def solve2(raw):
    bin = hex_to_bin(raw)
    packets = parse_packet(bin)
    return decode_bits(packets)

## Testing
assert parse_packet(hex_to_bin('D2FE28'))['num'] == 2021

bin = hex_to_bin('EE00D40C823060')
packets = parse_packet(bin)
assert len(packets['subpackets']) == 3
assert packets['subpackets'][2]['num'] == 3

assert get_version_sum(parse_packet(hex_to_bin('8A004A801A8002F478'))) == 16
assert get_version_sum(parse_packet(hex_to_bin('620080001611562C8802118E34'))) == 12
assert get_version_sum(parse_packet(hex_to_bin('C0015000016115A2E0802F182340'))) == 23
assert get_version_sum(parse_packet(hex_to_bin('A0016C880162017C3686B18A3D4780'))) == 31
assert solve('A0016C880162017C3686B18A3D4780') == 31
assert solve2('C200B40A82') == 3
assert solve2('D8005AC2A8F0') == 1

## Solutions
print(f'Part 1: the total of version numbers is {solve(raw)}')
print(f'Part 2: the BITS transmission evaluates to {solve2(raw)}')