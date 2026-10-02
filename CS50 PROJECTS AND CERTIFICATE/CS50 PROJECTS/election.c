#include <cs50.h>
#include <stdio.h>
#include <string.h>
    void vote(string y);
void checker();

typedef struct
{

    string name;
    int votes;

}
candidate;

candidate candidates[3];
int main(void)
{

candidates[0].name = "alice";
candidates[1].name = "bob";
candidates[2].name = "charlie";


    int x = get_int("number of voters ?");



  for(int FR  = 0;FR<x;FR++)
{
        string y = get_string("winner?\n");
vote(y);
}

checker();

}
void vote(string y)
{
    for (int count  = 0;count<3;count++)
{
if (strcmp(y, candidates[count].name) == 0) {candidates[count].votes++;}

}
}
void checker()
{
    if (candidates[0].votes>candidates[1].votes && candidates[0].votes>candidates[2].votes)
    {printf("winner is alice\n");}

    if (candidates[1].votes>candidates[0].votes && candidates[1].votes>candidates[2].votes)
    {printf("winner is bob\n");}

    if (candidates[2].votes>candidates[1].votes && candidates[2].votes>candidates[0].votes)
    {printf("winner is charlie\n");}
}
