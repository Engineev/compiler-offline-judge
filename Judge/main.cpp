#include <iostream>
#include <string>
#include <vector>

#include <boost/program_options.hpp>

#include "Build.h"
#include "TestCase.h"

void buildCompiler(const std::string & path);

void testCompiler(const std::vector<std::string> & phases, std::size_t threadNum);

std::vector<sjtu::TestCase> collectTestCases(const std::string & phase, const std::string & dir) {
    // TODO: collect
    auto tmp = sjtu::parse(dir + "testcase_513.txt");
    std::cout << tmp.src << "\n==========================\n";
    std::cout << tmp.comment << "\n=======================\n";
    std::cout << tmp.input << "\n===============\n";
    std::cout << tmp.output << "\n=============\n";
    return {};
}

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
        ("cases-dir", po::value<std::string>(), "path/to/testcases/")
        ;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "produce this message")
        ("tool,T", po::value<std::string>(), "arg = build/test");
    desc.add(build).add(test);

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    if (vm.count("help")) {
        std::cout << desc;
        return 0;
    }
    if (vm.count("tool")) {
        if (vm["tool"].as<std::string>() == "build") {
            if (!vm.count("path")) {
                std::cout << "path/to/build.bash is required.";
                return 0;
            }
            buildCompiler(vm["path"].as<std::string>());
            return 0;
        }
        if (vm["tool"].as<std::string>() == "test") {
            if (!vm.count("cases-dir")) {
                std::cout << "cases-dir is required" << std::endl;
                return 1;
            }
            // TODO: collect test cases
            if (vm.count("all")) {
                collectTestCases("semantic", vm["cases-dir"].as<std::string>());
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

void buildCompiler(const std::string &path) {
    sjtu::build(path);
}

void testCompiler(const std::vector<std::string> &phases, std::size_t threadNum) {}

