#include <stdio.h>
#include <string.h>
#include <ctype.h>  // Required for isalnum()
#include "utility.h"

#define MAX_PLATE_LEN 20

int validate_plate(const char *plate) {
    for (int i = 0; plate[i] != '\0'; i++) {
        if (!isalnum(plate[i]) && plate[i] != '-') {
            return 0; // Invalid
        }
    }
    return 1; // Valid
}

// ... inside main(), replace the loop with:
if (validate_plate(safe_plate)) {
    // Call existing park function...
int main(int argc, char *argv[]) {
    // --- MODE 1: AUTOMATED AI GATE (CLI Mode) ---
    // --- MODE 1: AUTOMATED AI GATE (CLI Mode) ---
    if (argc > 1) {
        if (strcmp(argv[1], "--park") == 0 && argc == 3) {
            // ... (your existing parking logic) ...
            return 0;
        } else {
            // NEW BLOCK: Handle invalid arguments
            printf("[Error] Invalid Usage.\nUsage: ./app --park <LICENSE-PLATE>\n");
            return 1; // Exit with error code
        }
    }
            
            // SECURITY: Prevent Buffer Overflow using strncpy
            strncpy(safe_plate, argv[2], MAX_PLATE_LEN - 1);
            safe_plate[MAX_PLATE_LEN - 1] = '\0'; // Ensure null-termination

            // SECURITY: Input Sanitization (Alphanumeric + Hyphens only)
            int valid = 1;
            for (int i = 0; safe_plate[i] != '\0'; i++) {
                if (!isalnum(safe_plate[i]) && safe_plate[i] != '-') {
                    valid = 0;
                    break;
                }
            }

            if (valid) {
                // Call the existing park function (ensure utility.c handles this logic)
                // For demonstration, we print the confirmation needed for the AI node
                printf("[C-Backend] Validated Plate: %s\n", safe_plate);
                printf("[C-Backend] Storage Transaction Complete.\n");
                // In a real scenario, you would call: park_vehicle_db(safe_plate);
            } else {
                printf("[Error] Security Alert: Invalid characters in license plate.\n");
            }
            return 0; // Exit immediately after handling AI request
        }
    }

    // --- MODE 2: MANUAL OPERATOR (Menu Mode) ---
    int choice;
    while(1) {
        printf("\n--- Smart Parking Node (Maintenance Mode) ---\n");
        printf("1. View Live Status\n2. Manual Park\n3. Manual Exit\n");
        printf("4. Search Log\n5. Exit System\n");
        printf("Select Operation: ");
        
        if (scanf("%d", &choice) != 1) {
            while(getchar() != '\n'); // Clear buffer on invalid input
            continue;
        }
        
        // Call your existing functions from utility.c here
        // switch(choice) { ... }
        if (choice == 5) break;
    }
    return 0;
}
