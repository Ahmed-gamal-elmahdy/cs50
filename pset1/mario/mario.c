
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int length = 0;
    do
    {
        length = get_int("Enter the length!");
    }
    while (length < 1 || length > 8);
    for (int i = 0; i < length ; i++)
    {
        for (int j = 1 ; j < length - i ; j++)
        {
            printf(" ");
        }
        for (int i2 = 0 ; i2 <= i ; i2++)// to make the left side
        {
            printf("#");
        }
        printf("  ");
        for (int i3 = 0; i3 <= i; i3++)//to make the right side
        {
            printf("#");
        }


        printf("\n");


    }

}