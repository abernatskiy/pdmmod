#ifndef __REACTION_H
#define __REACTION_H

#include <string>
#include <vector>
#include <iostream>
#include <tuple>
#include <cstdlib>
#include "types.h"

#define specieRecord_t std::tuple<std::string, int>
/* A type defining a record for a specie involved into a reaction:
 * tuple containing an id string and a stoichoimetric coefficient
 */
// optimization may be possible here by using a C structure instead

class Reaction
{
public:
    // Attributes
    std::vector<specieRecord_t> m_records;
    float m_rate;
    float m_partialPropensity; // a.k.a. Pi
    std::string m_pPWRespectTo; // id of the reagent, with respect to which the partial propensity was last computed (holder of the Relation)

    // Constructor
    Reaction(std::string reactant0, int stoichiometry0, std::string reactant1, int stoichiomentry1, float rate);

    // Operator reaload
    friend std::ostream& operator<<(std::ostream& os, const Reaction& rc);

    // Methods
    void addProduct(std::string product, int stoichiometry){addSpecie(product, stoichiometry);};
    void computePartialPropensity(std::string wRespectToSp, MOLINT populationOfOtherSp); // warning - the second argument is the population of the OTHER specie, not wRespectToSp
private:
    void addSpecie(std::string specie, int stoichiometry);
};

#endif
