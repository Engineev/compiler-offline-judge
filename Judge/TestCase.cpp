#include "TestCase.h"

#include <fstream>
#include <iostream>
#include <sstream>
#include <ios>
#include <regex>


namespace sjtu {

TestCase parse(const std::string &dir) {
    std::ifstream fin(dir);
    if (!fin.is_open())
        throw std::ifstream::failure(std::string("file does not exists"));
    std::string buffer(static_cast<std::stringstream const &>(std::stringstream() << fin.rdbuf()).str());

    TestCase result;
    result.src = readSource(buffer);

    CIter beg, end;

    std::tie(beg, end) = findBlock(buffer, "comment");
    result.comment = std::string(beg, end);

    std::tie(beg, end) = findBlock(buffer, "input");
    result.input = std::string(beg, end);

    std::tie(beg, end) = findBlock(buffer, "output");
    result.output = std::string(beg, end);

    std::tie(beg, end) = findBlock(buffer, "assert");
    if (beg != end) {
        std::string rawAssertion(beg, end);
        if (rawAssertion == "success_compile")
            result.assertion = AssertionType::SuccessCompile;
        else if (rawAssertion == "failure_compile")
            result.assertion = AssertionType::FailureCompile;
        else if (rawAssertion == "exitcode")
            result.assertion = AssertionType::Exitcode;
        else if (rawAssertion == "runtime_error")
            result.assertion = AssertionType::RuntimeError;
        else if (rawAssertion == "output")
            result.assertion = AssertionType::Output;
        else
            throw InvalidTestCase();
    }

    std::tie(beg, end) = findBlock(buffer, "timeout");
    if (beg != end) {
        std::string rawTimeout(beg, end);
        auto dTimeout = std::stod(rawTimeout, nullptr);
        result.timeout = (std::uint64_t) (dTimeout * 1000);
    }
    
    std::tie(beg, end) = findBlock(buffer, "exitcode");
    if (beg != end) {
        std::string rawExitcode(beg, end);
        result.exitcode = std::stoi(rawExitcode, nullptr);
    }

    std::tie(beg, end) = findBlock(buffer, "phase");
    std::string rawPhase(beg, end);
    if (rawPhase == "semantic pretest")
        result.phase = TestCasePhase::SemanticPretest;
    else if (rawPhase == "semantic extended")
        result.phase = TestCasePhase::SemanticExtended;
    else if (rawPhase == "codegen pretest")
        result.phase = TestCasePhase::CodegenPretest;
    else if (rawPhase == "codegen extended")
        result.phase = TestCasePhase::CodegenExtended;
    else if (rawPhase == "optim pretest")
        result.phase = TestCasePhase::OptimPretest;
    else if (rawPhase == "optim extended")
        result.phase = TestCasePhase::OptimExtended;
    else
        throw InvalidTestCase();

    return result;
}

std::string readSource(const std::string &buffer) {
    std::smatch m;
    if (!std::regex_search(buffer, m, std::regex("/\\*!! metadata:")))
        throw InvalidTestCase();
    return {buffer.begin(), m[0].first};
}

std::pair<CIter, CIter> findBlock(const std::string &buffer, const std::string &name) {
    std::smatch m;
    if (!std::regex_search(buffer, m,
                           std::regex("=== " + name + " ===\n(.|\n)*?===")))
        return {buffer.end(), buffer.end()};
    auto beg = m[0].first;
    auto end = m[0].second;

    std::string tmp(beg, end);
    std::cout << tmp << std::endl;

    while (*beg != '\n')
        ++beg;
    ++beg;
    while (*end != '\n')
        --end;
    return {beg, end};
}


} // namespace sjtu