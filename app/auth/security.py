# app/auth/security.py

import httpx
import logging
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings

logger = logging.getLogger("uvicorn.error")
bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    # 1) Verifica se veio algo no Authorization
    raw = request.headers.get("authorization")
    logger.info(f"→ Authorization header raw: {raw!r}")
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    logger.info(f"→ Token extraído: {token!r}")

    # 2) Chama serviço externo para validar
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{settings.AUTH_API_URL}/auth/verificar-token",
                headers={"Authorization": f"Bearer {token}"},
            )
    except httpx.RequestError:
        logger.exception("Serviço de autenticação indisponível")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de autenticação indisponível",
        )

    # 3) Erro de token inválido/expirado
    if resp.status_code != 200:
        logger.warning(f"Token inválido: {resp.status_code} {resp.text}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4) Extrai email da resposta JSON
    data = resp.json()
    email = data.get("email")
    if not email:
        logger.error(f"Resposta inesperada da API de Senhas: {data!r}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resposta inesperada da API de Senhas",
        )

    # 5) Retorna só o email (você pode usar o email como identificador)
    return {"email": email}
