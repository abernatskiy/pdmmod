#include "reaction.h"

Reaction::Reaction(std::string reactant0, int stoichiometry0, std::string reactant1, int stoichiometry1, float rate){
	addSpecie(reactant0, -1*stoichiometry0);
	addSpecie(reactant1, -1*stoichiometry1);
	m_rate = rate;
}

//Overloading <<
std::ostream& operator<<(std::ostream& os, const Reaction& rc)
{
    os <<  "Reaction: ";
    return os;
}

void Reaction::addSpecie(std::string specie, int stoichiometry){
	m_species.push_back(specie);
	m_stoichiometries.push_back(stoichiometry);
}

void Reaction::getReactants(){
    std::vector<std::string>::iterator it = m_species.begin();
        std::cout << *it;
    }
    

