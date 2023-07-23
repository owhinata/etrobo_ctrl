import grpc
from etrobo_grpc import etrobo_control_pb2 as pb2
from etrobo_grpc import etrobo_control_pb2_grpc as pb2_grpc

class EtRoboClient(object):
    def __init__(self, host='localhost'):
        self.host = host
        self.port = 50051
        print('Connect to {}:{}'.format(self.host, self.port))

        self.mode = 0
        self.edge = 0
        self.speed = 0
        self.steer = 0
        self.threshold = 0

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.port))

        self.stub = pb2_grpc.EtRoboStub(self.channel)

    def set(self, **kwargs):
        mode = kwargs.get('mode', self.mode)
        edge = kwargs.get('edge', self.edge)
        speed = kwargs.get('speed', self.speed)
        steer = kwargs.get('steer', self.steer)
        threshold = kwargs.get('threshold', self.threshold)

        req = pb2.ControlParameter(
                mode=mode, edge=edge, speed=speed, steer=steer,
                threshold=threshold)
        response = self.stub.Control(req)
        if response.message == 'OK':
            self.mode = response.param.mode
            self.edge = response.param.edge
            self.speed = response.param.speed
            self.steer = response.param.steer
            self.threshold = response.param.threshold

