#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int k = 0; k < candidate_count; k++)
    {
        if(!strcmp(candidates[k], name))
        {
            ranks[rank] = k;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // the global variable preferences initialized to all zeros already

   for (int i = 0; i < candidate_count - 1; i ++)
   {
    for (int j = i + 1; j < candidate_count; j++)
    {
        preferences[ranks[i]][ranks[j]] +=1;
    }
   }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // A,B,C ---> A&B;A&C;B&C
    //A&B ---> if Perference[A][B] > Perference [B][A] then A wins
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            //if i not equal to J, check the votes, not consider if i = j
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count += 1;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count += 1;
            }
            else
            {
                //tie
                continue;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory

void sort_pairs(void)
{
    // compute strength of victory
    int strength[pair_count];

    for (int i = 0; i < pair_count; i++)
    {
        strength[i] = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];
    }
    // sort pairs array based on the strength of victory --> from largest to smallest

    for (int i = 0; i < pair_count - 1; i++)
    {
        int n = i;

        for (int j = i + 1; j < pair_count; j++)
        {
            if (strength[n] < strength[j])
            {
                n = j;
            }
        }
        pair temp_pair = pairs[i];
        pairs[i] = pairs[n];
        pairs[n] = temp_pair;

        int temp_strength = strength[i];
        strength[i] = strength[n];
        strength[n] = temp_strength;
    }

}


// Lock pairs into the candidate graph in order, without creating cycles
bool has_cycle (int loser, int winner);

void lock_pairs(void)
{

    for (int i = 0; i < pair_count; i++)
    {
        int w = pairs[i].winner;
        int l = pairs[i].loser;

        if (!has_cycle(l,w))
        {
            locked[w][l] = true;
        }
     }
    return;
}

bool has_cycle (int loser, int winner)
{

    if (loser == winner)
    {
        return true;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if(locked[loser][i])
        {
            if (has_cycle(i,winner))
            {
                return true;
            }
        }
    }
    return false;
}

// Print the winner of the election
void print_winner(void)

{
    int count [candidate_count];
    for (int i = 0; i < candidate_count; i++)
    {
        count[i] = 0;
    }
    

    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[i][j])
            {
                count[j]++;
            }
        }
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if(count[i] == 0)
        {
            printf("%s\n", candidates[i]);
        }
    }

    return;
}
