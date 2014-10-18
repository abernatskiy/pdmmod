#include "population.h"

Population::Population(std::string id, MOLINT initPop){
    m_specie = Specie(id);
    m_n = initPop;
}

std::ostream& operator<<(std::ostream& os, const Population& pop){
    os << "Population of specie " << pop.m_specie << " with " << pop.m_n << " molecules in it";
    return os;
}
