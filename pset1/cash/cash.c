#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollars = 0;
    int steps = 0;
    do
    {
        dollars = get_float("Please the change owed ! "); //takes the input from user
    }
    while (dollars < 0) ;
    int cents = round(dollars * 100); //chane it all to cents
    while (cents >= 25) // calculate the number of spent quarters
    {
        cents -= 25;
        steps++;
    }
    while (cents >= 10) // calculate the number of spent dimes
    {
        cents -= 10;
        steps++;
    }
    while (cents >= 5)  //  calculate the number of spent nickels
    {
        cents -= 5;
        steps++;
    }
    while (cents >= 1)  //  calculate the number of spent pennies
    {
        cents--;
        steps++;
    }
    
    
    printf("%i\n", steps);
}