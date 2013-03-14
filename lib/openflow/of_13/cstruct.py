import struct

# Structure definitions
class ofp_table_feature_prop_header(object):
    """Automatically generated Python class for ofp_table_feature_prop_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.length = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.length)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        return outstr


class ofp_hello(object):
    """Automatically generated Python class for ofp_hello

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 0):
            return binaryString
        return binaryString[0:]

    def __len__(self):
        """Return length of message
        """
        l = 0
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        return outstr


class ofp_meter_band_header(object):
    """Automatically generated Python class for ofp_meter_band_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.rate = 0
        self.burst_size = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHLL", self.type, self.len, self.rate, self.burst_size)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 12):
            return binaryString
        fmt = '!HHLL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.rate, self.burst_size) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[12:]

    def __len__(self):
        """Return length of message
        """
        l = 12
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.rate !=  other.rate: return False
        if self.burst_size !=  other.burst_size: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'rate: ' + str(self.rate) + '\n'
        outstr += prefix + 'burst_size: ' + str(self.burst_size) + '\n'
        return outstr


class ofp_aggregate_stats_reply(object):
    """Automatically generated Python class for ofp_aggregate_stats_reply

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.packet_count = 0
        self.byte_count = 0
        self.flow_count = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!QQL", self.packet_count, self.byte_count, self.flow_count)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 24):
            return binaryString
        fmt = '!QQL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.packet_count, self.byte_count, self.flow_count) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 20
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[24:]

    def __len__(self):
        """Return length of message
        """
        l = 24
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.packet_count !=  other.packet_count: return False
        if self.byte_count !=  other.byte_count: return False
        if self.flow_count !=  other.flow_count: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'packet_count: ' + str(self.packet_count) + '\n'
        outstr += prefix + 'byte_count: ' + str(self.byte_count) + '\n'
        outstr += prefix + 'flow_count: ' + str(self.flow_count) + '\n'
        return outstr


class ofp_role_request(object):
    """Automatically generated Python class for ofp_role_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.role = 0
        self.pad= [0,0,0,0]
        self.generation_id = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.role)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        packed += struct.pack("!Q", self.generation_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.role,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!Q'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.generation_id,) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.role !=  other.role: return False
        if self.pad !=  other.pad: return False
        if self.generation_id !=  other.generation_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'role: ' + str(self.role) + '\n'
        outstr += prefix + 'generation_id: ' + str(self.generation_id) + '\n'
        return outstr


class ofp_table_stats(object):
    """Automatically generated Python class for ofp_table_stats

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.table_id = 0
        self.pad= [0,0,0]
        self.active_count = 0
        self.lookup_count = 0
        self.matched_count = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 3):
            return (False, "self.pad is not of size 3 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!B", self.table_id)
        packed += struct.pack("!BBB", self.pad[0], self.pad[1], self.pad[2])
        packed += struct.pack("!LQQ", self.active_count, self.lookup_count, self.matched_count)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 24):
            return binaryString
        fmt = '!B'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.table_id,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBB'
        start = 1
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LQQ'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.active_count, self.lookup_count, self.matched_count) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[24:]

    def __len__(self):
        """Return length of message
        """
        l = 24
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.table_id !=  other.table_id: return False
        if self.pad !=  other.pad: return False
        if self.active_count !=  other.active_count: return False
        if self.lookup_count !=  other.lookup_count: return False
        if self.matched_count !=  other.matched_count: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'active_count: ' + str(self.active_count) + '\n'
        outstr += prefix + 'lookup_count: ' + str(self.lookup_count) + '\n'
        outstr += prefix + 'matched_count: ' + str(self.matched_count) + '\n'
        return outstr


class ofp_table_mod(object):
    """Automatically generated Python class for ofp_table_mod

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.table_id = 0
        self.pad= [0,0,0]
        self.config = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 3):
            return (False, "self.pad is not of size 3 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!B", self.table_id)
        packed += struct.pack("!BBB", self.pad[0], self.pad[1], self.pad[2])
        packed += struct.pack("!L", self.config)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!B'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.table_id,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBB'
        start = 1
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!L'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.config,) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.table_id !=  other.table_id: return False
        if self.pad !=  other.pad: return False
        if self.config !=  other.config: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'config: ' + str(self.config) + '\n'
        return outstr


class ofp_group_stats(object):
    """Automatically generated Python class for ofp_group_stats

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.length = 0
        self.pad= [0,0]
        self.group_id = 0
        self.ref_count = 0
        self.pad2= [0,0,0,0]
        self.packet_count = 0
        self.byte_count = 0
        self.duration_sec = 0
        self.duration_nsec = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 2):
            return (False, "self.pad is not of size 2 as expected.")
        if(not isinstance(self.pad2, list)):
            return (False, "self.pad2 is not list as expected.")
        if(len(self.pad2) != 4):
            return (False, "self.pad2 is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!H", self.length)
        packed += struct.pack("!BB", self.pad[0], self.pad[1])
        packed += struct.pack("!LL", self.group_id, self.ref_count)
        packed += struct.pack("!BBBB", self.pad2[0], self.pad2[1], self.pad2[2], self.pad2[3])
        packed += struct.pack("!QQLL", self.packet_count, self.byte_count, self.duration_sec, self.duration_nsec)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 40):
            return binaryString
        fmt = '!H'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.length,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BB'
        start = 2
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LL'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.group_id, self.ref_count) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 12
        end = start + struct.calcsize(fmt)
        (self.pad2[0], self.pad2[1], self.pad2[2], self.pad2[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!QQLL'
        start = 16
        end = start + struct.calcsize(fmt)
        (self.packet_count, self.byte_count, self.duration_sec, self.duration_nsec) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[40:]

    def __len__(self):
        """Return length of message
        """
        l = 40
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.length !=  other.length: return False
        if self.pad !=  other.pad: return False
        if self.group_id !=  other.group_id: return False
        if self.ref_count !=  other.ref_count: return False
        if self.pad2 !=  other.pad2: return False
        if self.packet_count !=  other.packet_count: return False
        if self.byte_count !=  other.byte_count: return False
        if self.duration_sec !=  other.duration_sec: return False
        if self.duration_nsec !=  other.duration_nsec: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        outstr += prefix + 'group_id: ' + str(self.group_id) + '\n'
        outstr += prefix + 'ref_count: ' + str(self.ref_count) + '\n'
        outstr += prefix + 'packet_count: ' + str(self.packet_count) + '\n'
        outstr += prefix + 'byte_count: ' + str(self.byte_count) + '\n'
        outstr += prefix + 'duration_sec: ' + str(self.duration_sec) + '\n'
        outstr += prefix + 'duration_nsec: ' + str(self.duration_nsec) + '\n'
        return outstr


class ofp_bucket_counter(object):
    """Automatically generated Python class for ofp_bucket_counter

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.packet_count = 0
        self.byte_count = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!QQ", self.packet_count, self.byte_count)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!QQ'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.packet_count, self.byte_count) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.packet_count !=  other.packet_count: return False
        if self.byte_count !=  other.byte_count: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'packet_count: ' + str(self.packet_count) + '\n'
        outstr += prefix + 'byte_count: ' + str(self.byte_count) + '\n'
        return outstr


class ofp_instruction_actions(object):
    """Automatically generated Python class for ofp_instruction_actions

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.len)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        return outstr


class ofp_queue_stats(object):
    """Automatically generated Python class for ofp_queue_stats

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.port_no = 0
        self.queue_id = 0
        self.tx_bytes = 0
        self.tx_packets = 0
        self.tx_errors = 0
        self.duration_sec = 0
        self.duration_nsec = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LLQQQLL", self.port_no, self.queue_id, self.tx_bytes, self.tx_packets, self.tx_errors, self.duration_sec, self.duration_nsec)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 40):
            return binaryString
        fmt = '!LLQQQLL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.port_no, self.queue_id, self.tx_bytes, self.tx_packets, self.tx_errors, self.duration_sec, self.duration_nsec) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[40:]

    def __len__(self):
        """Return length of message
        """
        l = 40
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.port_no !=  other.port_no: return False
        if self.queue_id !=  other.queue_id: return False
        if self.tx_bytes !=  other.tx_bytes: return False
        if self.tx_packets !=  other.tx_packets: return False
        if self.tx_errors !=  other.tx_errors: return False
        if self.duration_sec !=  other.duration_sec: return False
        if self.duration_nsec !=  other.duration_nsec: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'port_no: ' + str(self.port_no) + '\n'
        outstr += prefix + 'queue_id: ' + str(self.queue_id) + '\n'
        outstr += prefix + 'tx_bytes: ' + str(self.tx_bytes) + '\n'
        outstr += prefix + 'tx_packets: ' + str(self.tx_packets) + '\n'
        outstr += prefix + 'tx_errors: ' + str(self.tx_errors) + '\n'
        outstr += prefix + 'duration_sec: ' + str(self.duration_sec) + '\n'
        outstr += prefix + 'duration_nsec: ' + str(self.duration_nsec) + '\n'
        return outstr


class ofp_meter_config(object):
    """Automatically generated Python class for ofp_meter_config

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.length = 0
        self.flags = 0
        self.meter_id = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHL", self.length, self.flags, self.meter_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.length, self.flags, self.meter_id) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.length !=  other.length: return False
        if self.flags !=  other.flags: return False
        if self.meter_id !=  other.meter_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        outstr += prefix + 'flags: ' + str(self.flags) + '\n'
        outstr += prefix + 'meter_id: ' + str(self.meter_id) + '\n'
        return outstr


class ofp_error_msg(object):
    """Automatically generated Python class for ofp_error_msg

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.code = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.code)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.code) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.code !=  other.code: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'code: ' + str(self.code) + '\n'
        return outstr


class ofp_experimenter_multipart_header(object):
    """Automatically generated Python class for ofp_experimenter_multipart_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.experimenter = 0
        self.exp_type = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LL", self.experimenter, self.exp_type)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!LL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.experimenter, self.exp_type) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.experimenter !=  other.experimenter: return False
        if self.exp_type !=  other.exp_type: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        outstr += prefix + 'exp_type: ' + str(self.exp_type) + '\n'
        return outstr


class ofp_experimenter_header(object):
    """Automatically generated Python class for ofp_experimenter_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.experimenter = 0
        self.exp_type = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LL", self.experimenter, self.exp_type)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!LL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.experimenter, self.exp_type) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.experimenter !=  other.experimenter: return False
        if self.exp_type !=  other.exp_type: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        outstr += prefix + 'exp_type: ' + str(self.exp_type) + '\n'
        return outstr


class ofp_table_feature_prop_next_tables(object):
    """Automatically generated Python class for ofp_table_feature_prop_next_tables

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.length = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.length)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        return outstr


class ofp_port_stats_request(object):
    """Automatically generated Python class for ofp_port_stats_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.port_no = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.port_no)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.port_no,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.port_no !=  other.port_no: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'port_no: ' + str(self.port_no) + '\n'
        return outstr


class ofp_instruction(object):
    """Automatically generated Python class for ofp_instruction

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.len)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        return outstr


class ofp_table_features(object):
    """Automatically generated Python class for ofp_table_features

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.length = 0
        self.table_id = 0
        self.pad= [0,0,0,0,0]
        self.name= ""
        self.metadata_match = 0
        self.metadata_write = 0
        self.config = 0
        self.max_entries = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 5):
            return (False, "self.pad is not of size 5 as expected.")
        if(not isinstance(self.name, str)):
            return (False, "self.name is not string as expected.")
        if(len(self.name) > 32):
            return (False, "self.name is not of size 32 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HB", self.length, self.table_id)
        packed += struct.pack("!BBBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4])
        packed += self.name.ljust(32,'\0')
        packed += struct.pack("!QQLL", self.metadata_match, self.metadata_write, self.config, self.max_entries)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 64):
            return binaryString
        fmt = '!HB'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.length, self.table_id) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBBB'
        start = 3
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4]) = struct.unpack(fmt, binaryString[start:end])
        self.name = binaryString[8:40].replace("\0","")
        fmt = '!QQLL'
        start = 40
        end = start + struct.calcsize(fmt)
        (self.metadata_match, self.metadata_write, self.config, self.max_entries) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[64:]

    def __len__(self):
        """Return length of message
        """
        l = 64
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.length !=  other.length: return False
        if self.table_id !=  other.table_id: return False
        if self.pad !=  other.pad: return False
        if self.name !=  other.name: return False
        if self.metadata_match !=  other.metadata_match: return False
        if self.metadata_write !=  other.metadata_write: return False
        if self.config !=  other.config: return False
        if self.max_entries !=  other.max_entries: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'name: ' + str(self.name) + '\n'
        outstr += prefix + 'metadata_match: ' + str(self.metadata_match) + '\n'
        outstr += prefix + 'metadata_write: ' + str(self.metadata_write) + '\n'
        outstr += prefix + 'config: ' + str(self.config) + '\n'
        outstr += prefix + 'max_entries: ' + str(self.max_entries) + '\n'
        return outstr


class ofp_group_stats_request(object):
    """Automatically generated Python class for ofp_group_stats_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.group_id = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.group_id)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.group_id,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.group_id !=  other.group_id: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'group_id: ' + str(self.group_id) + '\n'
        return outstr


class ofp_table_feature_prop_oxm(object):
    """Automatically generated Python class for ofp_table_feature_prop_oxm

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.length = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.length)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        return outstr


class ofp_hello_elem_header(object):
    """Automatically generated Python class for ofp_hello_elem_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.length = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.length)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        return outstr


class ofp_aggregate_stats_request(object):
    """Automatically generated Python class for ofp_aggregate_stats_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.table_id = 0
        self.pad= [0,0,0]
        self.out_port = 0
        self.out_group = 0
        self.pad2= [0,0,0,0]
        self.cookie = 0
        self.cookie_mask = 0
        self.match = ofp_match()
        self.match.length = OFP_MATCH_BYTES

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 3):
            return (False, "self.pad is not of size 3 as expected.")
        if(not isinstance(self.pad2, list)):
            return (False, "self.pad2 is not list as expected.")
        if(len(self.pad2) != 4):
            return (False, "self.pad2 is not of size 4 as expected.")
        if(not isinstance(self.match, ofp_match)):
            return (False, "self.match is not class ofp_match as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!B", self.table_id)
        packed += struct.pack("!BBB", self.pad[0], self.pad[1], self.pad[2])
        packed += struct.pack("!LL", self.out_port, self.out_group)
        packed += struct.pack("!BBBB", self.pad2[0], self.pad2[1], self.pad2[2], self.pad2[3])
        packed += struct.pack("!QQ", self.cookie, self.cookie_mask)
        packed += self.match.pack()
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 40):
            return binaryString
        fmt = '!B'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.table_id,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBB'
        start = 1
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LL'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.out_port, self.out_group) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 12
        end = start + struct.calcsize(fmt)
        (self.pad2[0], self.pad2[1], self.pad2[2], self.pad2[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!QQ'
        start = 16
        end = start + struct.calcsize(fmt)
        (self.cookie, self.cookie_mask) = struct.unpack(fmt,  binaryString[start:end])
        self.match.unpack(binaryString[32:])
        return binaryString[40:]

    def __len__(self):
        """Return length of message
        """
        l = 40
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.table_id !=  other.table_id: return False
        if self.pad !=  other.pad: return False
        if self.out_port !=  other.out_port: return False
        if self.out_group !=  other.out_group: return False
        if self.pad2 !=  other.pad2: return False
        if self.cookie !=  other.cookie: return False
        if self.cookie_mask !=  other.cookie_mask: return False
        if self.match !=  other.match: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'out_port: ' + str(self.out_port) + '\n'
        outstr += prefix + 'out_group: ' + str(self.out_group) + '\n'
        outstr += prefix + 'cookie: ' + str(self.cookie) + '\n'
        outstr += prefix + 'cookie_mask: ' + str(self.cookie_mask) + '\n'
        outstr += prefix + 'match: \n' 
        outstr += self.match.show(prefix + '  ')
        return outstr


class ofp_queue_get_config_request(object):
    """Automatically generated Python class for ofp_queue_get_config_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.port = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.port)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.port,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.port !=  other.port: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'port: ' + str(self.port) + '\n'
        return outstr


class ofp_packet_in(object):
    """Automatically generated Python class for ofp_packet_in

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.buffer_id = 0
        self.total_len = 0
        self.reason = 0
        self.table_id = 0
        self.cookie = 0
        self.match = ofp_match()
        self.match.length = OFP_MATCH_BYTES

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.match, ofp_match)):
            return (False, "self.match is not class ofp_match as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LHBBQ", self.buffer_id, self.total_len, self.reason, self.table_id, self.cookie)
        packed += self.match.pack()
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 24):
            return binaryString
        fmt = '!LHBBQ'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.buffer_id, self.total_len, self.reason, self.table_id, self.cookie) = struct.unpack(fmt,  binaryString[start:end])
        self.match.unpack(binaryString[16:])
        return binaryString[24:]

    def __len__(self):
        """Return length of message
        """
        l = 24
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.buffer_id !=  other.buffer_id: return False
        if self.total_len !=  other.total_len: return False
        if self.reason !=  other.reason: return False
        if self.table_id !=  other.table_id: return False
        if self.cookie !=  other.cookie: return False
        if self.match !=  other.match: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'buffer_id: ' + str(self.buffer_id) + '\n'
        outstr += prefix + 'total_len: ' + str(self.total_len) + '\n'
        outstr += prefix + 'reason: ' + str(self.reason) + '\n'
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'cookie: ' + str(self.cookie) + '\n'
        outstr += prefix + 'match: \n' 
        outstr += self.match.show(prefix + '  ')
        return outstr


class ofp_instruction_experimenter(object):
    """Automatically generated Python class for ofp_instruction_experimenter

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.experimenter = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHL", self.type, self.len, self.experimenter)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.experimenter) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.experimenter !=  other.experimenter: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        return outstr


