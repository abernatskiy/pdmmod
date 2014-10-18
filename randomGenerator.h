#include <random>
#include <time.h>
#include <string>

class RandomGenerator
{
private:
    unsigned int m_seed;
    std::mt19937 m_generator;
    std::uniform_real_distribution<float> m_distribution;

public:
    RandomGenerator();

    float getFloat01(){return m_distribution(m_generator);};
    void seedWithUInt(unsigned int seed){m_seed = seed; m_generator.seed();};
    void seedWithString(std::string str);
    void seedWithClock();
    unsigned int getSeed(){return m_seed;};
};
