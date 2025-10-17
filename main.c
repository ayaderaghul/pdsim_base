#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define GRID_SIZE 10
#define POP_SIZE (GRID_SIZE*GRID_SIZE)
#define ROUNDS 100
#define CYCLE 10000
#define MUTATION_RATE 0.05f

#define CC 3
#define CD 0
#define DC 4
#define DD 1

typedef enum { OUTCOME_CC, OUTCOME_CD, OUTCOME_DC, OUTCOME_DD } Outcome;

typedef struct {
    float p_after_CC;
    float p_after_CD;
    float p_after_DC;
    float p_after_DD;
    float accumAvgPayoff;
    int roundsPlayed;
    Outcome lastRound;
} Agent;

void printAgent(const Agent *a) {
    const char *lastRoundStr;
    switch(a->lastRound) {
        case OUTCOME_CC: lastRoundStr = "CC"; break;
        case OUTCOME_CD: lastRoundStr = "CD"; break;
        case OUTCOME_DC: lastRoundStr = "DC"; break;
        case OUTCOME_DD: lastRoundStr = "DD"; break;
        default: lastRoundStr = "??"; break;
    }

    printf("Agent { p_after_CC=%.2f, p_after_CD=%.2f, p_after_DC=%.2f, p_after_DD=%.2f, "
           "accumAvgPayoff=%.2f, roundsPlayed=%d, lastRound=%s }\n",
           a->p_after_CC, a->p_after_CD, a->p_after_DC, a->p_after_DD,
           a->accumAvgPayoff, a->roundsPlayed, lastRoundStr);
}

static float randFloat() { return (float)rand() / (float)RAND_MAX; }

static void shuffleArray(Agent *array, int n) {
    for(int i=n-1;i>0;i--) {
        int j = rand()% (i+1);
        Agent tmp=array[i]; array[i]=array[j]; array[j]=tmp;
    }
}

Agent makeRandomAgent() {
    Agent a;
    a.p_after_CC=randFloat();
    a.p_after_CD=randFloat();
    a.p_after_DC=randFloat();
    a.p_after_DD=randFloat();
    a.accumAvgPayoff=0.0f;
    a.roundsPlayed=0;
    a.lastRound=OUTCOME_DD;
    return a;
}

void playOneRound(Agent *a, Agent *b) {
    float pa, pb;
    switch(a->lastRound){case OUTCOME_CC:pa=a->p_after_CC;break;
                          case OUTCOME_CD:pa=a->p_after_CD;break;
                          case OUTCOME_DC:pa=a->p_after_DC;break;
                          case OUTCOME_DD:pa=a->p_after_DD;break;}
    switch(b->lastRound){case OUTCOME_CC:pb=b->p_after_CC;break;
                          case OUTCOME_CD:pb=b->p_after_CD;break;
                          case OUTCOME_DC:pb=b->p_after_DC;break;
                          case OUTCOME_DD:pb=b->p_after_DD;break;}
    int moveA = randFloat()<pa?1:0;
    int moveB = randFloat()<pb?1:0;

    int payoffA,payoffB;
    if(moveA&&moveB){payoffA=CC;payoffB=CC;a->lastRound=OUTCOME_CC;b->lastRound=OUTCOME_CC;}
    else if(moveA&&!moveB){payoffA=CD;payoffB=DC;a->lastRound=OUTCOME_CD;b->lastRound=OUTCOME_DC;}
    else if(!moveA&&moveB){payoffA=DC;payoffB=CD;a->lastRound=OUTCOME_DC;b->lastRound=OUTCOME_CD;}
    else{payoffA=DD;payoffB=DD;a->lastRound=OUTCOME_DD;b->lastRound=OUTCOME_DD;}

    a->accumAvgPayoff += payoffA;
    b->accumAvgPayoff += payoffB;
    a->roundsPlayed++;
    b->roundsPlayed++;
}

// Average payoff scaled 0-4
float computeAvgPopPayoffScaled(Agent pop[POP_SIZE]){
    float sum=0.0f;
    for(int i=0;i<POP_SIZE;i++){
        if(pop[i].roundsPlayed>0)
            sum += pop[i].accumAvgPayoff / pop[i].roundsPlayed; // per round
    }
    return sum / POP_SIZE;
}

