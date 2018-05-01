#include "Test.h"

#include <cassert>
#include <string>

#include <boost/process.hpp>

namespace sjtu {


std::pair<bool, std::string> test(const TestCase &testCase, const std::string &bashDir) {
    auto getBashPath = [&] () -> std::string {
        auto iter = testCase.phase.begin();
        while (*iter != ' ')
            ++iter;
        return bashDir + std::string(testCase.phase.begin(), iter) + ".bash";
    };
    auto path = getBashPath();

    if (testCase.phase == "semantic pretest" || testCase.phase == "semantic extended")
        return testCompile(testCase, path);
    assert(false);
    if (testCase.phase == "codegen pretest" || testCase.phase == "codegen extended")
        return testCodegen(testCase, path);

}


std::pair<bool, std::string> testCompile(const TestCase &testCase, const std::string & path) {
    namespace bp = boost::process;

    std::error_code ec;
    bp::ipstream is;
    bp::system(path, ec, bp::std_out > is);

    if (testCase.assertion == AssertionType::SuccessCompile && (bool)ec)
        return {false, ec.message()};
    if (testCase.assertion == AssertionType::FailureCompile && !(bool)ec)
        return {false, "The build should failed."};
    return {true, ""};
}

std::pair<bool, std::string> testCodegen(const TestCase &testCase, const std::string &path) {
    std::error_code ec;
    boost::process::system(path, ec);

    return {true, ""};
}

bool resultAssert(const TestCase &testCase, const CompileResult &result) {
    if (testCase.assertion == AssertionType::SuccessCompile && (bool)result.ec)
        return false;
    if (testCase.assertion == AssertionType::FailureCompile && !(bool)result.ec)
        return false;
    if ((bool)result.ec)
        return false;


    return false;
}

} // namespace sjtu