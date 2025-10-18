# Cat Backend

Django REST Framework ile geliştirilmiş kullanıcı yönetim API'si.

## Özellikler

- Kullanıcı kayıt (Register)
- Kullanıcı giriş (Login) 
- Kullanıcı bilgileri (User Info)
- JWT Token tabanlı kimlik doğrulama
- Argon2 şifre hashleme

## API Endpoints

- `POST /api/register/` - Kullanıcı kayıt
- `POST /api/login/` - Kullanıcı giriş
- `GET /api/user/` - Kullanıcı bilgileri (Token gerekli)


## Kullanım

### Kayıt
```json
POST /api/register/
{
    "name": "John",
    "surname": "Doe", 
    "email": "user@example.com",
    "password": "12345678"
}
```

### Giriş
```json
POST /api/login/
{
    "email": "user@example.com",
    "password": "12345678"
}
```

### Kullanıcı Bilgileri
```
GET /api/user/
Authorization: Bearer <token>
```