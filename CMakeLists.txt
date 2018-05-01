cmake_minimum_required(VERSION 3.8)

set(CMAKE_CXX_STANDARD 14)

project(compiler-oj)

file(GLOB_RECURSE SOURCE ${CMAKE_SOURCE_DIR}/Judge/*.cpp *.h)

if (MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /O2 /W4 /EHsc")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -o2 -Wall")
endif()
if (UNIX AND NOT APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")
endif ()

add_definitions(-DCMAKE_SOURCE_DIR="${CMAKE_SOURCE_DIR}")

add_executable(${PROJECT_NAME} ${SOURCE})

set(Boost_USE_STATIC_LIBS ON)
find_package(Boost REQUIRED
        COMPONENTS thread program_options filesystem
        )
include_directories(${Boost_INCLUDE_DIR})

target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})