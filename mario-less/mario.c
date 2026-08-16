# include <stdio.h>
# include <cs50.h>

void get_print(int space, int height);

int main (void)
{
 // prompt user for the height
 // if height is less or equal zero, reprompt

 int height;

 do
 {
    height = get_int("Height: ");
 }
 while (height < 1);

 for (int i = 0; i < height; i++)
 {
    get_print(height-1-i , i+1);
 }
}


void get_print(int space, int height)

{
    for (int i = 0; i < space; i ++)
    {
        printf(" ");
    }
    for (int i = 0; i < height; i ++)
    {
        printf("#");
    }
    printf("\n");
}
