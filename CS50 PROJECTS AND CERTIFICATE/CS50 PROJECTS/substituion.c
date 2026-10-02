#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
int main(int argc, string argv[])
{
if ( argc > 2 ) {printf("Incorrect number of words "
);
return 1;}

 string cipher = argv[1];
 int cipherlnt = strlen(cipher);

   if (cipherlnt != 26) {

    printf(" cipher isnt accurate  amount of numbers\n");
   }
   char  cipherarray[26] ;
 for (int i = 0; i <cipherlnt; i++){

 if ( !isalpha(argv[1][i]))
{
printf("cipher must not contain values other than letters\n");
return 1;
}

else {
 cipherarray[i] = argv[1][i];
}

 }
   int  count = 0;
int indexup = -1;
    for (int i = 0; i<26;i++)
  {
     indexup++;
     count = 0;mplurality
for (int j = 0; j<26; j++ ){

 if (toupper(cipherarray[j])==65+indexup){
 count++;
 }

}
if ( count !=1) { printf("the  letters are either missing or used more than once\n");
return 1;}
}

string word = get_string("Enter a word!\n");
 char temp;
   for (int k = 0; k< strlen(word); k++)
{
temp = toupper(word[k]);
   word[k] =  argv[1][temp -65];
}


printf("%s",word);

}
