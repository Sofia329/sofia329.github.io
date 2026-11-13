# From the Deep

In this problem, you'll write freeform responses to the questions provided in the specification.

## Random Partitioning

The pros are that it will allow boats A,B and C to evently carry the same amount of observations. However,
the cons are that a query has to be send to all boats to get the desired observations, as it doesn't know which observation is stored in which boat.

## Partitioning by Hour

the pros are that it allows narrowing down to a specific boat to query for a specific observation. The cons are that each boat is carrying an imbalanced load of observation data.

## Partitioning by Hash Value

The pros are that the observations row will evenly distributed among boats, and query will be more precious
to query the specific boat to get the result. The cons is if one of the boat is destroyed, there is no back up for the lost observation data in other boats.
