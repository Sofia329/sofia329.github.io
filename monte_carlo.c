#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <cs50.h>
#include <strings.h>

#include "pricing.h"


double standard_normal_generators(void);


/*
using multi-step simulations to simulate how stock price at current time t evolve to stock price at time T
each step will draw a fresh, independent standard normal value to generate the random shock for the stock price increments
each
divide time T into N intervals, each Δt is the same. if T is 1 year, then step is 252, delta T is T/252
*/

double monte_carlo_simulation(char *type, double K, double S, double T, double r, double sigma){
    /* rand function is pseudo random, as it is default to seed 1, each time will generate the identical
    random series, call srand() function to change the seed each time */
   srand(time(NULL));

    // simulate 1,000 path of stock price movement
    // each path will have T/252 steps to represent the stock price changes across discrete time intervals (delta T)
    int paths = 10000;
    int steps = (int) (T * 252);
    double delta_t = T/steps;
    double expected_payoff = 0;

    // loop through 10,000 paths, which is 10,000 possible stock price at expiration
    for (int i = 0; i < paths; i++){
        // initialize stock price at expiration S_t with the current stock price S
        double S_t = S;
        //discretely compute stock prices at increment of time intervals
        for (int j = 0; j < steps; j++){
            double Z = standard_normal_generators();
            S_t = S_t * exp ((r-sigma * sigma / 2) * (delta_t) + sigma * sqrt(delta_t) * Z);
        }
        // payoff is different across each path due to stock price S_t is different
        double payoff = (strcasecmp(type, "call")==0) ? fmax (S_t - K, 0) : fmax (K-S_t, 0);
        expected_payoff += payoff;
    }
    expected_payoff = exp(-r * T) * (expected_payoff/paths);
    // option price is the average of all the paths' payoff, each path weights equally
    return expected_payoff;
}

/*
rand function generates random integers draw from uniform distribution, each time being called will return
a random integer between 0 and RAND_MAX, which is a constant fixed value.

To avoid integer division truncation, cast the rand() to double type then divided by RAND_MAX will return a
random floating number between 0.0 and 1.0.
*/
double uniform_random_generators (void){
    double random = (double) rand()/ RAND_MAX;
    return random;
}

/*
Monte Carlo Simulation for underlying asset prices is following Geometric Brownian Motion (GBM)
GMB is based of normal distributed random values, hence need to convert the uniform values to standard normal values

Box-Muller to convert uniform random numbers between [0.0, 1.0] to standard normal random numbers

each time Box-Muller will take two random uniform numbers as inputs, and outputs two random standard normal numbers
however, given the complication, i will only take 1 output of stand normal value from box-muller transform.
*/
double standard_normal_generators(void){

    //generate two uniform distributed random values
    double u1 = uniform_random_generators();
    if (u1 == 0) u1 = 1e-9;
    double u2 = uniform_random_generators();

    //Box-Muller convert the uniform values to standard normal values
    double Z = sqrt(-2 * log(u1)) * cos(2 * PI * u2);
    return Z;
}



