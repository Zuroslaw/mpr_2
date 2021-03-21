cmake_minimum_required(VERSION 3.17)
project(mc C)

set(CMAKE_C_STANDARD 99)

find_package(MPI REQUIRED)
include_directories(SYSTEM ${MPI_INCLUDE_PATH})

add_executable(mc
        mc.c)
add_executable(mc_p
        mc_p.c)

target_link_libraries(mc_p ${MPI_C_LIBRARIES})