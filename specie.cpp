#include "specie.h"




Specie::Specie(int length){
    m_length = length;
}

bool Specie::ifCatalyst(){
    int X = globParam(std::string("X"));
    if(m_length > X)
        return 1;
    else
        return 0;
}


