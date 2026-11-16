"""Authentication endpoints for sc-oam-app.

Three-tier auth:
  Tier 1: OS Keychain (admin)
  Tier 2: Google OAuth (primary user)
  Tier 3: RSI Account (pledge hangar data)
"""

import json
import os
from pathlib import Path
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from api.services.rsi_auth import RSIAuthManager, TokenVault, create_rsi_auth_manager

router = APIRouter(prefix="/auth", tags=["auth"])


# ─── Request/Response Models ─────────────────────────────────────────

class RSILogin(BaseModel):
    """Login with RSI username/password."""
    username: str = Field(..., min_length=1, max_length=50, description="RSI account username/handle")
    password: str = Field(..., min_length=1, max_length=128, description="RSI account password")


class RSIHangarResponse(BaseModel):
    """Hangar data response schema."""
    ships: list = Field(default_factory=list, description="List of ship objects from RSI hangar")
    items: list = Field(default_factory=list, description="List of item objects from RSI hangar")
    packages: list = Field(default_factory=list, description="List of package objects from RSI hangar")
    upgrades: list = Field(default_factory=list, description="List of upgrade objects from RSI hangar")
    flair: list = Field(default_factory=list, description="List of flair objects from RSI hangar")
    buybacks: list = Field(default_factory=list, description="List of buyback objects from RSI hangar")
    is_empty: bool = Field(default=False, description="Whether the hangar is empty")
    fetched_at: int = Field(default_factory=int, description="Unix timestamp of data fetch")


class AuthStatus(BaseModel):
    """Current authentication status."""
    authenticated: bool = False
    auth_tier: Optional[str] = None  # "os", "google", "rsi", or None
    user: Optional[Dict[str, Any]] = None
    tiers: Dict[str, Any] = Field(default_factory=dict)


class GoogleLogin(BaseModel):
    """Initiate Google OAuth 2.0 login."""
    redirect_url: Optional[str] = Field(
        default=None,
        description="Custom redirect URL; defaults to configured backend URL",
    )


class GoogleCallback(BaseModel):
    """Google OAuth callback with authorization code."""
    code: str = Field(..., description="Authorization code from Google OAuth consent screen")


class GoogleUserInfo(BaseModel):
    """Google user information profile."""
    email: str = Field(..., description="User's Google email address")
    name: str = Field(..., description="User's full name")
    picture: Optional[str] = Field(None, description="URL to user's profile picture")
    sub: str = Field(..., description="Google user ID")


# ─── Global Auth Managers (lazy-loaded via dependencies) ─────────────

# We'll create per-request instances via dependency injection below


# ─── Dependency: Get RSI Auth Manager ────────────────────────────────

def get_rsi_auth() -> RSIAuthManager:
    """Provide an RSIAuthManager instance per request."""
    return create_rsi_auth_manager()


# ─── Auth Status ───────────────────────────────────────────────────

# ─── Auth Status ───────────────────────────────────────────────────

@router.get("/status", response_model=AuthStatus, summary="Check authentication status")
async def auth_status(rsi_auth: RSIAuthManager = Depends(get_rsi_auth)) -> AuthStatus:
    """Return current auth state across all tiers."""
    # Check OS admin (simplified: check if keyring has admin creds)
    # Check Google OAuth (would check session/cookies for Google user)
    # Check RSI
    rsi_status = False
    if rsi_auth.site is not None:
        # Create a temporary RSISite instance to check authentication status
        # without full login flow
        try:
            site = rsi_auth.site()
            rsi_status = site.is_authenticated if site else False
        except Exception:
            rsi_status = False

    # Check Google OAuth status
    # In a full implementation, this would check encrypted cookies or
    # a server-side session store for the Google user token.
    # For now, we check if Google user info has been stored from a
    # successful OAuth callback.
    from pathlib import Path as P
    google_user = None
    google_token_path = P.home() / '.config' / 'sc-oam-app' / 'google_token.json'
    if google_token_path.exists():
        try:
            import json
            token_data = json.loads(google_token_path.read_text())
            # Expect format: {"user": {"email": "...", "name": "...", ...}, "auth_tier": "google", ...}
            google_user = token_data.get('user')
            google_active = google_user is not None
        except Exception:
            google_active = False
            google_user = None
    else:
        google_active = False

    tiers = {
        "os": {"active": False},  # placeholder; real check via keyring
        "google": {
            "active": google_active,
            "user": google_user or {},
            "since": int(__import__('time').time()) if google_active else None,
        },
        "rsi": {
            "active": rsi_status,
            "since": int(__import__('time').time()) if rsi_status else None,
        },
    }

    # Determine primary auth tier (priority: os > google > rsi)
    primary = None
    if tiers["os"]["active"]:
        primary = "os"
    elif tiers["google"]["active"]:
        primary = "google"
    elif rsi_status:
        primary = "rsi"

    return AuthStatus(
        authenticated=any(t["active"] for t in tiers.values()),
        auth_tier=primary,
        tiers=tiers,
    )


