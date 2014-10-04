#include "specie.h"


Specie::Specie(std::string id){
    m_id = id;
    if (m_id==std::string("a")){
        m_length=1;
    }
    else
        m_length = std::atoi(m_id.c_str());
}



bool Specie::ifCatalyst(){
//    int X = (globParams[std::string("X")]).getInt();
//    if(m_length > X)
       return true;
//    else
//        return false;
}

std::list<Reaction> Specie::reactions(Specie specie){
    std::list<Reaction> allReactions;
    return allReactions;
}

Specie::~Specie(){
    
}
