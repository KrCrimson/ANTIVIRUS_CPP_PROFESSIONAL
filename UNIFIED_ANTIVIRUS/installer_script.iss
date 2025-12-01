#define MyAppName "Antivirus Profesional"
#define MyAppVersion "1.2.1"
#define MyAppPublisher "Security Solutions"
#define MyAppExeName "professional_ui_robust.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\AntivirusProfesional
DefaultGroupName=Antivirus Profesional
OutputDir=dist
OutputBaseFilename=Antivirus_Instalador_v1.2.1_FIXED
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
VersionInfoVersion={#MyAppVersion}.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Sistema Antivirus Profesional con Monitoreo Web y Auto-instalación de Dependencias

[Files]
; Ejecutable principal
Source: "dist\professional_ui_robust_v2.exe"; DestDir: "{app}"; DestName: "professional_ui_robust.exe"; Flags: ignoreversion

; Módulos core del antivirus
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "plugins\*"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "models\*"; DestDir: "{app}\models"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "utils\*"; DestDir: "{app}\utils"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "frontend\*"; DestDir: "{app}\frontend"; Flags: ignoreversion recursesubdirs createallsubdirs

; Sistema de monitoreo web
Source: "web_system\*"; DestDir: "{app}\web_system"; Flags: ignoreversion recursesubdirs createallsubdirs

; Scripts de inicio y utilidades
Source: "professional_ui_robust.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "launcher.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "convert_logs_to_vercel.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "install_dependencies.bat"; DestDir: "{app}"; Flags: ignoreversion

; Archivos de configuración
Source: "config\*"; DestDir: "{app}\config"; Flags: onlyifdoesntexist recursesubdirs createallsubdirs
Source: "client_monitor_config.json"; DestDir: "{app}"; Flags: ignoreversion

; Dependencias Python
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements_web_monitor.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Antivirus Profesional"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\Instalar Dependencias"; Filename: "{app}\install_dependencies.bat"; WorkingDir: "{app}"
Name: "{group}\Desinstalar Antivirus"; Filename: "{uninstallexe}"
Name: "{userdesktop}\Antivirus Profesional"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"

[Dirs]
; Directorios que se crean en la instalación
Name: "{app}\logs"; Permissions: users-modify
Name: "{app}\config"; Permissions: users-modify
Name: "{app}\quarantine"; Permissions: users-modify
Name: "{app}\temp"; Permissions: users-modify

[Run]
; Instalar dependencias de Python automáticamente
Filename: "{cmd}"; Parameters: "/C pip install -r ""{app}\requirements.txt"" --user --quiet"; Description: "Instalando dependencias del sistema"; Flags: runhidden waituntilterminated; StatusMsg: "Instalando dependencias de Python..."

; Ejecutar el antivirus después de la instalación (opcional)
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar Antivirus Profesional"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Limpiar archivos generados durante el uso
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\temp"
Type: files; Name: "{app}\config\client_identity.json"

[Code]
// Verificar si Python está instalado
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Verificar si Python está instalado
  if not FileExists(ExpandConstant('{sys}\python.exe')) and 
     not FileExists(ExpandConstant('{pf}\Python*\python.exe')) then
  begin
    if MsgBox('Python no está instalado en el sistema. El antivirus requiere Python para funcionar correctamente.' + #13#10 + 
              '¿Desea continuar con la instalación de todos modos?', 
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

// Mensaje después de la instalación
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Instalación completada exitosamente.' + #13#10 + #13#10 +
           'Características instaladas:' + #13#10 +
           '- Sistema de protección en tiempo real' + #13#10 +
           '- Monitoreo web con dashboard en Vercel' + #13#10 +
           '- Todas las dependencias instaladas automáticamente' + #13#10 + #13#10 +
           'El antivirus está listo para usarse.', 
           mbInformation, MB_OK);
  end;
end;
