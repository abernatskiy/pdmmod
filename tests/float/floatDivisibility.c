#include <stdio.h>
#include <math.h>

void checkDivisibility(float a, float b)
{
    float r = b/a;
    if(floorf(r) == r)
        printf("Division successful\n");
    else
        printf("Division unsuccessful, ratio %le\n", r);
}

int main(int argc, char** argv)
{
    checkDivisibility(0.3f, 300.f);

    float a = 0.1f;
    float b = 10.f;
    checkDivisibility(a, b);

    int r = (int) (b/a);
    float c = 0.f;
    int i;
    for(i=0; i<r; i++)
        c = c + a;
    if(c == b)
        printf("Iteration successful\n");
    else
        printf("Iteration unsuccessful, numerical error of %le detected\n", c - b);

    r = (int) (b/a);
    c = 0.f;
    for(i=0; i<=r; i++)
        c = ((float) i)*a;
    if(c == b)
        printf("Iteration successful\n");
    else
        printf("Iteration unsuccessful, numerical error of %le detected\n", c - b);
    return 0;
}
