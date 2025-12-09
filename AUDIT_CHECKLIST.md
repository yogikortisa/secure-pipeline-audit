# Audit Checklist - CI/CD Pipeline Security

## Panduan Audit untuk Branch `insecure`

Gunakan checklist ini untuk melakukan audit keamanan pada pipeline CI/CD. Centang setiap kerentanan yang Anda temukan.

---

## Bagian A: Audit Workflow (.github/workflows/pipeline.yml)

### A1. Supply Chain - GitHub Actions

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah actions menggunakan version pinning dengan SHA? | [ ] Ya / [ ] Tidak | |
| 2 | Apakah ada actions dari third-party yang tidak terverifikasi? | [ ] Ya / [ ] Tidak | |
| 3 | Versi apa yang digunakan untuk `actions/checkout`? | __________ | |

**Kerentanan yang dicari:**
```yaml
# INSECURE - hanya menggunakan tag
uses: actions/checkout@v2

# SECURE - menggunakan full SHA
uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608  # v4.1.0
```

---

### A2. Supply Chain - External Scripts

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah ada command `curl | bash` atau sejenisnya? | [ ] Ya / [ ] Tidak | |
| 2 | Dari URL mana script didownload? | __________ | |
| 3 | Apakah ada verifikasi checksum sebelum eksekusi? | [ ] Ya / [ ] Tidak | |

**Pattern berbahaya:**
```bash
# INSECURE - langsung execute tanpa verifikasi
curl -sSL https://example.com/script.sh | bash

# SECURE - download, verify, then execute
curl -sSL -o script.sh https://example.com/script.sh
echo "expected_sha256_hash  script.sh" | sha256sum -c -
bash script.sh
```

---

### A3. Dependency Management

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah requirements.txt menggunakan version pinning? | [ ] Ya / [ ] Tidak | |
| 2 | Apakah ada dependency scanning (pip-audit, safety)? | [ ] Ya / [ ] Tidak | |
| 3 | List dependencies tanpa version: | __________ | |

---

### A4. Secrets Management

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah ada hardcoded secrets di workflow file? | [ ] Ya / [ ] Tidak | |
| 2 | Apakah secrets di-print ke log? | [ ] Ya / [ ] Tidak | |
| 3 | Apakah menggunakan GitHub Secrets dengan benar? | [ ] Ya / [ ] Tidak | |

---

### A5. Permissions

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah permissions didefinisikan secara eksplisit? | [ ] Ya / [ ] Tidak | |
| 2 | Apa permission level yang digunakan? | __________ | |
| 3 | Apakah mengikuti principle of least privilege? | [ ] Ya / [ ] Tidak | |

---

### A6. Integrity Verification

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah ada checksum verification sebelum deployment? | [ ] Ya / [ ] Tidak | |
| 2 | Apakah artifacts ditandatangani? | [ ] Ya / [ ] Tidak | |
| 3 | Apakah ada SBOM (Software Bill of Materials)? | [ ] Ya / [ ] Tidak | |

---

## Bagian B: Audit Source Code (src/app.py)

### B1. Hardcoded Credentials

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah ada API key yang di-hardcode? | [ ] Ya / [ ] Tidak | |
| 2 | Apakah ada password yang di-hardcode? | [ ] Ya / [ ] Tidak | |
| 3 | List secrets yang ditemukan: | __________ | |

---

### B2. Code Injection

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah ada penggunaan `eval()`? | [ ] Ya / [ ] Tidak | |
| 2 | Apakah ada penggunaan `exec()`? | [ ] Ya / [ ] Tidak | |
| 3 | Apakah input divalidasi sebelum diproses? | [ ] Ya / [ ] Tidak | |

---

### B3. Insecure Deserialization

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah ada penggunaan `pickle` untuk data eksternal? | [ ] Ya / [ ] Tidak | |
| 2 | Apakah ada penggunaan `yaml.load()` tanpa Loader? | [ ] Ya / [ ] Tidak | |

---

### B4. Remote Code Execution

| No | Pertanyaan Audit | Temuan | Risiko |
|----|------------------|--------|--------|
| 1 | Apakah ada fungsi yang download dan execute code? | [ ] Ya / [ ] Tidak | |
| 2 | Apakah URL sumber terverifikasi? | [ ] Ya / [ ] Tidak | |

---

## Bagian C: Ringkasan Temuan

### C1. Daftar Kerentanan

| No | Lokasi | Kerentanan | Severity | Line Number |
|----|--------|------------|----------|-------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Severity Rating:**
- 🔴 Critical - Dapat dieksploitasi langsung untuk RCE
- 🟠 High - Supply chain risk atau credential exposure
- 🟡 Medium - Security misconfiguration
- 🟢 Low - Best practice violation

---

### C2. Rekomendasi Perbaikan

Untuk setiap kerentanan yang ditemukan, tuliskan rekomendasi perbaikan:

| Kerentanan | Rekomendasi Perbaikan |
|------------|----------------------|
| | |
| | |
| | |

---

## Bagian D: Hands-on Exercise

### Exercise 1: Generate SHA256 Hash

1. Buka file `src/app.py`
2. Generate SHA256 hash menggunakan salah satu metode:

**Windows PowerShell:**
```powershell
Get-FileHash src/app.py -Algorithm SHA256
```

**Linux/Mac:**
```bash
sha256sum src/app.py
```

**Online Tool:**
- https://emn178.github.io/online-tools/sha256_checksum.html

3. Catat hash yang dihasilkan: `__________________________________`

---

### Exercise 2: Bandingkan dengan Branch Secure

```bash
# Checkout branch secure
git checkout secure

# Lihat perbedaan workflow
git diff insecure secure -- .github/workflows/pipeline.yml
```

**Pertanyaan:**
1. Apa perbedaan utama dalam version pinning? __________
2. Tool keamanan apa yang ditambahkan? __________
3. Bagaimana integrity verification dilakukan? __________

---

### Exercise 3: Simulasi Supply Chain Attack

**Skenario:** Bayangkan Anda adalah attacker yang ingin menyusupkan malicious code.

1. Di branch `insecure`, modifikasi file `src/app.py`
2. Push perubahan
3. Observasi: Apakah pipeline mendeteksi perubahan?

**Di branch `secure`:**
1. Modifikasi file `src/app.py`
2. Push perubahan
3. Observasi: Apa yang terjadi saat SHA256 verification?

---

## Jawaban (untuk Instruktur)

<details>
<summary>Klik untuk melihat jawaban</summary>

### Kerentanan di Workflow:
1. **Line 24-25**: Unpinned actions (`actions/checkout@v2`)
2. **Line 40-43**: `curl | bash` tanpa verification
3. **Line 18-20**: Hardcoded secrets di env
4. **Line 45-49**: Secrets di-print ke log
5. **Tidak ada**: permissions block (defaults to read-write)
6. **Tidak ada**: Dependency scanning step
7. **Tidak ada**: Checksum verification

### Kerentanan di Code:
1. **Line 17-20**: Hardcoded credentials
2. **Line 27-34**: `eval()` pada user input
3. **Line 37-44**: Insecure pickle deserialization
4. **Line 47-58**: Download and execute remote code
5. **Line 61-75**: Secrets printed in debug mode

</details>

---

**Selamat melakukan audit!** 🔍

