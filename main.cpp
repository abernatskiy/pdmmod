#include <fstream>
#include "totalPopulation.h"
#include "output.h"
#include <time.h>

// Those modules are for loading parameters and data used by class Specie
#include <map>
#include "nativeListLoader.h"
#include "parametersLoader.h"

/* HP-model-specific global variables */
std::map<std::string,std::string> catPatterns;
std::map<std::string,int> wellDepths;

/* General-purpose global dictionary of parameters */
std::map<std::string,Parameter> configDict;

int main (int argc, char** argv){
    if (argc != 4 ){
        std::cout << "wrong number of arguments" << std::endl;
        std::cout << "the first argument: time the simulation runs, second: how often you want to record data" << std::endl;
        std::cout << "the last argument is the filename where you want to store results" << std::endl;
        std::cout << "Total Time = 0: if you want to run simulation until it breaks down/you get tired" << std::endl;
        std::cout << "Step = 0: record every step" << std::endl;
        return 1;
    }

    /* Loading HP-model-specific data */
    catPatterns = readCatPatterns("nativeList.txt");
    // 
    wellDepths = readWellDepths("nativeList.txt");
    
    /* Loading parameters */
    readConfig(&configDict, "parameters.ini");
    showConfig(&configDict);
    
    int reacNum= 0;
    clock_t t1,t2;

    int stp;
    //total time of simulation
    float totalTime = std::atoi((std::string(argv[1])).c_str());
    //how often to record
    float stepLen = std::atoi((std::string(argv[2])).c_str());
    std::string filename = std::string(argv[3]);
    //reading initial conditions frmo file
    TotalPopulation tp("populations.txt");

    //std::cout << "before stepping:\n"<< tp;
    std::string prevPops = storePopulations(&tp);
    float prevStep = 0.f;
    std::ofstream myfile;
    myfile.open (filename);
    writeToFile(prevPops, 0.0, &myfile);
    t1=clock();
    while(true){
        if (totalTime == 0.f)
        {
            //TODO
        }
        else{
            stp = tp.stepSimulation();
            reacNum=reacNum+1;
            //std::cout << "after stepping:\n" << tp;
            prevPops = writeOrNotTo(stepLen, &tp, prevStep, prevPops, &myfile);
            prevStep = getPrevStep(stepLen, prevStep, tp.m_t);
            if (tp.m_t >= totalTime){
                myfile.close();
                break;
            }
            if (stp==1){
                break;
            }
        }
    }
    t2=clock();
    std::cout << "status is " << stp << std::endl;
    if (tp.m_t < totalTime && stp == 1){
        std::cout <<"simulations is over. prevStep is " << prevStep << std::endl;
        for (float time=(prevStep+stepLen);time<=totalTime;time=time+stepLen){
            writeToFile(prevPops,time,&myfile);
         }

        myfile.close();
    }

    float diff = ((float)t2-(float)t1);
    float timePerReac = diff/CLOCKS_PER_SEC/reacNum;
    std::cout << "Number of reactions is " << reacNum << std::endl;
    std::ofstream timeFile;
    timeFile.open ("runtime.txt");
    timeFile << timePerReac << std:: endl;
    timeFile.close();
    std::cout << "total time is " << tp.m_t << std::endl;

    return 0;
}
