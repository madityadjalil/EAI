Simple JWT Marketplace API (Flask)

Cara Setup Environment & Menjalankan Server
1. Aktifkan virtual environment (opsional):
   python -m venv venv
   venv\Scripts\activate

2. Install dependencies:
   pip install flask pyjwt python-dotenv

3. Buat file `.env.example`:
   JWT_SECRET=supersecret123
   PORT=3000

4. Jalankan server:
   python app.py
   
   Server akan berjalan di `http://127.0.0.1:3000`


Variabel Environment yang Diperlukan
 `JWT_SECRET (supersecret123)` Secret key untuk encode/decode JWT 
 `PORT (3000)`  Port server Flask 


Daftar Endpoint + Skema Request/Response

1. `/auth/login` — POST (Public)
Body (JSON):
{
  "email": "user1@example.com",
  "password": "pass123"
}

Response 200:
{ "access_token": "<JWT_TOKEN>" }

Response 401:
{ "error": "error": "Invalid credentials" }


2. `/items` — GET (Public)
Response 200:
{
    "items": [
        {
            "id": 1,
            "name": "Laptop",
            "price": 10000000
        },
        {
            "id": 2,
            "name": "Headphone",
            "price": 500000
        },
        {
            "id": 3,
            "name": "Mouse",
            "price": 150000
        }
    ]
}

3️. `/profile` — PUT (Protected, JWT Required)
Header:
Authorization: Bearer <JWT_TOKEN>

Body:
{ "name": "New Name" }


Response 200:
{
  "message": "Profile updated",
    "profile": {
        "name": "New Name"
    }
}


Response 401:
{
    "error": "Invalid token"
}

 Contoh cURL

1.Login → Dapatkan Token
curl -X POST http://localhost:3000/auth/login   
-H "Content-Type: application/json"   
-d '{"email":"user1@example.com","password":"pass123"}'

2.Akses Public `/items`
curl -X GET http://localhost:3000/items

3️.Akses Protected `/profile`
TOKEN="<JWT_TOKEN>"
curl -X PUT http://localhost:3000/profile   
-H "Authorization: Bearer $TOKEN" 
-d '{"name":"New Name"}'


Catatan
- Token JWT berlaku 15 menit sejak login.  
- Jika token expired maka harus login ulang untuk dapat token baru.  
- Data user dan item disimpan sementara di memori (tanpa database).  
- Semua response dalam format JSON.  
- Digunakan hanya untuk simulasi JWT Authentication dasar dengan Flask.