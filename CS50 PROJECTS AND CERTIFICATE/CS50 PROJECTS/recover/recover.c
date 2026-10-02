#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    typedef uint8_t BYTE;

    BYTE buffer[512];
    int counter = 0;

    FILE *img = NULL;
    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        return 1;
    }

    char filename[8];

    while (fread(buffer, 512, 1, file) == 1)
    {
        bool statement = true;

        if (buffer[0] != 0xff)
        {
            statement = false;
        }

        if (buffer[1] != 0xd8)
        {
            statement = false;
        }

        if (buffer[2] != 0xff)
        {
            statement = false;
        }

        if ((buffer[3] & 0xf0) != 0xe0)
        {
            statement = false;
        }

        if (statement)
        {
            if (img != NULL)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", counter++);

            img = fopen(filename, "w");

            if (img == NULL)
            {
                fclose(file);
                return 1;
            }

            fwrite(buffer, 512, 1, img);
        }
        else if (img != NULL)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }

    fclose(file);

    return 0;
}
