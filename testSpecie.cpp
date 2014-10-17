#include "specie.h"
#include <stdio.h>
#include <iostream>

int main(int argc, char** argv){
    Specie a("a");
    Specie two("2");
    std::cout << a << "\n";
    std::list<Reaction> rs = a.reactions(two);
    (*rs.begin()).getReactants();
}