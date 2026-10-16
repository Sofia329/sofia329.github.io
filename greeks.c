#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <cs50.h>
#include <strings.h>

#include "pricing.h"


greeks compute_greeks(char *type, double K, double S, double T, double r, double sigma){
    greeks option;

    // borrow the formula from black schole to compute d1 and d2
    double d1 = (log(S/K)+ (r + sigma *sigma/2)* T)/(sigma * sqrt(T));
    double d2 = d1 - sigma*sqrt(T);
    double N_d1 = CDF_Normal(d1);
    double N_d2 = CDF_Normal(d2);
    double phi = PDF_Normal(d1);


    // compute delta for call or put, delta is how much option prices changes per unit change of underlying stock price
    option.delta = (strcasecmp(type, "call")==0) ? N_d1 : N_d1 - 1;

    // gamma is same across call and put, how delta changes per unit change of underlying stock price
    option.gamma = phi /(S * sigma * sqrt(T));

    // theta
    option.theta = (strcasecmp(type, "call")==0)
    ? -(S * phi * sigma)/ (2 * sqrt(T)) - r * K * exp(-r * T) * N_d2
    : -(S * phi * sigma)/ (2 * sqrt(T)) + r * K * exp(-r * T) * (1-N_d2);

    // vega is same across call and put
    option.vega = S * phi * sqrt(T);

    // rho
    option.rho = (strcasecmp(type, "call")==0)
    ? K * T * exp(-r * T) * N_d2
    : - K * T * exp(-r * T) * (1-N_d2);

    return option;
}

