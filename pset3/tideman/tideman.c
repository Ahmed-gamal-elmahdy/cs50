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
}
pair;

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
bool checkPath(int winner, int loser ,int pairIndex);

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

        printf("\n");
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
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)       //check if the name exits
        {
            ranks[rank] = i;        //record the rank in the name;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {

        for (int j = i + 1; j < candidate_count; j++)
        {
            if (j != i)
            {
            preferences[ranks[i]][ranks[j]]++;
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    pair_count = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1 ; j <  candidate_count; j++)
        {
             pair localOne;
            if ( preferences[i][j] > preferences[j][i])   //Check if the  i > j then i is the winner , j is loser
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;

            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int pairPower [pair_count];  //an arry to store the power of the pairs
    for (int i = 0; i < pair_count; i++) //calculate the power of the pairs
    {
        int cWinner = pairs[i].winner;  // local variable to store the index of the winner in the iTh arry
        int cLoser = pairs[i].loser;    // local variable to store the index of the loser in the iTh arry
        pairPower[i] = preferences[cWinner][cLoser] - preferences[cLoser][cWinner];   //calculate the power of the iTh pair in pairs arry
    }
    for (int i = 0; i < pair_count; i++)                     //Loop for descending ordering
	{
		for (int j = 0; j < pair_count; j++)             //Loop for comparing other values
		{
			if (pairPower[j] < pairPower[i])                //Comparing other array elements
			{
				pair trash = pairs[i];         //Using temporary variable for storing pairs
				pairs[i] = pairs[j];            //exchanging the pairs
				pairs[j] = trash;             //storing last pair
			}
		}
	}
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    locked[pairs[0].winner][pairs[0].loser] = true;
    for (int i = 0; i < pair_count; i++)
    {
        if (!checkPath(pairs[i].winner, pairs[i].loser, i)) //check if there is no path from loser to winner;
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}
bool checkPath(int winner, int loser, int pairIndex)
{
   for (int i = 0; i < pairIndex; i++)
   {
       if(locked[pairs[i].winner][pairs[i].loser] == true)
       {
           if(locked[loser][pairs[i].winner] == true && locked[pairs[i].loser][winner] == true)
           {
               return true;
           }
           if (locked[i][winner] == true && locked[loser][i] == true)
           }
                return true;
           }

       }
   }
   return false;
}
/*
if (locked[i][winner] == true && locked[loser][i] == true)
        {
            return true;
        }

*/
// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (i != j)
            {
                if (locked[i][j] == true && locked[j][i] !=  true)
                {
                    printf("%s\n", candidates[i]);
                }
            }
        }
    }
    return;
}

