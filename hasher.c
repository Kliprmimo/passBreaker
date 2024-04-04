#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BUFFER_SIZE 256

int checker(FILE * file, unsigned
    const char * known_hash) {
    unsigned char pass_candidate[BUFFER_SIZE];
    unsigned char hash[SHA256_DIGEST_LENGTH];

    while (fgets(pass_candidate, sizeof(pass_candidate), file) != NULL) {
        pass_candidate[strcspn(pass_candidate, "\r")] = 0;
        pass_candidate[strcspn(pass_candidate, "\n")] = 0;
        SHA256(pass_candidate, strlen(pass_candidate), hash);

        // printf("Hash of '%s' is: ", pass_candidate);
        // for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        //     printf("%02x", hash[i]);
        // }

        // printf("\n");
        int equal = 1;
        for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
            if (hash[i] != known_hash[i]) {
                equal = 0;
                break;
            }
        }

        if (equal) {
            printf("Hash of '%s' is: ", pass_candidate);
            for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
                printf("%02x", hash[i]);
            }

            printf("\n");
            return 0;
        }
    }
    return -1;
}

int main(int argc, char * argv[]) {
    if (argc != 3) {
        printf("Usage: %s <input_file> <hashe>\n", argv[0]);
        return 1;
    }

    FILE * file = fopen(argv[1], "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    unsigned char known_hash[SHA256_DIGEST_LENGTH];
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sscanf(argv[2] + 2 * i, "%2hhx", & known_hash[i]);
    }

    clock_t t;
    t = clock();
    checker(file, known_hash);
    t = clock() - t;
    double time_taken = ((double) t) / CLOCKS_PER_SEC;
    fclose(file);

    printf("Hashing took %f seconds to execute \n", time_taken);
    return 0;
}