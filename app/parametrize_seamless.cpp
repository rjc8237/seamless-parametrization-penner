#include "holonomy/interface.h"
#include "holonomy/holonomy/newton.h"
#include "holonomy/holonomy/cones.h"
#include "optimization/parameterization/refinement.h"

#include <igl/readOBJ.h>
#include <igl/writeOBJ.h>
#include <CLI/CLI.hpp>

using namespace Penner;
using namespace Penner::Optimization;
using namespace Penner::Holonomy;

int main(int argc, char* argv[])
{
    std::map<std::string, spdlog::level::level_enum> log_level_map {
        {"trace",    spdlog::level::trace},
        {"debug",    spdlog::level::debug},
        {"info",     spdlog::level::info},
        {"warn",     spdlog::level::warn},
        {"critical", spdlog::level::critical},
        {"off",      spdlog::level::off},
    };

    // Get command line arguments
    CLI::App app{"Generate a constrained seamless parametrization."};
    std::string mesh_filename = "";
    std::string Th_hat_filename = "";
    std::string rotation_form_filename = "";
    std::string output_dir = "./";

    // IO Parameters
    app.add_option("--mesh", mesh_filename, "Mesh filepath")->check(CLI::ExistingFile)->required();
    app.add_option("--cones", Th_hat_filename, "Cone angle filepath")
        ->check(CLI::ExistingFile);
    app.add_option("--field", rotation_form_filename, "Rotation field one form")
        ->check(CLI::ExistingFile);
    app.add_option("-o,--output", output_dir, "Output directory");
    std::filesystem::create_directory(output_dir);

    // Marked Metric Parameters
    // NOTE: Only several parameters are exposed to the CLI
    MarkedMetricParameters marked_metric_params;
    NewtonParameters alg_params;
    app.add_flag(
        "--remove_loop_constraints",
        marked_metric_params.remove_loop_constraints,
        "Remove homology basis loop holonomy constraints");
    app.add_option("--max_itr", alg_params.max_itr, "Upper bound for newton iterations")
        ->check(CLI::NonNegativeNumber);
    app.add_option("--error_eps", alg_params.error_eps, "Error convergence threshold")
        ->check(CLI::NonNegativeNumber);
    alg_params.output_dir = output_dir;
    alg_params.error_log = true;

    // Miscellaneous
    double max_triangle_quality = 0.;
    bool use_delaunay = true;
    bool fit_field = false;
    spdlog::level::level_enum log_level = spdlog::level::info;
    app.add_option(
           "--max_triangle_quality",
           max_triangle_quality,
           "Maximum allowed triangle quality (0 for unbounded)")
        ->check(CLI::NonNegativeNumber);
    app.add_flag("--use_delaunay", use_delaunay, "Use Delaunay connectivity");
    app.add_flag("--fit_field", fit_field, "Fit new cross field");
    app.add_option("--log_level", log_level, "Level of logging")
        ->transform(CLI::CheckedTransformer(log_level_map, CLI::ignore_case));

    CLI11_PARSE(app, argc, argv);
    spdlog::set_level(log_level);

    // Get input mesh
    Eigen::MatrixXd V, uv, N;
    Eigen::MatrixXi F, FT, FN;
    spdlog::info("Using mesh at {}", mesh_filename);
    igl::readOBJ(mesh_filename, V, uv, N, F, FT, FN);

    // Get input angles from cross field or file
    std::vector<Scalar> Th_hat;
    VectorX rotation_form;
    if (fit_field) {
        FieldParameters field_params;
        std::tie(rotation_form, Th_hat) = generate_intrinsic_rotation_form(V, F, field_params);
    } else {
        spdlog::info("Using cone angles at {}", Th_hat_filename);
        read_vector_from_file(Th_hat_filename, Th_hat);

        // Get input rotation
        std::vector<Scalar> rotation_form_vec;
        spdlog::info("Using rotation_form at {}", rotation_form_filename);
        read_vector_from_file(rotation_form_filename, rotation_form_vec);
        convert_std_to_eigen_vector(rotation_form_vec, rotation_form);
    }

    // Generate initial marked mesh for optimization
    std::vector<int> free_cones(0);
    auto [marked_metric, vtx_reindex] =
        generate_marked_metric(V, F, V, F, Th_hat, rotation_form, free_cones, marked_metric_params);

    // Check for invalid cones and fix any issues
    if (!validate_cones(marked_metric)) {
        spdlog::info("Fixing invalid cones");
        fix_cones(marked_metric);
    }

    // Make initial mesh Delaunay if desired
    std::vector<int> flip_seq = {};
    if (use_delaunay) {
        marked_metric.make_discrete_metric();
        flip_seq = marked_metric.get_flip_sequence();
        marked_metric.reset();
    }

    // Regularize
    if (max_triangle_quality > 0.) {
        regularize_metric(marked_metric, max_triangle_quality);
    }

    // Optimize metric
    spdlog::info("Beginning optimization");
    auto opt_marked_metric = optimize_metric_angles(marked_metric, alg_params);

    // Undo any initial flips to make Delaunay
    for (auto iter = flip_seq.rbegin(); iter != flip_seq.rend(); ++iter) {
        int h = *iter;
        spdlog::trace("Flipping {} cw", h);
        opt_marked_metric.flip_ccw(h, true);
        opt_marked_metric.flip_ccw(h, true);
        opt_marked_metric.flip_ccw(h, true);
    }

    // Write the output metric coordinates
    std::string output_filename;
    output_filename = join_path(output_dir, "optimized_metric_coords");
    write_vector(opt_marked_metric.get_reduced_metric_coordinates(), output_filename);

    // Generate full overlay
    std::vector<bool> is_cut = {};
    auto vf_res = generate_VF_mesh_from_metric(
        V,
        F,
        Th_hat,
        marked_metric,
        opt_marked_metric.get_metric_coordinates(),
        is_cut,
        false);
    Eigen::MatrixXd V_o = std::get<1>(vf_res);
    Eigen::MatrixXi F_o = std::get<2>(vf_res);
    Eigen::MatrixXd uv_o = std::get<3>(vf_res);
    Eigen::MatrixXi FT_o = std::get<4>(vf_res);
    std::vector<int> fn_to_f_o = std::get<7>(vf_res);
    std::vector<std::pair<int, int>> endpoints_o = std::get<8>(vf_res);

    // Generate minimal refinement
    RefinementMesh refinement_mesh(V_o, F_o, uv_o, FT_o, fn_to_f_o, endpoints_o);
    auto [V_r, F_r, uv_r, FT_r, fn_to_f_r, endpoints_r] = refinement_mesh.get_VF_mesh();

    // Write the output mesh
    output_filename = join_path(output_dir, "parameterized_mesh.obj");
    write_obj_with_uv(output_filename, V_r, F_r, uv_r, FT_r);
}
