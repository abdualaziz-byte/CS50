#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main (int argc , char*argv[])
{
uint8_t header;
int16_t wavs;


FILE *input = fopen(argv[1],"r");
FILE *output = fopen(argv[2],"w");

for (int i = 0; i<44 ; i++){
 fread(&header,sizeof(header),1,input );
    fwrite(&header,sizeof(header),1,output);
}

while (fread(&wavs,sizeof(wavs),1,input) != 0){
    float factor = atof(argv[3]);
    wavs = wavs  * factor;
        fwrite(&wavs,sizeof(wavs),1,output);

}
}
