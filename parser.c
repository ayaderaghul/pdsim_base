#include <string.h>
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

int parseAgent(const char *str, Agent *a) {
    char lastRoundStr[8];

    // Attempt to extract all numeric fields and lastRound as string
    int parsed = sscanf(str,
        "Agent { p_after_CC=%f, p_after_CD=%f, p_after_DC=%f, p_after_DD=%f, "
        "accumAvgPayoff=%f, roundsPlayed=%d, lastRound=%7s }",
        &a->p_after_CC, &a->p_after_CD, &a->p_after_DC, &a->p_after_DD,
        &a->accumAvgPayoff, &a->roundsPlayed, lastRoundStr
    );

    if (parsed != 7) {
        fprintf(stderr, "❌ Failed to parse agent from string: %s\n", str);
        return 0; // failure
    }

    // Map lastRound string to enum
    if (strcmp(lastRoundStr, "CC") == 0) a->lastRound = OUTCOME_CC;
    else if (strcmp(lastRoundStr, "CD") == 0) a->lastRound = OUTCOME_CD;
    else if (strcmp(lastRoundStr, "DC") == 0) a->lastRound = OUTCOME_DC;
    else if (strcmp(lastRoundStr, "DD") == 0) a->lastRound = OUTCOME_DD;
    else {
        fprintf(stderr, "❌ Unknown lastRound value: %s\n", lastRoundStr);
        return 0;
    }

    return 1; // success
}
static float randFloat() { return (float)rand() / (float)RAND_MAX; }

void playAndPrintHistory(Agent *a, Agent *b, int rounds) {
    char historyA[rounds + 1];
    char historyB[rounds + 1];

    // Copy last round outcomes so strategies evolve correctly
    Outcome lastA = a->lastRound;
    Outcome lastB = b->lastRound;

    for (int r = 0; r < rounds; r++) {
        // Determine cooperation probabilities based on last outcomes
        float pa, pb;
        switch (lastA) {
            case OUTCOME_CC: pa = a->p_after_CC; break;
            case OUTCOME_CD: pa = a->p_after_CD; break;
            case OUTCOME_DC: pa = a->p_after_DC; break;
            case OUTCOME_DD: pa = a->p_after_DD; break;
        }
        switch (lastB) {
            case OUTCOME_CC: pb = b->p_after_CC; break;
            case OUTCOME_CD: pb = b->p_after_CD; break;
            case OUTCOME_DC: pb = b->p_after_DC; break;
            case OUTCOME_DD: pb = b->p_after_DD; break;
        }

        int moveA = (randFloat() < pa) ? 1 : 0;
        int moveB = (randFloat() < pb) ? 1 : 0;

        // Record moves as C or D
        historyA[r] = moveA ? 'C' : 'D';
        historyB[r] = moveB ? 'C' : 'D';

        // Compute payoff and update lastRound for next turn
        if (moveA && moveB) { lastA = OUTCOME_CC; lastB = OUTCOME_CC; }
        else if (moveA && !moveB) { lastA = OUTCOME_CD; lastB = OUTCOME_DC; }
        else if (!moveA && moveB) { lastA = OUTCOME_DC; lastB = OUTCOME_CD; }
        else { lastA = OUTCOME_DD; lastB = OUTCOME_DD; }
    }

    historyA[rounds] = '\0';
    historyB[rounds] = '\0';

    printf("Agent A: %s\n", historyA);
    printf("Agent B: %s\n", historyB);
}


int main() {
    const char *text = "Agent { p_after_CC=1.00, p_after_CD=0.21, p_after_DC=0.05, p_after_DD=0.35, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }";
    const char *text2="Agent { p_after_CC=1.00, p_after_CD=0.31, p_after_DC=0.10, p_after_DD=0.25, accumAvgPayoff=0.00, roundsPlayed=0, lastRound=CC }";
    Agent a;
    Agent b;

    if (parseAgent(text, &a)) {
        printf("✅ Parsed agent successfully:\n");
        printAgent(&a);
    } else {
        printf("❌ Failed to parse agent.\n");
    }

    if (parseAgent(text2, &b)) {
        printf("✅ Parsed agent successfully:\n");
        printAgent(&b);
    } else {
        printf("❌ Failed to parse agent.\n");
    }

    printf("Initial states:\n");
    printAgent(&a);
    printAgent(&b);

    printf("\nPlaying 100 rounds:\n");
    playAndPrintHistory(&a, &b, 100);

    return 0;
}