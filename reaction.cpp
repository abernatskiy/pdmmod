#include "reaction.h"

Reaction::Reaction(std::string reactant0, int stoichiometry0, std::string reactant1, int stoichiomentry1, float rate){
	addSpecie(reactant0, stoichiometry0);
	addSpecie(reactant1, stoichiometry1);
	m_rate = rate;
}

void Reaction::addSpecie(std::string specie, int stoichiometry){
	m_species.push_back(specie);
	m_stoichiometries.push_back(stoichiometry);
}
