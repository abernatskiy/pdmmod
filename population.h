#include <string>
#include <list>
#include "types.h"
//#include "reaction.h"
#include "specie.h"

class Population
{
//private:
public:
    MOLINT m_n;
    Specie m_specie;
//    std::list<std::list<Reaction>> reactions;

    // maybe we can get away with only one of these
    float m_lambda;
    float m_ksi;

public:
    Population(std::string id, MOLINT initPop);
//    void removeReaction(std::list<Reaction>::iterator ptrReaction);
//    void addAllReactions(Specie* ptrOtherReagent);

    friend std::ostream& operator<<(std::ostream& os, const Population& pop);
};
