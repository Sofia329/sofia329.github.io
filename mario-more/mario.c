#include <stdio.h>
#include <cs50.h>

void get_print(int space, int height);

int main(void)
{
    int height;
    // prompt user input for the height, between 1 and 8 inclusive, re-prompt if not correct
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8 );

    // print # block

    for (int i = 0; i < height; i++)
    {
        get_print(height-i-1, i+1);
    }

}

void get_print(int space, int height)
{
    for (int i = 0; i < space; i++)
    {
        printf(" ");
    }
    for (int i = 0; i < height; i++)
    {
        printf("#");
    }
    printf("  ");
    for (int i = 0; i < height; i++)
    {
        printf("#");
    }
    printf("\n");
}
