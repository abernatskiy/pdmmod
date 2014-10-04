#include <string>
#include <vector>

class Specie
{
private:
	std::vector<std::string> m_species;
	std::vector<int> m_stoichiometries;
	float m_rate;
	void addSpecie(std::string specie, int stoichiometry);

public:
	Species(std::string reactant0, int stoichiometry0, std::string reactant1, int stoichiomentry1, float rate);
	void addProduct(std::string product, int stoichiometry){addSpecie(product, stoichiometry);};
};