class ofp_action_nw_ttl(object):
    """Automatically generated Python class for ofp_action_nw_ttl

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.nw_ttl = 0
        self.pad= [0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 3):
            return (False, "self.pad is not of size 3 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHB", self.type, self.len, self.nw_ttl)
        packed += struct.pack("!BBB", self.pad[0], self.pad[1], self.pad[2])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHB'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.nw_ttl) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBB'
        start = 5
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.nw_ttl !=  other.nw_ttl: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'nw_ttl: ' + str(self.nw_ttl) + '\n'
        return outstr


class ofp_port_status(object):
    """Automatically generated Python class for ofp_port_status

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.reason = 0
        self.pad= [0,0,0,0,0,0,0]
        self.desc = ofp_port()

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 7):
            return (False, "self.pad is not of size 7 as expected.")
        if(not isinstance(self.desc, ofp_port)):
            return (False, "self.desc is not class ofp_port as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!B", self.reason)
        packed += struct.pack("!BBBBBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5], self.pad[6])
        packed += self.desc.pack()
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 72):
            return binaryString
        fmt = '!B'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.reason,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBBBBB'
        start = 1
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5], self.pad[6]) = struct.unpack(fmt, binaryString[start:end])
        self.desc.unpack(binaryString[8:])
        return binaryString[72:]

    def __len__(self):
        """Return length of message
        """
        l = 72
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.reason !=  other.reason: return False
        if self.pad !=  other.pad: return False
        if self.desc !=  other.desc: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'reason: ' + str(self.reason) + '\n'
        outstr += prefix + 'desc: \n' 
        outstr += self.desc.show(prefix + '  ')
        return outstr


class ofp_meter_multipart_request(object):
    """Automatically generated Python class for ofp_meter_multipart_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.meter_id = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.meter_id)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.meter_id,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.meter_id !=  other.meter_id: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'meter_id: ' + str(self.meter_id) + '\n'
        return outstr


class ofp_multipart_reply(object):
    """Automatically generated Python class for ofp_multipart_reply

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.flags = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.flags)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.flags) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.flags !=  other.flags: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'flags: ' + str(self.flags) + '\n'
        return outstr


class ofp_action_header(object):
    """Automatically generated Python class for ofp_action_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.len)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        return outstr


class ofp_port_mod(object):
    """Automatically generated Python class for ofp_port_mod

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.port_no = 0
        self.pad= [0,0,0,0]
        self.hw_addr= [0,0,0,0,0,0]
        self.pad2= [0,0]
        self.config = 0
        self.mask = 0
        self.advertise = 0
        self.pad3= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        if(not isinstance(self.hw_addr, list)):
            return (False, "self.hw_addr is not list as expected.")
        if(len(self.hw_addr) != 6):
            return (False, "self.hw_addr is not of size 6 as expected.")
        if(not isinstance(self.pad2, list)):
            return (False, "self.pad2 is not list as expected.")
        if(len(self.pad2) != 2):
            return (False, "self.pad2 is not of size 2 as expected.")
        if(not isinstance(self.pad3, list)):
            return (False, "self.pad3 is not list as expected.")
        if(len(self.pad3) != 4):
            return (False, "self.pad3 is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.port_no)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        packed += struct.pack("!BBBBBB", self.hw_addr[0], self.hw_addr[1], self.hw_addr[2], self.hw_addr[3], self.hw_addr[4], self.hw_addr[5])
        packed += struct.pack("!BB", self.pad2[0], self.pad2[1])
        packed += struct.pack("!LLL", self.config, self.mask, self.advertise)
        packed += struct.pack("!BBBB", self.pad3[0], self.pad3[1], self.pad3[2], self.pad3[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 32):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.port_no,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBBBB'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.hw_addr[0], self.hw_addr[1], self.hw_addr[2], self.hw_addr[3], self.hw_addr[4], self.hw_addr[5]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BB'
        start = 14
        end = start + struct.calcsize(fmt)
        (self.pad2[0], self.pad2[1]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LLL'
        start = 16
        end = start + struct.calcsize(fmt)
        (self.config, self.mask, self.advertise) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 28
        end = start + struct.calcsize(fmt)
        (self.pad3[0], self.pad3[1], self.pad3[2], self.pad3[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[32:]

    def __len__(self):
        """Return length of message
        """
        l = 32
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.port_no !=  other.port_no: return False
        if self.pad !=  other.pad: return False
        if self.hw_addr !=  other.hw_addr: return False
        if self.pad2 !=  other.pad2: return False
        if self.config !=  other.config: return False
        if self.mask !=  other.mask: return False
        if self.advertise !=  other.advertise: return False
        if self.pad3 !=  other.pad3: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'port_no: ' + str(self.port_no) + '\n'
        outstr += prefix + 'hw_addr: ' + str(self.hw_addr) + '\n'
        outstr += prefix + 'config: ' + str(self.config) + '\n'
        outstr += prefix + 'mask: ' + str(self.mask) + '\n'
        outstr += prefix + 'advertise: ' + str(self.advertise) + '\n'
        return outstr


class ofp_action_output(object):
    """Automatically generated Python class for ofp_action_output

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.port = 0
        self.max_len = 0
        self.pad= [0,0,0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 6):
            return (False, "self.pad is not of size 6 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHLH", self.type, self.len, self.port, self.max_len)
        packed += struct.pack("!BBBBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!HHLH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.port, self.max_len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBBBB'
        start = 10
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.port !=  other.port: return False
        if self.max_len !=  other.max_len: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'port: ' + str(self.port) + '\n'
        outstr += prefix + 'max_len: ' + str(self.max_len) + '\n'
        return outstr


class ofp_switch_config(object):
    """Automatically generated Python class for ofp_switch_config

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.flags = 0
        self.miss_send_len = 128

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.flags, self.miss_send_len)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.flags, self.miss_send_len) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.flags !=  other.flags: return False
        if self.miss_send_len !=  other.miss_send_len: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'flags: ' + str(self.flags) + '\n'
        outstr += prefix + 'miss_send_len: ' + str(self.miss_send_len) + '\n'
        return outstr


class ofp_queue_prop_experimenter(object):
    """Automatically generated Python class for ofp_queue_prop_experimenter

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.prop_header = ofp_queue_prop_header()
        self.experimenter = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.prop_header, ofp_queue_prop_header)):
            return (False, "self.prop_header is not class ofp_queue_prop_header as expected.")
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += self.prop_header.pack()
        packed += struct.pack("!L", self.experimenter)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        self.prop_header.unpack(binaryString[0:])
        fmt = '!L'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.experimenter,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 12
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.prop_header !=  other.prop_header: return False
        if self.experimenter !=  other.experimenter: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'prop_header: \n' 
        outstr += self.prop_header.show(prefix + '  ')
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        return outstr


class ofp_instruction_write_metadata(object):
    """Automatically generated Python class for ofp_instruction_write_metadata

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.pad= [0,0,0,0]
        self.metadata = 0
        self.metadata_mask = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.len)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        packed += struct.pack("!QQ", self.metadata, self.metadata_mask)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 24):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!QQ'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.metadata, self.metadata_mask) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[24:]

    def __len__(self):
        """Return length of message
        """
        l = 24
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.pad !=  other.pad: return False
        if self.metadata !=  other.metadata: return False
        if self.metadata_mask !=  other.metadata_mask: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'metadata: ' + str(self.metadata) + '\n'
        outstr += prefix + 'metadata_mask: ' + str(self.metadata_mask) + '\n'
        return outstr


class ofp_meter_features(object):
    """Automatically generated Python class for ofp_meter_features

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.max_meter = 0
        self.band_types = 0
        self.capabilities = 0
        self.max_bands = 0
        self.max_color = 0
        self.pad= [0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 2):
            return (False, "self.pad is not of size 2 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LLLBB", self.max_meter, self.band_types, self.capabilities, self.max_bands, self.max_color)
        packed += struct.pack("!BB", self.pad[0], self.pad[1])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!LLLBB'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.max_meter, self.band_types, self.capabilities, self.max_bands, self.max_color) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BB'
        start = 14
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.max_meter !=  other.max_meter: return False
        if self.band_types !=  other.band_types: return False
        if self.capabilities !=  other.capabilities: return False
        if self.max_bands !=  other.max_bands: return False
        if self.max_color !=  other.max_color: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'max_meter: ' + str(self.max_meter) + '\n'
        outstr += prefix + 'band_types: ' + str(self.band_types) + '\n'
        outstr += prefix + 'capabilities: ' + str(self.capabilities) + '\n'
        outstr += prefix + 'max_bands: ' + str(self.max_bands) + '\n'
        outstr += prefix + 'max_color: ' + str(self.max_color) + '\n'
        return outstr


class ofp_table_feature_prop_instructions(object):
    """Automatically generated Python class for ofp_table_feature_prop_instructions

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.length = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.length)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        return outstr


class ofp_action_experimenter_header(object):
    """Automatically generated Python class for ofp_action_experimenter_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.experimenter = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHL", self.type, self.len, self.experimenter)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.experimenter) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.experimenter !=  other.experimenter: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        return outstr


class ofp_meter_band_drop(object):
    """Automatically generated Python class for ofp_meter_band_drop

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.rate = 0
        self.burst_size = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHLL", self.type, self.len, self.rate, self.burst_size)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!HHLL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.rate, self.burst_size) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 12
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.rate !=  other.rate: return False
        if self.burst_size !=  other.burst_size: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'rate: ' + str(self.rate) + '\n'
        outstr += prefix + 'burst_size: ' + str(self.burst_size) + '\n'
        return outstr


class ofp_table_feature_prop_actions(object):
    """Automatically generated Python class for ofp_table_feature_prop_actions

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.length = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.length)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        return outstr


class ofp_meter_band_experimenter(object):
    """Automatically generated Python class for ofp_meter_band_experimenter

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.rate = 0
        self.burst_size = 0
        self.experimenter = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHLLL", self.type, self.len, self.rate, self.burst_size, self.experimenter)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!HHLLL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.rate, self.burst_size, self.experimenter) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.rate !=  other.rate: return False
        if self.burst_size !=  other.burst_size: return False
        if self.experimenter !=  other.experimenter: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'rate: ' + str(self.rate) + '\n'
        outstr += prefix + 'burst_size: ' + str(self.burst_size) + '\n'
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        return outstr


class ofp_queue_get_config_reply(object):
    """Automatically generated Python class for ofp_queue_get_config_reply

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.port = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.port)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.port,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.port !=  other.port: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'port: ' + str(self.port) + '\n'
        return outstr


class ofp_desc(object):
    """Automatically generated Python class for ofp_desc

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.mfr_desc= ""
        self.hw_desc= ""
        self.sw_desc= ""
        self.serial_num= ""
        self.dp_desc= ""

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.mfr_desc, str)):
            return (False, "self.mfr_desc is not string as expected.")
        if(len(self.mfr_desc) > 256):
            return (False, "self.mfr_desc is not of size 256 as expected.")
        if(not isinstance(self.hw_desc, str)):
            return (False, "self.hw_desc is not string as expected.")
        if(len(self.hw_desc) > 256):
            return (False, "self.hw_desc is not of size 256 as expected.")
        if(not isinstance(self.sw_desc, str)):
            return (False, "self.sw_desc is not string as expected.")
        if(len(self.sw_desc) > 256):
            return (False, "self.sw_desc is not of size 256 as expected.")
        if(not isinstance(self.serial_num, str)):
            return (False, "self.serial_num is not string as expected.")
        if(len(self.serial_num) > 32):
            return (False, "self.serial_num is not of size 32 as expected.")
        if(not isinstance(self.dp_desc, str)):
            return (False, "self.dp_desc is not string as expected.")
        if(len(self.dp_desc) > 256):
            return (False, "self.dp_desc is not of size 256 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += self.mfr_desc.ljust(256,'\0')
        packed += self.hw_desc.ljust(256,'\0')
        packed += self.sw_desc.ljust(256,'\0')
        packed += self.serial_num.ljust(32,'\0')
        packed += self.dp_desc.ljust(256,'\0')
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 1056):
            return binaryString
        self.mfr_desc = binaryString[0:256].replace("\0","")
        self.hw_desc = binaryString[256:512].replace("\0","")
        self.sw_desc = binaryString[512:768].replace("\0","")
        self.serial_num = binaryString[768:800].replace("\0","")
        self.dp_desc = binaryString[800:1056].replace("\0","")
        return binaryString[1056:]

    def __len__(self):
        """Return length of message
        """
        l = 1056
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.mfr_desc !=  other.mfr_desc: return False
        if self.hw_desc !=  other.hw_desc: return False
        if self.sw_desc !=  other.sw_desc: return False
        if self.serial_num !=  other.serial_num: return False
        if self.dp_desc !=  other.dp_desc: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'mfr_desc: ' + str(self.mfr_desc) + '\n'
        outstr += prefix + 'hw_desc: ' + str(self.hw_desc) + '\n'
        outstr += prefix + 'sw_desc: ' + str(self.sw_desc) + '\n'
        outstr += prefix + 'serial_num: ' + str(self.serial_num) + '\n'
        outstr += prefix + 'dp_desc: ' + str(self.dp_desc) + '\n'
        return outstr


class ofp_meter_stats(object):
    """Automatically generated Python class for ofp_meter_stats

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.meter_id = 0
        self.len = 0
        self.pad= [0,0,0,0,0,0]
        self.flow_count = 0
        self.packet_in_count = 0
        self.byte_in_count = 0
        self.duration_sec = 0
        self.duration_nsec = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 6):
            return (False, "self.pad is not of size 6 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LH", self.meter_id, self.len)
        packed += struct.pack("!BBBBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5])
        packed += struct.pack("!LQQLL", self.flow_count, self.packet_in_count, self.byte_in_count, self.duration_sec, self.duration_nsec)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 40):
            return binaryString
        fmt = '!LH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.meter_id, self.len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBBBB'
        start = 6
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LQQLL'
        start = 12
        end = start + struct.calcsize(fmt)
        (self.flow_count, self.packet_in_count, self.byte_in_count, self.duration_sec, self.duration_nsec) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[40:]

    def __len__(self):
        """Return length of message
        """
        l = 40
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.meter_id !=  other.meter_id: return False
        if self.len !=  other.len: return False
        if self.pad !=  other.pad: return False
        if self.flow_count !=  other.flow_count: return False
        if self.packet_in_count !=  other.packet_in_count: return False
        if self.byte_in_count !=  other.byte_in_count: return False
        if self.duration_sec !=  other.duration_sec: return False
        if self.duration_nsec !=  other.duration_nsec: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'meter_id: ' + str(self.meter_id) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'flow_count: ' + str(self.flow_count) + '\n'
        outstr += prefix + 'packet_in_count: ' + str(self.packet_in_count) + '\n'
        outstr += prefix + 'byte_in_count: ' + str(self.byte_in_count) + '\n'
        outstr += prefix + 'duration_sec: ' + str(self.duration_sec) + '\n'
        outstr += prefix + 'duration_nsec: ' + str(self.duration_nsec) + '\n'
        return outstr


class ofp_oxm_experimenter_header(object):
    """Automatically generated Python class for ofp_oxm_experimenter_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.oxm_header = 0
        self.experimenter = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LL", self.oxm_header, self.experimenter)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!LL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.oxm_header, self.experimenter) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.oxm_header !=  other.oxm_header: return False
        if self.experimenter !=  other.experimenter: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'oxm_header: ' + str(self.oxm_header) + '\n'
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        return outstr


