#!/usr/bin/env python

# version: 2.002
#
# -*- coding: utf-8 -*-
#
# File: PacketSniffer.py ; This file is part of Twister.
#
# Copyright (C) 2012 , Luxoft
#
# Authors:
#    Adrian Toader <adtoader@luxoft.com>
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from scapy.all import (Packet, PacketField, ByteField, XByteField, X3BytesField,
                        ByteEnumField, ShortField, XShortField, ShortEnumField,
                        IntField, XIntField, LongField, XLongField, StrField,
                        StrLenField, StrFixedLenField, MACField, SourceMACField,
                        DestMACField, IPField, SourceIPField, ConditionalField)

#




class _PacketField(StrField):
    """
    Custom Packet Field
    """

    holds_packets = 0

    def __init__(self, name, default, cls, length=None):
        StrField.__init__(self, name, default)
        self.cls = cls
        if length is not None:
            self.length_from = lambda pkt,length=length: length

    def i2m(self, pkt, i):
        return str(i)

    def m2i(self, pkt, m):
        return self.cls(m)

    def getfield(self, pkt, s):
        l = self.length_from(pkt)
        return s[l:], self.m2i(pkt,s[:l])




# # # #  OpenFlow v1.0  # # # #

ofp_v1_0_message_type = {
    0: 'Hello', 1: 'Error', 2: 'Echo Request', 3: 'Echo Reply', 4: 'Vendor',
    5: 'Features Request', 6: 'Features Reply',  7: 'Get Config Request',
    8: 'Get Config Reply', 9: 'Set Config', 10: 'Packet Input Notification',
    11: 'Flow Removed Notification', 12: 'Port Status Notification',
    13: 'Packet Output', 14: 'Flow Modification', 15: 'Port Modification',
    16: 'Stats Request', 17: 'Stats Reply', 18: 'Barrier Request',
    19: 'Barrier Reply',
}
ofp_v1_0_action_descriptor_type = {
    0: 'Output Action Descriptor', 1: 'VLAN VID Action Descriptor',
    2: 'VLAN PCP Action Descriptor', 3: 'Strip VLAN tag Action Descriptor',
    4: 'Ethernet Address Action Descriptor (Ethernet source address)',
    5: 'Ethernet Address Action Descriptor (Ethernet destination address)',
    6: 'IPv4 Address Action Descriptor (IPv4 source address)',
    7: 'IPv4 Address Action Descriptor (IPv4 destination address)',
    8: 'IPv4 DSCP Action Descriptor',
    9: 'TCP/UDP Port Action Descriptor (TCP/UDP source port)',
    10: 'TCP/UDP Port Action Descriptor (TCP/UDP destination port)',
    65535: 'Vendor Action Descriptor',
}
ofp_v1_0_stats_requestreply_type = {
    0: 'Description of this OpenFlow switch',
    1: 'Individual flow statistical information',
    2: 'Aggregate flow statistical information',
    3: 'Flow table statistical information', 4: 'Port statistical information',
}


class PortDescriptorField_v1_0(Packet):
    """
    OpenFlow Port Descriptor Field
    """

    name = 'PortDescriptorField_v1_0'

    fields_desc = [
        ShortField('<PortNumber>', None),
        MACField('EthernetAddress', None),
        StrFixedLenField('PortDescription', None, 16),
        XIntField('<PortConfigurationFlags>', None),
        XIntField('<PortStatusFlags>', None),
        XIntField('Current<PortFeatureFlags>', None),
        XIntField('Advertising<PortFeatureFlags>', None),
        XIntField('Supported<PortFeatureFlags>', None),
        XIntField('LinkLayerNeighborAdvertising<PortFeatureFlags>', None),
    ]