void mutate(Agent pop[POP_SIZE]) {
    int numMut=(int)(POP_SIZE*MUTATION_RATE);
    if(numMut<1)numMut=1;
    for(int i=0;i<numMut;i++){
        int idx=rand()%POP_SIZE;
        Agent *a=&pop[idx];
        int which=rand()%4;
        float delta=(rand()%2==0?0.05f:-0.05f);
        float *target=NULL;
        switch(which){case 0:target=&a->p_after_CC;break;case 1:target=&a->p_after_CD;break;
                       case 2:target=&a->p_after_DC;break;case 3:target=&a->p_after_DD;break;}
        if(target){*target+=delta;if(*target<0.0f)*target=0.0f;if(*target>1.0f)*target=1.0f;}
    }
}

void regenerate(Agent pop[POP_SIZE]){
    // Roulette wheel selection based on payoff
    float total=0.0f;
    for(int i=0;i<POP_SIZE;i++){if(pop[i].accumAvgPayoff<0.0f)pop[i].accumAvgPayoff=0.0f;total+=pop[i].accumAvgPayoff;}
    if(total==0.0f) total=1.0f;
    float cumulative[POP_SIZE]; float running=0.0f;
    for(int i=0;i<POP_SIZE;i++){running+=pop[i].accumAvgPayoff/total;cumulative[i]=running;}
    Agent newPop[POP_SIZE];
    for(int k=0;k<POP_SIZE;k++){
        float r=randFloat();
        int chosen=0; while(chosen<POP_SIZE && r>cumulative[chosen]) chosen++;
        if(chosen>=POP_SIZE)chosen=POP_SIZE-1;
        newPop[k]=pop[chosen];
        newPop[k].accumAvgPayoff=0.0f;
        newPop[k].roundsPlayed=0;
    }
    for(int i=0;i<POP_SIZE;i++) pop[i]=newPop[i];
    shuffleArray(pop,POP_SIZE);
    mutate(pop);
}


// Save population to a single binary file, appending each cycle's data
void savePopulation(const Agent pop[POP_SIZE], int cycle) {
    FILE *fp = fopen("populations.bin", "ab"); // append binary mode
    if (!fp) {
        perror("Failed to open populations.bin for writing");
        return;
    }

    // Write a header (cycle number) before each population
    if (fwrite(&cycle, sizeof(int), 1, fp) != 1) {
        perror("Failed to write cycle header");
        fclose(fp);
        return;
    }

    // Write all agents
    size_t written = fwrite(pop, sizeof(Agent), POP_SIZE, fp);
    if (written != POP_SIZE) {
        fprintf(stderr, "Warning: only wrote %zu/%d agents at cycle %d\n", written, POP_SIZE, cycle);
    }

    fclose(fp);
    printf("✅ Saved population for cycle %d\n", cycle);
}

// Load population for a given cycle from the single file
int loadPopulation(Agent pop[POP_SIZE], int targetCycle) {
    FILE *fp = fopen("populations.bin", "rb");
    if (!fp) {
        perror("Failed to open populations.bin for reading");
        return 0; // failure
    }

    int cycle;
    while (fread(&cycle, sizeof(int), 1, fp) == 1) {
        if (fread(pop, sizeof(Agent), POP_SIZE, fp) != POP_SIZE) {
            fprintf(stderr, "Corrupted data at cycle %d\n", cycle);
            fclose(fp);
            return 0;
        }

        if (cycle == targetCycle) {
            fclose(fp);
            printf("✅ Loaded population from cycle %d\n", targetCycle);
            return 1; // success
        }
    }

    fclose(fp);
    fprintf(stderr, "❌ Cycle %d not found in populations.bin\n", targetCycle);
    return 0; // not found
}


int main(){
    srand((unsigned)time(NULL));
    Agent population[POP_SIZE];
    for(int i=0;i<POP_SIZE;i++) population[i]=makeRandomAgent();

    FILE *f=fopen("avg_payoff4.csv","w");
    fprintf(f,"cycle,avg_payoff\n");

    for(int c=0;c<CYCLE;c++){
        // Horizontal neighbor matching ONLY
        for(int i=0;i<GRID_SIZE;i++){
            for(int j=0;j<GRID_SIZE-1;j++){ // skip last column
                int idx=i*GRID_SIZE+j;
                int neighbor=i*GRID_SIZE+j+1;
                for(int r=0;r<ROUNDS;r++)
                    playOneRound(&population[idx],&population[neighbor]);
            }
        }

        float avgPay=computeAvgPopPayoffScaled(population);
        // printf("Cycle %d: avgPay=%.2f\n",c,avgPay);
        fprintf(f,"%d,%.2f\n",c,avgPay);

        regenerate(population);

        if (c % 100 == 0) {
            savePopulation(population, c);
        }
    }
    fclose(f);

    // for (int i = 0; i < 10; i++) {
    //     printAgent(&population[i]);
    // }

    return 0;
}
