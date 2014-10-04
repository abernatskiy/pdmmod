#include <string>
#include "specie.h"



Specie::Specie(std::string id){
    m_id = id;
    /*if m_id==std::string("a"){
        m_length=1;
    }
    else:
        m_length = std::atoi(m_id.c_str());*/
}

/*std::string Specie::str(){
    return std::string("Specie ")+m_id+std::string(" with length ")+std::to_string(length);
}*/

bool Specie::ifCatalyst(){
    int X = globParams(std::string("X"));
    if(m_length > X)
        return true;
    else
        return false;
}

Reaction Specie::reactions(Specie specie){
    if (if)
}

Specie::~Specie(){
    
}
