// reading a text file
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void pause() {
  cout << "\n\nPress any key to continue...";
  cin.get();
}



int main (int argc, char **argv) {

  cout << argv[2] << "\n";
  string line;
  ifstream gameFile(argv[2]);
  if (gameFile.is_open())
  {
    while ( getline (gameFile,line) )
    {
    //   cout << line << '\n';
    }
    gameFile.close();
  }

  else cout << "Unable to open file"; 

  pause();
  return 0;
}