[Setup]
AppName=GymCast
AppVersion=1.0
DefaultDirName={pf}\GymCast
OutputBaseFilename=GymCastInstaller
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes

[Files]
Source: "GymCast.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "predictionUI.py"; DestDir: "{app}"; Flags: ignoreversion
; Add more files if needed:
; Source: "someAsset.png"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "{app}\GymCast.exe"; Description: "Launch GymCast"; Flags: nowait postinstall skipifsilent
