#ifndef COMPILER_OJ_TESTCASE_H
#define COMPILER_OJ_TESTCASE_H

#include <fstream>
#include <string>
#include <utility>
#include <exception>

namespace sjtu {

enum class [[deprecated]] TestCasePhase {
    SemanticPretest = 0, SemanticExtended,
    CodegenPretest, CodegenExtended,
    OptimPretest, OptimExtended,
    Error
}; // enum class TestCasePhase

enum class AssertionType {
    SuccessCompile = 0, FailureCompile,
    Exitcode, RuntimeError, Output,
    Error
}; // enum class AssertionType

struct TestCase {
    std::string src;
    std::string comment;
    std::string input, output;
    AssertionType assertion = AssertionType::Error;
    std::uint64_t timeout = 0; // ms
    int exitcode = 0;
    std::string phase;

    TestCase() = default;
    TestCase(const TestCase &) = default;
    TestCase(TestCase &&) = default;
    TestCase& operator=(const TestCase &) = default;
    TestCase& operator=(TestCase &&) = default;
}; // struct TestCase


} /* namespace sjtu */

namespace sjtu {

struct InvalidTestCase : public std::exception {};

using CIter = std::string::const_iterator;

TestCase parse(std::ifstream & fin);

std::pair<CIter, CIter> findBlock(const std::string & buffer, const std::string & name);;

std::string readSource(const std::string & buffer);


} /* namespace sjtu */


#endif //COMPILER_OJ_TESTCASE_H
