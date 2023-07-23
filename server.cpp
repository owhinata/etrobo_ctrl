#include <unistd.h>
#include "Control.h"

int main() {
	Control ctrl;
	ctrl.RunServer();
	while (1) usleep(10*1000);
}
