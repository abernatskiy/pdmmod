#ifndef __SPECIE_H
#define __SPECIE_H

#include <vector>
#include <string>
#include <list>
#include "parameter.h"
#include "reaction.h"

class Specie
{
public:
    Specie(){};
    Specie(std::string id);
    ~Specie();
    std::string m_id;
    int m_length;
    bool m_ifCatalyst;

    std::string str();
    bool ifCatalyst();
    std::list<Reaction> reactions(Specie specie);
    friend std::ostream& operator<<(std::ostream& os, const Specie& sp);
};

#endif // __SPECIE_H
