#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#define BLOCK 512

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }
    //open the memory card
    FILE *card = fopen(argv[1],"r");
    if (card == NULL)
    {
        printf("Cannot Open Card\n");
        return 1;
    }
    // Create a buffer for a block of data
    uint8_t buffer[BLOCK];
    FILE *img = NULL;
    int count = 0;
    char *filename = malloc(8*sizeof(char));

    // while there are still memory left to read from the memory card
    while (fread(buffer, 1, BLOCK ,card) ==  BLOCK)
    {
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xff) == 0xe0)

            {
                if(img != NULL)
                    fclose(img);

                // then it is JPEG, write to a file with 000.jpg format
                sprintf(filename, "%03i.jpg", count);
                img = fopen(filename , "w");
                fwrite(buffer, 1, BLOCK, img);
                count ++;

            }
        else if (img != NULL)
        {
            fwrite(buffer, 1,BLOCK, img);
        }

    }

    if (img != NULL)
    {
         fclose(img);
    }

    fclose(card);
    free(filename);
    return 0;


}
