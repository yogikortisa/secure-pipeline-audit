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

---

## Struktur Repository

Repository ini memiliki **dua branch** untuk perbandingan:

| Branch | Deskripsi |
|--------|-----------|
| `insecure` | Pipeline dengan kerentanan keamanan (untuk di-audit) |
| `secure` | Pipeline dengan kontrol keamanan DevSecOps |

```
.github/workflows/
  pipeline.yml          # CI/CD workflow (berbeda di setiap branch)
src/
  app.py                # Aplikasi Python (berbeda di setiap branch)
  requirements.txt      # Dependencies
README.md               # Dokumentasi
AUDIT_CHECKLIST.md      # Panduan audit untuk peserta
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
- Penggunaan `curl | bash` dari sumber tidak terpercaya
- Dependencies tanpa version pinning
- Tidak ada verifikasi integritas

### Teknik Mitigasi

| Teknik | Implementasi di Lab |
|--------|---------------------|
| **Code Signing** | SHA256 checksum verification di branch `secure` |
| **Dependency Pinning** | requirements.txt dengan hash verification |
| **SAST** | Bandit untuk static analysis |
| **Dependency Scanning** | pip-audit untuk vulnerability scanning |
| **Least Privilege** | Minimal permissions di workflow |

---

## Cara Menggunakan Lab Ini

### Langkah 1: Audit Branch Insecure

```bash
# Clone repository
git clone https://github.com/yogikortisa/secure-pipeline-audit.git
cd secure-pipeline-audit

# Checkout branch insecure
git checkout insecure

# Review workflow file
cat .github/workflows/pipeline.yml

# Review application code
cat src/app.py
```

**Tugas:** Gunakan `AUDIT_CHECKLIST.md` untuk mengidentifikasi semua kerentanan.

### Langkah 2: Bandingkan dengan Branch Secure

```bash
# Checkout branch secure
git checkout secure

# Bandingkan workflow
git diff insecure secure -- .github/workflows/pipeline.yml

# Bandingkan kode aplikasi
git diff insecure secure -- src/app.py
```

### Langkah 3: Verifikasi SHA256 Checksum

**Menggunakan SHA256 Hash Generator:**

```bash
# Di Linux/Mac
sha256sum src/app.py

# Di Windows PowerShell
Get-FileHash src/app.py -Algorithm SHA256

# Online tool: https://emn178.github.io/online-tools/sha256_checksum.html
```

### Langkah 4: Jalankan Pipeline

1. Fork repository ini ke akun GitHub Anda
2. Buka tab **Actions**
3. Jalankan workflow dan observasi hasilnya
4. Bandingkan log dari branch `insecure` vs `secure`

---

## Kerentanan yang Didemonstrasikan

### Di Branch `insecure`:

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

### Di Branch `secure`:

**Workflow (pipeline.yml):**
- [x] Actions di-pin dengan SHA commit hash
- [x] Tidak ada remote script execution
- [x] Dependency scanning dengan pip-audit
- [x] SHA256 checksum verification
- [x] Static analysis dengan Bandit
- [x] Minimal permissions

**Kode (app.py):**
- [x] Tidak ada hardcoded secrets
- [x] Safe expression evaluation
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

---

## Catatan Penting

> **PERINGATAN:** Kode di branch `insecure` sengaja dibuat vulnerable untuk tujuan edukasi. **JANGAN** gunakan pattern tersebut di environment production.

---

## Author

Lab ini dibuat untuk sesi bootcamp **Dibimbing.id** - Day 23: Software and Data Integrity Failures

**Instructor:** Irwan Puspito
