
import xmlrpclib

# Resource level
# lvl 0: device ; lvl 1: device-modules ; lvl 2: device-module-port

class ResourceAllocatorClient:

    def __init__(self, proxy_path):
        self.level_pool = [0,0,0]
        self.hwdevices  = {}
        try:
            self.proxy = xmlrpclib.ServerProxy(proxy_path)
        except:
            self.proxy = None
            print 'No proxy!'
        try:
            self.proxy.echo('RA connection echo!')
        except:
            self.proxy = None
            print 'RA Client: No proxy connection!'
        print 'RA Client: Initialization done!'

    def queryResource(self, query):
        '''
        For server.
        '''
        if self.proxy is not None:
            return self.proxy.deviceQuery(query)
        else:
            return False

    def getProperty(self, resid, prop):
        '''
        For server, fallback on local.
        '''
        if self.proxy is not None:
            return self.proxy.getProperty(resid, prop)
        else:
            return self.getPropertyLocal(resid, prop)

    def setProperty(self, resid, prop, value):
        '''
        Local, set item property.
        '''
        return self.setPropertyLocal(resid, prop, value)

    def createEmptyResource(self, lvl):
        '''
        Create a virtual/ inexistent resource, used to getting and setting properties.
        '''
        try:
            lvl = int(lvl)
        except:
            print("Invalid level: %s" % str(lvl))
            return None

        if lvl > len(self.level_pool):
            print("Invalid level size %i, should be 0, 1 or 2" % lvl)
            return None

        # Create resource dictionary and add to list of devices
        self.level_pool[lvl] += 1
        resid = '00%02d_%02d_%03d' % (self.level_pool[0],self.level_pool[1],self.level_pool[2])
        self.hwdevices[resid] = {}
        return resid

    def delResourceLocal(self, resid):
        '''
        Local, delete item.
        '''
        if resid and type(resid)==type('') and resid in self.hwdevices:
            del self.hwdevices[resid]
            return True
        return False

    def getPropertyLocal(self, resid, prop):
        ''' If the resource ID exists and is a string, return property '''
        if resid and type(resid)==type('') and resid in self.hwdevices:
            device = self.hwdevices[resid]
            return device.get(prop, None)
        return None

    def setPropertyLocal(self, resid, prop, value):
        ''' If the resource ID exists and is a string, set property '''
        if resid and type(resid)==type('') and resid in self.hwdevices:
            if prop and value and type(prop)==type('') and type(value)==type(''):
                self.hwdevices[resid][prop] = value
            else:
                print('The property and the value must be a strings!')
                return False
            return True
        return False

#

def main():
    rac = ResourceAllocatorClient('http:')
    resid = rac.createEmptyResource(0)
    rac.setProperty(resid,'prop_1','value_1')
    rac.setProperty(resid,'prop_2','value_2')
    rac.setPropertyLocal(resid,'prop_3','value_3')
    #
    print 'Prop 1:', rac.getProperty(resid,'prop_1')
    print 'Prop 2:', rac.getProperty(resid,'prop_2')
    rac.delResourceLocal(resid)
    print 'Deleted resource.'
    print 'Prop 2:', rac.getProperty(resid,'prop_2')
    print 'Prop 3:', rac.getProperty(resid,'prop_3')
    #

#

if __name__ == "__main__":
    main()
