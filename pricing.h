#ifndef PRICING_H
#define PRICING_H

#define PI 3.1415926

// Greeks including Delta; Gamma; Theta; Vega; Rho
typedef struct {
    double delta;
    double gamma;
    double theta;
    double vega;
    double rho;
} greeks;


double monte_carlo_simulation(char *type, double K, double S, double T, double r, double sigma);
double black_scholes(char *type, double K, double S, double T, double r, double sigma);
greeks compute_greeks(char *type, double K, double S, double T, double r, double sigma);
double CDF_Normal(double z);
double PDF_Normal(double z);


#endif

