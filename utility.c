// Instead of text:
// fprintf(fp, "%s,%d\n", plate, timestamp);

// Use Binary Structs:
typedef struct {
    char plate[20];
    time_t timestamp;
    int is_parked;
} VehicleRecord;

// Save:
fwrite(&record, sizeof(VehicleRecord), 1, fp);
