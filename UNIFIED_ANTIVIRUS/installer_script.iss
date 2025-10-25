[Setup]
AppName=Antivirus Profesional
AppVersion=1.0
DefaultDirName={pf}\AntivirusProfesional
DefaultGroupName=Antivirus Profesional
OutputDir=dist
OutputBaseFilename=Antivirus_Instalador

[Files]
Source: "dist\professional_ui_robust.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs
Source: "plugins\*"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs
Source: "models\*"; DestDir: "{app}\models"; Flags: ignoreversion recursesubdirs
Source: "utils\*"; DestDir: "{app}\utils"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Antivirus Profesional"; Filename: "{app}\professional_ui_robust.exe"
Name: "{userdesktop}\Antivirus Profesional"; Filename: "{app}\professional_ui_robust.exe"

[Dirs]
Name: "{app}\logs"

& "C:/Program Files/Python313/python.exe" -m PyInstaller --onefile --windowed --icon=keylogger.ico --hidden-import=psutil --hidden-import=tkinter --hidden-import=queue --add-data "config;config" --add-data "core;core" --add-data "plugins;plugins" --add-data "models;models" 
--add-data "utils;utils" professional_ui_robust.py