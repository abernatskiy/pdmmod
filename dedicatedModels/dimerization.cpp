/*** Homoreaction.sbml ***/

/*** Compile with g++ -O2 -std=c++11 -o dimerization dimerization.cpp ***/

#include <iostream>
#include <random>
#include <cmath>

typedef double REAL;
typedef double REALTIME;

const REAL rates[] = {10., 0.2}; // rates[0] for \varnothing->A, rates[1] for 2A->\varnothing
const unsigned initialPopulation = 5;
const REALTIME terminationTime = 10.;
const unsigned numWalks = 100000;

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

int main(int argc, char** argv)
{
	REAL sum = 0.;
	for(int i=0; i<numWalks; i++)
		sum += performWalk(900000+i);
	cout << sum/REAL(numWalks) << endl;
	return 0;
}
