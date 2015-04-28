#!/usr/bin/env python
'''
support for interprocess communication using ZeroMQ
'''

import cStringIO

import zmq

from MAVProxy.modules.lib import mp_module


class ZeroMQModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(ZeroMQModule, self).__init__(mpstate, "zmq", "Communication via ZeroMQ support")

        self.mpstate = mpstate
        endpoint = 'ipc:///tmp/mavproxy-zmq'

        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.bind(endpoint)
        print "Listening for MAVProxy commands on {}".format(endpoint)

    def idle_task(self):
        '''called in idle time'''
        message = self.socket.recv()
        if message.startswith('status'):
            pattern = message.lstrip('status').strip() or None
            output = cStringIO.StringIO()
            response = self.mpstate.status.show(output, pattern=pattern)
            self.socket.send(output.getvalue())
            print "Status response sent"
            output.close()

def init(mpstate):
    '''initialise module'''
    return ZeroMQModule(mpstate)
