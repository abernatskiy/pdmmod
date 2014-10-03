#include <string>

class Parameter
{
public:
    Parameter();
    ~Parameter();
    Parameter(bool value);
    Parameter(int value);
    Parameter(float value);
    short m_type;
    void* m_value;
    //TODO from .cpp
};