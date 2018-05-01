#include <iostream>
#include <string>
#include <vector>

#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

#include "Build.h"
#include "TestCase.h"
#include "Test.h"

void buildCompiler(const std::string & path);

std::vector<sjtu::TestCase> collectTestCases(const std::string & phase, const std::string & dir_);

void testCompiler(const std::vector<sjtu::TestCase> & testCases,
                  const std::string & bashDir,
                  std::size_t threadNum);



int main(int argc, char ** argv) {
    namespace po = boost::program_options;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "produce this message")
        ("tool,T", po::value<std::string>(), "arg = build/test")
        ("bash-dir", po::value<std::string>(), "path/to/bashes/")
        ;

    std::size_t threadNum;
    po::options_description test("test options");
    test.add_options()
        ("all,A", "test all test cases")
        ("phase", po::value<std::string>(), "arg = semantic/codegen/optim + pretest/extended")
        ("thread,j", po::value<std::size_t>(&threadNum)->default_value(1))
        ("cases-dir", po::value<std::string>(), "path/to/testcases/")
        ("gcc-path", po::value<std::string>(), "gcc is used to compile the assembly code.")
        ;
    desc.add(test);

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);

    auto checkArg = [&vm] (const std::string & name) {
        if (!vm.count(name)) {
            std::cout << name << " is required" << std::endl;
            return false;
        }
        return true;
    };

    if (vm.count("help")) {
        std::cout << desc;
        return 0;
    }
    if (vm.count("tool")) {
        if (!vm.count("bash-dir")) {
            std::cout << "bash-dir is required." << std::endl;
            return 1;
        }
        const auto dir = vm["bash-dir"].as<std::string>();

        if (vm["tool"].as<std::string>() == "build") {
            buildCompiler(dir + "build.bash");
            return 0;
        }
        if (vm["tool"].as<std::string>() == "test") {
            if (!checkArg("cases-dir") || !checkArg("bash-dir"))
                return 1;
            std::cout << "collecting test cases...\t";
            std::vector<sjtu::TestCase> testcases;
            if (vm.count("all")) {
                testcases = collectTestCases("semantic", vm["cases-dir"].as<std::string>());
                // TODO
                return 0;
            }
            if (vm.count("phase")) {
                auto phase = vm["phase"].as<std::string>();
                testcases = collectTestCases(phase, vm["cases-dir"].as<std::string>());
                std::cout << "done." << std::endl;
                testCompiler(testcases, vm["bash-dir"].as<std::string>(), threadNum);
                return 0;
            }
        }
    }

    return 1;
}

void buildCompiler(const std::string &path) {
    sjtu::build(path);
}

std::vector<sjtu::TestCase> collectTestCases(const std::string &phase, const std::string &dir_) {
    namespace fs = boost::filesystem;

    std::vector<sjtu::TestCase> res;

    fs::path dir(dir_);

    for (auto & x : fs::directory_iterator(dir)) {
        if (x.path().extension() != ".txt")
            continue;
        auto tmp = x.path().string();
//        std::cerr << x.path().string() << std::endl;
        std::ifstream fin(std::ifstream(x.path().string()));
        auto testCase = sjtu::parse(fin);
        testCase.filename = x.path().filename().string();
        if (testCase.phase == phase)
            res.emplace_back(std::move(testCase));
    }

    return res;
}

void testCompiler(const std::vector<sjtu::TestCase> &testCases,
                  const std::string & bashDir,
                  std::size_t threadNum) {
    std::cout << "running " << testCases.size() << " test cases..." << std::endl;
    for (auto & test : testCases) {
        std::cout << "running " << test.filename << std::endl;
        bool res;
        std::string message;
        std::tie(res, message) = sjtu::test(test, bashDir);
        if (!res) {
            std::cout << test.filename << " has failed.\n"
                      << "Message = " << message << std::endl;
        }
    }
}

