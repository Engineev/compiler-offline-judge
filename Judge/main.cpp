#include <iostream>
#include <boost/program_options.hpp>

int main(int argc, char ** argv) {
    namespace po = boost::program_options;

    po::options_description build("build options");
    build.add_options()("path/to/build.bash", po::value<std::string>());

    std::size_t threadNum;
    po::options_description test("test options");
    test.add_options()
        ("all,A", "test all test cases")
        ("case", po::value<std::string>(), "arg = semantic/codegen/optim")
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

    return 0;
}