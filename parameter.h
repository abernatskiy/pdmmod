#ifndef __PARAMETER_H
#define __PARAMETER_H

#include <string>

//do not call with Constants
class Parameter
{
public:
    Parameter();
    ~Parameter();
    std::string getType();
    //bool
    Parameter(bool value);
    bool getBool();
    //int
    Parameter(int value);
    int getInt();
    //float
    Parameter(float value);
    float getFloat();
    //variables
    short m_type;
    void* m_valuePtr;
    //TODO from .cpp
    std::string getString();
private:
    template<typename T>
    Parameter(T value);
};

#endif // __PARAMETER_H
