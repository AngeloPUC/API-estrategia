# app/auth/security.py

import os
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

API_SENHAS_URL = os.getenv("API_SENHAS_URL", "https://api-senhas.vercel.app")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_SENHAS_URL}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Depedência que extrai o bearer token e valida contra a API de Senhas.
    Retorna dict com pelo menos: {'id': ..., 'email': ...}
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{API_SENHAS_URL}/auth/verificar-token",
                headers={"Authorization": f"Bearer {token}"}
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de autenticação indisponível"
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_data = resp.json()
    if not user_data.get("id") or not user_data.get("email"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resposta inesperada da API de Senhas"
        )

    return {"id": user_data["id"], "email": user_data["email"]}
