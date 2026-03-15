# CryptKnox 🔐

**CryptKnox** is a lightweight **CLI-based encrypted password manager** written in Python.
It allows you to securely **store, retrieve, delete, and generate passwords** using a single master password.

All stored credentials are **encrypted locally using AES encryption**, ensuring your secrets remain protected.

---

## Features

* 🔐 **AES Encryption** for secure password storage
* 🗂 **Store multiple accounts per service**
* 🔍 **Retrieve specific services or all stored credentials**
* ❌ **Delete credentials securely**
* 🔑 **Generate strong random passwords**
* 💻 **Simple CLI interface**
* 📦 **Installable via PyPI**

---

## Installation

Install from PyPI:

```bash
pip install cryptknox
```

After installation you can run:

```bash
cryptknox --help
```

---

## Usage

```
cryptknox --operation|-o [store|retrieve|delete|generate] [OPTIONS]
```

---

## Operations

### Store Credentials

Store a password for a service.

```
cryptknox -o store -m MySecretPassword -s gmail -u user@gmail.com -p mypassword
```

Options:

| Option                    | Description                         |
| ------------------------- | ----------------------------------- |
| `--operation`, `-o`       | Operation (`store`)                 |
| `--master-password`, `-m` | Master password used for encryption |
| `--service`, `-s`         | Service name (example: gmail)       |
| `--username`, `-u`        | Username for the service            |
| `--password`, `-p`        | Password to store                   |

---

### Retrieve Credentials

Retrieve stored passwords.

Retrieve a specific service:

```
cryptknox -o retrieve -m MySecretPassword -s gmail
```

Retrieve all services:

```
cryptknox -o retrieve -m MySecretPassword -s all
```

---

### Delete Credentials

Delete stored credentials.

Delete a specific service entry:

```
cryptknox -o delete -m MySecretPassword -s gmail
```

Delete all entries:

```
cryptknox -o delete -m MySecretPassword -s all
```

---

### Generate Secure Password

Generate a random secure password.

```
cryptknox -o generate -l 12
```

Options:

| Option           | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `--length`, `-l` | Length of generated password (must be greater than 4) |

The generated password includes:

* uppercase letters
* lowercase letters
* numbers
* special characters

---

## Examples

Store credentials:

```
cryptknox -o store -m MySecretPassword -s github -u myuser -p mypassword
```

Retrieve all credentials:

```
cryptknox -o retrieve -m MySecretPassword -s all
```

Generate a strong password:

```
cryptknox -o generate -l 16
```

Delete credentials:

```
cryptknox -o delete -m MySecretPassword -s github
```

---

## Security Notes

* All credentials are **encrypted before being stored**.
* Only the **master password can decrypt the vault**.
* The master password is **never stored**.

⚠️ If the master password is lost, the vault **cannot be recovered**.

---

## Requirements

* Python **3.9+**

---

## License

MIT License

---

## Author

Developed by **Sreejith**

GitHub: https://github.com/Sreejith-R-Mohan/cryptknox
