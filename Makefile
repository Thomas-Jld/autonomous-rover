.PHONY: all

all:	build launch

clean:
	rm -rf build

build:	clean
	-mkdir build
	# cd build && cmake .. && make && cp rf_gpio.cpython-36m-aarch64-linux-gnu.so ..
	cd build && cmake .. && make && cp rf_gpio.cpython-36m-aarch64-linux-gnu.so ..

launch:
	python3 rf_cpp.py
