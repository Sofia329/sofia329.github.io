#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool check_alpha(string key);
char convert (string key, char s);

int main (int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: /substitution key\n");
        return 1;
    }

    string key = argv[1];

    // check if key is alphabetic
    if (!check_alpha(key))
    {
        printf("Key need to be Alphabetic\n");
        return 1;
    }

    //check if key contains 26 alpha
    if (strlen(key) != 26)
    {
        printf("Key need to be 26 char\n");
        return 1;
    }
    //check no duplicate letter in key
    for (int i = 0; i < strlen(key) - 1; i++)
    {
        for (int j = i+1; j < strlen(key); j++)
        {
            if (toupper(key[i]) == toupper(key[j])) //char can use == to compare if same
        {
            printf("Duplicate letter in Key\n");
            return 1;
        }
        }
    }

    string plaintext = get_string("plaintext: ");
    string ciphertext;
    ciphertext = malloc((strlen(plaintext)+1)*sizeof(char));

    //treate plaintext as an array char
    for (int i = 0; i < strlen(plaintext); i++)
    {
        //only encrypt alphabetic letters
        if (isalpha(plaintext[i]))
        {
            ciphertext[i] = convert(key, plaintext[i]);
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }
    ciphertext[strlen(plaintext)] = '\0';
    printf("ciphertext: %s\n", ciphertext);
    free(ciphertext);
    return 0;

}

bool check_alpha(string key)
{
    //check every char is alpha
    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
    }
    return true;
}

char convert (string key, char s)
{
    // if char is upper, minus 65, else is lower, minus 97
    if (isupper(s))
    {
        return toupper(key[s-'A']);
    }
    else
    {
        return tolower(key[s-'a']);
    }
}
