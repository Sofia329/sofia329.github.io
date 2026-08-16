#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>
#include <math.h>

int compute_letters(string text);
int compute_words(string text);
int compute_sentence(string text);

int main(void)
{
    string text = get_string("Text: ");

    //L is the average number of letters in 100 words
    int letters = compute_letters(text);
    //Count words in the input
    int word = compute_words(text);
    //S is the average number of sentence in 100 words
    int sentence = compute_sentence(text);
    //Compute Coleman-Liau index
    //index = 0.0588 * L - 0.296 * S - 15.8
    double index = 0.0588 * letters/word * 100 - 0.296 * sentence/word * 100 - 15.8;
    //Print the grade
    if (index >= 16 )
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        int i = round(index);
        printf("Grade %d\n", i);
    }
}

int compute_letters(string text)
// letters only limits to alphabetical of lower case and upper case
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i ++)
    {
        if (isalpha(text[i]))
        {
            count += 1;
        }
    }
    return count;
}

int compute_words(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            count += 1;
        }
    }
    return count + 1;
}

int compute_sentence(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            count += 1;
        }
    }
    return count;
}
