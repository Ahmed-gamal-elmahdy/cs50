#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

bool isKeyValid(string input);
string toUpper(string input);
bool isRepeted (string input);

int main (int argc ,string argv[])
{
     if (argc > 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    else if (argc < 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        string key = argv[1];
        if( !isKeyValid(toUpper(key)))
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
        else
        {
            string txt = get_string("Input text : ");
            int txtLen = strlen(txt);
            char output [txtLen];
            key = toUpper(key);
            for (int i = 0; i < txtLen; i++)
            {
                char c = txt[i];
                if (c >= 'a' && c <= 'z')
                {
                    c = key[ c - 97] + 32;    // it sets the index of key in range of 26 words [0 -25], then after that add 32 ( the difference to make the Upper charachters to lower ones)
                }
                else if (c >= 'A' && c <= 'Z')
                {
                    c = key [c - 65];
                }
                else
                {
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
    if( len != 26)
    {
        ans = false;
    }

    else if (isRepeted(input))
    {
        ans = false;
    }

    else
    {
    for (int i = 0; i < len; i++)
    {
        if ((input[i] >= 'a' && input[i] <= 'z') || (input[i] >= 'A' && input[i] <= 'Z'))
        {
        }
        else
        {
            ans = false;
            break;
        }
    }
    }
    return ans;
}
string toUpper(string input)    //function to make all the key uppercase
{
    int len = strlen(input);
    for (int i = 0; i < len; i++)
    {
        if (input[i] >= 'a' && input[i] <= 'z')
        {
            input[i] -= 32;
        }
        else
        {
        }
    }
    return input;
}

bool isRepeted(string input)
{
    bool ans = false;
    int nums[26] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0} ;

    for (int i = 0; i < 26; i++)
    {
        //printf("nums[i] = %i at i = %i\n", ((int)input[i] - 65), i);
        nums[(int)input[i] - 65] += 1;
        if (nums[(int)input[i] - 65] > 1)
        {
                ans = true;
           //printf("REPEPTED %c AT I = %i", input[i] , i);
            break;
        }
    }
    return ans;
}
