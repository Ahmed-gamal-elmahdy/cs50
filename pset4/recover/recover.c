#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <cs50.h> 
typedef uint8_t Byte;


bool check(Byte Step1, Byte Step2, Byte Step3, Byte Step4);
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Error wrong\n");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Error, can't be read\n");
        return 1;
    }
    Byte buffer[512];
    int picNum = 0;
    bool isPic = false;
    FILE *img;
    while (fread(buffer, 512, 1, file))
    {
        //Check the conditions of the jpgb
        if (check(buffer[0], buffer[1], buffer[2], buffer[3]))
        {
            //check if there is exisitng image
            if (isPic)
            {
                fclose(img);
            }
            else
            {
                isPic = true;
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", picNum);
            img = fopen(filename, "w");
            picNum++;
        }
        if (isPic)
        {
            fwrite(buffer, 512, 1, img);
        }
    }
}

// check the header if it is jpgb
bool check(Byte Step1, Byte Step2, Byte Step3, Byte Step4)
{
    if ((Step1 == 0xff) && (Step2 == 0xd8) && (Step3 == 0xff) && ((Step4 & 0xf0) == 0xe0))
    {
        return true;
    }
    return false;
}
