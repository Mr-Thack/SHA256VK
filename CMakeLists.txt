cmake_minimum_required(VERSION 3.20)
project(sha256vk)

# Kompute has to remain compatiblity with older 11 and 14 code so that developers can be more enticed to use Kompute to it 
# So, changing this to 17 might not be good and changing it to 20 would be terrible
set(CMAKE_CXX_STANDARD 14)

include(FetchContent)
FetchContent_Declare(kompute GIT_REPOSITORY https://github.com/KomputeProject/kompute.git GIT_TAG master) 
FetchContent_MakeAvailable(kompute)
include_directories(${kompute_SOURCE_DIR}/src/include)

vulkan_compile_shader(
  INFILE alg.comp
  OUTFILE alg.hpp
  NAMESPACE "shader")

# Then add it to the library, so you can access it later in your code
add_library(shader INTERFACE "alg.hpp")
target_include_directories(shader INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>)

# Setting up main example code
add_executable(sha256vk main.cpp)
target_link_libraries(sha256vk PRIVATE shader kompute::kompute)

