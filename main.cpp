#include <bits/stdc++.h>

#include <kompute/Core.hpp>
#include <memory>
#include <vector>

#include "alg.hpp"
#include <kompute/Kompute.hpp>

#include <fmt/color.h>
#include <fmt/core.h>
#include <fmt/ranges.h>
#include <kompute/Tensor.hpp>
#include <vector>

using std::string;
using std::vector;

string capitalize(const string str) {
  if (str.empty())
    return str; // Handle empty strings
  string result = str;
  result[0] = std::toupper(result[0]); // Capitalize first character
  return result;
}

fmt::text_style FMTFLAGS = fmt::emphasis::bold | fg(fmt::color::green);

void printObj(string name, vector<uint32_t> data) {
  fmt::print(FMTFLAGS, "{} {{ {} }}\n", capitalize(name),
             fmt::join(data, ", "));
}

void printObj(string name, std::shared_ptr<kp::TensorT<uint32_t>> data) {
  printObj(name, data->vector());
}

void printObj(string name, std::vector<std::vector<uint32_t>> data) {
  fmt::print(FMTFLAGS, "{} {{\n", capitalize(name));
  for (const auto &iv : data) {
    printObj("", iv);
  }
  fmt::print(FMTFLAGS, "}}\n");
}

// Macro to print a vector with the capitalized variable name
#define printo(data) printObj(#data, data);

// I'm getting bored of typing out std::shared_ptr<kp::TensorT<float>>, so:
typedef std::shared_ptr<kp::TensorT<uint32_t>> UTens;
typedef std::vector<uint32_t> uvec;

int main() { kp::Manager mgr; }
