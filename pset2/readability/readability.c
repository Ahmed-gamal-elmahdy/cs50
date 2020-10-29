#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

int main(void)
{
    string text = get_string("Text: ");
    int txtLen = strlen(text);
    int lettersNum = 0, sentencesNum = 0, wordsNum = 1, index;
    float L, S;
    for (int i = 0; i < txtLen; i++)
    {
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')  // check ending of sentences
        {
            sentencesNum++;
        }
        else
        {
            if (text[i] == ' ')  // check ending of words
            {
                wordsNum++;
            }
            else if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))   //check letters
            {
                lettersNum++;
            }
            else
            {
            }
        }
    }
    L = (float) lettersNum / wordsNum * 100;   // calculate avg of letters per 100 word
    S = (float) sentencesNum / wordsNum * 100;  // carlculate avg of sentences per 100 word
    index = (int) round(0.0588 * L - 0.296 * S - 15.8);  // calculate the grade
    printf("Letters num = %i\n", lettersNum);
    printf("SenetancesNum = %i\n", sentencesNum);
    printf("Words Num = %i\n", wordsNum);
    printf("Text Lenght %i\n", txtLen);
    printf("L = %f\n", L);
    printf("S = %f\n", S);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}