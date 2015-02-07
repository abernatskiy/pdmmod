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

void printUsage(){
//    std::cout << "wrong number of arguments" << std::endl;
//    std::cout << "the first argument: time the simulation runs, second: how often you want to record data" << std::endl;
//    std::cout << "the last argument is the filename where you want to store results" << std::endl;
//    std::cout << "Total Time = 0: if you want to run simulation until it breaks down/you get tired" << std::endl;
//    std::cout << "Step = 0: record every step" << std::endl;
    std::cout << "Usage:" << std::endl;
    std::cout << "  pdmmod simulateTime <totalTime> <timeBetweenRecords> <outputFileName>" << std::endl;
    std::cout << "  pdmmod simulateReactions <numberOfReactions> <outputFileName>" << std::endl;
    std::cout << "totalTime=0 causes the program to run the simulation until it runs out of possible reactions or indefinitely" << std::endl;
    std::cout << "timeBetweenRecords=0 causes the program to record the population after every reaction" << std::endl;
}

int main (int argc, char** argv){

    /* Loading HP-model-specific data */
    catPatterns = readCatPatterns("nativeList.txt");
    wellDepths = readWellDepths("nativeList.txt");

    /* Loading parameters */
    readConfig(&configDict, "parameters.ini");
    showConfig(&configDict);

    int reacNum = 0;
    clock_t t1,t2;
    int stp;

    int simType = -1;
    float totalTime = 0.0;
    float stepLen = 0.0;
    int totalReactions = 0;
    std::string filename;
    if (argc == 5 && std::string(argv[1]).compare("simulateTime") == 0){
        simType = 0;
        //total time of simulation
        totalTime = std::atof(argv[2]);
        //how often to record
        stepLen = std::atof(argv[3]);
        filename = std::string(argv[4]);
    }
    else if (argc == 4 && std::string(argv[1]).compare("simulateReactions") == 0){
        simType = 1;
        //total number of reactions
        totalReactions = std::atoi(argv[2]);
        filename = std::string(argv[3]);
    }
    else {
        std::cout << "Unrecognized arguments" << std::endl;
        printUsage();
        return 1;
    }

    //reading initial conditions frmo file
    std::cout << " before beginning" << std::endl;
    TotalPopulation tp("populations.txt");

    //std::cout << "before stepping:\n"<< tp;
    std::cout << "beginning" << std::endl;
    std::string prevPops = storePopulations(&tp);
    float prevStep = 0.f;
    std::ofstream myfile;
    myfile.open (filename);
    writeHeaderToFile(&tp, argc, argv, &myfile);
    writeToFile(prevPops, 0.0, &myfile);
    t1=clock();
    while(true){
        if (simType == 0){
            if (totalTime == 0.f)
            {
                //TODO
            }
            else{
                stp = tp.stepSimulation();
                reacNum = reacNum+1;
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
        else if (simType == 1){
            reacNum = reacNum + 1;
            stp = tp.stepSimulation();
            writeToFile(storePopulations(&tp), tp.m_t, &myfile);

            if (stp == 1 || reacNum >= totalReactions){
                myfile.close();
                break;
            }
        }
    }
    t2=clock();
    std::cout << "status is " << stp << std::endl;
    if (simType == 0 && tp.m_t < totalTime && stp == 1){
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
