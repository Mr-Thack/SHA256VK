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

using std::shared_ptr;
using std::string;
using std::vector;

// I'm getting bored of typing out std::shared_ptr<kp::TensorT<float>>, so:
typedef shared_ptr<kp::TensorT<uint32_t>> UTens;
typedef vector<uint32_t> uvec;

fmt::text_style FMTFLAGS = fmt::emphasis::bold | fg(fmt::color::green);

void insert(uvec &res, const uvec &v) {
  res.insert(res.end(), v.begin(), v.end());
}

string chain_to_hex(const vector<uint32_t> &words) {
  std::stringstream ss;
  ss << std::hex << std::setfill('0');
  for (uint32_t word : words) {
    ss << std::setw(8) << word;
  }
  return ss.str();
}

int main() {
  kp::Manager mgr;

  string input_text = "Hello!";

  uvec chain(8);
  uvec block(16);
  uint32_t offset = 0;
  uint32_t length = input_text.size() * 8;
  uvec input_data(input_text.begin(), input_text.end());

  uvec data;
  data.reserve(8 + 16 + 1 + 1 + input_data.size());

  insert(data, chain);
  insert(data, block);
  data.push_back(offset);
  data.push_back(length);
  insert(data, input_data);

  UTens datat = mgr.tensorT(data);

  const vector<shared_ptr<kp::Memory>> params = {datat};

  const vector<uint32_t> shader = vector<uint32_t>(shader::ALG_COMP_SPV.begin(),
                                                   shader::ALG_COMP_SPV.end());

  kp::Workgroup workgroup({1, 1, 1});
  shared_ptr<kp::Algorithm> algo = mgr.algorithm(params, shader, workgroup);
  mgr.sequence()
      ->record<kp::OpSyncDevice>(params)
      ->record<kp::OpAlgoDispatch>(algo)
      ->record<kp::OpSyncLocal>(params)
      ->eval();

  uvec data_result = datat->vector();
  uvec rchain(data_result.begin(), data_result.begin() + 8);
  for (auto &it : rchain) {
    fmt::print("{} ", it);
  }
  fmt::print("\n");
  fmt::print(FMTFLAGS, chain_to_hex(rchain));
  return 0;
}
