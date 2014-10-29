#include "totalPopulation.h"
#include "output.h"

int main (int argc, char** argv){
    if (argc != 4 ){
        std::cout << "wrong number of arguments" << std::endl;
        std::cout << "the first argument: time the simulation runs, second: how often you want to record data" << std::endl;
        std::cout << "the last argument is the filename where you want to store results" << std::endl;
        std::cout << "Total Time = 0: if you want to run simulation until it breaks down/you get tired" << std::endl;
        std::cout << "Step = 0: record every step" << std::endl;
    }
    else{
        int stp;
        //total time of simulation
        float totalTime = std::atoi((std::string(argv[1])).c_str());
        //how often to record
        float stepLen = std::atoi((std::string(argv[2])).c_str());
        std::string filename = std::string(argv[3]);
        //reading initial conditions frmo file
        TotalPopulation tp("populations.txt");
        
        std::cout << "before stepping:\n"<< tp;
        std::string currPops = storePopulations(tp);
        float prevStep = 0.f;
        openFile(filename);
        writeToFile(currPops, filename);
        
        while(true){
            if (totalTime == 0.f)
            {
                //TODO
            }
            else{
                stp = tp.stepSimulation();
                std::cout << "after stepping:\n" << tp;
                prevPops = writeOrNotTo(stepLen, tp.m_t, prevStep, prevPops, filename);
                prevStep = getPrevStep(prevStep, tp.m_t);
                if (tp.m_t >= totalTime){
                    closeFile(filename);
                    break;
                }
            }
            
        }
        if (tp.m_t < totalTime && stp == 1){
            currPops = storePopulations(tp);
            writeOrNotTo(stepLen, totalTime, prevStep, currPops, filename);
            closeFile(filename);
        }
        
    }
    return 0;
}
