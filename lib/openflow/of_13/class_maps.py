
# Class to array member map
class_to_members_map = {
    'ofp_table_feature_prop_header' : [
                                       'type',
                                       'length'
                                      ],
    'ofp_meter_band_header'         : [
                                       'type',
                                       'len',
                                       'rate',
                                       'burst_size'
                                      ],
    'ofp_aggregate_stats_reply'     : [
                                       'packet_count',
                                       'byte_count',
                                       'flow_count'
                                      ],
    'ofp_role_request'              : [
                                       'role',
                                       'generation_id'
                                      ],
    'ofp_table_stats'               : [
                                       'table_id',
                                       'active_count',
                                       'lookup_count',
                                       'matched_count'
                                      ],
    'ofp_table_mod'                 : [
                                       'table_id',
                                       'config'
                                      ],
    'ofp_group_stats'               : [
                                       'length',
                                       'group_id',
                                       'ref_count',
                                       'packet_count',
                                       'byte_count',
                                       'duration_sec',
                                       'duration_nsec'
                                      ],
    'ofp_bucket_counter'            : [
                                       'packet_count',
                                       'byte_count'
                                      ],
    'ofp_instruction_actions'       : [
                                       'type',
                                       'len'
                                      ],
    'ofp_queue_stats'               : [
                                       'port_no',
                                       'queue_id',
                                       'tx_bytes',
                                       'tx_packets',
                                       'tx_errors',
                                       'duration_sec',
                                       'duration_nsec'
                                      ],
    'ofp_meter_config'              : [
                                       'length',
                                       'flags',
                                       'meter_id'
                                      ],
    'ofp_error_msg'                 : [
                                       'type',
                                       'code'
                                      ],
    'ofp_experimenter_multipart_header' : [
                                       'experimenter',
                                       'exp_type'
                                      ],
    'ofp_experimenter_header'       : [
                                       'experimenter',
                                       'exp_type'
                                      ],
    'ofp_table_feature_prop_next_tables' : [
                                       'type',
                                       'length'
                                      ],
    'ofp_port_stats_request'        : [
                                       'port_no'
                                      ],
    'ofp_instruction'               : [
                                       'type',
                                       'len'
                                      ],
    'ofp_table_features'            : [
                                       'length',
                                       'table_id',
                                       'name',
                                       'metadata_match',
                                       'metadata_write',
                                       'config',
                                       'max_entries'
                                      ],
    'ofp_group_stats_request'       : [
                                       'group_id'
                                      ],
    'ofp_table_feature_prop_oxm'    : [
                                       'type',
                                       'length'
                                      ],
    'ofp_hello_elem_header'         : [
                                       'type',
                                       'length'
                                      ],
    'ofp_aggregate_stats_request'   : [
                                       'table_id',
                                       'out_port',
                                       'out_group',
                                       'cookie',
                                       'cookie_mask',
                                       'match'
                                      ],
    'ofp_queue_get_config_request'  : [
                                       'port'
                                      ],
    'ofp_packet_in'                 : [
                                       'buffer_id',
                                       'total_len',
                                       'reason',
                                       'table_id',
                                       'cookie',
                                       'match'
                                      ],
    'ofp_instruction_experimenter'  : [
                                       'type',
                                       'len',
                                       'experimenter'
                                      ],
    'ofp_action_nw_ttl'             : [
                                       'type',
                                       'len',
                                       'nw_ttl'
                                      ],
    'ofp_port_status'               : [
                                       'reason',
                                       'desc'
                                      ],
    'ofp_meter_multipart_request'   : [
                                       'meter_id'
                                      ],
    'ofp_multipart_reply'           : [
                                       'type',
                                       'flags'
                                      ],
    'ofp_action_header'             : [
                                       'type',
                                       'len'
                                      ],
    'ofp_port_mod'                  : [
                                       'port_no',
                                       'hw_addr',
                                       'config',
                                       'mask',
                                       'advertise'
                                      ],
    'ofp_action_output'             : [
                                       'type',
                                       'len',
                                       'port',
                                       'max_len'
                                      ],
    'ofp_switch_config'             : [
                                       'flags',
                                       'miss_send_len'
                                      ],
    'ofp_queue_prop_experimenter'   : [
                                       'prop_header',
                                       'experimenter'
                                      ],
    'ofp_instruction_write_metadata' : [
                                       'type',
                                       'len',
                                       'metadata',
                                       'metadata_mask'
                                      ],
    'ofp_meter_features'            : [
                                       'max_meter',
                                       'band_types',
                                       'capabilities',
                                       'max_bands',
                                       'max_color'
                                      ],
    'ofp_table_feature_prop_instructions' : [
                                       'type',
                                       'length'
                                      ],
    'ofp_action_experimenter_header' : [
                                       'type',
                                       'len',
                                       'experimenter'
                                      ],
    'ofp_meter_band_drop'           : [
                                       'type',
                                       'len',
                                       'rate',
                                       'burst_size'
                                      ],
    'ofp_table_feature_prop_actions' : [
                                       'type',
                                       'length'
                                      ],
    'ofp_meter_band_experimenter'   : [
                                       'type',
                                       'len',
                                       'rate',
                                       'burst_size',
                                       'experimenter'
                                      ],
    'ofp_queue_get_config_reply'    : [
                                       'port'
                                      ],
    'ofp_desc'                      : [
                                       'mfr_desc',
                                       'hw_desc',
                                       'sw_desc',
                                       'serial_num',
                                       'dp_desc'
                                      ],
    'ofp_meter_stats'               : [
                                       'meter_id',
                                       'len',
                                       'flow_count',
                                       'packet_in_count',
                                       'byte_in_count',
                                       'duration_sec',
                                       'duration_nsec'
                                      ],
    'ofp_oxm_experimenter_header'   : [
                                       'oxm_header',
                                       'experimenter'
                                      ],
    'ofp_action_set_queue'          : [
                                       'type',
                                       'len',
                                       'queue_id'
                                      ],
    'ofp_action_set_field'          : [
                                       'type',
                                       'len',
                                       'field'
                                      ],
    'ofp_flow_stats'                : [
                                       'length',
                                       'table_id',
                                       'duration_sec',
                                       'duration_nsec',
                                       'priority',
                                       'idle_timeout',
                                       'hard_timeout',
                                       'cookie',
                                       'packet_count',
                                       'byte_count',
                                       'match'
                                      ],
    'ofp_meter_band_stats'          : [
                                       'packet_band_count',
                                       'byte_band_count'
                                      ],
    'ofp_flow_removed'              : [
                                       'cookie',
                                       'priority',
                                       'reason',
                                       'table_id',
                                       'duration_sec',
                                       'duration_nsec',
                                       'idle_timeout',
                                       'hard_timeout',
                                       'packet_count',
                                       'byte_count',
                                       'match'
                                      ],
    'ofp_queue_prop_min_rate'       : [
                                       'prop_header',
                                       'rate'
                                      ],
    'ofp_header'                    : [
                                       'version',
                                       'type',
                                       'length',
                                       'xid'
                                      ],
    'ofp_multipart_request'         : [
                                       'type',
                                       'flags'
                                      ],
    'ofp_queue_stats_request'       : [
                                       'port_no',
                                       'queue_id'
                                      ],
    'ofp_error_experimenter_msg'    : [
                                       'type',
                                       'exp_type',
                                       'experimenter'
                                      ],
    'ofp_group_mod'                 : [
                                       'command',
                                       'type',
                                       'group_id'
                                      ],
    'ofp_port_stats'                : [
                                       'port_no',
                                       'rx_packets',
                                       'tx_packets',
                                       'rx_bytes',
                                       'tx_bytes',
                                       'rx_dropped',
                                       'tx_dropped',
                                       'rx_errors',
                                       'tx_errors',
                                       'rx_frame_err',
                                       'rx_over_err',
                                       'rx_crc_err',
                                       'collisions',
                                       'duration_sec',
                                       'duration_nsec'
                                      ],
    'ofp_packet_queue'              : [
                                       'queue_id',
                                       'port',
                                       'len'
                                      ],
    'ofp_port'                      : [
                                       'port_no',
                                       'hw_addr',
                                       'name',
                                       'config',
                                       'state',
                                       'curr',
                                       'advertised',
                                       'supported',
                                       'peer',
                                       'curr_speed',
                                       'max_speed'
                                      ],
    'ofp_group_desc_stats'          : [
                                       'length',
                                       'type',
                                       'group_id'
                                      ],
    'ofp_switch_features'           : [
                                       'datapath_id',
                                       'n_buffers',
                                       'n_tables',
                                       'auxiliary_id',
                                       'capabilities',
                                       'reserved'
                                      ],
    'ofp_queue_prop_header'         : [
                                       'property',
                                       'len'
                                      ],
    'ofp_flow_stats_request'        : [
                                       'table_id',
                                       'out_port',
                                       'out_group',
                                       'cookie',
                                       'cookie_mask',
                                       'match'
                                      ],
    'ofp_meter_mod'                 : [
                                       'command',
                                       'flags',
                                       'meter_id'
                                      ],
    'ofp_bucket'                    : [
                                       'len',
                                       'weight',
                                       'watch_port',
                                       'watch_group'
                                      ],
    'ofp_action_pop_mpls'           : [
                                       'type',
                                       'len',
                                       'ethertype'
                                      ],
    'ofp_match'                     : [
                                       'type',
                                       'length',
                                       'oxm_fields'
                                      ],
    'ofp_flow_mod'                  : [
                                       'cookie',
                                       'cookie_mask',
                                       'table_id',
                                       'command',
                                       'idle_timeout',
                                       'hard_timeout',
                                       'priority',
                                       'buffer_id',
                                       'out_port',
                                       'out_group',
                                       'flags',
                                       'match'
                                      ],
    'ofp_vendor_header'             : [
                                       'vendor'
                                      ],
    'ofp_group_features'            : [
                                       'types',
                                       'capabilities',
                                       'max_groups',
                                       'actions'
                                      ],
    'ofp_meter_band_dscp_remark'    : [
                                       'type',
                                       'len',
                                       'rate',
                                       'burst_size',
                                       'prec_level'
                                      ],
    'ofp_hello_elem_versionbitmap'  : [
                                       'type',
                                       'length'
                                      ],
    'ofp_packet_out'                : [
                                       'buffer_id',
                                       'in_port',
                                       'actions_len'
                                      ],
    'ofp_instruction_goto_table'    : [
                                       'type',
                                       'len',
                                       'table_id'
                                      ],
    'ofp_queue_prop_max_rate'       : [
                                       'prop_header',
                                       'rate'
                                      ],
    'ofp_table_feature_prop_experimenter' : [
                                       'type',
                                       'length',
                                       'experimenter',
                                       'exp_type'
                                      ],
    'ofp_action_group'              : [
                                       'type',
                                       'len',
                                       'group_id'
                                      ],
    'ofp_action_push'               : [
                                       'type',
                                       'len',
                                       'ethertype'
                                      ],
    'ofp_instruction_meter'         : [
                                       'type',
                                       'len',
                                       'meter_id'
                                      ],
    'ofp_async_config'              : [
                                       'packet_in_mask',
                                       'port_status_mask',
                                       'flow_removed_mask'
                                      ],
    'ofp_action_mpls_ttl'           : [
                                       'type',
                                       'len',
                                       'mpls_ttl'
                                      ],
    '_ignore' : []
}
