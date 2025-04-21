#include <windows.h>

int main() {
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;

    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_MINIMIZE;

    CreateProcess(
        NULL,
        "pythonw predictionUI.py",  // command line
        NULL, NULL, FALSE,
        0, NULL, NULL,
        &si, &pi
    );

    // Close handles
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}
