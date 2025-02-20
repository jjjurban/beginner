#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    printf("Fetching a random joke...\n");

    // Fetch joke
    system("curl -s \"https://v2.jokeapi.dev/joke/Any?type=single\" > joke.txt");

    // Read entire file
    FILE *file = fopen("joke.txt", "r");
    if (file) {
        char buffer[1024] = {0};
        char line[512];
        while (fgets(line, sizeof(line), file) != NULL) {
            strncat(buffer, line, sizeof(buffer) - strlen(buffer) - 1);
        }

        char *joke_start = strstr(buffer, "\"joke\": \"");
        if (joke_start) {
            joke_start += 9;  // Skip "\"joke\": \""
            char *joke_end = strstr(joke_start, "\",");
            if (joke_end) {
                *joke_end = '\0';
                printf("Joke: %s\n", joke_start);
            } else {
                printf("Joke (partial): %s\n", joke_start);
            }
        } else {
            printf("Couldn’t find the joke!\n");
        }
        fclose(file);
        remove("joke.txt");
    } else {
        printf("Oops, couldn’t read the joke file!\n");
    }

    return 0;
}