# cryptography 密码学库

**Python现代密码学库**

---

## 📋 概述

cryptography是Python的现代密码学库，提供加密、解密、数字签名等功能。

### 核心特性

- 🔐 **对称加密** - AES等算法
- 🔑 **非对称加密** - RSA, ECC等
- ✍️ **数字签名** - 签名和验证
- 🔒 **哈希** - SHA256等
- 🎲 **安全随机数** - 密码学安全

---

## 🚀 快速开始

### 安装

```bash
uv add cryptography
```

### 对称加密

```python
from cryptography.fernet import Fernet

# 生成密钥
key = Fernet.generate_key()
cipher = Fernet(key)

# 加密
message = b"Secret message"
encrypted = cipher.encrypt(message)

# 解密
decrypted = cipher.decrypt(encrypted)
assert decrypted == message
```

---

## 🔐 加密算法

### AES加密

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# 生成密钥和IV
key = os.urandom(32)  # 256位
iv = os.urandom(16)

# 加密
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(b"message") + encryptor.finalize()

# 解密
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()
```

### RSA非对称加密

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# 生成密钥对
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# 加密
message = b"Secret data"
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 解密
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
```

---

## ✍️ 数字签名

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# 生成密钥
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# 签名
message = b"Important message"
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# 验证
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Signature valid")
except:
    print("Signature invalid")
```

---

## 🔒 哈希

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# SHA256
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(b"message")
hash_value = digest.finalize()

# 密码哈希 (使用bcrypt)
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password = b"user_password"
salt = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
key = kdf.derive(password)
```

---

## 📚 最佳实践

### 1. 密码存储

```python
import bcrypt

# 哈希密码
password = b"user_password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# 验证密码
if bcrypt.checkpw(password, hashed):
    print("Password correct")
```

### 2. 安全随机数

```python
import secrets

# 生成令牌
token = secrets.token_hex(32)  # 64字符
token = secrets.token_urlsafe(32)  # URL安全

# 随机数
random_number = secrets.randbelow(100)
```

---

## 🔗 相关资源

- [官方文档](https://cryptography.io/)
- [安全最佳实践](https://cryptography.io/en/latest/hazmat/primitives/)

---

**最后更新**: 2025年10月28日

