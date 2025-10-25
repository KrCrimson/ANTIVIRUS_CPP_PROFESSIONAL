#!/usr/bin/env python3
"""
Módulo de seguridad para el servidor de monitoreo web
Maneja autenticación JWT y contraseñas seguras
"""

import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Imports opcionales para JWT
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

class WebSecurity:
    """Maneja la seguridad del servidor web de monitoreo"""
    
    def __init__(self, config_path: str = "web_security_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.secret_key = self._get_or_create_secret_key()
        
    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración de seguridad"""
        default_config = {
            "jwt_expiry_hours": 24,
            "bcrypt_rounds": 12,
            "require_auth": False,
            "default_username": "admin",
            "session_timeout": 3600,
            "max_login_attempts": 5,
            "lockout_time": 300
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except:
                pass
        
        return default_config
    
    def _get_or_create_secret_key(self) -> str:
        """Obtiene o crea una clave secreta para JWT"""
        key_file = "jwt_secret.key"
        
        if os.path.exists(key_file):
            try:
                with open(key_file, 'r') as f:
                    return f.read().strip()
            except:
                pass
        
        # Generar nueva clave secreta
        secret_key = secrets.token_urlsafe(32)
        try:
            with open(key_file, 'w') as f:
                f.write(secret_key)
        except:
            pass
        
        return secret_key
    
    def hash_password(self, password: str) -> str:
        """Hash de contraseña usando bcrypt si está disponible, sino SHA-256"""
        if BCRYPT_AVAILABLE:
            salt = bcrypt.gensalt(rounds=self.config['bcrypt_rounds'])
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        else:
            # Fallback a SHA-256 con salt
            salt = secrets.token_hex(16)
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return f"sha256${salt}${password_hash}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica una contraseña contra su hash"""
        if BCRYPT_AVAILABLE and not hashed.startswith('sha256$'):
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        elif hashed.startswith('sha256$'):
            # Formato: sha256$salt$hash
            parts = hashed.split('$')
            if len(parts) == 3:
                salt = parts[1]
                expected_hash = parts[2]
                password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
                return password_hash == expected_hash
        
        return False
    
    def create_token(self, username: str, extra_data: Optional[Dict] = None) -> Optional[str]:
        """Crea un token JWT si está disponible"""
        if not JWT_AVAILABLE:
            return None
        
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=self.config['jwt_expiry_hours']),
            'iat': datetime.utcnow()
        }
        
        if extra_data:
            payload.update(extra_data)
        
        try:
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
        except:
            return None
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verifica un token JWT"""
        if not JWT_AVAILABLE:
            return None
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def create_session(self, username: str) -> str:
        """Crea una sesión simple sin JWT"""
        session_id = secrets.token_urlsafe(32)
        session_data = {
            'session_id': session_id,
            'username': username,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=self.config['session_timeout'])).isoformat()
        }
        
        # Guardar sesión (en producción usar Redis o base de datos)
        sessions_file = "active_sessions.json"
        sessions = {}
        
        if os.path.exists(sessions_file):
            try:
                with open(sessions_file, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
            except:
                pass
        
        sessions[session_id] = session_data
        
        try:
            with open(sessions_file, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, indent=2)
        except:
            pass
        
        return session_id
    
    def verify_session(self, session_id: str) -> Optional[Dict]:
        """Verifica una sesión"""
        sessions_file = "active_sessions.json"
        
        if not os.path.exists(sessions_file):
            return None
        
        try:
            with open(sessions_file, 'r', encoding='utf-8') as f:
                sessions = json.load(f)
        except:
            return None
        
        if session_id not in sessions:
            return None
        
        session = sessions[session_id]
        expires_at = datetime.fromisoformat(session['expires_at'])
        
        if datetime.now() > expires_at:
            # Sesión expirada
            del sessions[session_id]
            try:
                with open(sessions_file, 'w', encoding='utf-8') as f:
                    json.dump(sessions, f, indent=2)
            except:
                pass
            return None
        
        return session
    
    def get_default_credentials(self) -> Dict[str, str]:
        """Obtiene credenciales por defecto"""
        users_file = "web_users.json"
        
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Crear usuario por defecto
        default_password = "admin123"
        default_users = {
            self.config['default_username']: {
                'password_hash': self.hash_password(default_password),
                'created_at': datetime.now().isoformat(),
                'is_admin': True
            }
        }
        
        try:
            with open(users_file, 'w', encoding='utf-8') as f:
                json.dump(default_users, f, indent=2)
        except:
            pass
        
        return {self.config['default_username']: default_password}
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Autentica un usuario"""
        users_file = "web_users.json"
        
        if not os.path.exists(users_file):
            # Crear usuarios por defecto
            self.get_default_credentials()
        
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
        except:
            return False
        
        if username not in users:
            return False
        
        user_data = users[username]
        password_hash = user_data.get('password_hash', '')
        
        return self.verify_password(password, password_hash)

def create_security_config():
    """Crea configuración de seguridad por defecto"""
    config = {
        "jwt_expiry_hours": 24,
        "bcrypt_rounds": 12,
        "require_auth": False,
        "default_username": "admin",
        "session_timeout": 3600,
        "max_login_attempts": 5,
        "lockout_time": 300
    }
    
    config_path = "web_security_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Configuración de seguridad creada en: {config_path}")

if __name__ == "__main__":
    # Crear configuración si se ejecuta directamente
    create_security_config()
    
    # Crear instancia de seguridad
    security = WebSecurity()
    
    # Mostrar credenciales por defecto
    credentials = security.get_default_credentials()
    print("\n📋 Credenciales por defecto:")
    for username, password in credentials.items():
        print(f"Usuario: {username}")
        print(f"Contraseña: {password}")
    
    print(f"\n🔒 JWT disponible: {JWT_AVAILABLE}")
    print(f"🔐 bcrypt disponible: {BCRYPT_AVAILABLE}")