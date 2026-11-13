#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string text = get_string("Test: ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        int value = isalpha (text[i]);
        printf("%i", value);
    }
// so isalpha is only return a int of 1024 if it is alphabetic, 0 if not
}