class FlowMatchDescriptorField_v1_0(Packet):
    """
    OpenFlow Flow Match Descriptor Field
    """

    name = 'FlowMatchDescriptorField_v1_0'

    fields_desc = [
        IntField('<FlowWildcard>', None),
        ShortField('Ingresss<PortNumber>', None),
        SourceMACField(MACField('EthernetSourceAddress', None)),
        DestMACField(MACField('EthernetDestinationAddress', None)),
        XShortField('<VD+802.1QVID>', None),
        XByteField('PCP', None),
        XByteField('Reserved', None),
        ShortField('EthernetType/Length', None),
        ByteField('IPv4Protocol', None),
        X3BytesField('_Reserved', None),
        SourceIPField('IPv4SourceAddress', None),
        IPField('IPv4DestinationAddress', None),
        ShortField('SourcePort', None),
        ShortField('DestinationPort', None),
    ]


class ActionDescriptorField_v1_0(Packet):
    """
    OpenFlow Action Descriptor Field
    """

    name = 'ActionDescriptorField_v1_0'

    fields_desc = [
        ByteEnumField('Type', None, ofp_v1_0_action_descriptor_type),
        ShortField('Length', None),

        # Output Action Descriptor
        ConditionalField(ShortField('Egress<PortNumber>', None),
                            lambda pkt: pkt.Type == 0),
        ConditionalField(ShortField('MaxLength', None),
                            lambda pkt: pkt.Type == 0),

        # VLAN VID Action Descriptor
        ConditionalField(XShortField('CU+802.1QVID', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(XShortField('VLANVIDReserved', None),
                            lambda pkt: pkt.Type == 1),

        # VLAN PCP Action Descriptor
        ConditionalField(XByteField('CU+PCP', None),
                            lambda pkt: pkt.Type == 2),
        ConditionalField(X3BytesField('VLANPCPReserved', None),
                            lambda pkt: pkt.Type == 2),

        # Strip VLAN tag Action Descriptor
        ConditionalField(XIntField('StripVLANTagReserved', None),
                            lambda pkt: pkt.Type == 3),

        # Ethernet Address Action Descriptor (Ethernet source address) /
        # Ethernet Address Action Descriptor (Ethernet destination address)
        ConditionalField(SourceMACField(MACField('EthernetSourceAddress', None)),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(DestMACField(MACField('EthernetDestinationAddress', None)),
                            lambda pkt: pkt.Type == 5),
        ConditionalField(StrFixedLenField('EthernetAddressReserved', None, 48),
                            lambda pkt: pkt.Type in [4, 5]),

        # IPv4 Address Action Descriptor (IPv4 source address) /
        # IPv4 Address Action Descriptor (IPv4 destination address)
        ConditionalField(SourceIPField('IPv4SourceAddress', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(IPField('IPv4DestinationAddress', None),
                            lambda pkt: pkt.Type == 7),

        # IPv4 DSCP Action Descriptor
        ConditionalField(ByteField('IPv4DSCP+CU', None),
                            lambda pkt: pkt.Type == 8),
        ConditionalField(X3BytesField('IPv4DSCPReserved', None),
                            lambda pkt: pkt.Type == 8),

        # TCP/UDP Port Action Descriptor (TCP/UDP source port) /
        # TCP/UDP Port Action Descriptor (TCP/UDP destination port)
        ConditionalField(ShortField('SourcePort', None),
                            lambda pkt: pkt.Type == 9),
        ConditionalField(ShortField('DestinationPort', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(ShortField('TCP/UDPReserved', None),
                            lambda pkt: pkt.Type in [9, 10]),

        # Vendor Action Descriptor
        ConditionalField(IntField('VendorID', None),
                            lambda pkt: pkt.Type == 65535),
    ]


class StatsRequestBody_v1_0(Packet):
    """
    OpenFlow Stats Request Body
    """

    name = 'StatsRequestBody_v1_0'

    fields_desc = [
        ShortEnumField('Type', None, ofp_v1_0_stats_requestreply_type),
        ShortField('Flags', None),

        _PacketField('<FlowMatchDescriptor>', None,
                            FlowMatchDescriptorField_v1_0, 40),
        ByteField('TableID', None),
        XByteField('Reserved', None),
        ShortField('EgressPortNumber', None)
    ]


class StatsReplyBody_v1_0(Packet):
    """
    OpenFlow Stats Reply Body
    """

    name = 'StatsReplyBody_v1_0'

    fields_desc = [
        ShortEnumField('Type', None, ofp_v1_0_stats_requestreply_type),
        ShortField('Flags', None),

        # Description of this OpenFlow switch
        ConditionalField(StrFixedLenField('ManufacturerDescription', None, 256),
                            lambda pkt: pkt.Type == 0),
        ConditionalField(StrFixedLenField('HardwareDescription', None, 256),
                            lambda pkt: pkt.Type == 0),
        ConditionalField(StrFixedLenField('SoftwareDescription', None, 256),
                            lambda pkt: pkt.Type == 0),
        ConditionalField(IntField('SerialNumberDescription', None),
                            lambda pkt: pkt.Type == 0), ## ??

        # Individual flow statistical information /
        # Aggregate flow statistical information
        ConditionalField(ShortField('Length', None), lambda pkt: pkt.Type == 1),
        ConditionalField(ByteField('TableID', None), lambda pkt: pkt.Type == 1),
        ConditionalField(XByteField('Reserved', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(_PacketField('<FlowMatchDescriptor>',
                            None, FlowMatchDescriptorField_v1_0, 40),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(IntField('LifetimeDuration', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(ShortField('Priority', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(ShortField('SoftLifetime', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(ShortField('HardLifetime', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(ShortField('Reserved', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(LongField('NumberOfPacketsTransferred', None),
                            lambda pkt: pkt.Type in [1, 2]),
        ConditionalField(LongField('NumberOfOctetsTransferred', None),
                            lambda pkt: pkt.Type in [1, 2]),
        ConditionalField(_PacketField('<ActionDescriptors>', None,
                            ActionDescriptorField_v1_0), ## ???? bytes
                            lambda pkt: pkt.Type == 1),
        ConditionalField(IntField('NumberOfFlows', None),
                            lambda pkt: pkt.Type == 2),
        ConditionalField(IntField('Reserved', None),
                            lambda pkt: pkt.Type == 2),

        # Flow table statistical information
        ConditionalField(ByteField('Table_ID', None), lambda pkt: pkt.Type == 1),
        ConditionalField(X3BytesField('Reserved', None),
                            lambda pkt: pkt.Type == 3),
        ConditionalField(StrFixedLenField('TableDescriptionString', None, 16),
                            lambda pkt: pkt.Type == 3),
        ConditionalField(IntField('<FlowWildcard>', None),
                            lambda pkt: pkt.Type == 3),
        ConditionalField(IntField('MaximumNumberOfFlowsSupported', None),
                            lambda pkt: pkt.Type == 3),
        ConditionalField(IntField('NumberOfFlowsInstalled', None),
                            lambda pkt: pkt.Type == 3),
        ConditionalField(IntField('NumberOfPacketsLookedUp', None),
                            lambda pkt: pkt.Type == 3),
        ConditionalField(IntField('NumberOfPacketsMatched', None),
                            lambda pkt: pkt.Type == 3),

        # Port statistical information
        ConditionalField(LongField('NumberOfPakctesReceived', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfPakctesTransmitted', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfOctetsReceived', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfOctetsTransmitted', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfPacketsDroppedInReception', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfPacketsDroppedInTransmittion', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfErrorsInReception', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfErrorsInTransmittion', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfAlignmentErrors', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfOverrunErrors', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfCRCErrors', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(LongField('NumberOfCollisionErrors', None),
                            lambda pkt: pkt.Type == 4),
    ]


class OpenFlowBody_v1_0(Packet):
    """
    OpenFlow Packet v1.0
    """

    name = 'OpenFlowBody_v1_0'

    fields_desc = [
        # Header
        ByteEnumField('Type', None, ofp_v1_0_message_type),
        ShortField('Length', None),
        IntField('ID', None),

        # Error message body
        ConditionalField(ShortField('ErrorType', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(ShortField('ErrorCode', None),
                            lambda pkt: pkt.Type == 1),

        # Echo Request / Echo Reply message body
        ConditionalField(StrField('Data', None), lambda pkt: pkt.Type in [2, 3]),

        # Vendor message body
        ConditionalField(IntField('VendorID', None), lambda pkt: pkt.Type == 4),

        # Features Reply message body
        ConditionalField(XLongField('DatapathID', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(IntField('AvailableNumberOfPacketsCanBeHeld', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(ByteField('NumberOfFlowTabs', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(X3BytesField('FeaturesReplyReserved', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(XIntField('<SwitchCapabilityFlags>', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(XIntField('ActionCapabilityFlags', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(_PacketField('FeaturesReply<PortDescriptors>', None,
                            PortDescriptorField_v1_0, 48),
                            lambda pkt: pkt.Type == 6),

        # Get Config Reply / Set Config message body
        ConditionalField(XShortField('SwitchConfigurationFlags', None),
                            lambda pkt: pkt.Type in [8, 9]),
        ConditionalField(ShortField('MissSendLength', None),
                            lambda pkt: pkt.Type in [8, 9]),

        # Packet Input Notification message body
        ConditionalField(IntField('PacketInputNotificationPacketBufferID', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(ShortField('EthernetFrameLength', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(ShortField('PacketInputNotificationIngresss<PortNumber>', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(ByteField('PacketInputNotificationReason', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(XByteField('PacketInputNotificationReserved', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(StrLenField('EthenretFrame', None,
                            length_from=lambda pkt:pkt.EthernetFrameLength),
                            lambda pkt: pkt.Type == 10),

        # Flow Removed Notification message body
        ConditionalField(_PacketField('FlowRemovedNotification<FlowMatchDescriptor>',
                            None, FlowMatchDescriptorField_v1_0, 40),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(ShortField('FlowRemovedNotificationPriority', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(ByteField('FlowRemovedNotificationReason', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(XByteField('FlowRemovedNotificationReserved', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(IntField('LifetimeDuration', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(ShortField('FlowRemovedNotificationSoftLifetime', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(StrFixedLenField('FlowRemovedNotification_Reserved', None, 48),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(LongField('NumberOfPacketsTransferred', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(LongField('NumberOfOctetsTransferred', None),
                            lambda pkt: pkt.Type == 11),

        # Port Status Notification message body
        ConditionalField(ByteField('PortStatusNotificationReason', None),
                            lambda pkt: pkt.Type == 12),
        ConditionalField(StrFixedLenField('PortStatusNotificationReserved', None, 64),
                            lambda pkt: pkt.Type == 12),
        ConditionalField(_PacketField('PortStatusNotification<PortDescriptors>',
                            None, PortDescriptorField_v1_0, 48),
                            lambda pkt: pkt.Type == 12),

        # Packet Output message body
        ConditionalField(IntField('PacketOutputPacketBufferID', None),
                            lambda pkt: pkt.Type == 13),
        ConditionalField(ShortField('PacketOutputIngress<PortNumber>', None),
                            lambda pkt: pkt.Type == 13),
        ConditionalField(ShortField('LengthOfActionDescriptors', None),
                            lambda pkt: pkt.Type == 13),
        ConditionalField(_PacketField('PacketOutput<ActionDescriptors>', None,
                            ActionDescriptorField_v1_0), ## ???? bytes  ##
                            lambda pkt: pkt.Type == 13),
        ConditionalField(StrField('<PacketData>', None),
                            lambda pkt: pkt.Type == 13),

        # Flow Modification message body
        ConditionalField(_PacketField('FlowModification<FlowMatchDescriptor>', None,
                            FlowMatchDescriptorField_v1_0, 40),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ShortField('Command', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ShortField('FlowModificationSoftLifetime', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ShortField('HardLifetime', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ShortField('FlowModificationPriority', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(IntField('FlowModificationPacketBufferID', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ShortField('FlowModificationEgress<PortNumber>', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(XShortField('FlowModificationCU', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(XIntField('FlowModificationReserved', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(_PacketField('FlowModification<ActionDescriptors>', None,
                            ActionDescriptorField_v1_0), ## ???? bytes
                            lambda pkt: pkt.Type == 14),

        # Port Modification message body
        ConditionalField(ShortField('PortModification<PortNumber>', None),
                            lambda pkt: pkt.Type == 15),
        ConditionalField(MACField('Ethernet Address', None),
                            lambda pkt: pkt.Type == 15),
        ConditionalField(XIntField('<PortConfigurationFlags>', None),
                            lambda pkt: pkt.Type == 15),
        ConditionalField(XIntField('<PortConfigurationFlags>Mask', None),
                            lambda pkt: pkt.Type == 15),
        ConditionalField(XIntField('<PortFeatureFlags>', None),
                            lambda pkt: pkt.Type == 15),

        # Stats Request message body
        ConditionalField(_PacketField('StatsRequest', None,
                            StatsRequestBody_v1_0, 48),
                            lambda pkt: pkt.Type == 16),

        # Stats Reply message body
        ConditionalField(_PacketField('StatsReply', None,
                            StatsReplyBody_v1_0), ## ???? bytes
                            lambda pkt: pkt.Type == 17),

        StrField('Payload', None),
   ]

# # # #  ||  # # # #




# # # #  OpenFlow v1.3  # # # #

ofp_v1_3_message_type = {
    0: 'Hello', 1: 'Error', 2: 'Echo Request', 3: 'Echo Reply', 4: 'Experimenter',
    5: 'Features Request', 6: 'Features Reply',  7: 'Get Config Request',
    8: 'Get Config Reply', 9: 'Set Config', 10: 'Packet Input Notification',
    11: 'Flow Removed Notification', 12: 'Port Status Notification',
    13: 'Packet Output', 14: 'Flow Modification', 15: 'Group Modification',
    16: 'Port Modification', 17: 'Table Modification', 18: 'Multipart Request',
    19: 'Multipart Reply', 20: 'Barrier Request', 21: 'Barrier Reply',
    22: 'Queue Get Config Request', 23: 'Queue Get Config Reply', 24: 'Role Request',
    25: 'Role Reply', 26: 'Get Async Request', 27: 'Get Async Reply', 28: 'Set Async',
    29: 'Meter Modification',
}


class PortDescriptorField_v1_3(Packet):
    """
    OpenFlow Port Descriptor Field
    """

    name = 'PortDescriptorField_v1_3'

    fields_desc = [
        ShortField('<PortNumber>', None),
        XByteField('PortDescriptorFieldPad', None),
        MACField('EthernetAddress', None),
        XByteField('PortDescriptorFieldPad2', None),
        StrFixedLenField('Name', None, 16),
        XIntField('<PortConfigurationFlags>', None),
        XIntField('<PortStatusFlags>', None),
        XIntField('Current<PortFeatureFlags>', None),
        XIntField('Advertising<PortFeatureFlags>', None),
        XIntField('Supported<PortFeatureFlags>', None),
        XIntField('PeerAdvertising<PortFeatureFlags>', None),
        IntField('CurrentSpeed', None),
        IntField('MaxSpeed', None),
    ]


class ActionDescriptorField_v1_3(Packet):
    """
    OpenFlow Action Descriptor Field
    """

    name = 'ActionDescriptorField_v1_3'

    fields_desc = [
        ShortField('Type', None),
        ShortField('Length', None),
        XByteField('Pad', None),
    ]


class OpenFlowBucket_v1_3(Packet):
    """
    OpenFlow Bucket Field
    """

    name = 'OpenFlowBucket_v1_3'

    fields_desc = [
        ShortField('Length', None),
        ShortField('Weight', None),
        IntField('WatchPort', None),
        IntField('WatchGroup', None),
        XByteField('Pad', None),
        _PacketField('PacketOutput<ActionDescriptors>', None,
                            ActionDescriptorField_v1_3, 5),
    ]


class OpenFlowQueueProprieties_v1_3(Packet):
    """
    OpenFlow Queue Properties Field
    """

    name = 'OpenFlowBucket_v1_3'

    fields_desc = [
        ShortField('Property', None),
        ShortField('Length', None),
        XByteField('Pad', None),
    ]


class OpenFlowPacketQueue_v1_3(Packet):
    """
    OpenFlow Bucket Field
    """

    name = 'OpenFlowBucket_v1_3'

    fields_desc = [
        IntField('QueueID', None),
        IntField('Port', None),
        ShortField('Length', None),
        XByteField('Pad', None),
        _PacketField('QueueProprieties', None,
                            OpenFlowQueueProprieties_v1_3, 5),
    ]


class OpenFlowMeterBand_v1_3(Packet):
    """
    OpenFlow Meter Band Field
    """

    name = 'OpenFlowMeterBand_v1_3'

    fields_desc = [
        ShortField('Type', None),
        ShortField('Length', None),
        IntField('Rate', None),
        IntField('BurstSize', None),
    ]


class OpenFlowBody_v1_3(Packet):
    """
    OpenFlow Packet v1.3
    """

    name = 'OpenFlowBody_v1_3'

    fields_desc = [
        # Header
        ByteEnumField('Type', None, ofp_v1_3_message_type),
        ShortField('Length', None),
        IntField('ID', None),

        # Error message body
        ConditionalField(ShortField('ErrorType', None),
                            lambda pkt: pkt.Type == 1),
        ConditionalField(ShortField('ErrorCode', None),
                            lambda pkt: pkt.Type == 1),

        # Echo Request / Echo Reply message body
        ConditionalField(StrField('Data', None), lambda pkt: pkt.Type in [1, 2, 3]),

        # Vendor message body
        #ConditionalField(IntField('VendorID', None), lambda pkt: pkt.Type == 4), # type ????

        # Experimenter
        ConditionalField(XIntField('ExperimenterID', None),
                            lambda pkt: pkt.Type == 4),
        ConditionalField(IntField('ExperimenterType', None),
                            lambda pkt: pkt.Type == 4),

        # Features Reply message body
        ConditionalField(XLongField('DatapathID', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(IntField('MaxBuffers', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(ByteField('MaxTables', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(ByteField('AuxiliaryID', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(XByteField('FeaturesReplyPad', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(XIntField('Capabilities', None),
                            lambda pkt: pkt.Type == 6),
        ConditionalField(IntField('FeaturesReplyReserved', None),
                            lambda pkt: pkt.Type == 6),

        # Set Config message body
        ConditionalField(XShortField('SwitchConfigurationFlags', None),
                            lambda pkt: pkt.Type == 9),
        ConditionalField(ShortField('MissSendLength', None),
                            lambda pkt: pkt.Type == 9),

        # Packet Input Notification message body
        ConditionalField(IntField('PacketInputNotificationPacketBufferID', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(ShortField('EthernetFrameLength', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(ByteField('PacketInputNotificationReason', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(ByteField('PacketInputNotificationTableID', None),
                            lambda pkt: pkt.Type == 10),
        ConditionalField(XLongField('PacketInputNotificationCookie', None),
                            lambda pkt: pkt.Type == 10),

        # Flow Removed Notification message body
        ConditionalField(XLongField('FlowRemovedNotificationCookie', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(ShortField('FlowRemovedNotificationPriority', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(ByteField('FlowRemovedNotificationReason', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(ByteField('FlowRemovedNotificationTableID', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(IntField('Duration_sec', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(IntField('Duration_nsec', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(ShortField('FlowRemovedNotificationIdleTimeout', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(ShortField('HardTimeout', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(LongField('NumberOfPacketsTransferred', None),
                            lambda pkt: pkt.Type == 11),
        ConditionalField(LongField('NumberOfOctetsTransferred', None),
                            lambda pkt: pkt.Type == 11),

        # Port Status Notification message body
        ConditionalField(ByteField('PortStatusNotificationReason', None),
                            lambda pkt: pkt.Type == 12),
        ConditionalField(XByteField('PortStatusNotificationPad', None),
                            lambda pkt: pkt.Type == 12),
        ConditionalField(_PacketField('PortStatusNotification<PortDescriptors>',
                            None, PortDescriptorField_v1_3, 39),
                            lambda pkt: pkt.Type == 12),

        # Packet Output message body
        ConditionalField(IntField('PacketOutputPacketBufferID', None),
                            lambda pkt: pkt.Type == 13),
        ConditionalField(IntField('PacketOutputIngress<PortNumber>', None),
                            lambda pkt: pkt.Type == 13),
        ConditionalField(ShortField('LengthOfActionDescriptors', None),
                            lambda pkt: pkt.Type == 13),
        ConditionalField(XByteField('PacketOutputPad', None),
                            lambda pkt: pkt.Type == 13),
        ConditionalField(_PacketField('PacketOutput<ActionDescriptors>', None,
                            ActionDescriptorField_v1_3, 5),
                            lambda pkt: pkt.Type == 13),

        # Flow Modification message body
        ConditionalField(LongField('FlowModificationCookie', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(XLongField('FlowModificationCookieMask', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ByteField('FlowModificationTableID', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ByteField('FlowModificationCommand', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ShortField('FlowModificationIdleTimeout', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ShortField('FlowModificationHardTimeout', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(ShortField('FlowModificationPriority', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(IntField('FlowModificationPacketBufferID', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(IntField('FlowModificationOutputPort', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(IntField('FlowModificationOutputGroup', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(XShortField('FlowModificationFlags', None),
                            lambda pkt: pkt.Type == 14),
        ConditionalField(XByteField('FlowModificationPad', None),
                            lambda pkt: pkt.Type == 14),

        # Group Modification message body
        ConditionalField(ShortField('GroupModificationCommand', None),
                            lambda pkt: pkt.Type == 15),
        ConditionalField(ByteField('GroupModificationType', None),
                            lambda pkt: pkt.Type == 15),
        ConditionalField(ByteField('GroupModificationPad', None),
                            lambda pkt: pkt.Type == 15),
        ConditionalField(IntField('GroupModificationGroupID', None),
                            lambda pkt: pkt.Type == 15),
        ConditionalField(_PacketField('GroupModificationBucket', None,
                            OpenFlowBucket_v1_3, 18),
                            lambda pkt: pkt.Type == 15),

        # Port Modification message body
        ConditionalField(ShortField('PortModification<PortNumber>', None),
                            lambda pkt: pkt.Type == 16),
        ConditionalField(XByteField('PortModificationPad', None),
                            lambda pkt: pkt.Type == 16),
        ConditionalField(MACField('PortModificationEthernetAddress', None),
                            lambda pkt: pkt.Type == 16),
        ConditionalField(XByteField('PortModificationPad2', None),
                            lambda pkt: pkt.Type == 16),
        ConditionalField(XIntField('<PortConfigurationFlags>', None),
                            lambda pkt: pkt.Type == 16),
        ConditionalField(XIntField('<PortConfigurationFlags>Mask', None),
                            lambda pkt: pkt.Type == 16),
        ConditionalField(XIntField('<PortConfigurationFlags>Advertise', None),
                            lambda pkt: pkt.Type == 16),
        ConditionalField(XByteField('PortModificationPad3', None),
                            lambda pkt: pkt.Type == 16),

        # Table Modification message body
        ConditionalField(ByteField('TableModificationTableID', None),
                            lambda pkt: pkt.Type == 17),
        ConditionalField(XByteField('TableModificationPad', None),
                            lambda pkt: pkt.Type == 17),
        ConditionalField(XIntField('TableModificationConfiguration', None),
                            lambda pkt: pkt.Type == 17),

        # Multipart Request / Multipart Reply message body
        ConditionalField(ShortField('MultipartType', None),
                            lambda pkt: pkt.Type in [18, 19]),
        ConditionalField(XShortField('MultipartFlags', None),
                            lambda pkt: pkt.Type in [18, 19]),
        ConditionalField(XByteField('MultipartPad', None),
                            lambda pkt: pkt.Type in [18, 19]),
        ConditionalField(ByteField('MultipartBody', None),
                            lambda pkt: pkt.Type in [18, 19]),

        # Barrier Reply message body
        ConditionalField(IntField('BarrierReplyID', None),
                            lambda pkt: pkt.Type == 21),

        # Queue Get Config Request / Queue Get Config Reply message body
        ConditionalField(IntField('QueueGetConfigRequestPort', None),
                            lambda pkt: pkt.Type in [22, 23]),
        ConditionalField(ByteField('QueueGetConfigRequestPad', None),
                            lambda pkt: pkt.Type in [22, 23]),
        ConditionalField(_PacketField('OpenFlowPacketQueue', None,
                            OpenFlowPacketQueue_v1_3, 16),
                            lambda pkt: pkt.Type == 23),

        # Role Request / Role Reply message body
        ConditionalField(IntField('RoleRequestRole', None),
                            lambda pkt: pkt.Type in [24, 25]),
        ConditionalField(ByteField('RoleRequestPad', None),
                            lambda pkt: pkt.Type in [24, 25]),
        ConditionalField(LongField('RoleRequestGenerationID', None),
                            lambda pkt: pkt.Type in [24, 25]),

        # Get Async Reply / Set Async messages body
        ConditionalField(XIntField('GetAsyncReplyPacketInMask', None),
                            lambda pkt: pkt.Type in [27, 28]),
        ConditionalField(XIntField('GetAsyncReplyPortStatusMask', None),
                            lambda pkt: pkt.Type in [27, 28]),
        ConditionalField(XIntField('GetAsyncReplyFlowRemovedMask', None),
                            lambda pkt: pkt.Type in [27, 28]),

        # Meter Modification message body
        ConditionalField(ShortField('MeterModificationCommand', None),
                            lambda pkt: pkt.Type == 29),
        ConditionalField(XShortField('MeterModificationFlags', None),
                            lambda pkt: pkt.Type == 29),
        ConditionalField(IntField('MeterModificationMeterID', None),
                            lambda pkt: pkt.Type == 29),
        ConditionalField(_PacketField('MeterModificationMeterBand', None,
                            OpenFlowMeterBand_v1_3, 12),
                            lambda pkt: pkt.Type == 29),

        StrField('Payload', None),
   ]




class OpenFlow(Packet):
    """
    OpenFlow Packet
    """

    name = 'OFP'

    fields_desc = [
        # Header
        ByteField('Version', None),

        # Body
        ConditionalField(PacketField('OpenFlowBody_v1_0', None,
                            OpenFlowBody_v1_0),
                            lambda pkt: pkt.Version in [1, 2]),
        ConditionalField(PacketField('OpenFlowBody_v1_3', None,
                            OpenFlowBody_v1_3),
                            lambda pkt: pkt.Version in [3, 4]),
    ]




class CentralEngineObject:
    """
    Packet Sniffer Central Engine Objects
    """

    def __init__(self, proxy):
        self.proxy = proxy
        self.pluginStatus = None
        self.PAUSED = False
