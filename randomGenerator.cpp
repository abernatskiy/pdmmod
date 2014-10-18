#include "randomGenerator.h"

RandomGenerator::RandomGenerator(){
    seedWithClock();
    m_distribution = std::uniform_real_distribution<float>(0.f, 1.f);
}

void RandomGenerator::seedWithString(std::string str){
    // takes a string, treats it as an array of integers (one per symbol)
    // and creates a seed out of the result
    std::seed_seq seedGen(str.begin(),str.end());
    std::vector<unsigned int> seeds(1);
    seedGen.generate(seeds.begin(), seeds.end());
    m_seed = seeds[0];
    seedWithUInt(m_seed);
}

void RandomGenerator::seedWithClock(){
    m_seed = time(NULL);
    seedWithUInt(m_seed);
}
