#ifndef __SPECIE_H
#define __SPECIE_H

#include <vector>
#include <string>
#include <list>
#include "parameter.h"
#include "reaction.h"

const float GROWTH_RATE = 0.1;
const float SLOWHIDR_RATE = 0.00001;
const float HIDR_RATE = 0.003;
const float DEL_RATE = 0.03;


class Specie
{
public:
    std::string modelName;
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
