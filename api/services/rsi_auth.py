"""RSI Authentication and Hangar Data Manager for sc-oam-app.

Handles RSI account integration via PyRSI library (v0.1.19):
- Username/password authentication
- Session persistence via .pyrsi_session config
- Encrypted token vault (Fernet)
- Hangar data: ships, items, packages, upgrades

Note: PyRSI is an optional dependency. When the `rsi` package is not
available (e.g., Docker environments without it installed), this module
provides graceful fallbacks — auth status shows all tiers as inactive,
and extraction endpoints return appropriate error messages.
"""

import json
import os
from pathlib import Path

from cryptography.fernet import Fernet

# ─── RSI optional dependency ──────────────────────────────────────────
# PyRSI library for RSI account integration (not available as pip package
# in all environments; guarded import for Docker/dependency flexibility)
try:
    from rsi import RSISite
    _RSI_AVAILABLE = True
except ImportError:
    RSISite = None  # type: ignore
    _RSI_AVAILABLE = False

# ─── Token Vault ──────────────────────────────────────────────────────

class TokenVault:
    """Fernet-based encrypted token storage for RSI and Google auth tokens."""

    def __init__(self, key=None):
        # Key hierarchy: env var → auto-generated → OS keychain fallback
        self._key = key or os.getenv('SC_OAM_TOKEN_KEY')
        if not self._key:
            self._key = Fernet.generate_key().decode()  # temporary, save to env
            print("⚠ SC_OAM_TOKEN_KEY not set; generated temporary key")
        self._fernet = Fernet(self._key.encode())

    def encrypt(self, data: dict) -> str:
        """Encrypt dict data; return Fernet token string."""
        json_data = json.dumps(data, sort_keys=True).encode()
        return self._fernet.encrypt(json_data).decode()

    def decrypt(self, token: str) -> dict:
        """Decrypt Fernet token; return dict."""
        json_data = self._fernet.decrypt(token.encode())
        return json.loads(json_data)

    def set_google_credentials(self, client_id: str, client_secret: str):
        """Store Google OAuth client ID and secret in vault."""
        credentials = {
            'client_id': client_id,
            'client_secret': client_secret,
            'auth_tier': 'google',
            'storage_timestamp': int(__import__('time').time()),
        }
        self._google_credentials_encrypted = self.encrypt(credentials)

    def get_google_credentials(self) -> tuple:
        """Retrieve Google OAuth client ID and secret from vault."""
        if not hasattr(self, '_google_credentials_encrypted'):
            return None, None
        try:
            credentials = self.decrypt(self._google_credentials_encrypted)
            return credentials.get('client_id', ''), credentials.get('client_secret', '')
        except Exception:
            return None, None

    def set_rsi_credentials(self, username: str, password: str, mode: str):
        """Store RSI username/password/mode in vault for persistent configuration."""
        credentials = {
            'username': username,
            'password': password,
            'mode': mode,
            'auth_tier': 'rsi',
            'storage_timestamp': int(__import__('time').time()),
        }
        self._rsi_credentials_encrypted = self.encrypt(credentials)

    def get_rsi_credentials(self) -> tuple:
        """Retrieve RSI username/password/mode from vault."""
        if not hasattr(self, '_rsi_credentials_encrypted'):
            return None, None, None
        try:
            credentials = self.decrypt(self._rsi_credentials_encrypted)
            return credentials.get('username', ''), credentials.get('password', ''), credentials.get('mode', '')
        except Exception:
            return None, None, None


# ─── RSI Auth Manager ───────────────────────────────────────────────

