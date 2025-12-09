# CI/CD Pipeline Security Audit Lab - Secure Branch

## Branch: `secure`

Ini adalah branch **SECURE** yang mendemonstrasikan praktik keamanan CI/CD pipeline yang baik berdasarkan prinsip DevSecOps.

---

## Kontrol Keamanan yang Diimplementasikan

### 1. Supply Chain Protection

| Kontrol | Implementasi |
|---------|--------------|
| **Action Pinning** | Semua GitHub Actions menggunakan full SHA commit hash |
| **Dependency Pinning** | Semua package di requirements.txt memiliki version yang di-pin |
| **No Remote Execution** | Tidak ada `curl \| bash` atau download script dari sumber eksternal |

**Contoh Action Pinning:**
```yaml
# SECURE - menggunakan full SHA
uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v4.1.0
```

### 2. Integrity Verification

| Kontrol | Implementasi |
|---------|--------------|
| **SHA256 Checksum** | File aplikasi diverifikasi dengan hash sebelum eksekusi |
| **Audit Trail** | Semua file hash dicatat untuk audit |

**Verifikasi SHA256:**
```bash
# Generate hash
sha256sum src/app.py

# Di workflow, hash dibandingkan dengan expected value
```

### 3. Security Scanning

| Tool | Fungsi |
|------|--------|
| **Bandit** | Static Application Security Testing (SAST) untuk Python |
| **pip-audit** | Dependency vulnerability scanning |
| **Safety** | Additional dependency check |

### 4. Least Privilege

```yaml
# Minimal permissions - hanya yang diperlukan
permissions:
  contents: read
  actions: read
```

### 5. Secure Coding Practices

| Praktik | Implementasi di app.py |
|---------|------------------------|
| **No Hardcoded Secrets** | Semua credentials dari environment variables |
| **Safe Expression Eval** | AST-based calculator, bukan `eval()` |
| **Input Validation** | Whitelist-based validation |
| **Safe Serialization** | JSON instead of pickle |

---

## Perbandingan dengan Branch Insecure

```bash
# Lihat perbedaan workflow
git diff insecure secure -- .github/workflows/pipeline.yml

# Lihat perbedaan kode
git diff insecure secure -- src/app.py
```

### Key Differences

| Aspek | Insecure | Secure |
|-------|----------|--------|
| Action versions | `@v2` (tag) | `@SHA` (hash) |
| Remote scripts | `curl \| bash` | None |
| Dependency versions | Unpinned | Pinned |
| Security scanning | None | Bandit, pip-audit |
| Integrity check | None | SHA256 verification |
| Permissions | Default (full) | Minimal |
| Secrets handling | Hardcoded | Environment variables |
| User input | `eval()` | AST parsing |
| Deserialization | `pickle` | JSON |

---

## Cara Menggunakan Branch Ini

### Verifikasi Kontrol Keamanan

1. **Review workflow file:**
   ```bash
   cat .github/workflows/pipeline.yml
   ```

2. **Jalankan verifikasi SHA256 lokal:**
   ```bash
   sha256sum src/app.py
   ```

3. **Test security scanning:**
   ```bash
   pip install bandit pip-audit
   bandit -r src/
   pip-audit -r src/requirements.txt
   ```

### Fork dan Jalankan Pipeline

1. Fork repository ini
2. Checkout branch `secure`
3. Buka tab Actions di GitHub
4. Jalankan workflow
5. Review log untuk melihat security controls in action

---

## Update SHA256 Hash

Jika Anda memodifikasi `src/app.py`, update hash di workflow:

```bash
# Generate new hash
sha256sum src/app.py

# Output contoh:
# a1b2c3d4e5f6... src/app.py

# Update di .github/workflows/pipeline.yml:
env:
  EXPECTED_APP_HASH: 'a1b2c3d4e5f6...'
```

---

## Referensi

- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [SLSA - Supply-chain Levels for Software Artifacts](https://slsa.dev/)
- [OWASP A08:2021](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)

---

## Author

Lab ini dibuat untuk sesi bootcamp **Dibimbing.id** - Day 23: Software and Data Integrity Failures

**Instructor:** Irwan Puspito