class ofp_action_set_queue(object):
    """Automatically generated Python class for ofp_action_set_queue

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.queue_id = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHL", self.type, self.len, self.queue_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.queue_id) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.queue_id !=  other.queue_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'queue_id: ' + str(self.queue_id) + '\n'
        return outstr


class ofp_action_set_field(object):
    """Automatically generated Python class for ofp_action_set_field

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.field= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.field, list)):
            return (False, "self.field is not list as expected.")
        if(len(self.field) != 4):
            return (False, "self.field is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.len)
        packed += struct.pack("!BBBB", self.field[0], self.field[1], self.field[2], self.field[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.field[0], self.field[1], self.field[2], self.field[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.field !=  other.field: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'field: ' + str(self.field) + '\n'
        return outstr


class ofp_flow_stats(object):
    """Automatically generated Python class for ofp_flow_stats

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.length = 0
        self.table_id = 0
        self.pad = 0
        self.duration_sec = 0
        self.duration_nsec = 0
        self.priority = 0x8000
        self.idle_timeout = 0
        self.hard_timeout = 0
        self.pad2= [0,0,0,0,0,0]
        self.cookie = 0
        self.packet_count = 0
        self.byte_count = 0
        self.match = ofp_match()
        self.match.length = OFP_MATCH_BYTES

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad2, list)):
            return (False, "self.pad2 is not list as expected.")
        if(len(self.pad2) != 6):
            return (False, "self.pad2 is not of size 6 as expected.")
        if(not isinstance(self.match, ofp_match)):
            return (False, "self.match is not class ofp_match as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HBBLLHHH", self.length, self.table_id, self.pad, self.duration_sec, self.duration_nsec, self.priority, self.idle_timeout, self.hard_timeout)
        packed += struct.pack("!BBBBBB", self.pad2[0], self.pad2[1], self.pad2[2], self.pad2[3], self.pad2[4], self.pad2[5])
        packed += struct.pack("!QQQ", self.cookie, self.packet_count, self.byte_count)
        packed += self.match.pack()
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 56):
            return binaryString
        fmt = '!HBBLLHHH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.length, self.table_id, self.pad, self.duration_sec, self.duration_nsec, self.priority, self.idle_timeout, self.hard_timeout) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBBBB'
        start = 18
        end = start + struct.calcsize(fmt)
        (self.pad2[0], self.pad2[1], self.pad2[2], self.pad2[3], self.pad2[4], self.pad2[5]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!QQQ'
        start = 24
        end = start + struct.calcsize(fmt)
        (self.cookie, self.packet_count, self.byte_count) = struct.unpack(fmt,  binaryString[start:end])
        self.match.unpack(binaryString[48:])
        return binaryString[56:]

    def __len__(self):
        """Return length of message
        """
        l = 56
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.length !=  other.length: return False
        if self.table_id !=  other.table_id: return False
        if self.pad !=  other.pad: return False
        if self.duration_sec !=  other.duration_sec: return False
        if self.duration_nsec !=  other.duration_nsec: return False
        if self.priority !=  other.priority: return False
        if self.idle_timeout !=  other.idle_timeout: return False
        if self.hard_timeout !=  other.hard_timeout: return False
        if self.pad2 !=  other.pad2: return False
        if self.cookie !=  other.cookie: return False
        if self.packet_count !=  other.packet_count: return False
        if self.byte_count !=  other.byte_count: return False
        if self.match !=  other.match: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'duration_sec: ' + str(self.duration_sec) + '\n'
        outstr += prefix + 'duration_nsec: ' + str(self.duration_nsec) + '\n'
        outstr += prefix + 'priority: ' + str(self.priority) + '\n'
        outstr += prefix + 'idle_timeout: ' + str(self.idle_timeout) + '\n'
        outstr += prefix + 'hard_timeout: ' + str(self.hard_timeout) + '\n'
        outstr += prefix + 'cookie: ' + str(self.cookie) + '\n'
        outstr += prefix + 'packet_count: ' + str(self.packet_count) + '\n'
        outstr += prefix + 'byte_count: ' + str(self.byte_count) + '\n'
        outstr += prefix + 'match: \n' 
        outstr += self.match.show(prefix + '  ')
        return outstr


class ofp_meter_band_stats(object):
    """Automatically generated Python class for ofp_meter_band_stats

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.packet_band_count = 0
        self.byte_band_count = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!QQ", self.packet_band_count, self.byte_band_count)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!QQ'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.packet_band_count, self.byte_band_count) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.packet_band_count !=  other.packet_band_count: return False
        if self.byte_band_count !=  other.byte_band_count: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'packet_band_count: ' + str(self.packet_band_count) + '\n'
        outstr += prefix + 'byte_band_count: ' + str(self.byte_band_count) + '\n'
        return outstr


class ofp_flow_removed(object):
    """Automatically generated Python class for ofp_flow_removed

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.cookie = 0
        self.priority = 0
        self.reason = 0
        self.table_id = 0
        self.duration_sec = 0
        self.duration_nsec = 0
        self.idle_timeout = 0
        self.hard_timeout = 0
        self.packet_count = 0
        self.byte_count = 0
        self.match = ofp_match()
        self.match.length = OFP_MATCH_BYTES

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.match, ofp_match)):
            return (False, "self.match is not class ofp_match as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!QHBBLLHHQQ", self.cookie, self.priority, self.reason, self.table_id, self.duration_sec, self.duration_nsec, self.idle_timeout, self.hard_timeout, self.packet_count, self.byte_count)
        packed += self.match.pack()
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 48):
            return binaryString
        fmt = '!QHBBLLHHQQ'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.cookie, self.priority, self.reason, self.table_id, self.duration_sec, self.duration_nsec, self.idle_timeout, self.hard_timeout, self.packet_count, self.byte_count) = struct.unpack(fmt,  binaryString[start:end])
        self.match.unpack(binaryString[40:])
        return binaryString[48:]

    def __len__(self):
        """Return length of message
        """
        l = 48
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.cookie !=  other.cookie: return False
        if self.priority !=  other.priority: return False
        if self.reason !=  other.reason: return False
        if self.table_id !=  other.table_id: return False
        if self.duration_sec !=  other.duration_sec: return False
        if self.duration_nsec !=  other.duration_nsec: return False
        if self.idle_timeout !=  other.idle_timeout: return False
        if self.hard_timeout !=  other.hard_timeout: return False
        if self.packet_count !=  other.packet_count: return False
        if self.byte_count !=  other.byte_count: return False
        if self.match !=  other.match: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'cookie: ' + str(self.cookie) + '\n'
        outstr += prefix + 'priority: ' + str(self.priority) + '\n'
        outstr += prefix + 'reason: ' + str(self.reason) + '\n'
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'duration_sec: ' + str(self.duration_sec) + '\n'
        outstr += prefix + 'duration_nsec: ' + str(self.duration_nsec) + '\n'
        outstr += prefix + 'idle_timeout: ' + str(self.idle_timeout) + '\n'
        outstr += prefix + 'hard_timeout: ' + str(self.hard_timeout) + '\n'
        outstr += prefix + 'packet_count: ' + str(self.packet_count) + '\n'
        outstr += prefix + 'byte_count: ' + str(self.byte_count) + '\n'
        outstr += prefix + 'match: \n' 
        outstr += self.match.show(prefix + '  ')
        return outstr


class ofp_queue_prop_min_rate(object):
    """Automatically generated Python class for ofp_queue_prop_min_rate

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.prop_header = ofp_queue_prop_header()
        self.rate = 0
        self.pad= [0,0,0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.prop_header, ofp_queue_prop_header)):
            return (False, "self.prop_header is not class ofp_queue_prop_header as expected.")
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 6):
            return (False, "self.pad is not of size 6 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += self.prop_header.pack()
        packed += struct.pack("!H", self.rate)
        packed += struct.pack("!BBBBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        self.prop_header.unpack(binaryString[0:])
        fmt = '!H'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.rate,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBBBB'
        start = 10
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.prop_header !=  other.prop_header: return False
        if self.rate !=  other.rate: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'prop_header: \n' 
        outstr += self.prop_header.show(prefix + '  ')
        outstr += prefix + 'rate: ' + str(self.rate) + '\n'
        return outstr


class ofp_header(object):
    """Automatically generated Python class for ofp_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.version = 0x04
        self.type = 0
        self.length = 0
        self.xid = 0

    def __assert(self):
        """Sanity check
        """
        if (not (self.type in ofp_type_map.keys())):
            return (False, "type must have values from ofp_type_map.keys()")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!BBHL", self.version, self.type, self.length, self.xid)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!BBHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.version, self.type, self.length, self.xid) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.version !=  other.version: return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        if self.xid !=  other.xid: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'version: ' + str(self.version) + '\n'
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        outstr += prefix + 'xid: ' + str(self.xid) + '\n'
        return outstr


class ofp_multipart_request(object):
    """Automatically generated Python class for ofp_multipart_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.flags = 0
        self.__pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.__pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.__pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.flags)
        packed += struct.pack("!BBBB", self.__pad[0], self.__pad[1], self.__pad[2], self.__pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.flags) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.__pad[0], self.__pad[1], self.__pad[2], self.__pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.flags !=  other.flags: return False
        if self.__pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'flags: ' + str(self.flags) + '\n'
        return outstr


class ofp_queue_stats_request(object):
    """Automatically generated Python class for ofp_queue_stats_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.port_no = 0
        self.queue_id = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LL", self.port_no, self.queue_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!LL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.port_no, self.queue_id) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.port_no !=  other.port_no: return False
        if self.queue_id !=  other.queue_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'port_no: ' + str(self.port_no) + '\n'
        outstr += prefix + 'queue_id: ' + str(self.queue_id) + '\n'
        return outstr


class ofp_error_experimenter_msg(object):
    """Automatically generated Python class for ofp_error_experimenter_msg

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.exp_type = 0
        self.experimenter = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHL", self.type, self.exp_type, self.experimenter)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.exp_type, self.experimenter) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.exp_type !=  other.exp_type: return False
        if self.experimenter !=  other.experimenter: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'exp_type: ' + str(self.exp_type) + '\n'
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        return outstr


class ofp_group_mod(object):
    """Automatically generated Python class for ofp_group_mod

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.command = 0
        self.type = 0
        self.pad = 0
        self.group_id = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HBBL", self.command, self.type, self.pad, self.group_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HBBL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.command, self.type, self.pad, self.group_id) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.command !=  other.command: return False
        if self.type !=  other.type: return False
        if self.pad !=  other.pad: return False
        if self.group_id !=  other.group_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'command: ' + str(self.command) + '\n'
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'group_id: ' + str(self.group_id) + '\n'
        return outstr


class ofp_port_stats(object):
    """Automatically generated Python class for ofp_port_stats

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.port_no = 0
        self.pad= [0,0,0,0]
        self.rx_packets = 0
        self.tx_packets = 0
        self.rx_bytes = 0
        self.tx_bytes = 0
        self.rx_dropped = 0
        self.tx_dropped = 0
        self.rx_errors = 0
        self.tx_errors = 0
        self.rx_frame_err = 0
        self.rx_over_err = 0
        self.rx_crc_err = 0
        self.collisions = 0
        self.duration_sec = 0
        self.duration_nsec = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.port_no)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        packed += struct.pack("!QQQQQQQQQQQQLL", self.rx_packets, self.tx_packets, self.rx_bytes, self.tx_bytes, self.rx_dropped, self.tx_dropped, self.rx_errors, self.tx_errors, self.rx_frame_err, self.rx_over_err, self.rx_crc_err, self.collisions, self.duration_sec, self.duration_nsec)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 112):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.port_no,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!QQQQQQQQQQQQLL'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.rx_packets, self.tx_packets, self.rx_bytes, self.tx_bytes, self.rx_dropped, self.tx_dropped, self.rx_errors, self.tx_errors, self.rx_frame_err, self.rx_over_err, self.rx_crc_err, self.collisions, self.duration_sec, self.duration_nsec) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[112:]

    def __len__(self):
        """Return length of message
        """
        l = 112
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.port_no !=  other.port_no: return False
        if self.pad !=  other.pad: return False
        if self.rx_packets !=  other.rx_packets: return False
        if self.tx_packets !=  other.tx_packets: return False
        if self.rx_bytes !=  other.rx_bytes: return False
        if self.tx_bytes !=  other.tx_bytes: return False
        if self.rx_dropped !=  other.rx_dropped: return False
        if self.tx_dropped !=  other.tx_dropped: return False
        if self.rx_errors !=  other.rx_errors: return False
        if self.tx_errors !=  other.tx_errors: return False
        if self.rx_frame_err !=  other.rx_frame_err: return False
        if self.rx_over_err !=  other.rx_over_err: return False
        if self.rx_crc_err !=  other.rx_crc_err: return False
        if self.collisions !=  other.collisions: return False
        if self.duration_sec !=  other.duration_sec: return False
        if self.duration_nsec !=  other.duration_nsec: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'port_no: ' + str(self.port_no) + '\n'
        outstr += prefix + 'rx_packets: ' + str(self.rx_packets) + '\n'
        outstr += prefix + 'tx_packets: ' + str(self.tx_packets) + '\n'
        outstr += prefix + 'rx_bytes: ' + str(self.rx_bytes) + '\n'
        outstr += prefix + 'tx_bytes: ' + str(self.tx_bytes) + '\n'
        outstr += prefix + 'rx_dropped: ' + str(self.rx_dropped) + '\n'
        outstr += prefix + 'tx_dropped: ' + str(self.tx_dropped) + '\n'
        outstr += prefix + 'rx_errors: ' + str(self.rx_errors) + '\n'
        outstr += prefix + 'tx_errors: ' + str(self.tx_errors) + '\n'
        outstr += prefix + 'rx_frame_err: ' + str(self.rx_frame_err) + '\n'
        outstr += prefix + 'rx_over_err: ' + str(self.rx_over_err) + '\n'
        outstr += prefix + 'rx_crc_err: ' + str(self.rx_crc_err) + '\n'
        outstr += prefix + 'collisions: ' + str(self.collisions) + '\n'
        outstr += prefix + 'duration_sec: ' + str(self.duration_sec) + '\n'
        outstr += prefix + 'duration_nsec: ' + str(self.duration_nsec) + '\n'
        return outstr


class ofp_packet_queue(object):
    """Automatically generated Python class for ofp_packet_queue

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.queue_id = 0
        self.port = 0
        self.len = 0
        self.pad= [0,0,0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 6):
            return (False, "self.pad is not of size 6 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LLH", self.queue_id, self.port, self.len)
        packed += struct.pack("!BBBBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!LLH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.queue_id, self.port, self.len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBBBB'
        start = 10
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.queue_id !=  other.queue_id: return False
        if self.port !=  other.port: return False
        if self.len !=  other.len: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'queue_id: ' + str(self.queue_id) + '\n'
        outstr += prefix + 'port: ' + str(self.port) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        return outstr


class ofp_port(object):
    """Automatically generated Python class for ofp_port

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.port_no = 0
        self.pad= [0,0,0,0]
        self.hw_addr= [0,0,0,0,0,0]
        self.pad2= [0,0]
        self.name= ""
        self.config = 0
        self.state = 0
        self.curr = 0
        self.advertised = 0
        self.supported = 0
        self.peer = 0
        self.curr_speed = 0
        self.max_speed = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        if(not isinstance(self.hw_addr, list)):
            return (False, "self.hw_addr is not list as expected.")
        if(len(self.hw_addr) != 6):
            return (False, "self.hw_addr is not of size 6 as expected.")
        if(not isinstance(self.pad2, list)):
            return (False, "self.pad2 is not list as expected.")
        if(len(self.pad2) != 2):
            return (False, "self.pad2 is not of size 2 as expected.")
        if(not isinstance(self.name, str)):
            return (False, "self.name is not string as expected.")
        if(len(self.name) > 16):
            return (False, "self.name is not of size 16 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.port_no)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        packed += struct.pack("!BBBBBB", self.hw_addr[0], self.hw_addr[1], self.hw_addr[2], self.hw_addr[3], self.hw_addr[4], self.hw_addr[5])
        packed += struct.pack("!BB", self.pad2[0], self.pad2[1])
        packed += self.name.ljust(16,'\0')
        packed += struct.pack("!LLLLLLLL", self.config, self.state, self.curr, self.advertised, self.supported, self.peer, self.curr_speed, self.max_speed)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 64):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.port_no,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBBBB'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.hw_addr[0], self.hw_addr[1], self.hw_addr[2], self.hw_addr[3], self.hw_addr[4], self.hw_addr[5]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BB'
        start = 14
        end = start + struct.calcsize(fmt)
        (self.pad2[0], self.pad2[1]) = struct.unpack(fmt, binaryString[start:end])
        self.name = binaryString[16:32].replace("\0","")
        fmt = '!LLLLLLLL'
        start = 32
        end = start + struct.calcsize(fmt)
        (self.config, self.state, self.curr, self.advertised, self.supported, self.peer, self.curr_speed, self.max_speed) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[64:]

    def __len__(self):
        """Return length of message
        """
        l = 64
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.port_no !=  other.port_no: return False
        if self.pad !=  other.pad: return False
        if self.hw_addr !=  other.hw_addr: return False
        if self.pad2 !=  other.pad2: return False
        if self.name !=  other.name: return False
        if self.config !=  other.config: return False
        if self.state !=  other.state: return False
        if self.curr !=  other.curr: return False
        if self.advertised !=  other.advertised: return False
        if self.supported !=  other.supported: return False
        if self.peer !=  other.peer: return False
        if self.curr_speed !=  other.curr_speed: return False
        if self.max_speed !=  other.max_speed: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'port_no: ' + str(self.port_no) + '\n'
        outstr += prefix + 'hw_addr: ' + str(self.hw_addr) + '\n'
        outstr += prefix + 'name: ' + str(self.name) + '\n'
        outstr += prefix + 'config: ' + str(self.config) + '\n'
        outstr += prefix + 'state: ' + str(self.state) + '\n'
        outstr += prefix + 'curr: ' + str(self.curr) + '\n'
        outstr += prefix + 'advertised: ' + str(self.advertised) + '\n'
        outstr += prefix + 'supported: ' + str(self.supported) + '\n'
        outstr += prefix + 'peer: ' + str(self.peer) + '\n'
        outstr += prefix + 'curr_speed: ' + str(self.curr_speed) + '\n'
        outstr += prefix + 'max_speed: ' + str(self.max_speed) + '\n'
        return outstr


class ofp_group_desc_stats(object):
    """Automatically generated Python class for ofp_group_desc_stats

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.length = 0
        self.type = 0
        self.pad = 0
        self.group_id = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HBBL", self.length, self.type, self.pad, self.group_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HBBL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.length, self.type, self.pad, self.group_id) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.length !=  other.length: return False
        if self.type !=  other.type: return False
        if self.pad !=  other.pad: return False
        if self.group_id !=  other.group_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'group_id: ' + str(self.group_id) + '\n'
        return outstr


class ofp_switch_features(object):
    """Automatically generated Python class for ofp_switch_features

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.datapath_id = 0
        self.n_buffers = 0
        self.n_tables = 0
        self.auxiliary_id = 0
        self.pad= [0,0]
        self.capabilities = 0
        self.reserved = 0

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 2):
            return (False, "self.pad is not of size 2 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!QLBB", self.datapath_id, self.n_buffers, self.n_tables, self.auxiliary_id)
        packed += struct.pack("!BB", self.pad[0], self.pad[1])
        packed += struct.pack("!LL", self.capabilities, self.reserved)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 24):
            return binaryString
        fmt = '!QLBB'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.datapath_id, self.n_buffers, self.n_tables, self.auxiliary_id) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BB'
        start = 14
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LL'
        start = 16
        end = start + struct.calcsize(fmt)
        (self.capabilities, self.reserved) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[24:]

    def __len__(self):
        """Return length of message
        """
        l = 24
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.datapath_id !=  other.datapath_id: return False
        if self.n_buffers !=  other.n_buffers: return False
        if self.n_tables !=  other.n_tables: return False
        if self.auxiliary_id !=  other.auxiliary_id: return False
        if self.pad !=  other.pad: return False
        if self.capabilities !=  other.capabilities: return False
        if self.reserved !=  other.reserved: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'datapath_id: ' + str(self.datapath_id) + '\n'
        outstr += prefix + 'n_buffers: ' + str(self.n_buffers) + '\n'
        outstr += prefix + 'n_tables: ' + str(self.n_tables) + '\n'
        outstr += prefix + 'auxiliary_id: ' + str(self.auxiliary_id) + '\n'
        outstr += prefix + 'capabilities: ' + str(self.capabilities) + '\n'
        outstr += prefix + 'reserved: ' + str(self.reserved) + '\n'
        return outstr


