"""Custom topology example

author: Brandon Heller (brandonh@stanford.edu)

Two directly connected switches plus a host for each switch:

host --- switch --- switch --- host
          \              /  
           \            /
            \          /
             \        /
               switch
Adding the 'topos' dict with a key/value pair to generate our newly defined topology enables one to pass in '--topo=mytopo' from the command line. """

from mininet.topo import Topo, Node

class TwisterTopo( Topo ):
    "Simple topology example."

    def __init__( self, enable_all = True ):
        "Create twister topo."

        # Add default members to class.
        super( TwisterTopo, self ).__init__()

        # Set Node IDs for hosts and switches
        leftHost    = 1
        rightHost   = 2
        leftSwitch  = 3
        rightSwitch = 4
        middleSwich = 5

        # Add nodes
        self.add_node( leftSwitch, Node( is_switch=True ) )
        self.add_node( rightSwitch, Node( is_switch=True ) )
        self.add_node( leftHost, Node( is_switch=False ) )
        self.add_node( rightHost, Node( is_switch=False ) )                
        self.add_node( middleSwitch, Node( is_switch=True ) )

        # Add edges
        self.add_edge( leftHost, leftSwitch )
        self.add_edge( leftSwitch, rightSwitch )
        self.add_edge( rightSwitch, rightHost )
        self.add_edge( rightSwitch, middleSwich )
        self.add_edge( leftSwitch,  middleSwich )

        # Consider all switches and hosts 'on'
        self.enable_all()

topos = { 'twistertopo': ( lambda: TwisterTopo() ) }

