#include <stdio.h>
#include <stdlib.h>                     // for exit()
#include <unistd.h>
#include <thread>
#include <sys/time.h>

#include <pybind11/pybind11.h>
#include <JetsonGPIO.h>
//#include <signal.h>

namespace py=pybind11;

const int rf_pin = 18;


static int64_t getMicrotime()
{
  struct timeval currentTime;
  gettimeofday(&currentTime, NULL);

  return currentTime.tv_sec * (int)1e6 + currentTime.tv_usec;
}

py::list read_rf(int amount)
{
    GPIO::setmode(GPIO::BOARD);
    GPIO::setup(rf_pin, GPIO::IN);

	// int64_t tick0 = 0, tick1 = 0, tick2 = getMicrotime(), interval;
	// py::list records;
    // for(int i = 0; i < 100; i++){
        // // tick0 = getMicrotime();
        // GPIO::wait_for_edge(rf_pin, GPIO::Edge::FALLING);
        // tick1 = getMicrotime();
        // records.append(tick1 - tick2);
        // GPIO::wait_for_edge(rf_pin, GPIO::Edge::RISING);
        // tick2 = getMicrotime();
        // records.append(tick2 - tick1);
        // // printf("time: %.2i\n", (int)interval);
    // }

    // GPIO::cleanup();
    // return records;

	py::list records;
	int cur = GPIO:: input(rf_pin);
	int value = GPIO::input(rf_pin);
	for(int i = 0; i < amount; i++) {
    	int64_t start_t = getMicrotime();
		while (value == cur){
			value = GPIO::input(rf_pin);
		}
    	int64_t stop_t = getMicrotime();
        records.append(stop_t - start_t);
        cur = value;
	}
    GPIO::cleanup();
    return records;
}

// 
// int main(int argc, char** argv)
// {
	// return read_rf();
// }

PYBIND11_MODULE(rf_gpio, m) {
    m.doc() = "RF receiver binding"; // optional module docstring
    m.def("read_rf", &read_rf, "A function that returns the latest rf frame");
}
