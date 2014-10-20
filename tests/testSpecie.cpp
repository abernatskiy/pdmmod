#include "specie.h"
#include "parameter.h"
#include <stdio.h>
#include <iostream>

int main(int argc, char** argv){

//    extern std::map<std::string,Parameter> globParams;
//    globParams["a"] = Parameter(1.f);
//    globParams["d"] = Parameter(0.1f);

    Specie a("a");
    Specie two("2");
    std::cout << a << "\n";
    std::cout << two << "\n";
    std::cout << "Reactions:\n";
    std::list<Reaction> rs = a.reactions(two);
    for( auto itRea = rs.begin(); itRea != rs.end(); itRea++ )
        std::cout << "    " << (*itRea) << std::endl;
}
