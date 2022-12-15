#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* encode(char* s, int len, int* newlen) {
    *newlen = len * 2;
    char* ret = malloc(*newlen);
    int i = 0;
    int x = 0;
    while (i < len) {
	char c = s[i];
	int j;
	for (j = i + 1; j < len && s[j] == c; j++);
	int n = j - i;
	i = j;
	if (n > 9) {
	    fprintf(stderr, "n too big\n");
	    exit(1);
	}
	if (x + 1 > *newlen) {
	    *newlen *= 2;
	    ret = realloc(ret, *newlen);
	}
	ret[x++] = n + '0';
	ret[x++] = c;
    }
    ret[x] = '\0';
    *newlen = x;
    return ret;
}

int main() {
    char* s = "1321131112";

    int len = strlen(s), newlen;

    for (int i = 0; i < 50; i++) {
	s = encode(s, len, &newlen);
	len = newlen;
    }

    printf("%i\n", len);
}
