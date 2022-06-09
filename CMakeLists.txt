cmake_minimum_required(VERSION 3.4)
project(rf_gpio LANGUAGES CXX)

find_package(JetsonGPIO)

add_subdirectory(pybind11)
pybind11_add_module(rf_gpio rf_gpio.cpp)

target_link_libraries(rf_gpio PRIVATE JetsonGPIO::JetsonGPIO)
