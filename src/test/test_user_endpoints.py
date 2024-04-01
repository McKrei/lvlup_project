
# import sys
# sys.path.append(r'C:\Users\legion\projects\NEW\investment_portfolio\src')


# import pytest
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession
# from ..database.models import User


# @pytest.mark.asyncio
# async def test_create_user_and_authenticate(client: AsyncClient, session: AsyncSession):
#     # Создаем пользователя
#     user_data = {"username": "testuser", "email": "test@example.com", "password": "password123"}
#     response = await client.post("/user/", json=user_data)
#     assert response.status_code == 201
#     user = response.json()
#     assert user["username"] == user_data["username"]

#     # Аутентифицируем пользователя и получаем токен
#     response = await client.post("/user/token", data={
#         "username": user_data["username"],
#         "password": user_data["password"]
#     })
#     assert response.status_code == 200
#     token_data = response.json()
#     assert "access_token" in token_data
#     access_token = token_data["access_token"]

#     # Используем токен для доступа к защищенному эндпоинту
#     response = await client.get("/user/me", headers={"Authorization": f"Bearer {access_token}"})
#     assert response.status_code == 200
#     user_info = response.json()
#     assert user_info["username"] == user_data["username"]
