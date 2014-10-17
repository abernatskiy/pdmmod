#include <string>
#include <fstream>
#include <iostream>
#include <list>

int main(){
    std::string name;
    int population;
    std::cin.sync_with_stdio(false);
    std::string filename("populations.txt");
    std::cout << "Filename is " << filename << std::endl;
    std::ifstream infile;
    std::list<std::string> names;
    std::list<int> populations;
    infile.open(filename);
    while (infile.peek()!=EOF)
    {
    infile >> name; 
    names.push_back(name);
    infile >> population;
    populations.push_back(population);
    }
    infile.close();
    
    std::list<int>::iterator pop_it=populations.begin();
    std::list<std::string>::iterator names_it=names.begin();
    std::cout << "names and populations:\n";
    for (names_it = names.begin(); names_it != names.end(); names_it++)
        std::cout << " " << *names_it;
    std::cout << std::endl;
    for (pop_it = populations.begin(); pop_it != populations.end(); pop_it++)
        std::cout << " " << *pop_it;
    std::cout << std::endl;
    
}
