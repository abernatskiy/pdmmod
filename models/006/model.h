#ifndef __SPECIE_H
#define __SPECIE_H

#include <vector>
#include <string>
#include <list>
#include "parameter.h"
#include "reaction.h"




const float COLL_RATE = 0.5;

class Specie
{
public:
    std::string modelName;
    Specie(){};
    Specie(std::string id);
    ~Specie();
    
    //attributes
    std::string m_id;
    
    
    //constants
    
    
    //methods
    std::list<Reaction> reactions(Specie specie);
    
    friend std::ostream& operator<<(std::ostream& os, const Specie& sp);
};

#endif // __SPECIE_H
