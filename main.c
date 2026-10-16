#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <cs50.h>
#include <strings.h>
#include <unistd.h>
#include <time.h>

#include "pricing.h"

int main(void){

    // Print usage of the program
    printf("============================================================================================================================================================\n");
    printf("This Program will compute the fair value for European Call Option or European Put Option through Black Schole closed form formula and Monte Carlo Simulation\n");
    printf("============================================================================================================================================================\n\n");
    sleep(2);
    printf("***** Pls enter the below information to get started ***** \n\n");
    sleep(2);

    // Get user inputs for option pricing using both Black Scholes and Monte Carlo Simulation
    char *type = get_string("Call or Put: ");
    double K = get_double("Strike Price: ");
    double S = get_double("Current Stock Price: ");
    double T = get_double("Time To Expiration (in fraction of years, e.g. 0.25 = 3 months): ");
    double r = get_double("Risk Free Rate (e.g. 0.2 for 25%%): ");
    double sigma = get_double("Volatility (e.g. 0.25 for 25%%): ");

    // validate user inputs
    if (K <= 0 || S <= 0 || T <= 0 || sigma <= 0){
        printf("Error: Strike Price; Stock Price; Time to Expiration; Volatility must be positive\n");
        return 1;
    }

    if (strcasecmp(type,"call") != 0 && strcasecmp(type,"put") != 0){
        printf("Invalid Option Type. Use 'Call' or 'Put'.\n");
        return 1;
    }

    // compute option price using monte_carlo & black scholes approaches
    double monte_carlo_option_pricing =  monte_carlo_simulation(type, K, S, T, r, sigma);
    double black_scholes_option_pricing = black_scholes(type, K, S, T, r, sigma);
    printf("\n\n");
    printf("=====================================================================================================\n");
    printf("                                        Pricing Result                                               \n");
    printf("=====================================================================================================\n");
    printf("Option Type             : %s\n", type);
    printf("Strike Price            : $%.2f\n", K);
    printf("Current Stock Price     : $%.2f\n", S);
    printf("Time to Expiration      : $%.2f year\n", T);
    printf("Risk-Free Rate          : %.2f%%\n", r * 100);
    printf("Volatility              : %.2f%%\n", sigma * 100);
    printf("-------------------------------------------------------------------------------------------------------\n");
    printf("The Simulated %s Option Price Using Monte Carlo Simulation is : %.2f\n\n", type, monte_carlo_option_pricing);
    printf("The Simulated %s Option Price Using Black Scholes Formula is  : %.2f\n\n", type, black_scholes_option_pricing);
    printf("=============================================End=======================================================\n");
    printf("\n\n");

    // compute greeks for this option
    greeks option =  compute_greeks(type, K, S, T, r, sigma);
    printf("=======================================================================================================\n");
    printf("                                           Option Geeks                                                \n");
    printf("=======================================================================================================\n");
    printf("Delta           : %.2f\n", option.delta);
    printf("Gamma           : %.2f\n", option.gamma);
    printf("Theta           : %.2f\n", option.theta);
    printf("Vega            : %.2f\n", option.vega);
    printf("Rho             : %.2f\n", option.rho);
    printf("==============================================End======================================================\n");
    printf("\n\n");
    // Hedge Suggestion - Delta Hedging, assume contract size is 100 shares per contract
    int hedging = (int) (option.delta * 100);
    printf("=======================================================================================================\n");
    printf("                                           Hedging Suggestion                                          \n");
    printf("=======================================================================================================\n");
    printf("Delta Hedge to offset the price movement risk.\n");
    printf("Note: Delta hedging requires frequent rebalacning as delta changes.\n");
    printf("-------------------------------------------------------------------------------------------------------\n");
    if (strcasecmp(type,"call") == 0) {
        printf("Buy %d shares of underlying stocks to hedge delta\n", hedging);
    }
    else{
        printf("Sell %d shares of underlying stocks to hedge delta\n", hedging);
    }
    printf("==============================================End======================================================\n\n");
    printf("\n\n");
    return 0;
}
