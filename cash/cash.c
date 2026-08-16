# include <stdio.h>
# include <cs50.h>

int calculate_quarters(int change);
int calculate_dime(int change);
int calculate_nickel(int change);

int main (void)
{
    // prompt the user for change owned, re-prompt if wrong input
    int change;
    do
    {
       change =  get_int("Change ownded: ");
    }
    while (change < 0 );

    // calculate the minimum coins to dispense
    int quarter = calculate_quarters(change);
    change -= 25*quarter;
    int dime = calculate_dime(change);
    change -= 10*dime;
    int nickel = calculate_nickel(change);
    change -= 5*nickel;
    int number_of_coins = quarter + dime + nickel + change;
    printf("%i\n", number_of_coins);

}

int calculate_quarters(int change)
{
    // calculate the minimum quarter to give
    return change/25;
}

int calculate_dime(int change)
{
    return change/10;
}

int calculate_nickel(int change)
{
    return change/5;
}

