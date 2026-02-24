include(FetchContent)
FetchContent_Declare(
    seamless_optimization
    SYSTEM
    GIT_REPOSITORY https://github.com/rjc8237/seamless-optimization.git
    GIT_TAG main 
)
FetchContent_MakeAvailable(seamless_optimization)