# ─── RSI Login ─────────────────────────────────────────────────────

@router.post("/rsi/login", summary="Authenticate with RSI account")
async def rsi_login(
    payload: RSILogin,
    rsi_auth: RSIAuthManager = Depends(get_rsi_auth),
) -> Dict[str, Any]:
    """Authenticate with RSI via username/password.

    - On success: stores session in .pyrsi_session config, encrypts token data
      to ~/.config/sc-oam-app/rsi_token.json, returns success status.
    - On failure: returns error detail (invalid credentials, 2FA required, etc.).
    """
    # Check vault first for stored RSI credentials
    vault = rsi_auth.vault
    vault_username, vault_password, vault_mode = vault.get_rsi_credentials()
    # Use vault credentials if available, otherwise fall back to payload
    username = vault_username or payload.username
    password = vault_password or payload.password
    # Mode is not in the payload model, use vault mode if available, default to 'standard'
    mode = vault_mode or 'standard'

    result = rsi_auth.login(username, password)
    if result['status'] == 'success':
        return {
            'status': 'success',
            'message': result['message'],
            'auth_tier': 'rsi',
            'username': result['username'],
        }
    elif result['status'] in ('unavailable', 'error', 'failed'):
        raise HTTPException(
            status_code=400,
            detail=result.get('message', 'RSI authentication failed'),
        )
    else:
        raise HTTPException(
            status_code=400,
            detail='RSI authentication failed: unknown error',
        )


@router.post("/rsi/logout", summary="Clear RSI session")
async def rsi_logout(rsi_auth: RSIAuthManager = Depends(get_rsi_auth)) -> Dict[str, Any]:
    """Clear the RSI session and token data.

    - Calls site.session.clear_session()
    - Removes ~/.config/sc-oam-app/rsi_token.json
    - User's auth tier reverts to exclude 'rsi'.
    """
    result = rsi_auth.logout()
    if result['status'] == 'success':
        return {'status': 'success', 'message': result['message']}
    else:
        raise HTTPException(status_code=400, detail=result.get('message', 'Failed to clear session'))


# ─── Google OAuth 2.0 ─────────────────────────────────────────────────

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8000/api/auth/google/callback")

# ── Google OAuth Credential Vault ──────────────────────────────────────
# Credentials can be set via API (from prototype UI) or .env file.
# Vault takes priority over .env for persistent per-session configuration.
from api.services.rsi_auth import create_rsi_auth_manager
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@router.get("/google/login", summary="Initiate Google OAuth 2.0 login")
async def google_login(request: Request) -> Response:
    """Redirect the user to Google's OAuth consent screen.

    The user will be asked to select a Google account and grant permission.
    After consent, Google will redirect back to GOOGLE_REDIRECT_URI with
    an authorization code as a query parameter.
    """
    # Check vault first, then .env for Google OAuth credentials
    vault = TokenVault()
    vault_client_id, vault_client_secret = vault.get_google_credentials()
    # Use vault credentials if available, otherwise fall back to .env
    client_id = vault_client_id or GOOGLE_CLIENT_ID
    client_secret = vault_client_secret or GOOGLE_CLIENT_SECRET

    # Build the OAuth 2.0 authorization URL
    params = {
        "client_id": client_id,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    return Response(content="", status_code=307, headers={"Location": auth_url})


@router.get("/google/callback", summary="Handle Google OAuth callback")
async def google_callback(request: Request) -> Dict[str, Any]:
    """Handle the Google OAuth redirect back to the application.

    Exchange the authorization code for tokens, fetch user info,
    and store the session.
    """
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing authorization code in callback",
        )

    # Exchange authorization code for tokens
    import httpx

    token_params = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": GOOGLE_REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        # Get access token
        token_resp = await client.post(GOOGLE_TOKEN_URL, data=token_params)
        if token_resp.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to exchange authorization code: {token_resp.text}",
            )
        tokens = token_resp.json()

        # Fetch user info
        userinfo_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        if userinfo_resp.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch user info: {userinfo_resp.text}",
            )
        userinfo = userinfo_resp.json()

    # Create GoogleUserInfo model
    user = GoogleUserInfo(
        email=userinfo["email"],
        name=userinfo["name"],
        picture=userinfo.get("picture"),
        sub=userinfo["sub"],
    )

    # Store Google token for session persistence
    vault = TokenVault()
    google_token_path = P.home() / '.config' / 'sc-oam-app' / 'google_token.json'
    google_token_path.parent.mkdir(parents=True, exist_ok=True)
    encrypted_token = vault.encrypt({
        'user': user.model_dump(),
        'auth_tier': 'google',
        'login_timestamp': int(__import__('time').time()),
    })
    with open(google_token_path, 'w') as f:
        f.write(encrypted_token)

    return {
        "status": "success",
        "auth_tier": "google",
        "user": user.model_dump(),
        "message": "Google OAuth login successful",
    }


