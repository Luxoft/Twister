
import math
import logging

from wsgiref.simple_server import make_server

from rpclib.decorator import rpc, srpc
from rpclib.service import ServiceBase
from rpclib.application import Application
from rpclib.server.wsgi import WsgiApplication

from rpclib.interface.wsdl import Wsdl11
from rpclib.protocol.soap import Soap11

from rpclib.model.complex import Array, Iterable, ComplexModel
from rpclib.model.primitive import Integer, String

#
_user_database = {}
_user_id_seq = 1
#

class Permission(ComplexModel):
    __namespace__ = 'testing.user_manager'
    application = String
    operation = String


class User(ComplexModel):
    __namespace__ = 'testing.user_manager'
    user_id = Integer
    user_name = String
    first_name = String
    last_name = String
    email = String(pattern=r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[A-Z]{2,4}')
    permissions = Array(Permission)

#

class UserManagerService(ServiceBase):

# --- SERVICE ---

    @srpc(String, Integer, _returns=Iterable(String))
    def say_hello(name, times):
        '''
        <b>Docstrings for service methods appear as documentation in the WSDL</b>
        @param: name the name to say hello to
        @param: the number of times to say hello
        @returns: the completed array
        '''
        for i in xrange(times):
            yield 'Hello, %s' % name

    @srpc(Integer, _returns=Integer)
    def factorial(number):
        return math.factorial(number)

# --- FACTORY ---

    @rpc(User, _returns=Integer)
    def add_user(ctx, user):
        '''
        <b>Docstrings for service methods appear as documentation in the WSDL</b>
        @param: the user
        @returns: user ID
        '''
        user.user_id = ctx.udc.get_next_user_id()
        ctx.udc.users[user.user_id] = user
        return user.user_id

    @rpc(Integer, _returns=User)
    def get_user(ctx, user_id):
        return ctx.udc.users[user_id]

    @rpc(User)
    def set_user(ctx, user):
        ctx.udc.users[user.user_id] = user

    @rpc(Integer)
    def del_user(ctx, user_id):
        del ctx.udc.users[user_id]

    @rpc(_returns=Iterable(User))
    def get_all_users(ctx):
        return ctx.udc.users.itervalues()

#

class UserDefinedContext(object):
    def __init__(self):
        self.users = _user_database

    @staticmethod
    def get_next_user_id():
        global _user_id_seq
        _user_id_seq += 1
        return _user_id_seq


def _on_method_call(ctx):
    ctx.udc = UserDefinedContext()

#

if __name__=='__main__':

    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('rpclib.protocol.xml').setLevel(logging.WARNING)

    application = Application([UserManagerService],
            'testing.user_manager',
            interface=Wsdl11(),
            in_protocol=Soap11(),
            out_protocol=Soap11())
    application.event_manager.add_listener('method_call', _on_method_call)

    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8080, WsgiApplication(application))
    print "listening to http://localhost:8080"
    print "wsdl is at: http://localhost:8080/?wsdl"
    server.serve_forever()
