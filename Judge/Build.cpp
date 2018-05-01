#include "Build.h"

#include <iostream>

#include <boost/process.hpp>
#include <boost/filesystem.hpp>

namespace sjtu {


void build(const std::string &path) {
    namespace bp = boost::process;
    std::cout << "building...\t";
    std::cout.flush();
    bp::system("bash " + path);
    std::cout << "done." << std::endl;
}


} // namespace sjtu