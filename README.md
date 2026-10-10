# CI/CD Pipeline Security Audit Lab 

## Hands-on: Audit Keamanan Pipeline CI/CD Sederhana

Lab ini adalah bagian dari sesi **Software and Data Integrity Failures** (OWASP A08:2021) pada bootcamp cybersecurity Dibimbing.id.

---

## Tujuan Pembelajaran

Setelah menyelesaikan lab ini, peserta akan mampu:

1. **Mengidentifikasi** kerentanan supply chain dalam pipeline CI/CD
2. **Memahami** pentingnya integritas data dan software dalam DevSecOps
3. **Melakukan audit** keamanan pada workflow GitHub Actions
4. **Menerapkan** teknik mitigasi seperti SHA256 checksum verification dan dependency pinning
5. **Membandingkan** praktik insecure vs secure dalam CI/CD pipeline
6. **Mengobservasi** bagaimana security gates memblokir kode vulnerable

---

## Struktur Repository

Repository ini memiliki **tiga branch** untuk pembelajaran:

| Branch | Kode | Pipeline | Hasil | Tujuan |
|--------|------|----------|-------|--------|
| `insecure` | ❌ Vulnerable | ❌ Tidak aman | ✅ Pass | Untuk di-audit |
| `devsecops` | ❌ Vulnerable | ✅ Strict gates | ❌ **Fail** | Demo security gate |
| `secure` | ✅ Aman | ✅ Aman | ✅ Pass | Reference solution |

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEARNING PATH                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. insecure ──▶ 2. devsecops ──▶ 3. secure                     │
│     (audit)       (observe)        (learn fix)                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/batamhacker/secure-pipeline-audit.git
cd secure-pipeline-audit

# 1. Audit branch insecure
git checkout insecure
cat .github/workflows/pipeline.yml
cat src/app.py

# 2. Observasi security gate di branch devsecops
git checkout devsecops
# Jalankan workflow di GitHub Actions - akan GAGAL!

# 3. Pelajari solusi di branch secure
git checkout secure
git diff insecure secure -- .github/workflows/pipeline.yml
```

---

## Koneksi dengan Materi

### Supply Chain Attack

**Definisi:** Serangan yang menargetkan elemen kurang aman dalam rantai pasokan software, seperti dependencies, build tools, atau CI/CD pipeline.

**Contoh Nyata - SolarWinds Attack (2020):**
- Attacker menyusup ke sistem build SolarWinds
- Menyisipkan backdoor (SUNBURST) ke dalam update software Orion
- 18.000+ organisasi terinfeksi termasuk pemerintah AS
- Tidak terdeteksi selama berbulan-bulan karena update ditandatangani dengan sertifikat valid

**Dalam Lab Ini:**
- Branch `insecure` mendemonstrasikan vektor serangan serupa
- Branch `devsecops` menunjukkan bagaimana security gate mendeteksi serangan
- Branch `secure` menunjukkan cara mitigasi yang benar

### Teknik Mitigasi

| Teknik | Implementasi di Lab |
|--------|---------------------|
| **Code Signing** | SHA256 checksum verification di branch `secure` |
| **Dependency Pinning** | requirements.txt dengan version pinning |
| **SAST** | Bandit untuk static analysis |
| **Dependency Scanning** | pip-audit untuk vulnerability scanning |
| **Security Gates** | Pipeline yang memblokir kode vulnerable (branch `devsecops`) |
| **Least Privilege** | Minimal permissions di workflow |

---

## Cara Menggunakan Lab Ini

### Langkah 1: Audit Branch Insecure

```bash
git checkout insecure
```

**Tugas:** Gunakan `AUDIT_CHECKLIST.md` untuk mengidentifikasi semua kerentanan di:
- `.github/workflows/pipeline.yml`
- `src/app.py`
- `src/requirements.txt`

### Langkah 2: Observasi Security Gate (Branch DevSecOps)

```bash
git checkout devsecops
```

1. Fork repository ini
2. Buka tab **Actions**
3. Jalankan workflow
4. **Observasi:** Pipeline akan **GAGAL** karena security tools mendeteksi vulnerabilities

**Ini adalah expected behavior!** Security gate bekerja dengan benar memblokir kode vulnerable.

### Langkah 3: Pelajari Solusi (Branch Secure)

```bash
git checkout secure

# Bandingkan dengan insecure
git diff insecure secure -- .github/workflows/pipeline.yml
git diff insecure secure -- src/app.py
```

### Langkah 4: Verifikasi SHA256 Checksum

```bash
# Di Linux/Mac
sha256sum src/app.py

# Di Windows PowerShell
Get-FileHash src/app.py -Algorithm SHA256

# Online tool: https://emn178.github.io/online-tools/sha256_checksum.html
```

---

## Kerentanan yang Didemonstrasikan

### Branch `insecure` - Vulnerabilities to Find:

**Workflow (pipeline.yml):**
- [ ] Unpinned GitHub Actions (supply chain risk)
- [ ] `curl | bash` dari sumber eksternal
- [ ] Tidak ada dependency scanning
- [ ] Tidak ada integrity verification
- [ ] Secrets di-print ke log
- [ ] Permissions terlalu permissive

**Kode (app.py):**
- [ ] Hardcoded credentials
- [ ] Penggunaan `eval()` pada input
- [ ] Insecure deserialization (pickle)
- [ ] Download dan execute remote code
- [ ] Tidak ada input validation

### Branch `devsecops` - Security Gate Demo:

**Pipeline akan mendeteksi:**
- 🚨 Bandit: `eval()` usage (B307)
- 🚨 Bandit: `exec()` usage (B102)
- 🚨 Bandit: `pickle` usage (B301)
- 🚨 Secrets scanner: Hardcoded API keys
- 🚨 Secrets scanner: Hardcoded passwords

**Hasil:** ❌ Pipeline GAGAL (ini benar!)

### Branch `secure` - Fixed Code:

**Workflow (pipeline.yml):**
- [x] Actions di-pin dengan SHA commit hash
- [x] Tidak ada remote script execution
- [x] Dependency scanning dengan pip-audit
- [x] SHA256 checksum verification
- [x] Static analysis dengan Bandit
- [x] Minimal permissions

**Kode (app.py):**
- [x] Tidak ada hardcoded secrets
- [x] Safe expression evaluation (AST-based)
- [x] Input validation
- [x] Tidak ada insecure deserialization

---

## Tools yang Digunakan

| Tool | Fungsi |
|------|--------|
| **SHA256 Hash Generator** | Verifikasi integritas file |
| **Bandit** | Static Application Security Testing (SAST) untuk Python |
| **pip-audit** | Dependency vulnerability scanning |
| **GitHub Actions** | CI/CD platform |

---

## Referensi

- [OWASP A08:2021 - Software and Data Integrity Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [SolarWinds Attack Analysis](https://www.crowdstrike.com/blog/sunspot-malware-technical-analysis/)
- [Supply Chain Security Best Practices](https://slsa.dev/)
- [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)

---

## Catatan Penting

> **PERINGATAN:** Kode di branch `insecure` dan `devsecops` sengaja dibuat vulnerable untuk tujuan edukasi. **JANGAN** gunakan pattern tersebut di environment production.

---

## Author

Lab ini dibuat untuk sesi bootcamp **Dibimbing.id** - Day 23: Software and Data Integrity Failures

**Instructor:** Irwan Puspito
