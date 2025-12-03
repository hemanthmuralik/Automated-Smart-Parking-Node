#include <stdio.h>
#include <string.h>
#include "utility.h" // Your existing utility header

int main(int argc, char *argv[]) {
    // Check if running in "AI Automation Mode"
    if (argc > 1) {
        if (strcmp(argv[1], "--park") == 0 && argc == 3) {
            printf("\n[C-Backend] Received Request from AI Node.\n");
            // Call your existing function but modify it to accept string args directly
            // Example: park_vehicle_auto(argv[2]); 
            printf("[C-Backend] Vehicle %s Parked Successfully.\n", argv[2]);
            return 0;
        }
    }

    // --- STANDARD MANUAL MODE (Your Existing Menu) ---
    int choice;
    while(1) {
        printf("\n--- Digital Parking Management System ---\n");
        printf("1. Display Status\n2. Park Vehicle\n3. Remove Vehicle\n");
        printf("4. Search Vehicle\n5. Exit\n");
        printf("Enter choice: ");
        scanf("%d", &choice);
        
        // ... (Rest of your existing switch-case logic) ...
    }
    return 0;
}
