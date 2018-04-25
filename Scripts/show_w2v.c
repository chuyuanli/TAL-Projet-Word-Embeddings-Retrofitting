#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h> // mac os x
// #include <malloc.h>

const long long max_size = 2000;         // max length of strings
const long long N = 40;                  // number of closest words that will be shown
const long long max_w = 50;              // max length of vocabulary entries



int main(int argc, char **argv) {
  FILE *f;
  char st1[max_size];
  char *bestw[N];
  char file_name[max_size], st[100][max_size],file_name2[max_size];
  float dist, len, bestd[N], vec[max_size];
  long long words, size, a, b, c, d, cn, bi[100];
  char ch;
  float *M;
  char *vocab;
  // if (argc < 2) {
  //   printf("Usage: ./distance <FILE>\nwhere FILE contains word projections in the BINARY FORMAT\n");
  //   return 0;
  // }
  strcpy(file_name, argv[1]);
  strcpy(file_name2, argv[2]);
  f = fopen(file_name, "rb");
  if (f == NULL) {
    printf("Input file not found\n");
    return -1;
  }
  fscanf(f, "%lld", &words);
  fscanf(f, "%lld", &size);
  vocab = (char *)malloc((long long)words * max_w * sizeof(char));
  M = (float *)malloc((long long)words * (long long)size * sizeof(float));
  FILE *out = fopen(file_name2, "w");

  for (b = 0; b < words; b++) {
    a = 0;
    while (1) {
      vocab[b * max_w + a] = fgetc(f);
      if (feof(f) || (vocab[b * max_w + a] == ' ')) break;
      if ((a < max_w) && (vocab[b * max_w + a] != '\n')) a++;
    }
    vocab[b * max_w + a] = 0;
    for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f);
    len = 0;
    for (a = 0; a < size; a++) len += M[a + b * size] * M[a + b * size];
    len = sqrt(len);
    for (a = 0; a < size; a++) M[a + b * size] /= len;
  }

 for (b = 0; b < words; b++) {
    a = 0;
    while (1) {
      fputc(vocab[b * max_w + a],out);
      if (vocab[b * max_w + a] == 0) break;
      a++;
    }
    fprintf(out," ");
    for (a = 0; a < size; a++) fprintf(out,"%lf ",M[a + b * size]);
    fprintf(out,"\n");
  }

  // putc(vocab[0],stdout);
	fclose(f);
	fclose(out);
}
