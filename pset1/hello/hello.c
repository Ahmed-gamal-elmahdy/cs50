#include <stdio.h>
#include <cs50.h>
int main(void)
{
    string name = get_string("Type your name!\n");  //get names
    printf("hello, %s.\n", name); //print the output
}