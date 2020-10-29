// Implements a dictionary's functionality
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>
#include <cs50.h>
#include <stdint.h>
#include <stdio.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26*2;
unsigned int TotalNumWords = 0;
// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    char word1[LENGTH + 1];
    int Wsize = strlen(word);
    for(int j = 0; j < Wsize; j++)
    {
        word1[j] = tolower(word[j]);
    }
    word1[Wsize] = '\0';
    int IndexHash = hash(word1);
    if(table[IndexHash] == NULL)
    {
        return false;
    }
    node* n = table[IndexHash];
    while(n != NULL)
    {
        if(strcasecmp(word, n->word) == 0)
        {
            return true;
        }
        else
        {
            n = n->next;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char* needs_hashing)
{
    unsigned int hash = 0;
    for (int i = 0, n = 3,len = strlen(needs_hashing); i < n && i < len; i++)
    {
        hash = (hash << 2) ^ needs_hashing[i];
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];
    FILE *file = fopen (dictionary,"r");
    if (file == NULL)
    {
        return false;
    }
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
           return false;
        }
        strcpy(n->word,word);
        n->next = NULL;
        int index = hash(n->word);
        if (table[index] == NULL)
        {
           table[index] = n;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        TotalNumWords++;
    }
    fclose(file);
    return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{

    return TotalNumWords;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node* cursor = table[i];
        if (cursor != NULL)
        {
            do
            {
            node* temp = cursor ;
            cursor = cursor->next;
            free(temp);
            }while (cursor != NULL);
        }
    }
    return true;
}
