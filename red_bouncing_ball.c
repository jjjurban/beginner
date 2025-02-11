#include <SDL.h>
#include <stdio.h>

// Screen dimensions
const int SCREEN_WIDTH = 800;
const int SCREEN_HEIGHT = 600;

// Ball dimensions and properties
const int BALL_RADIUS = 20;
int ballX = SCREEN_WIDTH / 2;
int ballY = SCREEN_HEIGHT / 2;
int ballVelX = 5;
int ballVelY = 5;

int main(int argc, char* argv[]) {
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    // Create window
    SDL_Window* window = SDL_CreateWindow("Bouncing Ball",
                                          SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                          SCREEN_WIDTH, SCREEN_HEIGHT,
                                          SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Create renderer
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Game loop
    SDL_Event e;
    int quit = 0;
    while (!quit) {
        // Handle events
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                quit = 1;
            }
        }

        // Move the ball
        ballX += ballVelX;
        ballY += ballVelY;

        // Ball collision with walls
        if (ballX - BALL_RADIUS < 0 || ballX + BALL_RADIUS > SCREEN_WIDTH) {
            ballVelX = -ballVelX;
        }
        if (ballY - BALL_RADIUS < 0 || ballY + BALL_RADIUS > SCREEN_HEIGHT) {
            ballVelY = -ballVelY;
        }

        // Clear screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Set ball color to red
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);

        // Draw ball
        for (int w = 0; w < BALL_RADIUS * 2; w++) {
            for (int h = 0; h < BALL_RADIUS * 2; h++) {
                int dx = BALL_RADIUS - w; // horizontal offset
                int dy = BALL_RADIUS - h; // vertical offset
                if ((dx * dx + dy * dy) <= (BALL_RADIUS * BALL_RADIUS)) {
                    SDL_RenderDrawPoint(renderer, ballX + dx, ballY + dy);
                }
            }
        }

        // Update screen
        SDL_RenderPresent(renderer);

        // Delay for smooth animation
        SDL_Delay(16);  // ~60 FPS
    }

    // Clean up
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
