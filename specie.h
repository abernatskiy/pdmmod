#include <vector>
#include <map>
#include parameter.h

std::map<std::string,Parameter> globParams;

class Specie
{
public:
    Specie();
    ~Specie();
    int m_length;
    bool ifCatalyst;
    bool ifCatalyst();
    
};