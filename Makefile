#
# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

CXX = g++
CXXFLAGS += -std=c++11 -I. -Ietrobo_grpc -Iunit
LDFLAGS += -lprotobuf -lgrpc++ -pthread\
           -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed\
           -ldl
PROTOC = protoc
GRPC_CPP_PLUGIN_PATH ?= `which grpc_cpp_plugin`
GRPC_PYTHON_PLUGIN_PATH ?= `which grpc_python_plugin`

all: server

server: obj/server.o obj/Control.o obj/etrobo_control.grpc.pb.o obj/etrobo_control.pb.o
	$(CXX) obj/server.o obj/Control.o obj/etrobo_control.grpc.pb.o obj/etrobo_control.pb.o -o $@ $(LDFLAGS)

obj/server.o: server.cpp
	$(CXX) $(CXXFLAGS) $^ -c -o $@

obj/Control.o: unit/Control.cpp
	$(CXX) $(CXXFLAGS) $^ -c -o $@

obj/etrobo_control.grpc.pb.o: unit/etrobo_control.grpc.pb.cpp
	$(CXX) $(CXXFLAGS) $^ -c -o $@

obj/etrobo_control.pb.o: unit/etrobo_control.pb.cpp
	$(CXX) $(CXXFLAGS) $^ -c -o $@

#server: helloworld.pb.o helloworld.grpc.pb.o greeter_server.o
#	$(CXX) unit/$^ $(LDFLAGS) -o :q
#	$@
#
#%.grpc.pb.cc: %.proto
#	$(PROTOC) --grpc_out=. --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) $<
#
#%.pb.cc: %.proto
#	$(PROTOC) --cpp_out=. $<
#
#greeting/%_pb2.py: %.proto
#	$(PROTOC) --python_out=greeting $<
#
#greeting/%_pb2_grpc.py: %.proto
#	$(PROTOC) --grpc_python_out=greeting --plugin=protoc-gen-grpc_python=$(GRPC_PYTHON_PLUGIN_PATH) $<
#
clean:
	rm -f obj/*.o

#	rm -f *.o *.pb.cc *.pb.h greeter_client greeter_server greeting/helloworld_pb2.py greeting/helloworld_pb2_grpc.py

