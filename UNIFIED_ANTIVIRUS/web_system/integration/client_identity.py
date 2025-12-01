import os
import json
import uuid
import platform
import socket
from pathlib import Path
from typing import Dict, Any, Optional

class ClientIdentity:
    """
    Maneja la identidad única del cliente antivirus.
    Genera y persiste un UUID único para esta instalación.
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.identity_file = self.config_dir / "client_identity.json"
        self.identity_data = self._load_or_create_identity()
        
    def _load_or_create_identity(self) -> Dict[str, Any]:
        """Carga la identidad existente o crea una nueva si no existe"""
        if self.identity_file.exists():
            try:
                with open(self.identity_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error cargando identidad: {e}. Generando nueva.")
        
        return self._create_new_identity()
    
    def _create_new_identity(self) -> Dict[str, Any]:
        """Genera una nueva identidad y la guarda"""
        identity = {
            "instance_id": str(uuid.uuid4()),
            "created_at": str(uuid.uuid1().time), # Timestamp simple
            "hostname": socket.gethostname(),
            "os_info": f"{platform.system()} {platform.release()}",
            "version": "1.0.0" # Podría venir de config
        }
        
        # Asegurar que el directorio existe
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.identity_file, 'w', encoding='utf-8') as f:
                json.dump(identity, f, indent=4)
            print(f"Nueva identidad de cliente generada: {identity['instance_id']}")
        except Exception as e:
            print(f"Error guardando identidad: {e}")
            
        return identity

    @property
    def instance_id(self) -> str:
        return self.identity_data.get("instance_id")
    
    @property
    def hostname(self) -> str:
        return self.identity_data.get("hostname")
        
    def get_metadata(self) -> Dict[str, Any]:
        """Retorna metadata completa del cliente"""
        return self.identity_data
