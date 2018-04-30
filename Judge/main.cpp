#include <iostream>
#include <string>
#include <vector>

#include <boost/program_options.hpp>

void buildCompiler(const std::string & path) {}

void testCompiler(const std::vector<std::string> & phases, std::size_t threadNum) {}

int main(int argc, char ** argv) {
    namespace po = boost::program_options;

    po::options_description build("build options");
    build.add_options()
        ("path", po::value<std::string>(), "path/to/build.bash");

    std::size_t threadNum;
    po::options_description test("test options");
    test.add_options()
        ("all,A", "test all test cases")
        ("phase", po::value<std::string>(), "arg = semantic/codegen/optim")
        ("thread,j", po::value<std::size_t>(&threadNum)->default_value(1))
        ;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "produce this message")
        ("tool,T", "arg = build/test");
    desc.add(build).add(test);

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    if (vm.count("help")) {
        std::cout << desc;
        return 0;
    }
    if (vm.count("tool")) {
        if (vm.count("build")) {
            if (!vm.count("path")) {
                std::cout << "path/to/build.bash is required.";
                return 0;
            }
            buildCompiler(vm["path"].as<std::string>());
            return 0;
        }
        if (vm.count("test")) {
            if (vm.count("all")) {
                testCompiler({"semantic", "codegen", "optim"}, threadNum);
                return 0;
            }
            if (vm.count("phase")) {
                testCompiler({vm["phase"].as<std::string>()}, threadNum);
                return 0;
            }
        }
    }

    return 1;
}