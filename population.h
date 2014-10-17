#include <string>
#include <list>
#include "reaction.h"
#include "specie.h"

class Population
{
private:
    int n;
    Specie specie;
    std::list<std::list<Reaction>> reactions;

    // maybe we can get away with only one of these
    float lambda;
    float ksi;

public:
    Population(std::string id, int initPop);
    ~Population();
    void removeReaction(std::list<Reaction>::iterator ptrReaction);
    void addAllReactions(Specie* ptrOtherReagent);

};
