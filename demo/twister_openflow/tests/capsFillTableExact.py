
from ce_libs import *
try:
    caps.caps_config = getOpenflowConfig(globEpName)
    caps.caps_port_map = caps.caps_config['port_map']
except:
    print "Error: Invalid configuration for EPNAME: " + str(globEpName)

class FillTableExact(basic.SimpleProtocol):
    """
    Fill the flow table with exact matches; can take a while

    Fill table until no more flows can be added.  Report result.
    Increment the source IP address.  Assume the flow table will
    fill in less than 4 billion inserts

    To check the number of flows in the tables is expensive, so
    it's only done periodically.  This is controlled by the
    count_check variable.

    A switch may have multiple tables.  The default behaviour
    is to count all the flows in all the tables.  By setting 
    the parameter "caps_table_idx" in the configuration array,
    you can control which table to check.
    """
    def runTest(self):
        caps_logger.info("Running " + str(self))
        flow_caps_common(self)


tc=FillTableExact()
_RESULT = tc.run()
