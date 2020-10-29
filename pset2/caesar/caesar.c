#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

bool isKeyValid(string input);

int main(int argc, string argv[])
{
    if (argc > 2)
    {
        printf("One argument pls\n");
        return 1;
    }
    
    else if (argc < 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    
    else
    {
        if (!isKeyValid(argv[1]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        else 
        {
            int key = atoi(argv[1]);  //convert the key to int 
            if (key < 0)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
            string txt = get_string("plaintext:  ");
            int txtLen = strlen(txt);
            char output[txtLen];
            char c;
            for (int i = 0; i < txtLen; i++)
            {
                c = txt[i];
                if (c <= 'z' && c >= 'a')
                {
                    c = ((c - 97 + key) % 26) + 97;
                }
                else if (c <= 'Z' && c >= 'A')
                {
                    c = ((c - 65 + key) % 26) + 65 ;
                }
                output[i] = c;
            }
             
            printf("ciphertext: ");  //print the output after done shifting
            for (int i = 0; i < txtLen; i++)
            {
                printf("%c", output[i]);
            }
            printf("\n");
            return 0;
        }
    }
}
bool isKeyValid(string input)   //Function to check if the key is number
{
    bool ans = true;
    int len = strlen(input);
    for (int i = 0; i < len; i++)
    {
        if (input[i] >= '0' && input[i] <= '9')
        {
        }
        else
        {
            ans = false;
            break;
        }
    }
    return ans;
}
