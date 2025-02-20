#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define FILENAME "game_stats.txt"

void update_stats(int guesses, int number) {
    FILE *file = fopen(FILENAME, "a");
    if (file) {
        fprintf(file, "%d %d\n", guesses, number);
        fclose(file);
    }
}

void read_stats(int *total_games, float *avg_guesses, int *avg_number) {
    FILE *file = fopen(FILENAME, "r");
    int guesses, number, count = 0, sum_guesses = 0, sum_numbers = 0;
    if (file) {
        while (fscanf(file, "%d %d", &guesses, &number) == 2) {
            sum_guesses += guesses;
            sum_numbers += number;
            count++;
        }
        fclose(file);
    }
    *total_games = count;
    *avg_guesses = count ? (float)sum_guesses / count : 0;
    *avg_number = count ? sum_numbers / count : 50;
}

int main() {
    srand(time(NULL));
    int low = 1, high = 100, guess, response, guesses = 0, player_number;
    int total_games, avg_number;
    float avg_guesses;

    read_stats(&total_games, &avg_guesses, &avg_number);
    low = avg_number - 20 > 1 ? avg_number - 20 : 1;
    high = avg_number + 20 < 100 ? avg_number + 20 : 100;

    printf("Think of a number between 1 and 100. I’ll guess!\n");
    while (1) {
        guess = low + (high - low) / 2;
        printf("Guess #%d: %d. Too high (1), too low (2), or correct (0)? ", guesses + 1, guess);
        scanf("%d", &response);
        guesses++;

        if (response == 0) {
            printf("Got it in %d guesses!\n", guesses);
            player_number = guess;
            break;
        } else if (response == 1) {
            high = guess - 1;
        } else if (response == 2) {
            low = guess + 1;
        }

        if (low > high) {
            printf("Something’s off—let’s restart!\n");
            return 1;
        }
    }

    update_stats(guesses, player_number);
    read_stats(&total_games, &avg_guesses, &avg_number);
    printf("Stats: %d games played, avg guesses: %.1f, avg winning number: %d\n", 
           total_games, avg_guesses, avg_number);

    return 0;
}