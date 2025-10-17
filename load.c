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

int main() {
    Agent pop[POP_SIZE];

    if (loadPopulation(pop, 6000)) {
        printf("Population at cycle 6000:\n");
        for (int i = 0; i < POP_SIZE; i++) {
            printAgent(&pop[i]);
        }
    }

    return 0;
}