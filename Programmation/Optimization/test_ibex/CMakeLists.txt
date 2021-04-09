cmake_minimum_required(VERSION 3.16)
project(test_ibex)

include (FindPkgConfig)
pkg_search_module (IBEX REQUIRED ibex)
message (STATUS "Found Ibex version ${IBEX_VERSION}, CFLAGS: ${IBEX_CFLAGS}, LDFLAGS: ${IBEX_LDFLAGS}, INCLUDES: ${IBEX_INCLUDE_DIRS}")

set(CMAKE_CXX_STANDARD 20)
#set(CMAKE_EXE_LINKER_FLAGS "-static") # statically link all libraries
add_executable(test_ibex main.cpp QuantumOptimization.cpp)
target_compile_options(test_ibex PUBLIC ${IBEX_CFLAGS})
target_include_directories(test_ibex PUBLIC ${IBEX_INCLUDE_DIRS})
target_link_libraries(test_ibex PUBLIC ${IBEX_LDFLAGS} soplex z)