#!/bin/bash

cd $(cd $(dirname $0); pwd)

protoc -I=etrobo_grpc --cpp_out=unit --grpc_out=unit --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) etrobo_control.proto
protoc -I=. --python_out=. --grpc_python_out=. --plugin=protoc-gen-grpc_python=$(which grpc_python_plugin) etrobo_grpc/etrobo_control.proto

for f in `ls unit/*.cc`; do
  mv $f ${f%.cc}.cpp
done
