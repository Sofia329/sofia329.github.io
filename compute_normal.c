#include <math.h>
#include "pricing.h"


// Error Function in the math libraries convert a z-score to the cumulative probability for a standard normal distribution.
double CDF_Normal(double z) {
    return 0.5 * (1 + erf(z/sqrt(2)));
}

// PDF is the relative likelihood at a specific point
double PDF_Normal(double z) {
    return exp(- z * z / 2)/(sqrt( 2 * PI));
}
