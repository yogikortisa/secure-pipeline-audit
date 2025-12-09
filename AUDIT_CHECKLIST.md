# Security Controls Verification Checklist

## Branch: `secure`

Gunakan checklist ini untuk memverifikasi bahwa semua kontrol keamanan telah diimplementasikan dengan benar.

---

## Bagian A: Workflow Security Controls

### A1. Supply Chain - Action Pinning

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | actions/checkout menggunakan SHA | [x] | `@8ade135a41bc03ea155e62e844d188df1ea18608` |
| 2 | actions/setup-python menggunakan SHA | [x] | `@65d7f2d534ac1bc67fcd62888c5f4f3d2cb2b236` |
| 3 | Tidak ada action menggunakan tag saja | [x] | Verified |

---

### A2. Supply Chain - No Remote Execution

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | Tidak ada `curl \| bash` | [x] | No remote script execution |
| 2 | Tidak ada download dari URL eksternal | [x] | Verified |
| 3 | Tidak ada `wget` tanpa verification | [x] | Verified |

---

### A3. Dependency Management

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | Semua dependencies di-pin dengan version | [x] | See requirements.txt |
| 2 | pip-audit digunakan untuk scanning | [x] | Line 54-56 in workflow |
| 3 | Safety check dijalankan | [x] | Line 58-59 in workflow |

---

### A4. Integrity Verification

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | SHA256 hash verification step exists | [x] | `integrity-check` job |
| 2 | Expected hash didefinisikan | [x] | `EXPECTED_APP_HASH` env var |
| 3 | File checksums di-generate untuk audit | [x] | `Generate file checksums` step |

---

### A5. Permissions

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | Permissions block didefinisikan | [x] | Lines 23-25 |
| 2 | contents: read (bukan write) | [x] | Verified |
| 3 | Mengikuti least privilege | [x] | Only read permissions |

---

### A6. Security Scanning

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | SAST dengan Bandit | [x] | `security-scan` job |
| 2 | Dependency scanning | [x] | pip-audit, safety |
| 3 | Scans berjalan sebelum build | [x] | Job ordering dengan `needs` |

---

## Bagian B: Application Security Controls

### B1. Secrets Management

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | Tidak ada hardcoded API keys | [x] | Uses `os.getenv()` |
| 2 | Tidak ada hardcoded passwords | [x] | Verified |
| 3 | Secrets tidak di-print ke log | [x] | Only prints "Yes/No" for existence |

---

### B2. Code Injection Prevention

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | Tidak menggunakan `eval()` | [x] | Uses `SafeCalculator` class |
| 2 | Tidak menggunakan `exec()` | [x] | Verified |
| 3 | AST-based expression evaluation | [x] | `ast.parse()` dengan operator whitelist |

---

### B3. Input Validation

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | Input di-validate sebelum diproses | [x] | `validate_input()` function |
| 2 | Whitelist-based validation | [x] | `allowed_actions` list |
| 3 | Length limits diterapkan | [x] | Max 50-200 chars per field |

---

### B4. Safe Serialization

| No | Kontrol | Status | Evidence |
|----|---------|--------|----------|
| 1 | Tidak menggunakan `pickle` untuk external data | [x] | Uses JSON |
| 2 | JSON parsing dengan error handling | [x] | `load_data_safely()` |
| 3 | Data structure validation | [x] | Validates dict type |

---

## Bagian C: Comparison Exercise

### Instruksi

Bandingkan branch `insecure` dengan branch `secure` untuk melihat perbedaan:

```bash
# Checkout insecure branch
git checkout insecure

# Lihat isi workflow
cat .github/workflows/pipeline.yml

# Checkout secure branch
git checkout secure

# Bandingkan dengan diff
git diff insecure secure -- .github/workflows/pipeline.yml
git diff insecure secure -- src/app.py
```

### Pertanyaan Diskusi

1. **Action Pinning:** Mengapa SHA lebih aman dari tag version?
   > Tags dapat di-move ke commit yang berbeda, SHA tidak bisa

2. **curl | bash:** Apa risiko menjalankan script langsung dari URL?
   > Script bisa dimodifikasi oleh attacker (MITM, compromised server)

3. **Dependency Pinning:** Bagaimana unpinned dependencies bisa dieksploitasi?
   > Attacker bisa publish malicious version yang auto-installed

4. **Checksum Verification:** Apa yang dideteksi oleh SHA256 check?
   > Perubahan apapun pada file, termasuk tampering atau corruption

5. **Least Privilege:** Mengapa `contents: read` lebih baik dari default?
   > Default memberikan write access yang bisa dieksploitasi

---

## Bagian D: Hands-on Verification

### Exercise 1: Verify SHA256 Implementation

```bash
# Calculate hash dari app.py
sha256sum src/app.py

# Bandingkan dengan EXPECTED_APP_HASH di workflow
grep EXPECTED_APP_HASH .github/workflows/pipeline.yml
```

### Exercise 2: Test Security Scanning

```bash
# Install tools
pip install bandit pip-audit

# Run Bandit
bandit -r src/ -f txt

# Run pip-audit
pip-audit -r src/requirements.txt
```

### Exercise 3: Test Input Validation

Modifikasi `src/app.py` dan tambahkan test case:

```python
# Di function main(), tambahkan:
malicious = {"user_id": "user123", "action": "calculate", "payload": "__import__('os')"}
result = process_request(malicious)
print(f"Malicious input result: {result}")  # Should be blocked
```

---

## Kesimpulan

Branch `secure` mendemonstrasikan:

1. **Defense in Depth** - Multiple layers of security controls
2. **Shift Left Security** - Security checks early in pipeline
3. **Supply Chain Security** - Protection against dependency attacks
4. **Integrity Verification** - Detection of unauthorized modifications
5. **Least Privilege** - Minimal permissions to reduce attack surface

---

**Selamat! Anda telah memverifikasi kontrol keamanan pipeline CI/CD.** ✅

