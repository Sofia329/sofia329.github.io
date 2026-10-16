// implements European Option pricing using Black Scholes Merton (BSM) model
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <cs50.h>
#include <strings.h>

#include "pricing.h"

double black_scholes(char *type, double K, double S, double T, double r, double sigma){
    // compute d1 and d2 for black schole formula
    double d1 = (log(S/K)+ (r + sigma *sigma/2)* T)/(sigma * sqrt(T));
    double d2 = d1 - sigma*sqrt(T);

    // find the cumulative standard normal dsitribution
    if (strcasecmp(type, "call") == 0){
        double N_pos_d1 = CDF_Normal(d1);
        double N_pos_d2 = CDF_Normal(d2);
        double C = S * N_pos_d1 - K * exp(-r*T) * N_pos_d2;
        return C;
    }
    else if (strcasecmp(type, "put") == 0
        double N_neg_d1 = CDF_Normal(-d1);
        double N_neg_d2 = CDF_Normal(-d2);
        double P = K * exp(-r*T) * N_neg_d2 - S * N_neg_d1;
        return P;
    }
    else{
        return 0;
    }

}




