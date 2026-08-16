#include <cs50.h>
#include <stdio.h>

long first_digit(long card);
long second_digit(long card);
int check_digit(long card);
int compute (long card);

int main(void)

{
    long card = get_long("Number: ");
    long first = first_digit(card);
    long second = second_digit(card);

    //compute the digit of card no.
    int digit = check_digit(card);

    // compute an array of integer for card number in reversal number

    int list [digit];

    for (int i = 0; i < digit; i++)
    {
        {
            if (card < 10)
                list[i] = card;
            list[i] = card % 10;
            card = (card - list[i])/10;
        }
    }

    // compute the sum from the 2nd and jumps over 1 digit each time
    int sum = 0;

    for (int i = 0; i < digit; i++)
    {
        int position = 0;

        if ( i % 2 != 0)
        {
            position = 2 * list[i];
            if (position > 9)
            {
                sum += (position % 10 + position / 10);
            }
            else
            {
                sum += position;
            }

            continue;
        }
        sum += list[i];
    }


    if (sum %10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // check which card type and print out if digit is corresponding to the card type

    // visa starts 4
    if (first == 4 && (digit == 13 || digit == 16))
    {
        printf("VISA\n");
     }

    else if (digit == 15 && (second == 34 || second == 37))
    {
        printf("AMEX\n");
    }

    else if (digit == 16 && second >= 51 && second <= 55)
    {
        printf("MASTERCARD\n");
    }
    else
    {
       printf("INVALID\n");
       return 0;
    }

}

//compute the first digit
long first_digit(long card)
{
    while (card >= 10)
    {
        card /= 10;
    }
    return card;

}

//compute the first two digit
long second_digit(long card)
{
    while(card >= 100)
    {
        card /= 10;
    }
    return card;
}


// check the length of the card number
int check_digit(long card)

{
    int count = 0;
    while (card >= 10)
    {
        card /= 10;
        count ++;
    }
    return count + 1;
}


