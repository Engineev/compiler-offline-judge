#ifndef COMPILER_OJ_TEST_H
#define COMPILER_OJ_TEST_H

#include <string>
#include <utility>
#include <system_error>

#include "TestCase.h"

namespace sjtu {

std::pair<bool, std::string> test(const TestCase & testCase, const std::string &bashDir);

struct CompileResult {
    std::error_code ec;
    int exitcode;
    std::string asmCode;

    CompileResult() = default;
    CompileResult(const CompileResult &) = default;
    CompileResult(CompileResult &&) = default;
    CompileResult &operator=(const CompileResult &) = default;
    CompileResult &operator=(CompileResult &&) = default;
};

bool resultAssert(const TestCase & testCase, const CompileResult & result);

std::pair<bool, std::string> testCompile(const TestCase & testCase, const std::string & path);

std::pair<bool, std::string> testCodegen(const TestCase & testCase, const std::string & path);

} // namespace sjtu

#endif //COMPILER_OJ_TEST_H
