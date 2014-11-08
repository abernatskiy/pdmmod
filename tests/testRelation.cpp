#include <iostream>
#include "relation.h"
#include "specie.h"

int main(){
    Specie a("a");
    Specie two("2");
    Relation rel(two, a, 50);
    std::cout << "Relation of " << two << " to " << a << "(50 molecules of the latter):" << std::endl << rel << std::endl;
    Relation rel0(a, a, 50);
    std::cout << "Relation of " << a << " to " << a << "(50 molecules of the latter):" << std::endl << rel0 << std::endl;
    std::cout << "Reaction sampled with 15.f: " << rel0.sampleReaction(15.f) << std::endl;
    std::cout << "Updating population of a to be 500...\n";
    rel0.update(500);
    std::cout << "Got " << rel0 << std::endl;
    std::cout << "Reaction sampled with 60.f: " << rel0.sampleReaction(60.f) << std::endl;
    return 0;
}
