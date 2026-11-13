#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char rotate(int key, char text);

int main(int argc, string argv[])
{
    // check if user input 1 argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        char *digit_k = argv[1];
        for (int i = 0, n = strlen(digit_k); i < n; i++)
        {
            if (isdigit(digit_k[i]) == 0)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
    // Prompt user for plaintext and rotate
    int key = atoi(argv[1]);
    char *plaintext = get_string("Plaintext:  ");

    char ciphertext[strlen(plaintext) + 1];

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]) != 0)

        {
            ciphertext[i] = rotate(key, plaintext[i]);
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }
    ciphertext[strlen(plaintext)] = '\0';
    printf("ciphertext: %s\n", ciphertext);
    return 0;
}

char rotate(int key, char text)
{
    if (isupper(text))
    {
        int new_position = ((int) text - 65 + key) % 26;
        text = (char) (65 + new_position);
        return text;
    }
    else
    {
        int new_position = ((int) text - 97 + key) % 26;
        text = (char) (new_position + 97);
        return text;
    }
}


 