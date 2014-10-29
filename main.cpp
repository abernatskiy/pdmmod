#include "totalPopulation.h"
#include "output.h"

int main (int argc, char** argv){
    if (argc != 3 ){
        std::cout << "wrong number of arguments" << std::endl;
        std::cout << "the first argument: time the simulation runs, second: how often you want to record data" << std::endl;
        std::cout << "Total Time = 0: if you want to run simulation until it breaks down/you get tired" << std::endl;
        std::cout << "Step = 0: record every step" << std::endl;
    }
    else{        
        //total time of simulation
        float totalTime = std::atoi((std::string(argv[1])).c_str());
        //how often to record
        float stepLen = std::atoi((std::string(argv[2])).c_str());
        //reading initial conditions frmo file
        TotalPopulation tp("populations.txt");
        
        std::cout << "before stepping:\n"<< tp;
        std::list<Population> currentPops = storePopulations(tp);
        float prevStep = 0.f;
        writeToFile(currentPops, filename);
        
        while(true){
            if (totalTime != 0.f)
            {
                //TODO
            }
            else{
                tp.stepSimulation();
                writeOrNotTo(stepLen, tp.m_t, prevStep, filename);
                std::cout << "after stepping:\n" << tp;
                if (tp.m_t>= totalTime){
                    break;
                }
            }
            
        }
    }
    return 0;
}
