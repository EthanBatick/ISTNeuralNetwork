#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <stdio.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Child process: execute the Python script
        execlp("python3", "python3", "predictionUI.py", (char *)NULL);
        perror("execlp failed");
        exit(EXIT_FAILURE);
    }

    // Parent does not wait — it detaches
    return 0;
}