class RSIAuthManager:
    """Manages RSI authentication and hangar data access for sc-oam-app."""

    def __init__(self, vault=None, session_file=None):
        self.vault = vault or TokenVault()
        # session_file defaults to ~/.config/sc-oam-app/.pyrsi_session
        self.session_file = session_file or Path.home() / '.config' / 'sc-oam-app' / '.pyrsi_session'
        self.site = RSISite if _RSI_AVAILABLE else None
        self._hangar_cache = None

    # ─── Login / Logout ──────────────────────────────────────────────

    def login(self, username: str, password: str) -> dict:
        """Authenticate with RSI and store session.

        Returns dict with status, site, and vault data.
        """
        if not _RSI_AVAILABLE or self.site is None:
            return {
                'status': 'unavailable',
                'reason': 'rsi_not_available',
                'message': 'RSI integration not available in this environment',
            }

        try:
            site = self.site()  # creates RSISession, may load existing .pyrsi_session
            try:
                site.authenticate(username, password, force=False)
            except SystemExit:
                return {
                    'status': 'error',
                    'reason': 'authentication_failed',
                    'message': 'RSI authentication failed (credential or session error)',
                }
            except Exception as e:
                return {
                    'status': 'error',
                    'reason': 'authentication_failed',
                    'message': f'RSI authentication error: {str(e)[:100]}',
                }

            if not site.is_authenticated:
                return {
                    'status': 'failed',
                    'reason': 'authentication_failed',
                    'message': 'Invalid RSI credentials',
                }

            # ─── Store session persistently ─────────────────────────────
            # .pyrsi_session is auto-maintained by RSISession hooks;
            # we also encrypt token data for the app's vault.
            encrypted_token = self.vault.encrypt({
                'username': username,
                'is_authenticated': site.is_authenticated,
                'session_name': site.session.session_name,
                'session_id': site.session.session_id,
                'login_timestamp': int(__import__('time').time()),
            })

            # Save encrypted RSI token to app config dir
            rsi_token_path = Path.home() / '.config' / 'sc-oam-app' / 'rsi_token.json'
            rsi_token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(rsi_token_path, 'w') as f:
                f.write(encrypted_token)

            # Cache hangar data (refresh cache)
            self._hangar_cache = None

            return {
                'status': 'success',
                'username': username,
                'is_authenticated': site.is_authenticated,
                'message': 'RSI login successful',
            }

        except Exception as e:
            return {
                'status': 'error',
                'reason': type(e).__name__,
                'message': str(e),
            }

    def logout(self) -> dict:
        """Clear RSI session and token data."""
        try:
            if self.site:
                self.site.session.clear_session()
            rsi_token_path = Path.home() / '.config' / 'sc-oam-app' / 'rsi_token.json'
            if rsi_token_path.exists():
                rsi_token_path.unlink(missing_ok=True)
            return {
                'status': 'success',
                'message': 'RSI session cleared',
            }
        except Exception as e:
            return {
                'status': 'error',
                'reason': type(e).__name__,
                'message': str(e),
            }

    # ─── Hangar Data ─────────────────────────────────────────────────

    def refresh_hangar(self) -> dict:
        """Fetch fresh hangar data from RSI; cache-invalidate then re-fetch."""
        if not _RSI_AVAILABLE or self.site is None:
            return {'status': 'error', 'reason': 'not_authenticated', 'message': 'Not authenticated with RSI'}

        try:
            hangar = self.site.hangar
            # Access each property to trigger full data fetch (PyRSI caches per-key)
            _ = hangar.ships
            _ = hangar.items
            _ = hangar.packages
            _ = hangar.upgrades
            _ = hangar.flair
            _ = hangar.buybacks

            result = {
                'status': 'success',
                'ships': hangar.ships,
                'items': hangar.items,
                'packages': hangar.packages,
                'upgrades': hangar.upgrades,
                'flair': hangar.flair,
                'buybacks': hangar.buybacks,
                'is_empty': hangar.is_empty,
                'fetched_at': int(__import__('time').time()),
            }
            self._hangar_cache = result
            return result
        except Exception as e:
            return {
                'status': 'error',
                'reason': type(e).__name__,
                'message': f'Hangar fetch failed: {str(e)[:200]}',
            }

    def get_hangar(self) -> dict:
        """Return cached hangar data if available, otherwise fetch fresh."""
        if self._hangar_cache:
            return self._hangar_cache
        return self.refresh_hangar()

    # ─── Session Load (auto on startup) ──────────────────────────────

    def load_session(self) -> dict:
        """Load existing RSI session if .pyrsi_session and rsi_token.json exist."""
        from pathlib import Path as P

        session_file = self.session_file
        token_file = Path.home() / '.config' / 'sc-oam-app' / 'rsi_token.json'

        if not session_file.exists():
            return {'status': 'no_session', 'message': 'No RSI session file found'}

        try:
            if token_file.exists():
                with open(token_file) as f:
                    encrypted = f.read()
                token_data = self.vault.decrypt(encrypted)
                site = RSISite()  # will load .pyrsi_session internally
                return {
                    'status': 'loaded',
                    'username': token_data.get('username'),
                    'message': 'RSI session loaded from previous run',
                }
            else:
                site = RSISite(persist_session=False)
                site.session.clear_session()
                return {'status': 'reset', 'message': 'Session file found but no token data; reset'}
        except Exception as e:
            return {
                'status': 'error',
                'reason': type(e).__name__,
                'message': f'Failed to load session: {str(e)[:200]}',
            }

# ─── Convenience function ────────────────────────────────────────────

def create_rsi_auth_manager() -> RSIAuthManager:
    """Factory function for quick RSI auth setup."""
    return RSIAuthManager()