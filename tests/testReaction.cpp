#include <string>
#include <iostream>
#include "reaction.h"

int main(){
    // Test for heteromolecular reaction
    Reaction reac("a", 1, "12", 1, 10.f);
    std::cout << "Made a reaction: " << reac << std::endl;
    reac.addProduct("13", 1);
    std::cout << "After product addition: " << reac << std::endl;
    reac.computePartialPropensity("a", 100);
    std::cout << "After Pi computation w/r to a (given 100 mols of 12): " << reac << std::endl;
    reac.computePartialPropensity("12", 50);
    std::cout << "After Pi computation w/r to 12 (given 50 mols of a): " << reac << std::endl;
    std::cout << std::endl;

    // Test for the "reagent not found" error message
//    std::cout << "Trying to compute Pi with respect to 20...\n";
//    reac.computePartialPropensity("20", 25);

    // Test for homomolecular, bimolecular reaction
    Reaction hreac("1", 1, "1", 1, 20.f);
    std::cout << "Homomolecular reaction 1: " << hreac << std::endl;
    hreac.computePartialPropensity("1", 100);
    std::cout << "Reaction 1 after partial propensity computation: " << hreac << std::endl;
    std::cout << std::endl;

    // Test for homomolecular, unimolecular reaction
    hreac = Reaction("1", 1, "1", 0, 20.f);
    std::cout << "Homomolecular reaction 2: " << hreac << std::endl;
    hreac.computePartialPropensity("1", 100);
    std::cout << "Reaction 2 after partial propensity computation: " << hreac << std::endl;
    std::cout << std::endl;

    // Test for improper conventions
    Reaction ireac = Reaction("134", 2, "134", 0, 20.f);
    std::cout << "Improper convention reaction 1: " << ireac << std::endl;
    std::cout << "Trying to compute Pi with respect to 134...\n";
    ireac.computePartialPropensity("134", 25);

    return 0;
}
