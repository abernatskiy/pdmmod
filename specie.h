#include <vector>
#include <map>
#include <string>
#include "parameter.h"

std::map<std::string,Parameter> globParams;

class Specie
{
public:
    Specie(std::string id);
    ~Specie();
    std::string m_id;
    int m_length;
    
    std::string str();
    bool m_ifCatalyst;
    bool ifCatalyst();
};