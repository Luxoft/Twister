from meter import *
from cstruct import ofp_header
from base_list import ofp_base_list
import copy

meter_object_map = {
    OFPMBT_DROP                         : meter_band_drop,
    OFPMBT_DSCP_REMARK                  : meter_band_dscp_remark
}

class meter_list(ofp_base_list):

    def __init__(self):
        ofp_base_list.__init__(self)
        self.meters = self.items
        self.name = "meter"
        self.class_list = meter_class_list

    def unpack(self, binary_string, bytes=None):
        
	if bytes == None:
            bytes = len(binary_string)
        bytes_done = 0
        count = 0
        cur_string = binary_string
        while bytes_done < bytes:
            hdr = ofp_meter_band_header()
            hdr.unpack(cur_string)
	    if hdr.len < OFP_METER_BAND_HEADER_BYTES:
                print "ERROR: Meter too short"
                break
            if not hdr.type in meter_object_map.keys():
                print "WARNING: Skipping unknown meter ", hdr.type, hdr.len
            else:
                self.meters.append(meter_object_map[hdr.type]())
                self.meters[count].unpack(cur_string)
                count += 1
            cur_string = cur_string[hdr.len:]
            bytes_done += hdr.len
        return cur_string