# ─── Google OAuth Credential Vault ──────────────────────────────────────
@router.post("/config/google-credentials", summary="Store Google OAuth client credentials in vault")
async def store_google_credentials(request: Request) -> Dict[str, Any]:
    """Store Google OAuth client ID and secret in the vault for persistent configuration.

    Accepts JSON with `client_id` and `client_secret`.
    These take priority over .env environment variables.
    """
    body = await request.json()
    client_id = body.get("client_id", "")
    client_secret = body.get("client_secret", "")

    if not client_id or not client_secret:
        raise HTTPException(
            status_code=400,
            detail="Both client_id and client_secret are required",
        )

    vault = TokenVault()
    vault.set_google_credentials(client_id, client_secret)

    return {
        "status": "success",
        "message": "Google OAuth credentials stored in vault",
    }


# ─── RSI Credential Vault ───────────────────────────────────────────────
@router.post("/config/rsi-credentials", summary="Store RSI username/password/mode in vault")
async def store_rsi_credentials(request: Request) -> Dict[str, Any]:
    """Store RSI username, password, and mode in the vault for persistent configuration.

    Accepts JSON with `username`, `password`, and `mode`.
    These take priority over direct form input for RSI login.
    """
    body = await request.json()
    username = body.get("username", "")
    password = body.get("password", "")
    mode = body.get("mode", "standard")

    if not username or not password:
        raise HTTPException(
            status_code=400,
            detail="Both username and password are required",
        )

    vault = TokenVault()
    vault.set_rsi_credentials(username, password, mode)

    return {
        "status": "success",
        "message": "RSI credentials stored in vault",
    }


# ─── RSI Hangar Data ───────────────────────────────────────────────

@router.get("/rsi/hangar", response_model=RSIHangarResponse, summary="Get RSI pledge hangar data")
async def rsi_hangar(rsi_auth: RSIAuthManager = Depends(get_rsi_auth)) -> RSIHangarResponse:
    """Retrieve the user's RSI pledge hangar data.

    Returns ships, items, packages, upgrades, flair, and buybacks
    from the authenticated RSI session.

    Requires prior `POST /auth/rsi/login` successful authentication.
    Returns 401 if not authenticated.
    """
    result = rsi_auth.get_hangar()
    if result['status'] != 'success':
        raise HTTPException(status_code=401, detail=result.get('message', 'RSI not authenticated'))

    # Build the Pydantic response model
    return RSIHangarResponse(
        ships=result.get('ships', []),
        items=result.get('items', []),
        packages=result.get('packages', []),
        upgrades=result.get('upgrades', []),
        flair=result.get('flair', []),
        buybacks=result.get('buybacks', []),
        is_empty=result.get('is_empty', True),
        fetched_at=result.get('fetched_at', 0),
    )


# ─── Optional: Auth-Checked Routes ──────────────────────────────────

# These would be used for routes that require any auth tier.
# For now, the RSI endpoints are opt-in; unauthenticated access returns 401 naturally.

# ─── Register Router ────────────────────────────────────────────────

# Note: app.include_router(auth_router, prefix="/api") is in app.py.
# This router has prefix="/auth", so final paths are /api/auth/...
