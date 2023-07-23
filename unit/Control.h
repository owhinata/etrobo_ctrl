/******************************************************************************
 *  Control.h (for LEGO Mindstorms EV3)
 *  Copyright (c) 2023 Emtechs Inc.
 *****************************************************************************/

#ifndef EV3_UNIT_CONTROL_H_
#define EV3_UNIT_CONTROL_H_

class Control {
public:
  Control();
  ~Control();

  void RunServer();

  int GetMode() const;
  int GetEdge() const;
  int GetSpeed() const;
  int GetSteer() const;
  int GetThreshold() const;

  Control(const Control&) = delete;
  Control& operator=(const Control&) = delete;

private:
  struct Service;
  Service* service_;
};

#endif // EV3_UNIT_CONTROL_H_
