#include <algorithm>
#include <string>
#include <iostream>
#include <iomanip>


char to_uppercase(unsigned char c)
{
  return std::toupper(c);
}


int main() {
  std::string hello("hello");
  std::transform(hello.cbegin(), hello.cend(), hello.begin(), to_uppercase);
  std::cout << "hello = " << std::quoted(hello) << "\n";
  return 0;
}