class ofp_queue_prop_header(object):
    """Automatically generated Python class for ofp_queue_prop_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.property = 0
        self.len = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.property, self.len)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.property, self.len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.property !=  other.property: return False
        if self.len !=  other.len: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'property: ' + str(self.property) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        return outstr


class ofp_flow_stats_request(object):
    """Automatically generated Python class for ofp_flow_stats_request

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.table_id = 0
        self.pad= [0,0,0]
        self.out_port = 0
        self.out_group = 0
        self.pad2= [0,0,0,0]
        self.cookie = 0
        self.cookie_mask = 0
        self.match = ofp_match()
        self.match.length = OFP_MATCH_BYTES

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 3):
            return (False, "self.pad is not of size 3 as expected.")
        if(not isinstance(self.pad2, list)):
            return (False, "self.pad2 is not list as expected.")
        if(len(self.pad2) != 4):
            return (False, "self.pad2 is not of size 4 as expected.")
        if(not isinstance(self.match, ofp_match)):
            return (False, "self.match is not class ofp_match as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!B", self.table_id)
        packed += struct.pack("!BBB", self.pad[0], self.pad[1], self.pad[2])
        packed += struct.pack("!LL", self.out_port, self.out_group)
        packed += struct.pack("!BBBB", self.pad2[0], self.pad2[1], self.pad2[2], self.pad2[3])
        packed += struct.pack("!QQ", self.cookie, self.cookie_mask)
        packed += self.match.pack()
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 40):
            return binaryString
        fmt = '!B'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.table_id,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBB'
        start = 1
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LL'
        start = 4
        end = start + struct.calcsize(fmt)
        (self.out_port, self.out_group) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 12
        end = start + struct.calcsize(fmt)
        (self.pad2[0], self.pad2[1], self.pad2[2], self.pad2[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!QQ'
        start = 16
        end = start + struct.calcsize(fmt)
        (self.cookie, self.cookie_mask) = struct.unpack(fmt,  binaryString[start:end])
        self.match.unpack(binaryString[32:])
        return binaryString[40:]

    def __len__(self):
        """Return length of message
        """
        l = 40
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.table_id !=  other.table_id: return False
        if self.pad !=  other.pad: return False
        if self.out_port !=  other.out_port: return False
        if self.out_group !=  other.out_group: return False
        if self.pad2 !=  other.pad2: return False
        if self.cookie !=  other.cookie: return False
        if self.cookie_mask !=  other.cookie_mask: return False
        if self.match !=  other.match: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'out_port: ' + str(self.out_port) + '\n'
        outstr += prefix + 'out_group: ' + str(self.out_group) + '\n'
        outstr += prefix + 'cookie: ' + str(self.cookie) + '\n'
        outstr += prefix + 'cookie_mask: ' + str(self.cookie_mask) + '\n'
        outstr += prefix + 'match: \n' 
        outstr += self.match.show(prefix + '  ')
        return outstr


class ofp_meter_mod(object):
    """Automatically generated Python class for ofp_meter_mod

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.command = 0
        self.flags = 0
        self.meter_id = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHL", self.command, self.flags, self.meter_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.command, self.flags, self.meter_id) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.command !=  other.command: return False
        if self.flags !=  other.flags: return False
        if self.meter_id !=  other.meter_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'command: ' + str(self.command) + '\n'
        outstr += prefix + 'flags: ' + str(self.flags) + '\n'
        outstr += prefix + 'meter_id: ' + str(self.meter_id) + '\n'
        return outstr


class ofp_bucket(object):
    """Automatically generated Python class for ofp_bucket

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.len = 0
        self.weight = 0
        self.watch_port = 0
        self.watch_group = 0
        self.pad= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 4):
            return (False, "self.pad is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHLL", self.len, self.weight, self.watch_port, self.watch_group)
        packed += struct.pack("!BBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!HHLL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.len, self.weight, self.watch_port, self.watch_group) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBB'
        start = 12
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.len !=  other.len: return False
        if self.weight !=  other.weight: return False
        if self.watch_port !=  other.watch_port: return False
        if self.watch_group !=  other.watch_group: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'weight: ' + str(self.weight) + '\n'
        outstr += prefix + 'watch_port: ' + str(self.watch_port) + '\n'
        outstr += prefix + 'watch_group: ' + str(self.watch_group) + '\n'
        return outstr


class ofp_action_pop_mpls(object):
    """Automatically generated Python class for ofp_action_pop_mpls

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.ethertype = 0
        self.pad= [0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 2):
            return (False, "self.pad is not of size 2 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHH", self.type, self.len, self.ethertype)
        packed += struct.pack("!BB", self.pad[0], self.pad[1])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.ethertype) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BB'
        start = 6
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.ethertype !=  other.ethertype: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'ethertype: ' + str(self.ethertype) + '\n'
        return outstr

class ofp_match(object):
    """Automatically generated Python class for ofp_match

    Date 2012-11-23
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = OFPMT_OXM
        self.length = 0

    def __assert(self):
        """Sanity check
        """
#        if(not isinstance(self.oxm_fields, list)):
#            return (False, "self.oxm_fields is not list as expected.")
#        if(len(self.oxm_fields) != 4):
#            return (False, "self.oxm_fields is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.length)
        return packed
#        if(assertstruct):
#            if(not self.__assert()[0]):
#                return None
#        packed = ""
#        packed += struct.pack("!HH", self.type, self.length)
#        packed += struct.pack("!BBBB", self.oxm_fields[0], self.oxm_fields[1], self.oxm_fields[2], self.oxm_fields[3])
#        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]
#        if (len(binaryString) < 8):
#            return binaryString
#        fmt = '!HH'
#        start = 0
#        end = start + struct.calcsize(fmt)
#        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
#        fmt = '!BBBB'
#        start = 4
#        end = start + struct.calcsize(fmt)
#        (self.oxm_fields[0], self.oxm_fields[1], self.oxm_fields[2], self.oxm_fields[3]) = struct.unpack(fmt, binaryString[start:end])
#        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
#        if self.oxm_fields !=  other.oxm_fields: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
#        outstr += prefix + 'oxm_fields: ' + str(self.oxm_fields) + '\n'
        return outstr

class ofp_flow_mod(object):
    """Automatically generated Python class for ofp_flow_mod

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.cookie = 0
        self.cookie_mask = 0
        self.table_id = 0
        self.command = 0
        self.idle_timeout = 0
        self.hard_timeout = 0
        self.priority = 0x8000
        self.buffer_id = 0
        self.out_port = 0
        self.out_group = 0
        self.flags = 0
        self.pad= [0,0]
        self.match = ofp_match()
        self.match.length = OFP_MATCH_BYTES

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 2):
            return (False, "self.pad is not of size 2 as expected.")
        if(not isinstance(self.match, ofp_match)):
            return (False, "self.match is not class ofp_match as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!QQBBHHHLLLH", self.cookie, self.cookie_mask, self.table_id, self.command, self.idle_timeout, self.hard_timeout, self.priority, self.buffer_id, self.out_port, self.out_group, self.flags)
        packed += struct.pack("!BB", self.pad[0], self.pad[1])
        packed += self.match.pack()
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 48):
            return binaryString
        fmt = '!QQBBHHHLLLH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.cookie, self.cookie_mask, self.table_id, self.command, self.idle_timeout, self.hard_timeout, self.priority, self.buffer_id, self.out_port, self.out_group, self.flags) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BB'
        start = 38
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1]) = struct.unpack(fmt, binaryString[start:end])
        self.match.unpack(binaryString[40:])
        return binaryString[48:]

    def __len__(self):
        """Return length of message
        """
        l = OFP_FLOW_MOD_BYTES
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.cookie !=  other.cookie: return False
        if self.cookie_mask !=  other.cookie_mask: return False
        if self.table_id !=  other.table_id: return False
        if self.command !=  other.command: return False
        if self.idle_timeout !=  other.idle_timeout: return False
        if self.hard_timeout !=  other.hard_timeout: return False
        if self.priority !=  other.priority: return False
        if self.buffer_id !=  other.buffer_id: return False
        if self.out_port !=  other.out_port: return False
        if self.out_group !=  other.out_group: return False
        if self.flags !=  other.flags: return False
        if self.pad !=  other.pad: return False
        if self.match !=  other.match: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'cookie: ' + str(self.cookie) + '\n'
        outstr += prefix + 'cookie_mask: ' + str(self.cookie_mask) + '\n'
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        outstr += prefix + 'command: ' + str(self.command) + '\n'
        outstr += prefix + 'idle_timeout: ' + str(self.idle_timeout) + '\n'
        outstr += prefix + 'hard_timeout: ' + str(self.hard_timeout) + '\n'
        outstr += prefix + 'priority: ' + str(self.priority) + '\n'
        outstr += prefix + 'buffer_id: ' + str(self.buffer_id) + '\n'
        outstr += prefix + 'out_port: ' + str(self.out_port) + '\n'
        outstr += prefix + 'out_group: ' + str(self.out_group) + '\n'
        outstr += prefix + 'flags: ' + str(self.flags) + '\n'
        outstr += prefix + 'match: \n' 
        outstr += self.match.show(prefix + '  ')
        return outstr


class ofp_vendor_header(object):
    """Automatically generated Python class for ofp_vendor_header

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.vendor = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!L", self.vendor)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!L'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.vendor,) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.vendor !=  other.vendor: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'vendor: ' + str(self.vendor) + '\n'
        return outstr


class ofp_group_features(object):
    """Automatically generated Python class for ofp_group_features

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.types = 0
        self.capabilities = 0
        self.max_groups= [0,0,0,0]
        self.actions= [0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.max_groups, list)):
            return (False, "self.max_groups is not list as expected.")
        if(len(self.max_groups) != 4):
            return (False, "self.max_groups is not of size 4 as expected.")
        if(not isinstance(self.actions, list)):
            return (False, "self.actions is not list as expected.")
        if(len(self.actions) != 4):
            return (False, "self.actions is not of size 4 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LL", self.types, self.capabilities)
        packed += struct.pack("!LLLL", self.max_groups[0], self.max_groups[1], self.max_groups[2], self.max_groups[3])
        packed += struct.pack("!LLLL", self.actions[0], self.actions[1], self.actions[2], self.actions[3])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 40):
            return binaryString
        fmt = '!LL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.types, self.capabilities) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!LLLL'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.max_groups[0], self.max_groups[1], self.max_groups[2], self.max_groups[3]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LLLL'
        start = 24
        end = start + struct.calcsize(fmt)
        (self.actions[0], self.actions[1], self.actions[2], self.actions[3]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[40:]

    def __len__(self):
        """Return length of message
        """
        l = 40
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.types !=  other.types: return False
        if self.capabilities !=  other.capabilities: return False
        if self.max_groups !=  other.max_groups: return False
        if self.actions !=  other.actions: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'types: ' + str(self.types) + '\n'
        outstr += prefix + 'capabilities: ' + str(self.capabilities) + '\n'
        outstr += prefix + 'max_groups: ' + str(self.max_groups) + '\n'
        outstr += prefix + 'actions: ' + str(self.actions) + '\n'
        return outstr


class ofp_meter_band_dscp_remark(object):
    """Automatically generated Python class for ofp_meter_band_dscp_remark

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.rate = 0
        self.burst_size = 0
        self.prec_level = 0
        self.pad= [0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 3):
            return (False, "self.pad is not of size 3 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHLLB", self.type, self.len, self.rate, self.burst_size, self.prec_level)
        packed += struct.pack("!BBB", self.pad[0], self.pad[1], self.pad[2])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!HHLLB'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.rate, self.burst_size, self.prec_level) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBB'
        start = 13
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.rate !=  other.rate: return False
        if self.burst_size !=  other.burst_size: return False
        if self.prec_level !=  other.prec_level: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'rate: ' + str(self.rate) + '\n'
        outstr += prefix + 'burst_size: ' + str(self.burst_size) + '\n'
        outstr += prefix + 'prec_level: ' + str(self.prec_level) + '\n'
        return outstr


class ofp_hello_elem_versionbitmap(object):
    """Automatically generated Python class for ofp_hello_elem_versionbitmap

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.length = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HH", self.type, self.length)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 4):
            return binaryString
        fmt = '!HH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[4:]

    def __len__(self):
        """Return length of message
        """
        l = 4
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        return outstr


class ofp_packet_out(object):
    """Automatically generated Python class for ofp_packet_out

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.buffer_id = 4294967295
        self.in_port = 0
        self.actions_len = 0
        self.pad= [0,0,0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 6):
            return (False, "self.pad is not of size 6 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LLH", self.buffer_id, self.in_port, self.actions_len)
        packed += struct.pack("!BBBBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        fmt = '!LLH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.buffer_id, self.in_port, self.actions_len) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBBBBB'
        start = 10
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.buffer_id !=  other.buffer_id: return False
        if self.in_port !=  other.in_port: return False
        if self.actions_len !=  other.actions_len: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'buffer_id: ' + str(self.buffer_id) + '\n'
        outstr += prefix + 'in_port: ' + str(self.in_port) + '\n'
        outstr += prefix + 'actions_len: ' + str(self.actions_len) + '\n'
        return outstr


class ofp_instruction_goto_table(object):
    """Automatically generated Python class for ofp_instruction_goto_table

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.table_id = 0
        self.pad= [0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 3):
            return (False, "self.pad is not of size 3 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHB", self.type, self.len, self.table_id)
        packed += struct.pack("!BBB", self.pad[0], self.pad[1], self.pad[2])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHB'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.table_id) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBB'
        start = 5
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.table_id !=  other.table_id: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'table_id: ' + str(self.table_id) + '\n'
        return outstr


class ofp_queue_prop_max_rate(object):
    """Automatically generated Python class for ofp_queue_prop_max_rate

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.prop_header = ofp_queue_prop_header()
        self.rate = 0
        self.pad= [0,0,0,0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.prop_header, ofp_queue_prop_header)):
            return (False, "self.prop_header is not class ofp_queue_prop_header as expected.")
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 6):
            return (False, "self.pad is not of size 6 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += self.prop_header.pack()
        packed += struct.pack("!H", self.rate)
        packed += struct.pack("!BBBBBB", self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 16):
            return binaryString
        self.prop_header.unpack(binaryString[0:])
        fmt = '!H'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.rate,) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!BBBBBB'
        start = 10
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2], self.pad[3], self.pad[4], self.pad[5]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[16:]

    def __len__(self):
        """Return length of message
        """
        l = 16
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.prop_header !=  other.prop_header: return False
        if self.rate !=  other.rate: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'prop_header: \n' 
        outstr += self.prop_header.show(prefix + '  ')
        outstr += prefix + 'rate: ' + str(self.rate) + '\n'
        return outstr


class ofp_table_feature_prop_experimenter(object):
    """Automatically generated Python class for ofp_table_feature_prop_experimenter

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.length = 0
        self.experimenter = 0
        self.exp_type = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHLL", self.type, self.length, self.experimenter, self.exp_type)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 12):
            return binaryString
        fmt = '!HHLL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.length, self.experimenter, self.exp_type) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[12:]

    def __len__(self):
        """Return length of message
        """
        l = 12
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.length !=  other.length: return False
        if self.experimenter !=  other.experimenter: return False
        if self.exp_type !=  other.exp_type: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'length: ' + str(self.length) + '\n'
        outstr += prefix + 'experimenter: ' + str(self.experimenter) + '\n'
        outstr += prefix + 'exp_type: ' + str(self.exp_type) + '\n'
        return outstr


class ofp_action_group(object):
    """Automatically generated Python class for ofp_action_group

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.group_id = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHL", self.type, self.len, self.group_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.group_id) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.group_id !=  other.group_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'group_id: ' + str(self.group_id) + '\n'
        return outstr


