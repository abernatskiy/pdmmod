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
private:
    template<typename T>
    Parameter(T value);
};