#ifndef __SPECIE_H
#define __SPECIE_H

#include <vector>
#include <string>
#include <list>
#include "parameter.h"
#include "reaction.h"

/*binary polymers
 * sequences grow on its own and never decay
 */




class Specie
{
public:
    Specie(){};
    Specie(std::string id);
    ~Specie();
    
    //attributes
    std::string m_id;
    std::string m_catalyst;
    std::string m_substrate;
    bool m_product;
    int m_length;
    bool m_folded;
    int m_native;
    
    //constants
    
    
    //methods
    std::list<Reaction> reactions(Specie specie);
    
    friend std::ostream& operator<<(std::ostream& os, const Specie& sp);
};

#endif // __SPECIE_H
