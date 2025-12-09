# CI/CD Pipeline Security Audit Lab - DevSecOps Branch

## Branch: `devsecops`

Ini adalah branch **DevSecOps** yang mendemonstrasikan bagaimana **security gates** dalam pipeline CI/CD mendeteksi dan **memblokir** kode yang vulnerable.

---

## Konsep: Security Gate dalam DevSecOps

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   COMMIT    │───▶│  SECURITY   │───▶│    BUILD    │───▶│   DEPLOY    │
│             │    │    SCAN     │    │             │    │             │
└─────────────┘    └──────┬──────┘    └─────────────┘    └─────────────┘
                          │
                    ┌─────▼─────┐
                    │  ❌ FAIL  │  ◀── Pipeline berhenti di sini!
                    │ (blocked) │
                    └───────────┘
```

**Branch ini berisi:**
- **INSECURE CODE** - Kode dengan kerentanan (sama seperti branch `insecure`)
- **SECURE PIPELINE** - Pipeline dengan security gates yang ketat

**Hasil:** Pipeline akan **GAGAL** karena security tools mendeteksi kerentanan!

---

## Apa yang Terjadi Saat Pipeline Berjalan?

### Stage 1: Security Scan ❌ FAIL

```
🔍 Running Bandit Static Analysis (STRICT)
============================================
>> Issue: [B307:eval] Use of possibly insecure function - consider using safer ast.literal_eval.
   Severity: Medium   Confidence: High
   Location: src/app.py:35

>> Issue: [B102:exec_used] Use of exec detected.
   Severity: Medium   Confidence: High
   Location: src/app.py:58

>> Issue: [B301:pickle] Pickle and modules that wrap it can be unsafe.
   Severity: Medium   Confidence: High
   Location: src/app.py:44

🚨 SECURITY GATE FAILED - Vulnerabilities detected!
```

### Stage 2: Code Quality ❌ FAIL

```
🔍 Scanning for Hardcoded Secrets
============================================
🚨 ALERT: Hardcoded API keys found!
   src/app.py:17: API_KEY = "sk-production-key-super-secret-12345"
   
🚨 ALERT: Hardcoded passwords found!
   src/app.py:18: DATABASE_PASSWORD = "admin123"
```

### Stage 3: Build ⏭️ SKIPPED

```
Build stage skipped because security-scan failed.
```

### Stage 4: Deploy ⏭️ SKIPPED

```
Deploy stage skipped - security gate blocked deployment.
✅ Security Gate: WORKING AS EXPECTED
❌ Deployment: BLOCKED
```

---

## Perbandingan 3 Branch

| Aspek | `insecure` | `devsecops` | `secure` |
|-------|------------|-------------|----------|
| **Kode** | Vulnerable | Vulnerable | Secure |
| **Pipeline** | Tidak aman | Aman (strict) | Aman |
| **Hasil** | ✅ Pass (berbahaya!) | ❌ Fail (benar!) | ✅ Pass |
| **Deploy** | Ya (buruk) | Tidak (bagus) | Ya (aman) |

---

## Kerentanan yang Dideteksi

Security gate mendeteksi kerentanan berikut:

| Tool | Kerentanan | Severity | File:Line |
|------|------------|----------|-----------|
| Bandit | `eval()` usage (B307) | Medium | app.py:35 |
| Bandit | `exec()` usage (B102) | Medium | app.py:58 |
| Bandit | `pickle` usage (B301) | Medium | app.py:44 |
| Grep | Hardcoded API_KEY | High | app.py:17 |
| Grep | Hardcoded PASSWORD | High | app.py:18 |
| Grep | Hardcoded TOKEN | High | app.py:19 |

---

## Cara Melihat Pipeline Gagal

### Option 1: Jalankan di GitHub Actions

1. Fork repository ini
2. Checkout branch `devsecops`
3. Buka tab **Actions**
4. Klik **Run workflow**
5. Lihat pipeline **GAGAL** dengan security findings

### Option 2: Jalankan Lokal

```bash
# Clone dan checkout
git clone https://github.com/batamhacker/secure-pipeline-audit.git
cd secure-pipeline-audit
git checkout devsecops

# Install Bandit
pip install bandit

# Jalankan Bandit (akan menemukan vulnerabilities)
bandit -r src/ -ll -ii

# Output akan menunjukkan security issues!
```

---

## Mengapa Pipeline Harus GAGAL?

Ini adalah **expected behavior** dalam DevSecOps:

1. **Shift Left Security** - Masalah keamanan terdeteksi lebih awal
2. **Fail Fast** - Pipeline berhenti sebelum kode berbahaya di-deploy
3. **Automated Gates** - Tidak bergantung pada review manual saja
4. **Compliance** - Memenuhi standar keamanan organisasi

> **Quote:** "A failing security gate is a SUCCESSFUL security control."

---

## Cara Memperbaiki (Untuk Lulus Pipeline)

Untuk membuat pipeline berhasil, perbaiki kerentanan:

```python
# INSECURE (akan gagal)
result = eval(expression)

# SECURE (akan lulus)
import ast
result = ast.literal_eval(expression)
```

```python
# INSECURE (akan gagal)
API_KEY = "sk-production-key-12345"

# SECURE (akan lulus)
API_KEY = os.getenv("API_KEY")
```

Atau, checkout branch `secure` untuk melihat kode yang sudah diperbaiki.

---

## Tools Security Gate

| Tool | Fungsi | Exit Code |
|------|--------|-----------|
| **Bandit** | Static code analysis untuk Python | ≠0 jika ada issue |
| **pip-audit** | Dependency vulnerability scan | ≠0 jika ada CVE |
| **Grep** | Pattern matching untuk secrets | ≠0 jika ditemukan |

---

## Referensi

- [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [GitHub Actions Security](https://docs.github.com/en/actions/security-guides)
- [NIST DevSecOps](https://csrc.nist.gov/publications/detail/sp/800-204d/draft)

---

## Author

Lab ini dibuat untuk sesi bootcamp **Dibimbing.id** - Day 23: Software and Data Integrity Failures

**Instructor:** Irwan Puspito
