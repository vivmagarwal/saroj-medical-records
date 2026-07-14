# Saroj Agarwal — Medical Records Collection

Compiled medical-record archive totalling **204 reports**, organised for quick clinical handoff. The core **188 reports** are from Sir H. N. Reliance Foundation Hospital, Mumbai (20 Feb – 13 Apr 2026); **16 post-discharge Surat follow-ups** have since been added: 6 from May–Jun 2026 (4 Nobel Micropath lab panels, a 1 May right-lower-limb venous Doppler [no DVT, from Navkar], and the 22 Jun follow-up WB FDG PET-CT from Prismaa Oncoimaging showing **RECIST 1.1 Partial Response, −47.1%** vs the February baseline), and **10 from the 5–13 Jul 2026 Maitreya Hospital (Surat) admission** for chest pain/syncope — HRCT chest (**pleural effusions increased** vs the Jun PET-CT), echo (**severe PAH, RVSP ~70 mmHg; LVEF ~50%**), 3 ECGs (RVH pattern, prolonged QTc up to ~529 ms), admission labs (creatinine climbing to **1.20**, CRP 9 mg/L, NT-proBNP 151, Hb normalised at 11.4), iron studies (no deficiency), urine (normal), and a reassuring **72-h Holter (10–13 Jul: sinus rhythm, no AF/VT/pauses; symptoms occurred in NSR)**.

For navigability, the **101 clinically pivotal reports** (imaging, summaries, cultures, sentinel/abnormal labs) sit in the main `report_pdf/`/`report_md/`, while **103 routine serial-monitoring labs** (repeat CBCs, electrolytes, creatinine, daily portable chest X-rays) were moved to `archived/` subfolders — their values are consolidated in **[TRENDS.md](./TRENDS.md)**. Nothing was deleted (archiving is a `git mv`).

> 🌐 **Live site**: https://vivmagarwal.github.io/saroj-medical-records/ (after Pages is enabled)

## Contents

| File / folder | What it is |
|---|---|
| `index.html` | Landing page — navigation hub for the three handoff notes |
| `referral_notes/` | The three 2-page specialty handoff notes (ENT, Pulmonology, Cardiology) as `{html,pdf}` |
| `TRENDS.md` | Dated tables of every serial lab value (Hb, electrolytes, creatinine, CRP, NT-proBNP, coagulation) |
| `MASTER_INDEX.md` | Date-grouped index of all 204 reports (101 key + 103 archived), newest → oldest |
| `ALL_MD_REPORTS.md` | All 204 per-report markdowns combined (key reports first, archived appendix) |
| `report_pdf/` | 101 key source PDFs, renamed `YYYY-MM-DD_Type_Description.pdf` (+ companion Doppler images); routine serials under `report_pdf/archived/` |
| `report_md/` | 101 key per-report markdowns; routine serials under `report_md/archived/` |
| `surat_reports_and_other_details/` | Raw original Surat PDFs (Nobel Micropath), by lab registration no. |

## Patient

- **Name**: Saroj Agarwal
- **Sex / Age**: Female / 63 y
- **DOB**: 27 Aug 1962
- **Patient ID**: 0010663186
- **Diagnosis**: Carcinoma uterus (ICD-10 C54), metastatic recurrence

## Distribution by report type

| Category | Count |
|---|---:|
| Lab — Biochemistry | 74 |
| Lab — Haematology | 40 |
| X-ray (chest) | 35 |
| Lab — Microbiology | 13 |
| Lab — Serology / Immunology | 12 |
| Lab — Surat follow-up (Nobel Micropath / Maitreya) | 8 |
| Echocardiography | 4 |
| CT (incl. PET-CT, HRCT) | 4 |
| ECG | 4 |
| Ultrasonography (incl. limb venous Doppler) | 3 |
| Lab — Clinical pathology | 2 |
| Holter | 2 |
| Discharge Summary, Daycare Summary, Consent | 1 each |

## Verification

- All 204 per-report summaries were **vision-verified** against the rendered source PDFs.
- The three specialty handoff notes were **independently fact-checked** by separate verification agents — every date, drug, dose, value, and verbatim quote was cross-referenced to the original.

## Privacy

Reports contain identifiable medical information of an actively-treated patient. Treat as confidential.
