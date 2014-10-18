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
    void buildRelationship(std::list<Population>::iterator itOther){};
    /* Checks if this Population's Specie can react with *ptrOther's and appends
     * Relationship object to its internal list of relationships. Returns
     * iterator to the Relationship object if there were some possible
     * reactions and NULL otherwise.
     */
    float computeKsi(){return 0.f;};
    float updateKsi(){return 0.f;};

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
