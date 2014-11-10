#ifndef __SPECIE_H
#define __SPECIE_H

#include <vector>
#include <string>
#include <list>
#include "parameter.h"
#include "reaction.h"

const float IMP0 = 2.f;
const float IMP1 = 2.f;
const float DECAY_RATE = 1.f;
const float DEGR_RATE = 0.f;
const float GROWTH_RATE = 0.1;
const float FAST_RATE = 0.1;


class Specie
{
public:
    Specie(){};
    Specie(std::string id);
    ~Specie();
    
    //attributes
    std::string m_id;
    int m_length;
    std::string m_type;
    
    //constants
    
    
    //methods
    std::list<Reaction> reactions(Specie specie);
    
    friend std::ostream& operator<<(std::ostream& os, const Specie& sp);
};

#endif // __SPECIE_H
