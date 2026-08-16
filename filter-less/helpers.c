#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // loop over all pixels
    // take average of RGB
    // update pixels value
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // loop through each pixel, take average of rgb, and replace avg to rgb in each pixel
            int rgb =
                round((image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0);
            image[i][j].rgbtBlue = rgb;
            image[i][j].rgbtGreen = rgb;
            image[i][j].rgbtRed = rgb;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen +
                                 .189 * image[i][j].rgbtBlue);
            sepiaRed = sepiaRed > 255 ? 255 : sepiaRed;
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen +
                                   .168 * image[i][j].rgbtBlue);
            sepiaGreen = sepiaGreen > 255 ? 255 : sepiaGreen;
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen +
                                  .131 * image[i][j].rgbtBlue);
            sepiaBlue = sepiaBlue > 255 ? 255 : sepiaBlue;

            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;

    for (int i = 0; i < height; i++)
    {
        for (int j = width - 1; j >= 0; j--)
        {
            temp = image[i][j];
            if (j <= width - j - 1)
            {
                break;
            }
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++) 
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            int count = 0;
            int sum_green = 0;
            int sum_blue = 0;
            int sum_red = 0;

            for (int ai = -1; ai <= 1; ai++)
            {
                for (int aj = -1; aj <= 1; aj++)
                {
                    int ni = i + ai;
                    int nj = j + aj;

                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        sum_blue += copy[i + ai][j + aj].rgbtBlue;
                        sum_green += copy[i + ai][j + aj].rgbtGreen;
                        sum_red += copy[i + ai][j + aj].rgbtRed;
                        count++;
                    }
                }
            }

            image[i][j].rgbtBlue = round((float) sum_blue / count);
            image[i][j].rgbtGreen = round((float) sum_green / count);
            image[i][j].rgbtRed = round((float) sum_red / count);
        }
    }

    return;
}
