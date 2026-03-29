[Setup]
AppName=Study AI
AppVersion=1.0
DefaultDirName={pf}\StudyAI
DefaultGroupName=Study AI
OutputBaseFilename=StudyAI_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=app.ico

[Files]
Source: "dist\launcher.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Study AI"; Filename: "{app}\launcher.exe"
Name: "{commondesktop}\Study AI"; Filename: "{app}\launcher.exe"

[Run]
Filename: "{app}\launcher.exe"; Description: "Launch Study AI"; Flags: nowait postinstall skipifsilent
