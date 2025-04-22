#include <stdio.h>
#include <stdlib.h>

int is_installed(const char *package) {
    char cmd[256];
    snprintf(cmd, sizeof(cmd), "python3 -m pip show %s > /dev/null 2>&1", package);
    return system(cmd) == 0;
}

int main() {
    printf("Installing dependencies if needed...\n");
    const char *packages[] = { "pygame", "pillow", "numpy" };
    for (int i = 0; i < 3; ++i) {
        if (!is_installed(packages[i])) {
            printf("Installing %s...\n", packages[i]);
            char install_cmd[256];
            snprintf(install_cmd, sizeof(install_cmd), "python3 -m pip install %s", packages[i]);
            system(install_cmd);
        } else {
            printf("%s is already installed.\n", packages[i]);
        }
    }

    // Run the Python script
    printf("Launching predictionUI.py...\n");
    system("python3 predictionUI.py");

    return 0;
}
