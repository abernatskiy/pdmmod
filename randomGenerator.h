#ifndef __RANDOM_GENERATOR_H
#define __RANDOM_GENERATOR_H

#include <random>
#include <time.h>
#include <string>

/* Class which generates random numbers and
 * keeps within itself info about generator state
 * and random seed.
 */

class RandomGenerator
{
private:
    // Attributes
    unsigned int m_seed;
    std::mt19937 m_generator;
    std::uniform_real_distribution<float> m_distribution;

public:
    // Constructor
    RandomGenerator();

    // Methods
    float getFloat01(){return m_distribution(m_generator);}; // this function returns random float from [0,1)
    void seedWithUInt(unsigned int seed){m_seed = seed; m_generator.seed(seed);};
    void seedWithString(std::string str);
    void seedWithClock(); // used in the default constructor
    /* The seed may be defined in three different ways - by specifying it directly as an unsigned int,
     * by generating it from string or by using the universal time on from the system clock (no. of seconds
     * since 1970). All these numbers get converted into unsigned int, so if you want to save the seed, save
     * that value (available from getseed() defined below).
     */
    unsigned int getSeed(){return m_seed;};
};

#endif // __RANDOM_GENERATOR_H
