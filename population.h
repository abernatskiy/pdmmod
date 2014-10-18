#include <string>
#include <list>
#include "types.h"
//#include "reaction.h"
#include "specie.h"

class Population
{
public:
    // Constructors
    Population(std::string id, MOLINT initPop);

    // Methods
//    void removeReaction(std::list<Reaction>::iterator ptrReaction);
//    void addAllReactions(Specie* ptrOtherReagent);

    // Operator overloads
    friend std::ostream& operator<<(std::ostream& os, const Population& pop);

private:
//public:
    // Attributes
    MOLINT m_n;
    Specie m_specie;
    // std::list<std::list<Reaction>> reactions;
    float m_lambda;
    float m_ksi;
};
