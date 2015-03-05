
#
# version: 1.000
# <title>test_sniffer_tshark file</title>
# <description>...</description>
#

# `USER`, `EP`, `SUITE_NAME` and `FILE_NAME` are magic variables,
# injected inside all Twister tests.

try:
    import tShark
except Exception as e:
    print 'Sniffer library not set!{}'.format(e)

print 'I am test_sniffer_tshark file.'

tShark.start_capture(True, 
                     tshark_iface = 'lo', 
                     tshark_read_flags= '', 
                     tshark_write_flags = '')
time.sleep(10)
tShark.stop_capture()

_RESULT = 'PASS'

#
