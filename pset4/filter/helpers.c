#include "helpers.h"
#include <math.h>
#include <cs50.h> 

bool Ctop(int i,int h,int w);
bool Cbot(int i,int h,int w);
bool Cleft(int j,int h,int w);
bool Cright(int j,int h,int w);
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            int grey = image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed; // Calculate the sum of the colors
            grey  = round(grey / 3.0); // round up the avrage;
            image[i][j].rgbtBlue = grey;
            image[i][j].rgbtRed = grey;
            image[i][j].rgbtGreen = grey;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            int red,blue,green,Cred,Cblue,Cgreen;
            red = image[i][j].rgbtRed; //current red
            blue = image[i][j].rgbtBlue;    //current blue 
            green = image[i][j].rgbtGreen;  //curent green 
            Cblue = round(.272 * red + .534 * green + .131 * blue);
            Cred = round(.393 * red + .769 * green + .189 * blue);
            Cgreen = round(.349 * red + .686 * green + .168 * blue);
            //conditions to make sure that all the numbers are capped at max 255;
             if(Cblue > 255){
                image[i][j].rgbtBlue = 255;
            }
            else{
                image[i][j].rgbtBlue = Cblue;
            }
             if(Cred > 255){
                image[i][j].rgbtRed = 255;
            }
            else{
                image[i][j].rgbtRed = Cred;
            }
             if(Cgreen > 255){
                image[i][j].rgbtGreen = 255;
            }
            else{
                image[i][j].rgbtGreen = Cgreen;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE cPixel;
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width / 2 ; j++){
            cPixel = image[i][j];  //saves the current pixel as temp
            image[i][j] = image[i][width - j - 1]; //swaps the pixels in the same line 1<----->2
            image[i][width - j - 1] = cPixel; // switch pack the current pixel in the 2nd postion
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blured[height][width];
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            int rgbtRed = image[i][j].rgbtRed;
            int rgbtBlue = image[i][j].rgbtBlue;
            int rgbtGreen = image[i][j].rgbtGreen;
            float c = 1;
            //Check Left
            if(Cleft(j,height,width)){
                rgbtRed += image[i][j - 1].rgbtRed;
                rgbtBlue += image[i][j - 1].rgbtBlue;
                rgbtGreen += image[i][j - 1].rgbtGreen;
                c++;
            }
            //Check Right
            if(Cright(j,height,width)){
                rgbtRed += image[i][j + 1].rgbtRed;
                rgbtBlue += image[i][j + 1].rgbtBlue;
                rgbtGreen += image[i][j + 1].rgbtGreen;
                c++;
            }
            //check top
            if (Ctop(i,height,width))
            {
                
                rgbtRed += image[i - 1][j].rgbtRed;
                rgbtBlue += image[i - 1][j].rgbtBlue;
                rgbtGreen += image[i - 1][j].rgbtGreen;
                c++;
                if(Cleft(j,height,width)){
                    rgbtRed += image[i - 1][j - 1].rgbtRed;
                    rgbtBlue += image[i - 1][j - 1].rgbtBlue;
                    rgbtGreen += image[i - 1][j - 1].rgbtGreen;
                    c++;
                }
                if(Cright(j,height,width)){
                    rgbtRed += image[i - 1][j + 1].rgbtRed;
                    rgbtBlue += image[i - 1][j + 1].rgbtBlue;
                    rgbtGreen += image[i - 1][j + 1].rgbtGreen;
                    c++;
                }
            }
            //check bot
            if (Cbot(i,height,width))
            {
               
                rgbtRed += image[i + 1][j].rgbtRed;
                rgbtBlue += image[i + 1][j].rgbtBlue;
                rgbtGreen += image[i + 1][j].rgbtGreen;
                c++;
                if(Cleft(j,height,width)){
                    rgbtRed += image[i + 1][j - 1].rgbtRed;
                    rgbtBlue += image[i + 1][j - 1].rgbtBlue;
                    rgbtGreen += image[i + 1][j - 1].rgbtGreen;
                    c++;
                }
                if(Cright(j,height,width)){
                    rgbtRed += image[i + 1][j + 1].rgbtRed;
                    rgbtBlue += image[i + 1][j + 1].rgbtBlue;
                    rgbtGreen += image[i + 1][j + 1].rgbtGreen;
                    c++;
                }
            }
          
            blured[i][j].rgbtRed = round(rgbtRed / c);
            blured[i][j].rgbtBlue = round(rgbtBlue / c);
            blured[i][j].rgbtGreen = round(rgbtGreen / c);
        }
    }
    // replace the blured with the original;
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            image[i][j] = blured[i][j];
        }
    }
    return;
}
//check top
bool Ctop(int i,int h,int w)
{
    if((i - 1) >= 0){
        return true;
    }
    else{
    return false;
    }
}
//check bot
bool Cbot(int i,int h,int w)
{
    if((i + 1) < h){
        return true;
    }
    else{
    return false;
    }
}
//check left
bool Cleft(int j,int h,int w)
{
    if((j - 1) >= 0){
        return true;
    }
    else{
    return false;
    }
}
//check right
bool Cright(int j,int h,int w)
{
    if((j + 1) < w){
        return true;
    }
    else{
    return false;
    }
}