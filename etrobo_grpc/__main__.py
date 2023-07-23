import sys
import pprint

import grpc
from etrobo_grpc import etrobo_control_pb2 as pb2
from etrobo_grpc import etrobo_control_pb2_grpc as pb2_grpc

if len(sys.argv) < 6:
    print("etrobo_grpc <host> <mode> <edge> <speed> <steer>")
    sys.exit(1)

host = sys.argv[1]
port = 50051

mode = int(sys.argv[2])
edge = int(sys.argv[3])
speed = int(sys.argv[4])
steer = int(sys.argv[5])
threshold = int(sys.argv[6])

req = pb2.ControlParameter(mode=mode, edge=edge, speed=speed, steer=steer, threshold=threshold)

with grpc.insecure_channel('{}:{}'.format(host, port)) as channel:
    stub = pb2_grpc.EtRoboStub(channel)
    response = stub.Control(req)

pprint.pprint(response)
