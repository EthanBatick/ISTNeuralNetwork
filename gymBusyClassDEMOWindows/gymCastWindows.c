#include <windows.h>
#include <stdio.h>

int run(const char *cmd) {
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    if (!CreateProcess(NULL, (LPSTR)cmd, NULL, NULL, FALSE,
                       CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
        printf("Failed: %s\n", cmd);
        return 1;
    }
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return 0;
}

int is_installed(const char *package) {
    char cmd[256];
    snprintf(cmd, sizeof(cmd), "cmd.exe /C python -m pip show %s >nul 2>&1", package);
    return system(cmd) == 0;
}

int main() {
    printf("Installing dependencies if needed...\n");
    const char *packages[] = { "pygame", "pillow", "numpy" };
    for (int i = 0; i < 3; ++i) {
        if (!is_installed(packages[i])) {
            printf("Installing %s...\n", packages[i]);
            char install_cmd[256];
            snprintf(install_cmd, sizeof(install_cmd), "cmd.exe /C python -m pip install %s", packages[i]);
            run(install_cmd);
        } else {
            printf("%s is already installed.\n", packages[i]);
        }
    }

    // Get the folder where the .exe is
    char exePath[MAX_PATH];
    GetModuleFileName(NULL, exePath, MAX_PATH);
    char *lastSlash = strrchr(exePath, '\\');
    if (lastSlash) *lastSlash = '\0'; // truncate to directory

    // Run predictionUI.py from same folder
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    printf("Launching predictionUI.py...\n");
    if (!CreateProcess(NULL, "python3 predictionUI.py", NULL, NULL, FALSE,
                       CREATE_NO_WINDOW, NULL, exePath, &si, &pi)) {
        printf("Failed to launch predictionUI.py\n");
        return 1;
    }

    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}
