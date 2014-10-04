#include <vector>
#include <string>
#include <list>
#include "parameter.h"
#include "reaction.h"

class Specie
{
public:
    Specie(std::string id);
    ~Specie();
    std::string m_id;
    int m_length;
    bool m_ifCatalyst;

    std::string str();
    bool ifCatalyst();
    std::list<Reaction> reactions(Specie specie);
};
