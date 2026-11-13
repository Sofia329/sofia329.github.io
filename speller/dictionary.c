// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <cs50.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 70;

// Hash table
node *table[N];

//count how many words loaded in dictionary
int count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //hash the word to determine which bucket/linked list of the hash table
    int n = hash(word);

    //set a traversal pointer
    node *traverse = table[n];

    while(traverse != NULL)
    {
        if (strcasecmp(word,traverse->word)==0)
        {
            return true;
        }
        traverse = traverse->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int length = strlen(word)-1;
    int n = toupper(word[0]) - 'A';

    // length between 0 and 44,  n between 0 and 25, thus return value between 0 and 69
    return length + n;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE * source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    char buffer[LENGTH + 1];
    while (fscanf(source, "%s", buffer) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(source);
            return false;
        }

        // defensive programming ensure new node next is pointing to null
        new_node->next = NULL;

        //calculate the hash value
        int n = hash(buffer);

        // paste the word to the new node
        strcpy (new_node->word, buffer);

        //point the new node to what head is pointing to
        new_node->next = table[n];

        // change the head to point to new node
        table[n] = new_node;

        count++;

    }

    // read each word in the dictionary to hash table
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // check whilst loading words into dictionary
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    //delete each linked list loop through i to N
    for (int i = 0; i < N; i++)
    {
        //if it is not empty node
        node *delete = table[i];

        if(delete == NULL)
        {
            continue;
        }
        while (delete != NULL)
        {
            node *temp = delete;
            delete = delete->next;
            free(temp);
        }
        table[i] = NULL;
    }
    return true;
}


