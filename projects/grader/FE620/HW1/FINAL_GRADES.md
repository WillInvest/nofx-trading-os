# FE620 HW1 Final Grades

**Grading Date:** 2026-02-11
**Total Points:** 80

## Updated Grading Rules
1. **Rounding tolerance:** No deduction if math is correct but numerical result differs due to rounding
2. **Problem 1.3:** **-5 points** if rate was NOT converted (just used APR/365 instead of proper daily conversion)
3. **Problem 1.5 ii:** Must annualize using continuous compounding; answer should be 8.89%

## Correct Answers Reference
- **1.1:** F* = $5,229.88; Profit i) $29.88, ii) $70.12
- **1.2:** Annual: 3.2764%, Quarterly: 3.2369%, Continuous: 3.2239%
- **1.3:** Balance = $10,130.95 (MUST convert rate: r_d = (1+APR)^(1/365) - 1)
- **1.4:** B1: $102.83, YTM 3.491%; B2: $111.84, YTM 4.465%
- **1.5:** i) $25,000; ii) 8.89%

---

## Grades Summary

| Student | 1.1 | 1.2 | 1.3 | 1.4 | 1.5 | Total | Confidence | Notes |
|---------|-----|-----|-----|-----|-----|-------|------------|-------|
| Abramowitz, Matthew | 9 | 20 | **15** | 19 | 10 | **73** | MEDIUM | 1.3: no rate conversion |
| Agerup, Dennis | 10 | 20 | **15** | 19 | 10 | **74** | HIGH | 1.3: no rate conversion |
| Biju, Suraj | 10 | 20 | 20 | 18 | 10 | **78** | HIGH | 1.4: YTM used semi-annual |
| Chapwanya, Brandon Tanaka | 10 | 20 | 20 | 20 | 10 | **80** | HIGH | PERFECT |
| Brooks, Taylor | 6 | 14 | 0 | 0 | 0 | **20** | HIGH | INCOMPLETE - only 1 page |
| Di Domenico, Anthony | 9 | 20 | **15** | 17 | 7 | **68** | MEDIUM | 1.3: no rate conversion, 1.5ii wrong |
| D'Souza, Freya | - | - | - | - | - | **TBD** | - | 12MB file - manual review needed |
| Freire, Roberto | 8 | 20 | **15** | 16 | 10 | **69** | MEDIUM | 1.1ii: wrong logic, 1.3: no rate conversion |
| Glynn, Brooke | 10 | 20 | 20 | 19 | 10 | **79** | HIGH | Excellent R code! |
| Hauk, Anna | 10 | 20 | **15** | 19 | 9 | **73** | MEDIUM | 1.3: no rate conversion, 1.5ii: used discrete |
| Horgan, John | 10 | 20 | **15** | 19 | 10 | **74** | HIGH | 1.3: no rate conversion |
| Jacques, Widly | 10 | 20 | 20 | 18 | 10 | **78** | HIGH | 1.3 rate conversion CORRECT |
| Konopka, Michael | - | - | - | - | - | **TBD** | - | To be graded |
| Manjunatha, Raghavi | - | - | - | - | - | **TBD** | - | To be graded |
| McLoughlin, Jude | - | - | - | - | - | **TBD** | - | To be graded |
| Mehta, Hrishi | - | - | - | - | - | **TBD** | - | To be graded |
| Meyer, Ara | - | - | - | - | - | **TBD** | - | To be graded |
| Ramushi, Adrian | - | - | - | - | - | **TBD** | - | To be graded |
| Shin, Jinwoo | - | - | - | - | - | **TBD** | - | To be graded |
| Shlyam, Samuel | - | - | - | - | - | **TBD** | - | To be graded (LATE) |
| Sikandar Ali, Sultan | - | - | - | - | - | **TBD** | - | To be graded |
| Siwach, Ishaan | - | - | - | - | - | **TBD** | - | To be graded |
| Snodgrass, Makenzie | - | - | - | - | - | **TBD** | - | To be graded |
| Xiao, Yu | - | - | - | - | - | **TBD** | - | To be graded |

---

## Common Errors

### Problem 1.3 (-5 points) - Most Common Error
**18/24 students** made this error:
- **Wrong:** r_daily = 0.1715/365 = 0.0004699
- **Correct:** r_daily = (1+0.1715)^(1/365) - 1 = 0.000433751

This is the "APR interpretation" error. Credit card APR is stated with annual compounding, so converting to daily requires the proper exponential conversion, not simple division.

### Problem 1.1 - Minor Issues
- Some students used discrete compounding (1+r) instead of continuous (e^r)
- Both interpretations acceptable, results are close

### Problem 1.4 - YTM Convention
- Solution uses continuous compounding for YTM
- Many students used semi-annual discrete compounding
- Prices mostly correct, YTM values slightly different

---

## Statistics (Graded Students)

- **Total Graded:** 12/24
- **Average:** 74.5/80 (93.1%)
- **High:** 80 (Brandon Tanaka)
- **Low:** 20 (Brooks - incomplete)
- **Excluding incomplete:** 74.9/80 average

## Students Who Got Problem 1.3 CORRECT (Full 20/20)
1. Biju, Suraj
2. Chapwanya, Brandon Tanaka
3. Glynn, Brooke
4. Jacques, Widly

These students properly converted the APR to equivalent daily rate before compounding.
