
# Python OpenFlow meter wrapper classes

from cstruct import *

class meter_band_drop(ofp_meter_band_drop):
    """
    Wrapper class for meter_band_drop instruction object

    """
    def __init__(self):
        ofp_meter_band_drop.__init__(self)
        self.type = OFPMBT_DROP
        self.len = self.__len__()
    def show(self, prefix=''):
        outstr = prefix + "meter_band_drop\n"
        outstr += ofp_meter_band_drop.show(self, prefix)
        return outstr


class meter_band_dscp_remark(ofp_meter_band_dscp_remark	):
    """
    Wrapper class for meter dscp remark object

    """
    def __init__(self):
        ofp_meter_band_dscp_remark.__init__(self)
        self.type = OFPMBT_DSCP_REMARK 
        self.len = self.__len__()
    def show(self, prefix=''):
        outstr = prefix + "meter_band_dscp_remark\n"
        outstr += ofp_meter_band_dscp_remark.show(self, prefix)
        return outstr


meter_class_list = (
    meter_band_drop,
    meter_band_dscp_remark)
