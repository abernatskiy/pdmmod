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


const float COLL_RATE = 0.0001;



class Specie
{
public:
    Specie(){};
    Specie(std::string id);
    ~Specie();
    
    //attributes
    std::string m_id;
    int m_length;
    
    //constants
    
    
    //methods
    std::list<Reaction> reactions(Specie specie);
    
    friend std::ostream& operator<<(std::ostream& os, const Specie& sp);
};

#endif // __SPECIE_H
