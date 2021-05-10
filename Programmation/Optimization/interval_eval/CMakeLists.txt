cmake_minimum_required(VERSION 3.17)
project(interval_eval)

#set(CMAKE_CXX_STANDARD 12)

add_executable(interval_eval main.cpp)
target_link_libraries(interval_eval prim)