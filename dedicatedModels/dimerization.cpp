/*** Homoreaction.sbml ***/

/*** Compile with g++ -O2 -std=c++11 -o dimerization dimerization.cpp ***/

#include <iostream>
#include <random>
#include <cmath>
#include <vector>
#include <fstream>
#include <sstream>
#include <cstdlib>

typedef double REAL;
typedef double REALTIME;

const REAL rates[] = {10., 0.2}; // rates[0] for \varnothing->A, rates[1] for 2A->\varnothing
const unsigned initialPopulation = 5;
const REALTIME terminationTime = 10.;
const unsigned numWalks = 10000;

using namespace std;

unsigned performWalk(unsigned randomSeed)
{
	// Setting up the random number generator
	mt19937 gen;
	gen.seed(randomSeed);
	uniform_real_distribution<REAL> dist(0., 1.);

	// Setting up the initial conditions of Gillespie's Direct Method
	unsigned n = initialPopulation;
	REAL propensities[] = {rates[0], rates[1]*n*(n-1)};
	REAL totalPropensity = propensities[0] + propensities[1];
	REALTIME t = 0.;

	// Simulation loop
	while(true)
	{
		// Advancing the simulation time
		t += (1./totalPropensity)*log(1./dist(gen));
		if(t > terminationTime)
			break;

		// Sampling the reaction, updating the population of A and propensities
		REAL juice = (propensities[0]+propensities[1])*dist(gen);
		if(juice < propensities[0])
			n++; // Production reaction happens: \varnothing->A
		else
			n -= 2; // Dimerization + precipitation reaction happens: 2A->\varnothing
		propensities[1] = rates[1]*n*(n-1);
		totalPropensity = propensities[0] + propensities[1];

		// cout << propensities[0] << ' ' << propensities[1] << endl;
		// cout << t << ' ' << n << endl;
	}
	return n;
}

vector<unsigned> readSeeds()
{
	ostringstream ss;
	ss << "seeds" << numWalks;

	ifstream seedFile(ss.str());
	if(seedFile.is_open())
	{
		vector<unsigned> seeds;
		string seedStr;
		while(getline(seedFile, seedStr))
			seeds.push_back(stoul(seedStr));
		seedFile.close();
		return seeds;
	}
	else
	{
		cout << "Cannot read file " << ss.str() << endl;
		exit(EXIT_FAILURE);
	}
}

int main(int argc, char** argv)
{
	vector<unsigned> seeds = readSeeds();
	for(auto it=seeds.begin(); it!=seeds.end(); it++)
		cout << performWalk(*it) << endl;
	return 0;
}
