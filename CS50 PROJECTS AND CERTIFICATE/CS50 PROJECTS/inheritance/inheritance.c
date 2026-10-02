// Simulate genetic inheritance of blood type
#define _DEFAULT_SOURCE
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct person
{
    struct person *parents[2];
    char alleles[2];
} person;

const int GENERATIONS = 3;
const int INDENT_LENGTH = 4;

person *create_family(int generations);
void print_family(person *p, int generation);
void free_family(person *p);
char random_allele();

int main(void)
{
    srandom(time(0));

    person *p = create_family(GENERATIONS);

    // make family tree of blood types
    print_family(p, 0);

    free_family(p);
}

person *create_family(int generations)
{
 person *p = malloc(sizeof(person));

    if (generations > 1)
    {
        person *father = create_family(generations - 1);
        person *mother = create_family(generations - 1);
          p->parents[0] = father;
        p->parents[1] = mother;

                int r = rand() % 2;
        p->alleles[0] = father->alleles[r];
                 r = rand() % 2;

                p->alleles[1] = mother->alleles[r];


    }

    else
    {
        p->parents[0] = NULL;
                p->parents[1] = NULL;


         p->alleles[0] = random_allele();
        p->alleles[1] = random_allele();
    }

    return p;
}

void free_family(person *p)

{
 if (p->parents[0] == NULL)
 {
    free(p);
 }
else{
    free_family(p->parents[0]);
        free_family(p->parents[1]);
        free(p);

}
}

void print_family(person *p, int generation)
{
    // Handle base case
    if (p == NULL)
    {
        return;
    }

    for (int i = 0; i < generation * INDENT_LENGTH; i++)
    {
        printf(" ");
    }

    if (generation == 0)
    {
        printf("Child (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }
    else if (generation == 1)
    {
        printf("Parent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }
    else
    {
        for (int i = 0; i < generation - 2; i++)
        {
            printf("Great-");
        }
        printf("Grandparent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }

    print_family(p->parents[0], generation + 1);
    print_family(p->parents[1], generation + 1);
}

char random_allele()
{
    int r = random() % 3;
    if (r == 0)
    {
        return 'A';
    }
    else if (r == 1)
    {
        return 'B';
    }
    else
    {
        return 'O';
    }
}
