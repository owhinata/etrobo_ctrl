/******************************************************************************
 *  Diagnostics.cpp (for LEGO Mindstorms EV3)
 *  Copyright (c) 2023 Emtechs Inc.
 *****************************************************************************/

#include "Control.h"

#include <iostream>
#include <memory>

#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/grpcpp.h>
#include <grpcpp/health_check_service_interface.h>

#include "etrobo_control.grpc.pb.h"
#include "etrobo_control.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

using etrobo_grpc::ControlParameter;
using etrobo_grpc::ControlReply;
using etrobo_grpc::EtRobo;

class EtRoboServiceImpl final : public EtRobo::Service {
  Status Control(ServerContext *context, const ControlParameter *request,
                 ControlReply *reply) override {
    int mode = request->mode();
    int edge = request->edge();
    int speed = request->speed();
    int steer = request->steer();
    int threshold = request->threshold();

    if (mode != 0 && mode != 1) {
      std::cout << "[Ctrl] Invalid parameter: mode=" << mode << std::endl;
      reply->set_message("Failed: Invalid parameter");
    } else if (edge != 0 && edge != 1) {
      std::cout << "[Ctrl] Invalid parameter: edge=" << edge << std::endl;
      reply->set_message("Failed: Invalid parameter");
    } else if (speed < -100 || speed > 100) {
      std::cout << "[Ctrl] Invalid parameter: speed=" << speed << std::endl;
      reply->set_message("Failed: Invalid parameter");
    } else if (steer < -100 || steer > 100) {
      std::cout << "[Ctrl] Invalid parameter: steer=" << steer << std::endl;
      reply->set_message("Failed: Invalid parameter");
    } else if (threshold < 0) {
      std::cout << "[Ctrl] Invalid parameter: threshold=" << threshold
                << std::endl;
      reply->set_message("Failed: Invalid parameter");
    } else {
      mode_ = mode;
      edge_ = edge;
      speed_ = speed;
      steer_ = steer;
      threshold_ = threshold;
      std::cout << "[Ctrl] mode=" << mode << " edge=" << edge
                << " speed=" << speed << " steer=" << steer
                << " threshold=" << threshold << std::endl;
      reply->set_message("OK");
      reply->set_allocated_param(new ControlParameter(*request));
    }
    return Status::OK;
  }

  int mode_;
  int edge_;
  int speed_;
  int steer_;
  int threshold_;

  friend class Control;
};

struct Control::Service {
  std::unique_ptr<Server> server;
  EtRoboServiceImpl impl;
};

Control::Control() : service_(new Service) {}

Control::~Control() { delete service_; }

int Control::GetMode() const { return service_->impl.mode_; }

int Control::GetEdge() const { return service_->impl.edge_; }

int Control::GetSpeed() const { return service_->impl.speed_; }

int Control::GetSteer() const { return service_->impl.steer_; }

int Control::GetThreshold() const { return service_->impl.threshold_; }

void Control::RunServer() {
  std::string server_address = "0.0.0.0:50051";

  grpc::EnableDefaultHealthCheckService(true);
  grpc::reflection::InitProtoReflectionServerBuilderPlugin();

  ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service_->impl);

  service_->server = builder.BuildAndStart();
  std::cout << "[Ctrl] Server listening on " << server_address << std::endl;
}
