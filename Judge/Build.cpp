#include "Build.h"

#include <iostream>

#include <boost/process.hpp>
#include <boost/filesystem.hpp>

namespace sjtu {


void build(const std::string &path) {
    namespace bp = boost::process;
    namespace fs = boost::filesystem;
    bp::system(fs::path(path));
}


} // namespace sjtu