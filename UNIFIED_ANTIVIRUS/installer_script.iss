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
Source: "web_templates\*"; DestDir: "{app}\web_templates"; Flags: ignoreversion recursesubdirs
Source: "web_monitor_server.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "web_security.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "client_monitor_config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Antivirus Profesional"; Filename: "{app}\professional_ui_robust.exe"
Name: "{userdesktop}\Antivirus Profesional"; Filename: "{app}\professional_ui_robust.exe"

[Dirs]
Name: "{app}\logs"
