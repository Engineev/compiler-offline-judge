cmake_minimum_required(VERSION 3.8)

project(compiler-oj)

file(GLOB_RECURSE SOURCE ${CMAKE_SOURCE_DIR}/Judge/*.cpp *.h)

add_executable(${PROJECT_NAME} ${SOURCE})

set(Boost_USE_STATIC_LIBS ON)
find_package(Boost REQUIRED
        COMPONENTS thread
        )
include_directories(${Boost_INCLUDE_DIR})

target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})