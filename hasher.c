#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include<unistd.h>

#define BUFFER_SIZE 256
// compile using:
// gcc hasher.c -o hasher -I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib -lssl -lcrypto

int checker(FILE * file, unsigned
    const char * known_hash) {
    unsigned char pass_candidate[BUFFER_SIZE];
    unsigned char hash[SHA256_DIGEST_LENGTH];
    unsigned int i = 0;

    while (fgets(pass_candidate, sizeof(pass_candidate), file) != NULL) {
        pass_candidate[strcspn(pass_candidate, "\r")] = 0;
        pass_candidate[strcspn(pass_candidate, "\n")] = 0;
        SHA256(pass_candidate, strlen(pass_candidate), hash);

        // print out hashe every 1k not to hinder performance and to make pogging in wrapper nice
        if (i%1000 == 0){
            // printf("Hash of '%s' is: ", pass_candidate);
            for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
                printf("%02x", hash[i]);
            }
            printf("\n");
            fflush(stdout);
//            usleep(1000);

        }
        i++;
        int equal = 1;
        for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
            if (hash[i] != known_hash[i]) {
                equal = 0;
                break;
            }
        }

        if (equal) {
            printf("%s ", pass_candidate);
            for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
                printf("%02x", hash[i]);
            }

//            printf("\n");
            fflush(stdout);
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
    if (checker(file, known_hash) == -1){
	return -1;
}
    t = clock() - t;
    double time_taken = ((double) t) / CLOCKS_PER_SEC;
    fclose(file);

    // printf("Hashing took %f seconds to execute \n", time_taken);
    return 0;
}
