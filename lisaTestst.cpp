#include <string>
#include <fstream>
#include <iostream>
#include <list>
#include <sstream>

int main(){
    std::string line;
    std::cin.sync_with_stdio(false);
    std::string filename("populations.txt");
    std::cout << "Filename is " << filename << std::endl;
    std::list<std::string> names;
    std::list<int> populations;
    std::ifstream file(filename);
    
    if (file.is_open())
    {
    while (std::getline(file, line))
        {
            std::stringstream   linestream(line);
            std::string         data;
            std::string         name;
            int                 population;
            
            linestream >> name >> population;
            names.push_back(name);
            populations.push_back(population);
        }
    }
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
