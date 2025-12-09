# DevSecOps Security Gate - Observation Checklist

## Branch: `devsecops`

Gunakan checklist ini untuk mengobservasi bagaimana security gate bekerja dalam pipeline DevSecOps.

---

## Bagian A: Observasi Pipeline

### A1. Jalankan Pipeline

1. Fork repository ini (jika belum)
2. Pastikan Anda di branch `devsecops`
3. Buka tab **Actions** di GitHub
4. Klik **Run workflow** → **Run workflow**
5. Tunggu pipeline selesai

### A2. Observasi Hasil

| Stage | Expected Result | Actual Result |
|-------|-----------------|---------------|
| Security Scan | ❌ FAIL | [ ] FAIL / [ ] PASS |
| Code Quality | ❌ FAIL | [ ] FAIL / [ ] PASS |
| Build | ⏭️ SKIPPED | [ ] SKIPPED / [ ] RAN |
| Deploy | ⏭️ SKIPPED | [ ] SKIPPED / [ ] RAN |

---

## Bagian B: Analisis Security Findings

### B1. Bandit Findings

Buka log dari job **Security Scan** dan catat findings:

| Issue ID | Description | File | Line |
|----------|-------------|------|------|
| B307 | | | |
| B102 | | | |
| B301 | | | |
| B105/B106 | | | |

### B2. Hardcoded Secrets

Buka log dari job **Code Quality** dan catat findings:

| Pattern | Found? | Location |
|---------|--------|----------|
| API_KEY = "..." | [ ] Ya / [ ] Tidak | |
| PASSWORD = "..." | [ ] Ya / [ ] Tidak | |
| TOKEN = "..." | [ ] Ya / [ ] Tidak | |

---

## Bagian C: Pertanyaan Diskusi

### C1. Security Gate Effectiveness

1. **Mengapa pipeline gagal?**
   > _Jawaban Anda:_ ________________________________

2. **Apakah kegagalan ini hal yang baik atau buruk? Mengapa?**
   > _Jawaban Anda:_ ________________________________

3. **Apa yang akan terjadi jika tidak ada security gate?**
   > _Jawaban Anda:_ ________________________________

### C2. DevSecOps Principles

4. **Apa yang dimaksud dengan "Shift Left Security"?**
   > _Jawaban Anda:_ ________________________________

5. **Mengapa automated security gates lebih baik daripada hanya manual code review?**
   > _Jawaban Anda:_ ________________________________

### C3. Comparison

6. **Bandingkan hasil pipeline di 3 branch:**

   | Branch | Pipeline Result | Apakah Ini Aman? |
   |--------|-----------------|------------------|
   | `insecure` | | |
   | `devsecops` | | |
   | `secure` | | |

---

## Bagian D: Hands-on Exercise

### Exercise 1: Jalankan Bandit Lokal

```bash
# Install Bandit
pip install bandit

# Jalankan scan
bandit -r src/ -ll -ii -f txt

# Atau dengan format JSON untuk detail lebih
bandit -r src/ -ll -ii -f json
```

**Pertanyaan:** Berapa total issues yang ditemukan? _____

### Exercise 2: Cari Hardcoded Secrets

```bash
# Cari API keys
grep -rn "API_KEY\s*=\s*['\"]" src/

# Cari passwords
grep -rn "PASSWORD\s*=\s*['\"]" src/

# Cari tokens
grep -rn "TOKEN\s*=\s*['\"]" src/
```

**Pertanyaan:** Di baris berapa secrets ditemukan?
- API_KEY: Line _____
- PASSWORD: Line _____
- TOKEN: Line _____

### Exercise 3: Fix One Vulnerability

1. Edit `src/app.py`
2. Ganti satu instance `eval()` dengan alternatif aman
3. Jalankan Bandit lagi
4. Apakah jumlah findings berkurang?

**Before fix:** _____ issues
**After fix:** _____ issues

---

## Bagian E: Security Gate Architecture

### E1. Pipeline Flow Diagram

```
┌──────────────┐
│   Developer  │
│   Push Code  │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│   Checkout   │────▶│   SECURITY   │
│     Code     │     │    SCAN      │
└──────────────┘     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │  Vuln Found? │
                     └──────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
        ┌─────▼─────┐               ┌─────▼─────┐
        │    YES    │               │    NO     │
        │  ❌ FAIL  │               │  ✅ PASS  │
        └─────┬─────┘               └─────┬─────┘
              │                           │
              ▼                           ▼
        ┌───────────┐               ┌───────────┐
        │   STOP    │               │   BUILD   │
        │ Pipeline  │               │   STAGE   │
        └───────────┘               └─────┬─────┘
                                          │
                                          ▼
                                    ┌───────────┐
                                    │  DEPLOY   │
                                    └───────────┘
```

### E2. Identifikasi Stage

Untuk setiap stage, identifikasi:

| Stage | Tool yang Digunakan | Apa yang Dicek |
|-------|---------------------|----------------|
| Security Scan | | |
| Code Quality | | |
| Build | | |
| Deploy | | |

---

## Bagian F: Kesimpulan

### F1. Key Takeaways

Setelah mengobservasi branch `devsecops`, saya memahami bahwa:

1. [ ] Security gates dapat mendeteksi vulnerabilities secara otomatis
2. [ ] Pipeline yang gagal karena security issue adalah hal yang BAIK
3. [ ] DevSecOps mengintegrasikan security ke dalam CI/CD pipeline
4. [ ] Tools seperti Bandit dapat menemukan code injection vulnerabilities
5. [ ] Hardcoded secrets dapat dideteksi dengan pattern matching

### F2. Reflection

**Apa yang paling mengejutkan Anda dari observasi ini?**

> _Jawaban Anda:_ ________________________________

**Bagaimana Anda akan menerapkan konsep ini di project Anda?**

> _Jawaban Anda:_ ________________________________

---

## Jawaban (untuk Instruktur)

<details>
<summary>Klik untuk melihat jawaban</summary>

### Bandit Findings:
- **B307**: eval() usage - Line 35
- **B102**: exec() usage - Line 58  
- **B301**: pickle usage - Line 44
- **B105/B106**: Hardcoded password - Lines 17-20

### Hardcoded Secrets:
- API_KEY: Line 17
- DATABASE_PASSWORD: Line 18
- SECRET_TOKEN: Line 19

### Discussion Answers:
1. Pipeline gagal karena Bandit mendeteksi vulnerabilities
2. Ini adalah hal BAIK - mencegah vulnerable code ter-deploy
3. Tanpa security gate, kode vulnerable akan di-deploy ke production
4. Shift Left = mendeteksi masalah keamanan lebih awal di development cycle
5. Automated gates: konsisten, tidak lelah, tidak ada human error, scalable

### Comparison:
| Branch | Result | Aman? |
|--------|--------|-------|
| insecure | PASS | ❌ TIDAK (berbahaya!) |
| devsecops | FAIL | ✅ YA (gate bekerja) |
| secure | PASS | ✅ YA (kode aman) |

</details>

---

**Selamat mengobservasi DevSecOps pipeline!** 🔐
