cmake_minimum_required(VERSION 3.25)
project(SeamlessParametrizationPenner)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_compile_options(-fPIC)

if(PROJECT_IS_TOP_LEVEL)
  # Options for the project
  option(USE_PYBIND "Generate pybindings" OFF)
  option(USE_MULTIPRECISION "Use high precision floating point" OFF)

  option(USE_SUITESPARSE "Use suitesparse for QR factorization" ON)
  # TODO Need to disable most features for mpfr, including suitesparse
  option(USE_COMISO "Use Comiso for field generation" ON)

  option(RENDER_TEXTURE "Render results" ON)
  option(ENABLE_VISUALIZATION "Generate viewers for visualization" OFF)

  option(CHECK_VALIDITY "Check validity pre and post conditions" OFF)
  option(BUILD_CURVATURE_METRIC_TESTS "Build tests" OFF)
  option(USE_EMBREE "Use embree" ON)

  # Set libigl options
  option(LIBIGL_PREDICATES "Use Predicates" ON)
  set ( SUITESPARSE_ENABLE_PROJECTS "suitesparse_config;cholmod;spqr" )
  option ( SUITESPARSE_USE_CUDA OFF )
endif()

# Install executables to bin directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# add core Penner methods
add_subdirectory(ext/penner-optimization)

# add executables
add_subdirectory(app)