class ofp_action_push(object):
    """Automatically generated Python class for ofp_action_push

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.ethertype = 0
        self.pad= [0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 2):
            return (False, "self.pad is not of size 2 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHH", self.type, self.len, self.ethertype)
        packed += struct.pack("!BB", self.pad[0], self.pad[1])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHH'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.ethertype) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BB'
        start = 6
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.ethertype !=  other.ethertype: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'ethertype: ' + str(self.ethertype) + '\n'
        return outstr


class ofp_instruction_meter(object):
    """Automatically generated Python class for ofp_instruction_meter

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.meter_id = 0

    def __assert(self):
        """Sanity check
        """
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHL", self.type, self.len, self.meter_id)
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.meter_id) = struct.unpack(fmt,  binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.meter_id !=  other.meter_id: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'meter_id: ' + str(self.meter_id) + '\n'
        return outstr


class ofp_async_config(object):
    """Automatically generated Python class for ofp_async_config

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.packet_in_mask= [0,0]
        self.port_status_mask= [0,0]
        self.flow_removed_mask= [0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.packet_in_mask, list)):
            return (False, "self.packet_in_mask is not list as expected.")
        if(len(self.packet_in_mask) != 2):
            return (False, "self.packet_in_mask is not of size 2 as expected.")
        if(not isinstance(self.port_status_mask, list)):
            return (False, "self.port_status_mask is not list as expected.")
        if(len(self.port_status_mask) != 2):
            return (False, "self.port_status_mask is not of size 2 as expected.")
        if(not isinstance(self.flow_removed_mask, list)):
            return (False, "self.flow_removed_mask is not list as expected.")
        if(len(self.flow_removed_mask) != 2):
            return (False, "self.flow_removed_mask is not of size 2 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!LL", self.packet_in_mask[0], self.packet_in_mask[1])
        packed += struct.pack("!LL", self.port_status_mask[0], self.port_status_mask[1])
        packed += struct.pack("!LL", self.flow_removed_mask[0], self.flow_removed_mask[1])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 24):
            return binaryString
        fmt = '!LL'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.packet_in_mask[0], self.packet_in_mask[1]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LL'
        start = 8
        end = start + struct.calcsize(fmt)
        (self.port_status_mask[0], self.port_status_mask[1]) = struct.unpack(fmt, binaryString[start:end])
        fmt = '!LL'
        start = 16
        end = start + struct.calcsize(fmt)
        (self.flow_removed_mask[0], self.flow_removed_mask[1]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[24:]

    def __len__(self):
        """Return length of message
        """
        l = 24
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.packet_in_mask !=  other.packet_in_mask: return False
        if self.port_status_mask !=  other.port_status_mask: return False
        if self.flow_removed_mask !=  other.flow_removed_mask: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'packet_in_mask: ' + str(self.packet_in_mask) + '\n'
        outstr += prefix + 'port_status_mask: ' + str(self.port_status_mask) + '\n'
        outstr += prefix + 'flow_removed_mask: ' + str(self.flow_removed_mask) + '\n'
        return outstr


class ofp_action_mpls_ttl(object):
    """Automatically generated Python class for ofp_action_mpls_ttl

    Date 2013-01-17
    Created by of.pythonize.pythonizer
    Core structure: Messages do not include ofp_header
    Does not include var-length arrays
    """
    def __init__(self):
        """Initialize
        Declare members and default values
        """
        self.type = 0
        self.len = 0
        self.mpls_ttl = 0
        self.pad= [0,0,0]

    def __assert(self):
        """Sanity check
        """
        if(not isinstance(self.pad, list)):
            return (False, "self.pad is not list as expected.")
        if(len(self.pad) != 3):
            return (False, "self.pad is not of size 3 as expected.")
        return (True, None)

    def pack(self, assertstruct=True):
        """Pack message
        Packs empty array used as placeholder
        """
        if(assertstruct):
            if(not self.__assert()[0]):
                return None
        packed = ""
        packed += struct.pack("!HHB", self.type, self.len, self.mpls_ttl)
        packed += struct.pack("!BBB", self.pad[0], self.pad[1], self.pad[2])
        return packed

    def unpack(self, binaryString):
        """Unpack message
        Do not unpack empty array used as placeholder
        since they can contain heterogeneous type
        """
        if (len(binaryString) < 8):
            return binaryString
        fmt = '!HHB'
        start = 0
        end = start + struct.calcsize(fmt)
        (self.type, self.len, self.mpls_ttl) = struct.unpack(fmt,  binaryString[start:end])
        fmt = '!BBB'
        start = 5
        end = start + struct.calcsize(fmt)
        (self.pad[0], self.pad[1], self.pad[2]) = struct.unpack(fmt, binaryString[start:end])
        return binaryString[8:]

    def __len__(self):
        """Return length of message
        """
        l = 8
        return l

    def __eq__(self, other):
        """Return True if self and other have same values
        """
        if type(self) != type(other): return False
        if self.type !=  other.type: return False
        if self.len !=  other.len: return False
        if self.mpls_ttl !=  other.mpls_ttl: return False
        if self.pad !=  other.pad: return False
        return True

    def __ne__(self, other): return not self.__eq__(other)

    def show(self, prefix=''):
        """Generate string showing basic members of structure
        """
        outstr = ''
        outstr += prefix + 'type: ' + str(self.type) + '\n'
        outstr += prefix + 'len: ' + str(self.len) + '\n'
        outstr += prefix + 'mpls_ttl: ' + str(self.mpls_ttl) + '\n'
        return outstr


# Enumerated type definitions
ofp_multipart_request_flags = ['OFPMPF_REQ_MORE']
OFPMPF_REQ_MORE                     = 1
ofp_multipart_request_flags_map = {
    1                               : 'OFPMPF_REQ_MORE'
}

ofp_error_type = ['OFPET_HELLO_FAILED', 'OFPET_BAD_REQUEST', 'OFPET_BAD_ACTION', 'OFPET_BAD_INSTRUCTION', 'OFPET_BAD_MATCH', 'OFPET_FLOW_MOD_FAILED', 'OFPET_GROUP_MOD_FAILED', 'OFPET_PORT_MOD_FAILED', 'OFPET_TABLE_MOD_FAILED', 'OFPET_QUEUE_OP_FAILED', 'OFPET_SWITCH_CONFIG_FAILED', 'OFPET_ROLE_REQUEST_FAILED', 'OFPET_METER_MOD_FAILED', 'OFPET_TABLE_FEATURES_FAILED', 'OFPET_EXPERIMENTER']
OFPET_HELLO_FAILED                  = 0
OFPET_BAD_REQUEST                   = 1
OFPET_BAD_ACTION                    = 2
OFPET_BAD_INSTRUCTION               = 3
OFPET_BAD_MATCH                     = 4
OFPET_FLOW_MOD_FAILED               = 5
OFPET_GROUP_MOD_FAILED              = 6
OFPET_PORT_MOD_FAILED               = 7
OFPET_TABLE_MOD_FAILED              = 8
OFPET_QUEUE_OP_FAILED               = 9
OFPET_SWITCH_CONFIG_FAILED          = 10
OFPET_ROLE_REQUEST_FAILED           = 11
OFPET_METER_MOD_FAILED              = 12
OFPET_TABLE_FEATURES_FAILED         = 13
OFPET_EXPERIMENTER                  = 65535
ofp_error_type_map = {
    0                               : 'OFPET_HELLO_FAILED',
    1                               : 'OFPET_BAD_REQUEST',
    2                               : 'OFPET_BAD_ACTION',
    3                               : 'OFPET_BAD_INSTRUCTION',
    4                               : 'OFPET_BAD_MATCH',
    5                               : 'OFPET_FLOW_MOD_FAILED',
    6                               : 'OFPET_GROUP_MOD_FAILED',
    7                               : 'OFPET_PORT_MOD_FAILED',
    8                               : 'OFPET_TABLE_MOD_FAILED',
    9                               : 'OFPET_QUEUE_OP_FAILED',
    10                              : 'OFPET_SWITCH_CONFIG_FAILED',
    11                              : 'OFPET_ROLE_REQUEST_FAILED',
    12                              : 'OFPET_METER_MOD_FAILED',
    13                              : 'OFPET_TABLE_FEATURES_FAILED',
    65535                           : 'OFPET_EXPERIMENTER'
}

ofp_hello_failed_code = ['OFPHFC_INCOMPATIBLE', 'OFPHFC_EPERM']
OFPHFC_INCOMPATIBLE                 = 0
OFPHFC_EPERM                        = 1
ofp_hello_failed_code_map = {
    0                               : 'OFPHFC_INCOMPATIBLE',
    1                               : 'OFPHFC_EPERM'
}

ofp_flow_mod_flags = ['OFPFF_SEND_FLOW_REM', 'OFPFF_CHECK_OVERLAP', 'OFPFF_RESET_COUNTS', 'OFPFF_NO_PKT_COUNTS', 'OFPFF_NO_BYT_COUNTS']
OFPFF_SEND_FLOW_REM                 = 1
OFPFF_CHECK_OVERLAP                 = 2
OFPFF_RESET_COUNTS                  = 4
OFPFF_NO_PKT_COUNTS                 = 8
OFPFF_NO_BYT_COUNTS                 = 16
ofp_flow_mod_flags_map = {
    1                               : 'OFPFF_SEND_FLOW_REM',
    2                               : 'OFPFF_CHECK_OVERLAP',
    4                               : 'OFPFF_RESET_COUNTS',
    8                               : 'OFPFF_NO_PKT_COUNTS',
    16                              : 'OFPFF_NO_BYT_COUNTS'
}

ofp_controller_role = ['OFPCR_ROLE_NOCHANGE', 'OFPCR_ROLE_EQUAL', 'OFPCR_ROLE_MASTER', 'OFPCR_ROLE_SLAVE']
OFPCR_ROLE_NOCHANGE                 = 0
OFPCR_ROLE_EQUAL                    = 1
OFPCR_ROLE_MASTER                   = 2
OFPCR_ROLE_SLAVE                    = 3
ofp_controller_role_map = {
    0                               : 'OFPCR_ROLE_NOCHANGE',
    1                               : 'OFPCR_ROLE_EQUAL',
    2                               : 'OFPCR_ROLE_MASTER',
    3                               : 'OFPCR_ROLE_SLAVE'
}

ofp_port_no = ['OFPP_MAX', 'OFPP_IN_PORT', 'OFPP_TABLE', 'OFPP_NORMAL', 'OFPP_FLOOD', 'OFPP_ALL', 'OFPP_CONTROLLER', 'OFPP_LOCAL', 'OFPP_ANY']
OFPP_MAX                            = 4294967040
OFPP_IN_PORT                        = 4294967288
OFPP_TABLE                          = 4294967289
OFPP_NORMAL                         = 4294967290
OFPP_FLOOD                          = 4294967291
OFPP_ALL                            = 4294967292
OFPP_CONTROLLER                     = 4294967293
OFPP_LOCAL                          = 4294967294
OFPP_ANY                            = 4294967295
ofp_port_no_map = {
    4294967040                      : 'OFPP_MAX',
    4294967288                      : 'OFPP_IN_PORT',
    4294967289                      : 'OFPP_TABLE',
    4294967290                      : 'OFPP_NORMAL',
    4294967291                      : 'OFPP_FLOOD',
    4294967292                      : 'OFPP_ALL',
    4294967293                      : 'OFPP_CONTROLLER',
    4294967294                      : 'OFPP_LOCAL',
    4294967295                      : 'OFPP_ANY'
}

ofp_meter_band_type = ['OFPMBT_DROP', 'OFPMBT_DSCP_REMARK', 'OFPMBT_EXPERIMENTER']
OFPMBT_DROP                         = 1
OFPMBT_DSCP_REMARK                  = 2
OFPMBT_EXPERIMENTER                 = 65535
ofp_meter_band_type_map = {
    1                               : 'OFPMBT_DROP',
    2                               : 'OFPMBT_DSCP_REMARK',
    65535                           : 'OFPMBT_EXPERIMENTER'
}

ofp_bad_instruction_code = ['OFPBIC_UNKNOWN_INST', 'OFPBIC_UNSUP_INST', 'OFPBIC_BAD_TABLE_ID', 'OFPBIC_UNSUP_METADATA', 'OFPBIC_UNSUP_METADATA_MASK', 'OFPBIC_BAD_EXPERIMENTER', 'OFPBIC_BAD_EXP_TYPE', 'OFPBIC_BAD_LEN', 'OFPBIC_EPERM']
OFPBIC_UNKNOWN_INST                 = 0
OFPBIC_UNSUP_INST                   = 1
OFPBIC_BAD_TABLE_ID                 = 2
OFPBIC_UNSUP_METADATA               = 3
OFPBIC_UNSUP_METADATA_MASK          = 4
OFPBIC_BAD_EXPERIMENTER             = 5
OFPBIC_BAD_EXP_TYPE                 = 6
OFPBIC_BAD_LEN                      = 7
OFPBIC_EPERM                        = 8
ofp_bad_instruction_code_map = {
    0                               : 'OFPBIC_UNKNOWN_INST',
    1                               : 'OFPBIC_UNSUP_INST',
    2                               : 'OFPBIC_BAD_TABLE_ID',
    3                               : 'OFPBIC_UNSUP_METADATA',
    4                               : 'OFPBIC_UNSUP_METADATA_MASK',
    5                               : 'OFPBIC_BAD_EXPERIMENTER',
    6                               : 'OFPBIC_BAD_EXP_TYPE',
    7                               : 'OFPBIC_BAD_LEN',
    8                               : 'OFPBIC_EPERM'
}

ofp_port_config = ['OFPPC_PORT_DOWN', 'OFPPC_NO_RECV', 'OFPPC_NO_FWD', 'OFPPC_NO_PACKET_IN']
OFPPC_PORT_DOWN                     = 1
OFPPC_NO_RECV                       = 4
OFPPC_NO_FWD                        = 32
OFPPC_NO_PACKET_IN                  = 64
ofp_port_config_map = {
    1                               : 'OFPPC_PORT_DOWN',
    4                               : 'OFPPC_NO_RECV',
    32                              : 'OFPPC_NO_FWD',
    64                              : 'OFPPC_NO_PACKET_IN'
}

ofp_meter = ['OFPM_MAX', 'OFPM_SLOWPATH', 'OFPM_CONTROLLER', 'OFPM_ALL']
OFPM_MAX                            = 4294901760
OFPM_SLOWPATH                       = 4294967293
OFPM_CONTROLLER                     = 4294967294
OFPM_ALL                            = 4294967295
ofp_meter_map = {
    4294901760                      : 'OFPM_MAX',
    4294967293                      : 'OFPM_SLOWPATH',
    4294967294                      : 'OFPM_CONTROLLER',
    4294967295                      : 'OFPM_ALL'
}

ofp_port_state = ['OFPPS_LINK_DOWN', 'OFPPS_BLOCKED', 'OFPPS_LIVE']
OFPPS_LINK_DOWN                     = 1
OFPPS_BLOCKED                       = 2
OFPPS_LIVE                          = 4
ofp_port_state_map = {
    1                               : 'OFPPS_LINK_DOWN',
    2                               : 'OFPPS_BLOCKED',
    4                               : 'OFPPS_LIVE'
}

ofp_config_flags = ['OFPC_FRAG_NORMAL', 'OFPC_FRAG_DROP', 'OFPC_FRAG_REASM', 'OFPC_FRAG_MASK']
OFPC_FRAG_NORMAL                    = 0
OFPC_FRAG_DROP                      = 1
OFPC_FRAG_REASM                     = 2
OFPC_FRAG_MASK                      = 3
ofp_config_flags_map = {
    0                               : 'OFPC_FRAG_NORMAL',
    1                               : 'OFPC_FRAG_DROP',
    2                               : 'OFPC_FRAG_REASM',
    3                               : 'OFPC_FRAG_MASK'
}

ofp_table_feature_prop_type = ['OFPTFPT_INSTRUCTIONS', 'OFPTFPT_INSTRUCTIONS_MISS', 'OFPTFPT_NEXT_TABLES', 'OFPTFPT_NEXT_TABLES_MISS', 'OFPTFPT_WRITE_ACTIONS', 'OFPTFPT_WRITE_ACTIONS_MISS', 'OFPTFPT_APPLY_ACTIONS', 'OFPTFPT_APPLY_ACTIONS_MISS', 'OFPTFPT_MATCH', 'OFPTFPT_WILDCARDS', 'OFPTFPT_WRITE_SETFIELD', 'OFPTFPT_WRITE_SETFIELD_MISS', 'OFPTFPT_APPLY_SETFIELD', 'OFPTFPT_APPLY_SETFIELD_MISS', 'OFPTFPT_EXPERIMENTER', 'OFPTFPT_EXPERIMENTER_MISS']
OFPTFPT_INSTRUCTIONS                = 0
OFPTFPT_INSTRUCTIONS_MISS           = 1
OFPTFPT_NEXT_TABLES                 = 2
OFPTFPT_NEXT_TABLES_MISS            = 3
OFPTFPT_WRITE_ACTIONS               = 4
OFPTFPT_WRITE_ACTIONS_MISS          = 5
OFPTFPT_APPLY_ACTIONS               = 6
OFPTFPT_APPLY_ACTIONS_MISS          = 7
OFPTFPT_MATCH                       = 8
OFPTFPT_WILDCARDS                   = 10
OFPTFPT_WRITE_SETFIELD              = 12
OFPTFPT_WRITE_SETFIELD_MISS         = 13
OFPTFPT_APPLY_SETFIELD              = 14
OFPTFPT_APPLY_SETFIELD_MISS         = 15
OFPTFPT_EXPERIMENTER                = 65534
OFPTFPT_EXPERIMENTER_MISS           = 65535
ofp_table_feature_prop_type_map = {
    0                               : 'OFPTFPT_INSTRUCTIONS',
    1                               : 'OFPTFPT_INSTRUCTIONS_MISS',
    2                               : 'OFPTFPT_NEXT_TABLES',
    3                               : 'OFPTFPT_NEXT_TABLES_MISS',
    4                               : 'OFPTFPT_WRITE_ACTIONS',
    5                               : 'OFPTFPT_WRITE_ACTIONS_MISS',
    6                               : 'OFPTFPT_APPLY_ACTIONS',
    7                               : 'OFPTFPT_APPLY_ACTIONS_MISS',
    8                               : 'OFPTFPT_MATCH',
    10                              : 'OFPTFPT_WILDCARDS',
    12                              : 'OFPTFPT_WRITE_SETFIELD',
    13                              : 'OFPTFPT_WRITE_SETFIELD_MISS',
    14                              : 'OFPTFPT_APPLY_SETFIELD',
    15                              : 'OFPTFPT_APPLY_SETFIELD_MISS',
    65534                           : 'OFPTFPT_EXPERIMENTER',
    65535                           : 'OFPTFPT_EXPERIMENTER_MISS'
}

ofp_switch_config_failed_code = ['OFPSCFC_BAD_FLAGS', 'OFPSCFC_BAD_LEN', 'OFPQCFC_EPERM']
OFPSCFC_BAD_FLAGS                   = 0
OFPSCFC_BAD_LEN                     = 1
OFPQCFC_EPERM                       = 2
ofp_switch_config_failed_code_map = {
    0                               : 'OFPSCFC_BAD_FLAGS',
    1                               : 'OFPSCFC_BAD_LEN',
    2                               : 'OFPQCFC_EPERM'
}

ofp_multipart_reply_flags = ['OFPMPF_REPLY_MORE']
OFPMPF_REPLY_MORE                   = 1
ofp_multipart_reply_flags_map = {
    1                               : 'OFPMPF_REPLY_MORE'
}

ofp_controller_max_len = ['OFPCML_MAX', 'OFPCML_NO_BUFFER']
OFPCML_MAX                          = 65509
OFPCML_NO_BUFFER                    = 65535
ofp_controller_max_len_map = {
    65509                           : 'OFPCML_MAX',
    65535                           : 'OFPCML_NO_BUFFER'
}

ofp_role_request_failed_code = ['OFPRRFC_STALE', 'OFPRRFC_UNSUP', 'OFPRRFC_BAD_ROLE']
OFPRRFC_STALE                       = 0
OFPRRFC_UNSUP                       = 1
OFPRRFC_BAD_ROLE                    = 2
ofp_role_request_failed_code_map = {
    0                               : 'OFPRRFC_STALE',
    1                               : 'OFPRRFC_UNSUP',
    2                               : 'OFPRRFC_BAD_ROLE'
}

ofp_capabilities = ['OFPC_FLOW_STATS', 'OFPC_TABLE_STATS', 'OFPC_PORT_STATS', 'OFPC_GROUP_STATS', 'OFPC_IP_REASM', 'OFPC_QUEUE_STATS', 'OFPC_PORT_BLOCKED']
OFPC_FLOW_STATS                     = 1
OFPC_TABLE_STATS                    = 2
OFPC_PORT_STATS                     = 4
OFPC_GROUP_STATS                    = 8
OFPC_IP_REASM                       = 32
OFPC_QUEUE_STATS                    = 64
OFPC_PORT_BLOCKED                   = 256
ofp_capabilities_map = {
    1                               : 'OFPC_FLOW_STATS',
    2                               : 'OFPC_TABLE_STATS',
    4                               : 'OFPC_PORT_STATS',
    8                               : 'OFPC_GROUP_STATS',
    32                              : 'OFPC_IP_REASM',
    64                              : 'OFPC_QUEUE_STATS',
    256                             : 'OFPC_PORT_BLOCKED'
}

ofp_bad_match_code = ['OFPBMC_BAD_TYPE', 'OFPBMC_BAD_LEN', 'OFPBMC_BAD_TAG', 'OFPBMC_BAD_DL_ADDR_MASK', 'OFPBMC_BAD_NW_ADDR_MASK', 'OFPBMC_BAD_WILDCARDS', 'OFPBMC_BAD_FIELD', 'OFPBMC_BAD_VALUE', 'OFPBMC_BAD_MASK', 'OFPBMC_BAD_PREREQ', 'OFPBMC_DUP_FIELD', 'OFPBMC_EPERM']
OFPBMC_BAD_TYPE                     = 0
OFPBMC_BAD_LEN                      = 1
OFPBMC_BAD_TAG                      = 2
OFPBMC_BAD_DL_ADDR_MASK             = 3
OFPBMC_BAD_NW_ADDR_MASK             = 4
OFPBMC_BAD_WILDCARDS                = 5
OFPBMC_BAD_FIELD                    = 6
OFPBMC_BAD_VALUE                    = 7
OFPBMC_BAD_MASK                     = 8
OFPBMC_BAD_PREREQ                   = 9
OFPBMC_DUP_FIELD                    = 10
OFPBMC_EPERM                        = 11
ofp_bad_match_code_map = {
    0                               : 'OFPBMC_BAD_TYPE',
    1                               : 'OFPBMC_BAD_LEN',
    2                               : 'OFPBMC_BAD_TAG',
    3                               : 'OFPBMC_BAD_DL_ADDR_MASK',
    4                               : 'OFPBMC_BAD_NW_ADDR_MASK',
    5                               : 'OFPBMC_BAD_WILDCARDS',
    6                               : 'OFPBMC_BAD_FIELD',
    7                               : 'OFPBMC_BAD_VALUE',
    8                               : 'OFPBMC_BAD_MASK',
    9                               : 'OFPBMC_BAD_PREREQ',
    10                              : 'OFPBMC_DUP_FIELD',
    11                              : 'OFPBMC_EPERM'
}

ofp_ipv6exthdr_flags = ['OFPIEH_NONEXT', 'OFPIEH_ESP', 'OFPIEH_AUTH', 'OFPIEH_DEST', 'OFPIEH_FRAG', 'OFPIEH_ROUTER', 'OFPIEH_HOP', 'OFPIEH_UNREP', 'OFPIEH_UNSEQ']
OFPIEH_NONEXT                       = 1
OFPIEH_ESP                          = 2
OFPIEH_AUTH                         = 4
OFPIEH_DEST                         = 8
OFPIEH_FRAG                         = 16
OFPIEH_ROUTER                       = 32
OFPIEH_HOP                          = 64
OFPIEH_UNREP                        = 128
OFPIEH_UNSEQ                        = 256
ofp_ipv6exthdr_flags_map = {
    1                               : 'OFPIEH_NONEXT',
    2                               : 'OFPIEH_ESP',
    4                               : 'OFPIEH_AUTH',
    8                               : 'OFPIEH_DEST',
    16                              : 'OFPIEH_FRAG',
    32                              : 'OFPIEH_ROUTER',
    64                              : 'OFPIEH_HOP',
    128                             : 'OFPIEH_UNREP',
    256                             : 'OFPIEH_UNSEQ'
}

ofp_flow_removed_reason = ['OFPRR_IDLE_TIMEOUT', 'OFPRR_HARD_TIMEOUT', 'OFPRR_DELETE', 'OFPRR_GROUP_DELETE']
OFPRR_IDLE_TIMEOUT                  = 0
OFPRR_HARD_TIMEOUT                  = 1
OFPRR_DELETE                        = 2
OFPRR_GROUP_DELETE                  = 3
ofp_flow_removed_reason_map = {
    0                               : 'OFPRR_IDLE_TIMEOUT',
    1                               : 'OFPRR_HARD_TIMEOUT',
    2                               : 'OFPRR_DELETE',
    3                               : 'OFPRR_GROUP_DELETE'
}

ofp_table_mod_failed_code = ['OFPTMFC_BAD_TABLE', 'OFPTMFC_BAD_CONFIG', 'OFPTMFC_EPERM']
OFPTMFC_BAD_TABLE                   = 0
OFPTMFC_BAD_CONFIG                  = 1
OFPTMFC_EPERM                       = 2
ofp_table_mod_failed_code_map = {
    0                               : 'OFPTMFC_BAD_TABLE',
    1                               : 'OFPTMFC_BAD_CONFIG',
    2                               : 'OFPTMFC_EPERM'
}

ofp_queue_properties = ['OFPQT_MIN_RATE', 'OFPQT_MAX_RATE', 'OFPQT_EXPERIMENTER']
OFPQT_MIN_RATE                      = 1
OFPQT_MAX_RATE                      = 2
OFPQT_EXPERIMENTER                  = 65535
ofp_queue_properties_map = {
    1                               : 'OFPQT_MIN_RATE',
    2                               : 'OFPQT_MAX_RATE',
    65535                           : 'OFPQT_EXPERIMENTER'
}

ofp_table = ['OFPTT_MAX', 'OFPTT_ALL']
OFPTT_MAX                           = 254
OFPTT_ALL                           = 255
ofp_table_map = {
    254                             : 'OFPTT_MAX',
    255                             : 'OFPTT_ALL'
}

ofp_flow_wildcards = ['OFPFW_IN_PORT', 'OFPFW_DL_VLAN', 'OFPFW_DL_SRC', 'OFPFW_DL_DST', 'OFPFW_DL_TYPE', 'OFPFW_NW_PROTO', 'OFPFW_TP_SRC', 'OFPFW_TP_DST', 'OFPFW_NW_SRC_SHIFT', 'OFPFW_NW_SRC_BITS', 'OFPFW_NW_SRC_MASK', 'OFPFW_NW_SRC_ALL', 'OFPFW_NW_DST_SHIFT', 'OFPFW_NW_DST_BITS', 'OFPFW_NW_DST_MASK', 'OFPFW_NW_DST_ALL', 'OFPFW_DL_VLAN_PCP', 'OFPFW_NW_TOS', 'OFPFW_ALL']
OFPFW_IN_PORT                       = 1
OFPFW_DL_VLAN                       = 2
OFPFW_DL_SRC                        = 4
OFPFW_DL_DST                        = 8
OFPFW_DL_TYPE                       = 16
OFPFW_NW_PROTO                      = 32
OFPFW_TP_SRC                        = 64
OFPFW_TP_DST                        = 128
OFPFW_NW_SRC_SHIFT                  = 8
OFPFW_NW_SRC_BITS                   = 6
OFPFW_NW_SRC_MASK                   = 16128
OFPFW_NW_SRC_ALL                    = 8192
OFPFW_NW_DST_SHIFT                  = 14
OFPFW_NW_DST_BITS                   = 6
OFPFW_NW_DST_MASK                   = 1032192
OFPFW_NW_DST_ALL                    = 524288
OFPFW_DL_VLAN_PCP                   = 1048576
OFPFW_NW_TOS                        = 2097152
OFPFW_ALL                           = 4194303
ofp_flow_wildcards_map = {
    1                               : 'OFPFW_IN_PORT',
    2                               : 'OFPFW_DL_VLAN',
    4                               : 'OFPFW_DL_SRC',
    8                               : 'OFPFW_DL_DST',
    16                              : 'OFPFW_DL_TYPE',
    32                              : 'OFPFW_NW_PROTO',
    64                              : 'OFPFW_TP_SRC',
    128                             : 'OFPFW_TP_DST',
    8                               : 'OFPFW_NW_SRC_SHIFT',
    6                               : 'OFPFW_NW_SRC_BITS',
    16128                           : 'OFPFW_NW_SRC_MASK',
    8192                            : 'OFPFW_NW_SRC_ALL',
    14                              : 'OFPFW_NW_DST_SHIFT',
    6                               : 'OFPFW_NW_DST_BITS',
    1032192                         : 'OFPFW_NW_DST_MASK',
    524288                          : 'OFPFW_NW_DST_ALL',
    1048576                         : 'OFPFW_DL_VLAN_PCP',
    2097152                         : 'OFPFW_NW_TOS',
    4194303                         : 'OFPFW_ALL'
}

ofp_meter_mod_failed_code = ['OFPMMFC_UNKNOWN', 'OFPMMFC_METER_EXISTS', 'OFPMMFC_INVALID_METER', 'OFPMMFC_UNKNOWN_METER', 'OFPMMFC_BAD_COMMAND', 'OFPMMFC_BAD_FLAGS', 'OFPMMFC_BAD_RATE', 'OFPMMFC_BAD_BURST', 'OFPMMFC_BAD_BAND', 'OFPMMFC_BAD_BAND_VALUE', 'OFPMMFC_OUT_OF_METERS', 'OFPMMFC_OUT_OF_BANDS']
OFPMMFC_UNKNOWN                     = 0
OFPMMFC_METER_EXISTS                = 1
OFPMMFC_INVALID_METER               = 2
OFPMMFC_UNKNOWN_METER               = 3
OFPMMFC_BAD_COMMAND                 = 4
OFPMMFC_BAD_FLAGS                   = 5
OFPMMFC_BAD_RATE                    = 6
OFPMMFC_BAD_BURST                   = 7
OFPMMFC_BAD_BAND                    = 8
OFPMMFC_BAD_BAND_VALUE              = 9
OFPMMFC_OUT_OF_METERS               = 10
OFPMMFC_OUT_OF_BANDS                = 11
ofp_meter_mod_failed_code_map = {
    0                               : 'OFPMMFC_UNKNOWN',
    1                               : 'OFPMMFC_METER_EXISTS',
    2                               : 'OFPMMFC_INVALID_METER',
    3                               : 'OFPMMFC_UNKNOWN_METER',
    4                               : 'OFPMMFC_BAD_COMMAND',
    5                               : 'OFPMMFC_BAD_FLAGS',
    6                               : 'OFPMMFC_BAD_RATE',
    7                               : 'OFPMMFC_BAD_BURST',
    8                               : 'OFPMMFC_BAD_BAND',
    9                               : 'OFPMMFC_BAD_BAND_VALUE',
    10                              : 'OFPMMFC_OUT_OF_METERS',
    11                              : 'OFPMMFC_OUT_OF_BANDS'
}

ofp_group = ['OFPG_MAX', 'OFPG_ALL', 'OFPG_ANY']
OFPG_MAX                            = 4294967040
OFPG_ALL                            = 4294967292
OFPG_ANY                            = 4294967295
ofp_group_map = {
    4294967040                      : 'OFPG_MAX',
    4294967292                      : 'OFPG_ALL',
    4294967295                      : 'OFPG_ANY'
}

ofp_port_reason = ['OFPPR_ADD', 'OFPPR_DELETE', 'OFPPR_MODIFY']
OFPPR_ADD                           = 0
OFPPR_DELETE                        = 1
OFPPR_MODIFY                        = 2
ofp_port_reason_map = {
    0                               : 'OFPPR_ADD',
    1                               : 'OFPPR_DELETE',
    2                               : 'OFPPR_MODIFY'
}

ofp_group_capabilities = ['OFPGFC_SELECT_WEIGHT', 'OFPGFC_SELECT_LIVENESS', 'OFPGFC_CHAINING', 'OFPGFC_CHAINING_CHECKS']
OFPGFC_SELECT_WEIGHT                = 1
OFPGFC_SELECT_LIVENESS              = 2
OFPGFC_CHAINING                     = 4
OFPGFC_CHAINING_CHECKS              = 8
ofp_group_capabilities_map = {
    1                               : 'OFPGFC_SELECT_WEIGHT',
    2                               : 'OFPGFC_SELECT_LIVENESS',
    4                               : 'OFPGFC_CHAINING',
    8                               : 'OFPGFC_CHAINING_CHECKS'
}

ofp_table_config = ['OFPTC_DEPRECATED_MASK']
OFPTC_DEPRECATED_MASK               = 3
ofp_table_config_map = {
    3                               : 'OFPTC_DEPRECATED_MASK'
}

ofp_action_type = ['OFPAT_OUTPUT', 'OFPAT_COPY_TTL_OUT', 'OFPAT_COPY_TTL_IN', 'OFPAT_SET_MPLS_TTL', 'OFPAT_DEC_MPLS_TTL', 'OFPAT_PUSH_VLAN', 'OFPAT_POP_VLAN', 'OFPAT_PUSH_MPLS', 'OFPAT_POP_MPLS', 'OFPAT_SET_QUEUE', 'OFPAT_GROUP', 'OFPAT_SET_NW_TTL', 'OFPAT_DEC_NW_TTL', 'OFPAT_SET_FIELD', 'OFPAT_PUSH_PBB', 'OFPAT_POP_PBB', 'OFPAT_EXPERIMENTER']
OFPAT_OUTPUT                        = 0
OFPAT_COPY_TTL_OUT                  = 11
OFPAT_COPY_TTL_IN                   = 12
OFPAT_SET_MPLS_TTL                  = 15
OFPAT_DEC_MPLS_TTL                  = 16
OFPAT_PUSH_VLAN                     = 17
OFPAT_POP_VLAN                      = 18
OFPAT_PUSH_MPLS                     = 19
OFPAT_POP_MPLS                      = 20
OFPAT_SET_QUEUE                     = 21
OFPAT_GROUP                         = 22
OFPAT_SET_NW_TTL                    = 23
OFPAT_DEC_NW_TTL                    = 24
OFPAT_SET_FIELD                     = 25
OFPAT_PUSH_PBB                      = 26
OFPAT_POP_PBB                       = 27
OFPAT_EXPERIMENTER                  = 65535
ofp_action_type_map = {
    0                               : 'OFPAT_OUTPUT',
    11                              : 'OFPAT_COPY_TTL_OUT',
    12                              : 'OFPAT_COPY_TTL_IN',
    15                              : 'OFPAT_SET_MPLS_TTL',
    16                              : 'OFPAT_DEC_MPLS_TTL',
    17                              : 'OFPAT_PUSH_VLAN',
    18                              : 'OFPAT_POP_VLAN',
    19                              : 'OFPAT_PUSH_MPLS',
    20                              : 'OFPAT_POP_MPLS',
    21                              : 'OFPAT_SET_QUEUE',
    22                              : 'OFPAT_GROUP',
    23                              : 'OFPAT_SET_NW_TTL',
    24                              : 'OFPAT_DEC_NW_TTL',
    25                              : 'OFPAT_SET_FIELD',
    26                              : 'OFPAT_PUSH_PBB',
    27                              : 'OFPAT_POP_PBB',
    65535                           : 'OFPAT_EXPERIMENTER'
}

ofp_flow_mod_command = ['OFPFC_ADD', 'OFPFC_MODIFY', 'OFPFC_MODIFY_STRICT', 'OFPFC_DELETE', 'OFPFC_DELETE_STRICT']
OFPFC_ADD                           = 0
OFPFC_MODIFY                        = 1
OFPFC_MODIFY_STRICT                 = 2
OFPFC_DELETE                        = 3
OFPFC_DELETE_STRICT                 = 4
ofp_flow_mod_command_map = {
    0                               : 'OFPFC_ADD',
    1                               : 'OFPFC_MODIFY',
    2                               : 'OFPFC_MODIFY_STRICT',
    3                               : 'OFPFC_DELETE',
    4                               : 'OFPFC_DELETE_STRICT'
}

ofp_meter_flags = ['OFPMF_KBPS', 'OFPMF_PKTPS', 'OFPMF_BURST', 'OFPMF_STATS']
OFPMF_KBPS                          = 1
OFPMF_PKTPS                         = 2
OFPMF_BURST                         = 4
OFPMF_STATS                         = 8
ofp_meter_flags_map = {
    1                               : 'OFPMF_KBPS',
    2                               : 'OFPMF_PKTPS',
    4                               : 'OFPMF_BURST',
    8                               : 'OFPMF_STATS'
}

ofp_queue_op_failed_code = ['OFPQOFC_BAD_PORT', 'OFPQOFC_BAD_QUEUE', 'OFPQOFC_EPERM']
OFPQOFC_BAD_PORT                    = 0
OFPQOFC_BAD_QUEUE                   = 1
OFPQOFC_EPERM                       = 2
ofp_queue_op_failed_code_map = {
    0                               : 'OFPQOFC_BAD_PORT',
    1                               : 'OFPQOFC_BAD_QUEUE',
    2                               : 'OFPQOFC_EPERM'
}

ofp_meter_mod_command = ['OFPMC_ADD', 'OFPMC_MODIFY', 'OFPMC_DELETE']
OFPMC_ADD                           = 0
OFPMC_MODIFY                        = 1
OFPMC_DELETE                        = 2
ofp_meter_mod_command_map = {
    0                               : 'OFPMC_ADD',
    1                               : 'OFPMC_MODIFY',
    2                               : 'OFPMC_DELETE'
}

ofp_match_type = ['OFPMT_STANDARD', 'OFPMT_OXM']
OFPMT_STANDARD                      = 0
OFPMT_OXM                           = 1
ofp_match_type_map = {
    0                               : 'OFPMT_STANDARD',
    1                               : 'OFPMT_OXM'
}

ofp_vlan_id = ['OFPVID_PRESENT', 'OFPVID_NONE']
OFPVID_PRESENT                      = 4096
OFPVID_NONE                         = 0
ofp_vlan_id_map = {
    4096                            : 'OFPVID_PRESENT',
    0                               : 'OFPVID_NONE'
}

ofp_hello_elem_type = ['OFPHET_VERSIONBITMAP']
OFPHET_VERSIONBITMAP                = 1
ofp_hello_elem_type_map = {
    1                               : 'OFPHET_VERSIONBITMAP'
}

ofp_table_features_failed_code = ['OFPTFFC_BAD_TABLE', 'OFPTFFC_BAD_METADATA', 'OFPTFFC_BAD_TYPE', 'OFPTFFC_BAD_LEN', 'OFPTFFC_BAD_ARGUMENT', 'OFPTFFC_EPERM']
OFPTFFC_BAD_TABLE                   = 0
OFPTFFC_BAD_METADATA                = 1
OFPTFFC_BAD_TYPE                    = 2
OFPTFFC_BAD_LEN                     = 3
OFPTFFC_BAD_ARGUMENT                = 4
OFPTFFC_EPERM                       = 5
ofp_table_features_failed_code_map = {
    0                               : 'OFPTFFC_BAD_TABLE',
    1                               : 'OFPTFFC_BAD_METADATA',
    2                               : 'OFPTFFC_BAD_TYPE',
    3                               : 'OFPTFFC_BAD_LEN',
    4                               : 'OFPTFFC_BAD_ARGUMENT',
    5                               : 'OFPTFFC_EPERM'
}

ofp_oxm_class = ['OFPXMC_NXM_0', 'OFPXMC_NXM_1', 'OFPXMC_OPENFLOW_BASIC', 'OFPXMC_EXPERIMENTER']
OFPXMC_NXM_0                        = 0
OFPXMC_NXM_1                        = 1
OFPXMC_OPENFLOW_BASIC               = 32768
OFPXMC_EXPERIMENTER                 = 65535
ofp_oxm_class_map = {
    0                               : 'OFPXMC_NXM_0',
    1                               : 'OFPXMC_NXM_1',
    32768                           : 'OFPXMC_OPENFLOW_BASIC',
    65535                           : 'OFPXMC_EXPERIMENTER'
}

ofp_group_type = ['OFPGT_ALL', 'OFPGT_SELECT', 'OFPGT_INDIRECT', 'OFPGT_FF']
OFPGT_ALL                           = 0
OFPGT_SELECT                        = 1
OFPGT_INDIRECT                      = 2
OFPGT_FF                            = 3
ofp_group_type_map = {
    0                               : 'OFPGT_ALL',
    1                               : 'OFPGT_SELECT',
    2                               : 'OFPGT_INDIRECT',
    3                               : 'OFPGT_FF'
}

ofp_instruction_type = ['OFPIT_GOTO_TABLE', 'OFPIT_WRITE_METADATA', 'OFPIT_WRITE_ACTIONS', 'OFPIT_APPLY_ACTIONS', 'OFPIT_CLEAR_ACTIONS', 'OFPIT_METER', 'OFPIT_EXPERIMENTER']
OFPIT_GOTO_TABLE                    = 1
OFPIT_WRITE_METADATA                = 2
OFPIT_WRITE_ACTIONS                 = 3
OFPIT_APPLY_ACTIONS                 = 4
OFPIT_CLEAR_ACTIONS                 = 5
OFPIT_METER                         = 6
OFPIT_EXPERIMENTER                  = 65535
ofp_instruction_type_map = {
    1                               : 'OFPIT_GOTO_TABLE',
    2                               : 'OFPIT_WRITE_METADATA',
    3                               : 'OFPIT_WRITE_ACTIONS',
    4                               : 'OFPIT_APPLY_ACTIONS',
    5                               : 'OFPIT_CLEAR_ACTIONS',
    6                               : 'OFPIT_METER',
    65535                           : 'OFPIT_EXPERIMENTER'
}

ofp_bad_action_code = ['OFPBAC_BAD_TYPE', 'OFPBAC_BAD_LEN', 'OFPBAC_BAD_EXPERIMENTER', 'OFPBAC_BAD_EXP_TYPE', 'OFPBAC_BAD_OUT_PORT', 'OFPBAC_BAD_ARGUMENT', 'OFPBAC_EPERM', 'OFPBAC_TOO_MANY', 'OFPBAC_BAD_QUEUE', 'OFPBAC_BAD_OUT_GROUP', 'OFPBAC_MATCH_INCONSISTENT', 'OFPBAC_UNSUPPORTED_ORDER', 'OFPBAC_BAD_TAG', 'OFPBAC_BAD_SET_TYPE', 'OFPBAC_BAD_SET_LEN', 'OFPBAC_BAD_SET_ARGUMENT']
OFPBAC_BAD_TYPE                     = 0
OFPBAC_BAD_LEN                      = 1
OFPBAC_BAD_EXPERIMENTER             = 2
OFPBAC_BAD_EXP_TYPE                 = 3
OFPBAC_BAD_OUT_PORT                 = 4
OFPBAC_BAD_ARGUMENT                 = 5
OFPBAC_EPERM                        = 6
OFPBAC_TOO_MANY                     = 7
OFPBAC_BAD_QUEUE                    = 8
OFPBAC_BAD_OUT_GROUP                = 9
OFPBAC_MATCH_INCONSISTENT           = 10
OFPBAC_UNSUPPORTED_ORDER            = 11
OFPBAC_BAD_TAG                      = 12
OFPBAC_BAD_SET_TYPE                 = 13
OFPBAC_BAD_SET_LEN                  = 14
OFPBAC_BAD_SET_ARGUMENT             = 15
ofp_bad_action_code_map = {
    0                               : 'OFPBAC_BAD_TYPE',
    1                               : 'OFPBAC_BAD_LEN',
    2                               : 'OFPBAC_BAD_EXPERIMENTER',
    3                               : 'OFPBAC_BAD_EXP_TYPE',
    4                               : 'OFPBAC_BAD_OUT_PORT',
    5                               : 'OFPBAC_BAD_ARGUMENT',
    6                               : 'OFPBAC_EPERM',
    7                               : 'OFPBAC_TOO_MANY',
    8                               : 'OFPBAC_BAD_QUEUE',
    9                               : 'OFPBAC_BAD_OUT_GROUP',
    10                              : 'OFPBAC_MATCH_INCONSISTENT',
    11                              : 'OFPBAC_UNSUPPORTED_ORDER',
    12                              : 'OFPBAC_BAD_TAG',
    13                              : 'OFPBAC_BAD_SET_TYPE',
    14                              : 'OFPBAC_BAD_SET_LEN',
    15                              : 'OFPBAC_BAD_SET_ARGUMENT'
}

oxm_ofb_match_fields = ['OFPXMT_OFB_IN_PORT', 'OFPXMT_OFB_IN_PHY_PORT', 'OFPXMT_OFB_METADATA', 'OFPXMT_OFB_ETH_DST', 'OFPXMT_OFB_ETH_SRC', 'OFPXMT_OFB_ETH_TYPE', 'OFPXMT_OFB_VLAN_VID', 'OFPXMT_OFB_VLAN_PCP', 'OFPXMT_OFB_IP_DSCP', 'OFPXMT_OFB_IP_ECN', 'OFPXMT_OFB_IP_PROTO', 'OFPXMT_OFB_IPV4_SRC', 'OFPXMT_OFB_IPV4_DST', 'OFPXMT_OFB_TCP_SRC', 'OFPXMT_OFB_TCP_DST', 'OFPXMT_OFB_UDP_SRC', 'OFPXMT_OFB_UDP_DST', 'OFPXMT_OFB_SCTP_SRC', 'OFPXMT_OFB_SCTP_DST', 'OFPXMT_OFB_ICMPV4_TYPE', 'OFPXMT_OFB_ICMPV4_CODE', 'OFPXMT_OFB_ARP_OP', 'OFPXMT_OFB_ARP_SPA', 'OFPXMT_OFB_ARP_TPA', 'OFPXMT_OFB_ARP_SHA', 'OFPXMT_OFB_ARP_THA', 'OFPXMT_OFB_IPV6_SRC', 'OFPXMT_OFB_IPV6_DST', 'OFPXMT_OFB_IPV6_FLABEL', 'OFPXMT_OFB_ICMPV6_TYPE', 'OFPXMT_OFB_ICMPV6_CODE', 'OFPXMT_OFB_IPV6_ND_TARGET', 'OFPXMT_OFB_IPV6_ND_SLL', 'OFPXMT_OFB_IPV6_ND_TLL', 'OFPXMT_OFB_MPLS_LABEL', 'OFPXMT_OFB_MPLS_TC', 'OFPXMT_OFP_MPLS_BOS', 'OFPXMT_OFB_PBB_ISID', 'OFPXMT_OFB_TUNNEL_ID', 'OFPXMT_OFB_IPV6_EXTHDR']
OFPXMT_OFB_IN_PORT                  = 0
OFPXMT_OFB_IN_PHY_PORT              = 1
OFPXMT_OFB_METADATA                 = 2
OFPXMT_OFB_ETH_DST                  = 3
OFPXMT_OFB_ETH_SRC                  = 4
OFPXMT_OFB_ETH_TYPE                 = 5
OFPXMT_OFB_VLAN_VID                 = 6
OFPXMT_OFB_VLAN_PCP                 = 7
OFPXMT_OFB_IP_DSCP                  = 8
OFPXMT_OFB_IP_ECN                   = 9
OFPXMT_OFB_IP_PROTO                 = 10
OFPXMT_OFB_IPV4_SRC                 = 11
OFPXMT_OFB_IPV4_DST                 = 12
OFPXMT_OFB_TCP_SRC                  = 13
OFPXMT_OFB_TCP_DST                  = 14
OFPXMT_OFB_UDP_SRC                  = 15
OFPXMT_OFB_UDP_DST                  = 16
OFPXMT_OFB_SCTP_SRC                 = 17
OFPXMT_OFB_SCTP_DST                 = 18
OFPXMT_OFB_ICMPV4_TYPE              = 19
OFPXMT_OFB_ICMPV4_CODE              = 20
OFPXMT_OFB_ARP_OP                   = 21
OFPXMT_OFB_ARP_SPA                  = 22
OFPXMT_OFB_ARP_TPA                  = 23
OFPXMT_OFB_ARP_SHA                  = 24
OFPXMT_OFB_ARP_THA                  = 25
OFPXMT_OFB_IPV6_SRC                 = 26
OFPXMT_OFB_IPV6_DST                 = 27
OFPXMT_OFB_IPV6_FLABEL              = 28
OFPXMT_OFB_ICMPV6_TYPE              = 29
OFPXMT_OFB_ICMPV6_CODE              = 30
OFPXMT_OFB_IPV6_ND_TARGET           = 31
OFPXMT_OFB_IPV6_ND_SLL              = 32
OFPXMT_OFB_IPV6_ND_TLL              = 33
OFPXMT_OFB_MPLS_LABEL               = 34
OFPXMT_OFB_MPLS_TC                  = 35
OFPXMT_OFP_MPLS_BOS                 = 36
OFPXMT_OFB_PBB_ISID                 = 37
OFPXMT_OFB_TUNNEL_ID                = 38
OFPXMT_OFB_IPV6_EXTHDR              = 39
oxm_ofb_match_fields_map = {
    0                               : 'OFPXMT_OFB_IN_PORT',
    1                               : 'OFPXMT_OFB_IN_PHY_PORT',
    2                               : 'OFPXMT_OFB_METADATA',
    3                               : 'OFPXMT_OFB_ETH_DST',
    4                               : 'OFPXMT_OFB_ETH_SRC',
    5                               : 'OFPXMT_OFB_ETH_TYPE',
    6                               : 'OFPXMT_OFB_VLAN_VID',
    7                               : 'OFPXMT_OFB_VLAN_PCP',
    8                               : 'OFPXMT_OFB_IP_DSCP',
    9                               : 'OFPXMT_OFB_IP_ECN',
    10                              : 'OFPXMT_OFB_IP_PROTO',
    11                              : 'OFPXMT_OFB_IPV4_SRC',
    12                              : 'OFPXMT_OFB_IPV4_DST',
    13                              : 'OFPXMT_OFB_TCP_SRC',
    14                              : 'OFPXMT_OFB_TCP_DST',
    15                              : 'OFPXMT_OFB_UDP_SRC',
    16                              : 'OFPXMT_OFB_UDP_DST',
    17                              : 'OFPXMT_OFB_SCTP_SRC',
    18                              : 'OFPXMT_OFB_SCTP_DST',
    19                              : 'OFPXMT_OFB_ICMPV4_TYPE',
    20                              : 'OFPXMT_OFB_ICMPV4_CODE',
    21                              : 'OFPXMT_OFB_ARP_OP',
    22                              : 'OFPXMT_OFB_ARP_SPA',
    23                              : 'OFPXMT_OFB_ARP_TPA',
    24                              : 'OFPXMT_OFB_ARP_SHA',
    25                              : 'OFPXMT_OFB_ARP_THA',
    26                              : 'OFPXMT_OFB_IPV6_SRC',
    27                              : 'OFPXMT_OFB_IPV6_DST',
    28                              : 'OFPXMT_OFB_IPV6_FLABEL',
    29                              : 'OFPXMT_OFB_ICMPV6_TYPE',
    30                              : 'OFPXMT_OFB_ICMPV6_CODE',
    31                              : 'OFPXMT_OFB_IPV6_ND_TARGET',
    32                              : 'OFPXMT_OFB_IPV6_ND_SLL',
    33                              : 'OFPXMT_OFB_IPV6_ND_TLL',
    34                              : 'OFPXMT_OFB_MPLS_LABEL',
    35                              : 'OFPXMT_OFB_MPLS_TC',
    36                              : 'OFPXMT_OFP_MPLS_BOS',
    37                              : 'OFPXMT_OFB_PBB_ISID',
    38                              : 'OFPXMT_OFB_TUNNEL_ID',
    39                              : 'OFPXMT_OFB_IPV6_EXTHDR'
}

ofp_bad_request_code = ['OFPBRC_BAD_VERSION', 'OFPBRC_BAD_TYPE', 'OFPBRC_BAD_MULTIPART', 'OFPBRC_BAD_EXPERIMENTER', 'OFPBRC_BAD_EXP_TYPE', 'OFPBRC_EPERM', 'OFPBRC_BAD_LEN', 'OFPBRC_BUFFER_EMPTY', 'OFPBRC_BUFFER_UNKNOWN', 'OFPBRC_BAD_TABLE_ID', 'OFPBRC_IS_SLAVE', 'OFPBRC_BAD_PORT', 'OFPBRC_BAD_PACKET', 'OFPBRC_MULTIPART_BUFFER_OVERFLOW']
OFPBRC_BAD_VERSION                  = 0
OFPBRC_BAD_TYPE                     = 1
OFPBRC_BAD_MULTIPART                = 2
OFPBRC_BAD_EXPERIMENTER             = 3
OFPBRC_BAD_EXP_TYPE                 = 4
OFPBRC_EPERM                        = 5
OFPBRC_BAD_LEN                      = 6
OFPBRC_BUFFER_EMPTY                 = 7
OFPBRC_BUFFER_UNKNOWN               = 8
OFPBRC_BAD_TABLE_ID                 = 9
OFPBRC_IS_SLAVE                     = 10
OFPBRC_BAD_PORT                     = 11
OFPBRC_BAD_PACKET                   = 12
OFPBRC_MULTIPART_BUFFER_OVERFLOW    = 13
ofp_bad_request_code_map = {
    0                               : 'OFPBRC_BAD_VERSION',
    1                               : 'OFPBRC_BAD_TYPE',
    2                               : 'OFPBRC_BAD_MULTIPART',
    3                               : 'OFPBRC_BAD_EXPERIMENTER',
    4                               : 'OFPBRC_BAD_EXP_TYPE',
    5                               : 'OFPBRC_EPERM',
    6                               : 'OFPBRC_BAD_LEN',
    7                               : 'OFPBRC_BUFFER_EMPTY',
    8                               : 'OFPBRC_BUFFER_UNKNOWN',
    9                               : 'OFPBRC_BAD_TABLE_ID',
    10                              : 'OFPBRC_IS_SLAVE',
    11                              : 'OFPBRC_BAD_PORT',
    12                              : 'OFPBRC_BAD_PACKET',
    13                              : 'OFPBRC_MULTIPART_BUFFER_OVERFLOW'
}

ofp_flow_mod_failed_code = ['OFPFMFC_UNKNOWN', 'OFPFMFC_TABLE_FULL', 'OFPFMFC_BAD_TABLE_ID', 'OFPFMFC_OVERLAP', 'OFPFMFC_EPERM', 'OFPFMFC_BAD_TIMEOUT', 'OFPFMFC_BAD_COMMAND', 'OFPFMFC_BAD_FLAGS']
OFPFMFC_UNKNOWN                     = 0
OFPFMFC_TABLE_FULL                  = 1
OFPFMFC_BAD_TABLE_ID                = 2
OFPFMFC_OVERLAP                     = 3
OFPFMFC_EPERM                       = 4
OFPFMFC_BAD_TIMEOUT                 = 5
OFPFMFC_BAD_COMMAND                 = 6
OFPFMFC_BAD_FLAGS                   = 7
ofp_flow_mod_failed_code_map = {
    0                               : 'OFPFMFC_UNKNOWN',
    1                               : 'OFPFMFC_TABLE_FULL',
    2                               : 'OFPFMFC_BAD_TABLE_ID',
    3                               : 'OFPFMFC_OVERLAP',
    4                               : 'OFPFMFC_EPERM',
    5                               : 'OFPFMFC_BAD_TIMEOUT',
    6                               : 'OFPFMFC_BAD_COMMAND',
    7                               : 'OFPFMFC_BAD_FLAGS'
}

ofp_port_mod_failed_code = ['OFPPMFC_BAD_PORT', 'OFPPMFC_BAD_HW_ADDR', 'OFPPMFC_BAD_CONFIG', 'OFPPMFC_BAD_ADVERTISE', 'OFPPMFC_EPERM']
OFPPMFC_BAD_PORT                    = 0
OFPPMFC_BAD_HW_ADDR                 = 1
OFPPMFC_BAD_CONFIG                  = 2
OFPPMFC_BAD_ADVERTISE               = 3
OFPPMFC_EPERM                       = 4
ofp_port_mod_failed_code_map = {
    0                               : 'OFPPMFC_BAD_PORT',
    1                               : 'OFPPMFC_BAD_HW_ADDR',
    2                               : 'OFPPMFC_BAD_CONFIG',
    3                               : 'OFPPMFC_BAD_ADVERTISE',
    4                               : 'OFPPMFC_EPERM'
}

ofp_type = ['OFPT_HELLO', 'OFPT_ERROR', 'OFPT_ECHO_REQUEST', 'OFPT_ECHO_REPLY', 'OFPT_EXPERIMENTER', 'OFPT_FEATURES_REQUEST', 'OFPT_FEATURES_REPLY', 'OFPT_GET_CONFIG_REQUEST', 'OFPT_GET_CONFIG_REPLY', 'OFPT_SET_CONFIG', 'OFPT_PACKET_IN', 'OFPT_FLOW_REMOVED', 'OFPT_PORT_STATUS', 'OFPT_PACKET_OUT', 'OFPT_FLOW_MOD', 'OFPT_GROUP_MOD', 'OFPT_PORT_MOD', 'OFPT_TABLE_MOD', 'OFPT_MULTIPART_REQUEST', 'OFPT_MULTIPART_REPLY', 'OFPT_BARRIER_REQUEST', 'OFPT_BARRIER_REPLY', 'OFPT_QUEUE_GET_CONFIG_REQUEST', 'OFPT_QUEUE_GET_CONFIG_REPLY', 'OFPT_ROLE_REQUEST', 'OFPT_ROLE_REPLY', 'OFPT_GET_ASYNC_REQUEST', 'OFPT_GET_ASYNC_REPLY', 'OFPT_SET_ASYNC', 'OFPT_METER_MOD']
OFPT_HELLO                          = 0
OFPT_ERROR                          = 1
OFPT_ECHO_REQUEST                   = 2
OFPT_ECHO_REPLY                     = 3
OFPT_EXPERIMENTER                   = 4
OFPT_FEATURES_REQUEST               = 5
OFPT_FEATURES_REPLY                 = 6
OFPT_GET_CONFIG_REQUEST             = 7
OFPT_GET_CONFIG_REPLY               = 8
OFPT_SET_CONFIG                     = 9
OFPT_PACKET_IN                      = 10
OFPT_FLOW_REMOVED                   = 11
OFPT_PORT_STATUS                    = 12
OFPT_PACKET_OUT                     = 13
OFPT_FLOW_MOD                       = 14
OFPT_GROUP_MOD                      = 15
OFPT_PORT_MOD                       = 16
OFPT_TABLE_MOD                      = 17
OFPT_MULTIPART_REQUEST              = 18
OFPT_MULTIPART_REPLY                = 19
OFPT_BARRIER_REQUEST                = 20
OFPT_BARRIER_REPLY                  = 21
OFPT_QUEUE_GET_CONFIG_REQUEST       = 22
OFPT_QUEUE_GET_CONFIG_REPLY         = 23
OFPT_ROLE_REQUEST                   = 24
OFPT_ROLE_REPLY                     = 25
OFPT_GET_ASYNC_REQUEST              = 26
OFPT_GET_ASYNC_REPLY                = 27
OFPT_SET_ASYNC                      = 28
OFPT_METER_MOD                      = 29
ofp_type_map = {
    0                               : 'OFPT_HELLO',
    1                               : 'OFPT_ERROR',
    2                               : 'OFPT_ECHO_REQUEST',
    3                               : 'OFPT_ECHO_REPLY',
    4                               : 'OFPT_EXPERIMENTER',
    5                               : 'OFPT_FEATURES_REQUEST',
    6                               : 'OFPT_FEATURES_REPLY',
    7                               : 'OFPT_GET_CONFIG_REQUEST',
    8                               : 'OFPT_GET_CONFIG_REPLY',
    9                               : 'OFPT_SET_CONFIG',
    10                              : 'OFPT_PACKET_IN',
    11                              : 'OFPT_FLOW_REMOVED',
    12                              : 'OFPT_PORT_STATUS',
    13                              : 'OFPT_PACKET_OUT',
    14                              : 'OFPT_FLOW_MOD',
    15                              : 'OFPT_GROUP_MOD',
    16                              : 'OFPT_PORT_MOD',
    17                              : 'OFPT_TABLE_MOD',
    18                              : 'OFPT_MULTIPART_REQUEST',
    19                              : 'OFPT_MULTIPART_REPLY',
    20                              : 'OFPT_BARRIER_REQUEST',
    21                              : 'OFPT_BARRIER_REPLY',
    22                              : 'OFPT_QUEUE_GET_CONFIG_REQUEST',
    23                              : 'OFPT_QUEUE_GET_CONFIG_REPLY',
    24                              : 'OFPT_ROLE_REQUEST',
    25                              : 'OFPT_ROLE_REPLY',
    26                              : 'OFPT_GET_ASYNC_REQUEST',
    27                              : 'OFPT_GET_ASYNC_REPLY',
    28                              : 'OFPT_SET_ASYNC',
    29                              : 'OFPT_METER_MOD'
}

ofp_packet_in_reason = ['OFPR_NO_MATCH', 'OFPR_ACTION', 'OFPR_INVALID_TTL']
OFPR_NO_MATCH                       = 0
OFPR_ACTION                         = 1
OFPR_INVALID_TTL                    = 2
ofp_packet_in_reason_map = {
    0                               : 'OFPR_NO_MATCH',
    1                               : 'OFPR_ACTION',
    2                               : 'OFPR_INVALID_TTL'
}

ofp_group_mod_command = ['OFPGC_ADD', 'OFPGC_MODIFY', 'OFPGC_DELETE']
OFPGC_ADD                           = 0
OFPGC_MODIFY                        = 1
OFPGC_DELETE                        = 2
ofp_group_mod_command_map = {
    0                               : 'OFPGC_ADD',
    1                               : 'OFPGC_MODIFY',
    2                               : 'OFPGC_DELETE'
}

ofp_port_features = ['OFPPF_10MB_HD', 'OFPPF_10MB_FD', 'OFPPF_100MB_HD', 'OFPPF_100MB_FD', 'OFPPF_1GB_HD', 'OFPPF_1GB_FD', 'OFPPF_10GB_FD', 'OFPPF_40GB_FD', 'OFPPF_100GB_FD', 'OFPPF_1TB_FD', 'OFPPF_OTHER', 'OFPPF_COPPER', 'OFPPF_FIBER', 'OFPPF_AUTONEG', 'OFPPF_PAUSE', 'OFPPF_PAUSE_ASYM']
OFPPF_10MB_HD                       = 1
OFPPF_10MB_FD                       = 2
OFPPF_100MB_HD                      = 4
OFPPF_100MB_FD                      = 8
OFPPF_1GB_HD                        = 16
OFPPF_1GB_FD                        = 32
OFPPF_10GB_FD                       = 64
OFPPF_40GB_FD                       = 128
OFPPF_100GB_FD                      = 256
OFPPF_1TB_FD                        = 512
OFPPF_OTHER                         = 1024
OFPPF_COPPER                        = 2048
OFPPF_FIBER                         = 4096
OFPPF_AUTONEG                       = 8192
OFPPF_PAUSE                         = 16384
OFPPF_PAUSE_ASYM                    = 32768
ofp_port_features_map = {
    1                               : 'OFPPF_10MB_HD',
    2                               : 'OFPPF_10MB_FD',
    4                               : 'OFPPF_100MB_HD',
    8                               : 'OFPPF_100MB_FD',
    16                              : 'OFPPF_1GB_HD',
    32                              : 'OFPPF_1GB_FD',
    64                              : 'OFPPF_10GB_FD',
    128                             : 'OFPPF_40GB_FD',
    256                             : 'OFPPF_100GB_FD',
    512                             : 'OFPPF_1TB_FD',
    1024                            : 'OFPPF_OTHER',
    2048                            : 'OFPPF_COPPER',
    4096                            : 'OFPPF_FIBER',
    8192                            : 'OFPPF_AUTONEG',
    16384                           : 'OFPPF_PAUSE',
    32768                           : 'OFPPF_PAUSE_ASYM'
}

ofp_multipart_types = ['OFPMP_DESC', 'OFPMP_FLOW', 'OFPMP_AGGREGATE', 'OFPMP_TABLE', 'OFPMP_PORT_STATS', 'OFPMP_QUEUE', 'OFPMP_GROUP', 'OFPMP_GROUP_DESC', 'OFPMP_GROUP_FEATURES', 'OFPMP_METER', 'OFPMP_METER_CONFIG', 'OFPMP_METER_FEATURES', 'OFPMP_TABLE_FEATURES', 'OFPMP_PORT_DESC', 'OFPMP_EXPERIMENTER']
OFPMP_DESC                          = 0
OFPMP_FLOW                          = 1
OFPMP_AGGREGATE                     = 2
OFPMP_TABLE                         = 3
OFPMP_PORT_STATS                    = 4
OFPMP_QUEUE                         = 5
OFPMP_GROUP                         = 6
OFPMP_GROUP_DESC                    = 7
OFPMP_GROUP_FEATURES                = 8
OFPMP_METER                         = 9
OFPMP_METER_CONFIG                  = 10
OFPMP_METER_FEATURES                = 11
OFPMP_TABLE_FEATURES                = 12
OFPMP_PORT_DESC                     = 13
OFPMP_EXPERIMENTER                  = 65535
ofp_multipart_types_map = {
    0                               : 'OFPMP_DESC',
    1                               : 'OFPMP_FLOW',
    2                               : 'OFPMP_AGGREGATE',
    3                               : 'OFPMP_TABLE',
    4                               : 'OFPMP_PORT_STATS',
    5                               : 'OFPMP_QUEUE',
    6                               : 'OFPMP_GROUP',
    7                               : 'OFPMP_GROUP_DESC',
    8                               : 'OFPMP_GROUP_FEATURES',
    9                               : 'OFPMP_METER',
    10                              : 'OFPMP_METER_CONFIG',
    11                              : 'OFPMP_METER_FEATURES',
    12                              : 'OFPMP_TABLE_FEATURES',
    13                              : 'OFPMP_PORT_DESC',
    65535                           : 'OFPMP_EXPERIMENTER'
}

ofp_group_mod_failed_code = ['OFPGMFC_GROUP_EXISTS', 'OFPGMFC_INVALID_GROUP', 'OFPGMFC_OUT_OF_GROUPS', 'OFPGMFC_OUT_OF_BUCKETS', 'OFPGMFC_CHAINING_UNSUPPORTED', 'OFPGMFC_WATCH_UNSUPPORTED', 'OFPGMFC_LOOP', 'OFPGMFC_UNKNOWN_GROUP', 'OFPGMFC_CHAINED_GROUP', 'OFPGMFC_BAD_TYPE', 'OFPGMFC_BAD_COMMAND', 'OFPGMFC_BAD_BUCKET', 'OFPGMFC_BAD_WATCH', 'OFPGMFC_EPERM']
OFPGMFC_GROUP_EXISTS                = 0
OFPGMFC_INVALID_GROUP               = 1
OFPGMFC_OUT_OF_GROUPS               = 3
OFPGMFC_OUT_OF_BUCKETS              = 4
OFPGMFC_CHAINING_UNSUPPORTED        = 5
OFPGMFC_WATCH_UNSUPPORTED           = 6
OFPGMFC_LOOP                        = 7
OFPGMFC_UNKNOWN_GROUP               = 8
OFPGMFC_CHAINED_GROUP               = 9
OFPGMFC_BAD_TYPE                    = 10
OFPGMFC_BAD_COMMAND                 = 11
OFPGMFC_BAD_BUCKET                  = 12
OFPGMFC_BAD_WATCH                   = 13
OFPGMFC_EPERM                       = 14
ofp_group_mod_failed_code_map = {
    0                               : 'OFPGMFC_GROUP_EXISTS',
    1                               : 'OFPGMFC_INVALID_GROUP',
    3                               : 'OFPGMFC_OUT_OF_GROUPS',
    4                               : 'OFPGMFC_OUT_OF_BUCKETS',
    5                               : 'OFPGMFC_CHAINING_UNSUPPORTED',
    6                               : 'OFPGMFC_WATCH_UNSUPPORTED',
    7                               : 'OFPGMFC_LOOP',
    8                               : 'OFPGMFC_UNKNOWN_GROUP',
    9                               : 'OFPGMFC_CHAINED_GROUP',
    10                              : 'OFPGMFC_BAD_TYPE',
    11                              : 'OFPGMFC_BAD_COMMAND',
    12                              : 'OFPGMFC_BAD_BUCKET',
    13                              : 'OFPGMFC_BAD_WATCH',
    14                              : 'OFPGMFC_EPERM'
}

# Values from macro definitions
OFP_ETH_ALEN = 6
OFP_MAX_PORT_NAME_LEN = 16
OFP_TCP_PORT = 6633
OFP_FLOW_PERMANENT = 0
OFPQ_MIN_RATE_UNCFG = 0xffff
OFPQ_ALL = 0xffffffff
OFP_VERSION = 0x04
OFP_MAX_TABLE_NAME_LEN = 32
OFP_DEFAULT_PRIORITY = 0x8000
OFP_NO_BUFFER = 0xffffffff
OFP_SSL_PORT = 6633
OFP_DEFAULT_MISS_SEND_LEN = 128
DESC_STR_LEN = 256
SERIAL_NUM_LEN = 32

# Basic structure size definitions.
# Does not include ofp_header members.
# Does not include variable length arrays.
OFP_ACTION_EXPERIMENTER_HEADER_BYTES = 8
OFP_ACTION_GROUP_BYTES = 8
OFP_ACTION_HEADER_BYTES = 8
OFP_ACTION_MPLS_TTL_BYTES = 8
OFP_ACTION_NW_TTL_BYTES = 8
OFP_ACTION_OUTPUT_BYTES = 16
OFP_ACTION_POP_MPLS_BYTES = 8
OFP_ACTION_PUSH_BYTES = 8
OFP_ACTION_SET_FIELD_BYTES = 8
OFP_ACTION_SET_QUEUE_BYTES = 8
OFP_AGGREGATE_STATS_REPLY_BYTES = 24
OFP_AGGREGATE_STATS_REQUEST_BYTES = 40
OFP_ASYNC_CONFIG_BYTES = 24
OFP_BUCKET_BYTES = 16
OFP_BUCKET_COUNTER_BYTES = 16
OFP_DESC_BYTES = 1056
OFP_ERROR_EXPERIMENTER_MSG_BYTES = 8
OFP_ERROR_MSG_BYTES = 4
OFP_EXPERIMENTER_HEADER_BYTES = 8
OFP_EXPERIMENTER_MULTIPART_HEADER_BYTES = 8
OFP_FLOW_MOD_BYTES = 48
OFP_FLOW_REMOVED_BYTES = 48
OFP_FLOW_STATS_BYTES = 56
OFP_FLOW_STATS_REQUEST_BYTES = 40
OFP_GROUP_DESC_STATS_BYTES = 8
OFP_GROUP_FEATURES_BYTES = 40
OFP_GROUP_MOD_BYTES = 8
OFP_GROUP_STATS_BYTES = 40
OFP_GROUP_STATS_REQUEST_BYTES = 8
OFP_HEADER_BYTES = 8
OFP_HELLO_BYTES = 0
OFP_HELLO_ELEM_HEADER_BYTES = 4
OFP_HELLO_ELEM_VERSIONBITMAP_BYTES = 4
OFP_INSTRUCTION_BYTES = 8
OFP_INSTRUCTION_ACTIONS_BYTES = 8
OFP_INSTRUCTION_EXPERIMENTER_BYTES = 8
OFP_INSTRUCTION_GOTO_TABLE_BYTES = 8
OFP_INSTRUCTION_METER_BYTES = 8
OFP_INSTRUCTION_WRITE_METADATA_BYTES = 24
OFP_MATCH_BYTES = 4 
OFP_METER_BAND_DROP_BYTES = 16
OFP_METER_BAND_DSCP_REMARK_BYTES = 16
OFP_METER_BAND_EXPERIMENTER_BYTES = 16
OFP_METER_BAND_HEADER_BYTES = 12
OFP_METER_BAND_STATS_BYTES = 16
OFP_METER_CONFIG_BYTES = 8
OFP_METER_FEATURES_BYTES = 16
OFP_METER_MOD_BYTES = 8
OFP_METER_MULTIPART_REQUEST_BYTES = 8
OFP_METER_STATS_BYTES = 40
OFP_MULTIPART_REPLY_BYTES = 8
OFP_MULTIPART_REQUEST_BYTES = 8
OFP_OXM_EXPERIMENTER_HEADER_BYTES = 8
OFP_PACKET_IN_BYTES = 24
OFP_PACKET_OUT_BYTES = 16
OFP_PACKET_QUEUE_BYTES = 16
OFP_PORT_BYTES = 64
OFP_PORT_MOD_BYTES = 32
OFP_PORT_STATS_BYTES = 112
OFP_PORT_STATS_REQUEST_BYTES = 8
OFP_PORT_STATUS_BYTES = 72
OFP_QUEUE_GET_CONFIG_REPLY_BYTES = 8
OFP_QUEUE_GET_CONFIG_REQUEST_BYTES = 8
OFP_QUEUE_PROP_EXPERIMENTER_BYTES = 16
OFP_QUEUE_PROP_HEADER_BYTES = 8
OFP_QUEUE_PROP_MAX_RATE_BYTES = 16
OFP_QUEUE_PROP_MIN_RATE_BYTES = 16
OFP_QUEUE_STATS_BYTES = 40
OFP_QUEUE_STATS_REQUEST_BYTES = 8
OFP_ROLE_REQUEST_BYTES = 16
OFP_SWITCH_CONFIG_BYTES = 4
OFP_SWITCH_FEATURES_BYTES = 24
OFP_TABLE_FEATURE_PROP_ACTIONS_BYTES = 4
OFP_TABLE_FEATURE_PROP_EXPERIMENTER_BYTES = 12
OFP_TABLE_FEATURE_PROP_HEADER_BYTES = 8
OFP_TABLE_FEATURE_PROP_INSTRUCTIONS_BYTES = 4
OFP_TABLE_FEATURE_PROP_NEXT_TABLES_BYTES = 4
OFP_TABLE_FEATURE_PROP_OXM_BYTES = 4
OFP_TABLE_FEATURES_BYTES = 64
OFP_TABLE_MOD_BYTES = 8
OFP_TABLE_STATS_BYTES = 24
OFP_VENDOR_HEADER_BYTES = 4

