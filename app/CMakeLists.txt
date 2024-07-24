add_executable(parametrize_seamless
  parametrize_seamless.cpp
)
target_link_libraries(parametrize_seamless PRIVATE
  PennerLib
  CLI11::CLI11
)

add_executable(generate_frame_field
  generate_frame_field.cpp
)
target_link_libraries(generate_frame_field PRIVATE
  PennerLib
  CLI11::CLI11
)

