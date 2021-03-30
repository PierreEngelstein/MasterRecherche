cmake_minimum_required(VERSION 3.17)
project(test_ibex)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXE_LINKER_FLAGS "-static") # statically link all libraries
link_directories(/usr/local/lib/)
link_directories(/usr/local/lib/ibex/3rd/)
include_directories(/usr/local/include/ibex/)
include_directories(/usr/local/include/ibex/3rd/)
add_executable(test_ibex main.cpp)
target_link_libraries(test_ibex ibex gaol gdtoa ultim)