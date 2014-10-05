#include <string>
#include <vector>
#include <iostream>
class Reaction
{
private:
	std::vector<std::string> m_species;
	std::vector<int> m_stoichiometries;
	float m_rate;
	void addSpecie(std::string specie, int stoichiometry);
    

public:
	Reaction(std::string reactant0, int stoichiometry0, std::string reactant1, int stoichiomentry1, float rate);
    
    friend std::ostream& operator<<(std::ostream& os, const Reaction& rc);
    std::vector<std::string> getReactants(std::vector<std::string> *reacts, std::vector<std::string> * prodts);
    void addProduct(std::string product, int stoichiometry){addSpecie(product, stoichiometry);};
    void getReactants();
};
