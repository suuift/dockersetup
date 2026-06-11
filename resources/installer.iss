; DockerSetup Inno Setup Script
; Generates a user-level standalone setup installer for Windows

[Setup]
AppName=DockerSetup
AppVersion=1.5.32
AppPublisher=suuift
AppPublisherURL=https://github.com/suuift/dockersetup
DefaultDirName={localappdata}\DockerSetup
DefaultGroupName=DockerSetup
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=dockersetupinstaller
SetupIconFile=app.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
ChangesEnvironment=no

[Files]
Source: "..\dist\dockersetup.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DockerSetup"; Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -Command ""& '{app}\dockersetup.exe'"""; WorkingDir: "{userdocs}"
Name: "{userdesktop}\DockerSetup"; Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -Command ""& '{app}\dockersetup.exe'"""; WorkingDir: "{userdocs}"

[Run]
Description: "Launch DockerSetup"; Filename: "powershell.exe"; Parameters: "-NoExit -ExecutionPolicy Bypass -Command ""& '{app}\dockersetup.exe'"""; WorkingDir: "{userdocs}"; Flags: postinstall nowait
