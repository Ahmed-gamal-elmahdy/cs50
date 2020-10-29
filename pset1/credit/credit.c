#include <cs50.h>
#include <stdio.h>

int getLength(long input);     //to get the length of the card ( Number of Digits)
int getLastTwo(long cardNum); //Function to get the last two digits

int main(void)
{
    long card = 1;
    int sum1 = 0;
    int sum2 = 0;
    int sum = 0;
    do
    {
        card = get_long("Enter the card number ");
    }
    while(card < 0);
    int lastTwo = getLastTwo(card);
    int length = getLength(card); //get the length of the card
    for(int i = 0 ; i < length ; i++)
    {
        if(i % 2 == 0)
        {
         sum1 += card % 10;
        }
        else
        {
            int num = (card % 10) * 2;
            if(num > 9)
            {
                for(int j = 0 ; j < 2 ; j++){
                    sum2 += num % 10;
                    num /= 10;
                }
            }
            else
            {
                sum2 += num;
            }
        }
        card /= 10;
    }
    printf("Sum1 =%i",sum1);
    printf("   Sum2=%i",sum2);
    sum = sum1 + sum2;
    if(sum % 10 == 0)
    {


        switch (length)
        {
            case  15:
            if(lastTwo == 34 || lastTwo == 37)
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
            break;
            case 16:
            if(lastTwo >= 51 && lastTwo <= 55)
            {
                printf("MASTERCARD\n");
            }
            else if(lastTwo / 10 == 4)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
            break;
            case 13:
            if(lastTwo / 10 == 4)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
            break;
            default:
            printf("INVALID\n");
            break;
        }
    }
    else
    {
        printf("INVALID\n");
    }
}


int getLength(long input)
{
    int output = 0;
    while(input > 0)
    {
        input /= 10;
        output++;
    }
    return output;

}
int getLastTwo(long cardNum)
{
    int output = 0;
    while(cardNum > 100)
    {
        cardNum /= 10;
    }
    output = cardNum;
    return output;
}