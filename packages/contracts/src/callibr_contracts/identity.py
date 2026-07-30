from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AuthenticatedUser(BaseModel):
    tenant_id: str
    user_id: str
    email: str
    display_name: str
    roles: list[str] = Field(default_factory=list)
    trace_id: str


class TenantInfo(BaseModel):
    tenant_id: str
    name: str
    environment: str


class IdentityUserRecord(BaseModel):
    tenant_id: str
    user_id: str
    email: str
    display_name: str
    roles: list[str] = Field(default_factory=list)
    password_hash: str
    is_active: bool = True


class LoginRequest(BaseModel):
    tenant_id: str = Field(default="tenant_demo", min_length=1)
    email: str = Field(min_length=3)
    password: str = Field(min_length=1)


class AuthToken(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    user: AuthenticatedUser
