#include <stdio.h>
#include <math.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>

int main() {
    float A = 0, B = 0;
    float i, j;
    int k;
    struct winsize w;
    int cols, rows, buffer_size;
    float *z;
    char *b;

    for (;;) {
        // Get terminal size on each iteration
        ioctl(STDOUT_FILENO, TIOCGWINSZ, &w);
        cols = w.ws_col;
        rows = w.ws_row;
        buffer_size = cols * rows;

        // Allocate memory dynamically for buffers
        z = (float *)calloc(buffer_size, sizeof(float));
        b = (char *)calloc(buffer_size, sizeof(char));

        memset(b, ' ', buffer_size); // Fill buffer with spaces
        memset(z, 0, buffer_size * sizeof(float)); // Zero depth buffer

        for (j = 0; j < 6.28; j += 0.07) {
            for (i = 0; i < 6.28; i += 0.02) {
                float c = sin(i);
                float d = cos(j);
                float e = sin(A);
                float f = sin(j);
                float g = cos(A);
                float h = d + 2;
                float D = 1 / (c * h * e + f * g + 5);
                float l = cos(i);
                float m = cos(B);
                float n = sin(B);
                float t = c * h * g - f * e;
                int x = cols / 2 + (cols / 2) * D * (l * h * m - t * n);
                int y = rows / 2 + (rows / 2) * D * (l * h * n + t * m);
                int o = x + cols * y;
                int N = 8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n);
                if (rows > y && y > 0 && x > 0 && cols > x && D > z[o]) {
                    z[o] = D;
                    b[o] = ".,-~:;=!*#$@"[N > 0 ? N : 0];
                }
            }
        }

        printf("\x1b[2J\x1b[H"); // Clear screen and move cursor to top-left
        for (k = 0; k < buffer_size; k++) {
            putchar(k % cols ? b[k] : '\n');
        }

        free(z); // Free dynamically allocated memory
        free(b);

        A += 0.04; // Rotation speed for A
        B += 0.02; // Rotation speed for B
        usleep(30000); // Frame delay (30ms)
    }
    return 0;
}
