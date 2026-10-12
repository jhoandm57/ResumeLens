# ResumeLens – Formal Definitions of the Transducers

> This file was generated from the transducers built by the code (class `NormalizationTransducers` with the tables of `NormalizationVocabulary`). If the vocabulary changes, these tables, the summary of `06_fst_design.md` (Section 6.8), and the diagrams of `diagrams/fst/` must be updated.

It contains the complete 7-tuple `M = (Q, Σ, Γ, δ, ω, q0, F)` of every transducer of the normalization stage. The design and the construction method are explained in `06_fst_design.md`.

Notation:

- `␣` is the space character.
- `#` is the end-of-input marker appended to every input.
- `ε` is the empty output.

## Summary

| Transducer | States (size of Q) | Input symbols (size of Σ) | Output symbols (size of Γ) | Transitions |
| :--- | :---: | :---: | :---: | :---: |
| `M_LANG` | 36 | 18 | 5 | 40 |
| `M_FW` | 140 | 27 | 13 | 161 |
| `M_DB` | 20 | 11 | 3 | 22 |
| `M_TOOLS` | 89 | 23 | 11 | 106 |
| `M_OTHER` | 137 | 22 | 6 | 145 |
| `M_ACAD` | 107 | 24 | 7 | 125 |
| `M_EXP` | 4 | 39 | 10 | 87 |

## M_LANG — Programming languages

```text
M_LANG = (Q, Σ, Γ, δ, ω, q0, F)

Q  = { q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, qf }
     |Q| = 36
Σ  = { a, b, c, e, h, i, j, l, n, o, p, q, r, s, t, v, y, # }
     |Σ| = 18
Γ  = { JAVASCRIPT, TYPESCRIPT, PYTHON, SQL, BASH }
     |Γ| = 5
q0 = q0
F  = { qf }
```

Number of transitions: 40.

Diagram: `diagrams/fst/m_lang.svg` (source: `diagrams/fst/m_lang.dot`).

### States

| State | Meaning |
| :--- | :--- |
| `q0` | prefix ε (nothing read) |
| `q1` | prefix `j` |
| `q2` | prefix `ja` |
| `q3` | prefix `jav` |
| `q4` | prefix `java` |
| `q5` | prefix `javas` |
| `q6` | prefix `javasc` |
| `q7` | prefix `javascr` |
| `q8` | prefix `javascri` |
| `q9` | prefix `javascrip` |
| `q10` | prefix `javascript` |
| `q11` | prefix `js` |
| `q12` | prefix `t` |
| `q13` | prefix `ty` |
| `q14` | prefix `typ` |
| `q15` | prefix `type` |
| `q16` | prefix `types` |
| `q17` | prefix `typesc` |
| `q18` | prefix `typescr` |
| `q19` | prefix `typescri` |
| `q20` | prefix `typescrip` |
| `q21` | prefix `typescript` |
| `q22` | prefix `p` |
| `q23` | prefix `py` |
| `q24` | prefix `pyt` |
| `q25` | prefix `pyth` |
| `q26` | prefix `pytho` |
| `q27` | prefix `python` |
| `q28` | prefix `s` |
| `q29` | prefix `sq` |
| `q30` | prefix `sql` |
| `q31` | prefix `b` |
| `q32` | prefix `ba` |
| `q33` | prefix `bas` |
| `q34` | prefix `bash` |
| `qf` | accepting state (end marker read) |

### Transition relation δ and output relation ω

`δ(state, input)` is the column *To*, and `ω(state, input)` is the column *Output*.

| From | Input | To | Output |
| :--- | :---: | :--- | :--- |
| `q0` | `j` | `q1` | `ε` |
| `q1` | `a` | `q2` | `ε` |
| `q2` | `v` | `q3` | `ε` |
| `q3` | `a` | `q4` | `ε` |
| `q4` | `s` | `q5` | `ε` |
| `q5` | `c` | `q6` | `ε` |
| `q6` | `r` | `q7` | `ε` |
| `q7` | `i` | `q8` | `ε` |
| `q8` | `p` | `q9` | `ε` |
| `q9` | `t` | `q10` | `ε` |
| `q10` | `#` | `qf` | `JAVASCRIPT` |
| `q1` | `s` | `q11` | `ε` |
| `q11` | `#` | `qf` | `JAVASCRIPT` |
| `q0` | `t` | `q12` | `ε` |
| `q12` | `y` | `q13` | `ε` |
| `q13` | `p` | `q14` | `ε` |
| `q14` | `e` | `q15` | `ε` |
| `q15` | `s` | `q16` | `ε` |
| `q16` | `c` | `q17` | `ε` |
| `q17` | `r` | `q18` | `ε` |
| `q18` | `i` | `q19` | `ε` |
| `q19` | `p` | `q20` | `ε` |
| `q20` | `t` | `q21` | `ε` |
| `q21` | `#` | `qf` | `TYPESCRIPT` |
| `q0` | `p` | `q22` | `ε` |
| `q22` | `y` | `q23` | `ε` |
| `q23` | `t` | `q24` | `ε` |
| `q24` | `h` | `q25` | `ε` |
| `q25` | `o` | `q26` | `ε` |
| `q26` | `n` | `q27` | `ε` |
| `q27` | `#` | `qf` | `PYTHON` |
| `q0` | `s` | `q28` | `ε` |
| `q28` | `q` | `q29` | `ε` |
| `q29` | `l` | `q30` | `ε` |
| `q30` | `#` | `qf` | `SQL` |
| `q0` | `b` | `q31` | `ε` |
| `q31` | `a` | `q32` | `ε` |
| `q32` | `s` | `q33` | `ε` |
| `q33` | `h` | `q34` | `ε` |
| `q34` | `#` | `qf` | `BASH` |

Any pair (state, input) that is not in the table has no transition, so the input is rejected.

## M_FW — Frameworks and libraries

```text
M_FW = (Q, Σ, Γ, δ, ω, q0, F)

Q  = { q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36, q37, q38, q39, q40, q41, q42, q43, q44, q45, q46, q47, q48, q49, q50, q51, q52, q53, q54, q55, q56, q57, q58, q59, q60, q61, q62, q63, q64, q65, q66, q67, q68, q69, q70, q71, q72, q73, q74, q75, q76, q77, q78, q79, q80, q81, q82, q83, q84, q85, q86, q87, q88, q89, q90, q91, q92, q93, q94, q95, q96, q97, q98, q99, q100, q101, q102, q103, q104, q105, q106, q107, q108, q109, q110, q111, q112, q113, q114, q115, q116, q117, q118, q119, q120, q121, q122, q123, q124, q125, q126, q127, q128, q129, q130, q131, q132, q133, q134, q135, q136, q137, q138, qf }
     |Q| = 140
Σ  = { ␣, -, ., a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, r, s, t, u, v, w, y, # }
     |Σ| = 27
Γ  = { REACT, ANGULAR, VUE, NODE_JS, DJANGO, SPRING_BOOT, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, PYTORCH, SPARK, AIRFLOW }
     |Γ| = 13
q0 = q0
F  = { qf }
```

Number of transitions: 161.

Diagram: `diagrams/fst/m_fw.svg` (source: `diagrams/fst/m_fw.dot`).

### States

| State | Meaning |
| :--- | :--- |
| `q0` | prefix ε (nothing read) |
| `q1` | prefix `r` |
| `q2` | prefix `re` |
| `q3` | prefix `rea` |
| `q4` | prefix `reac` |
| `q5` | prefix `react` |
| `q6` | prefix `react.` |
| `q7` | prefix `react.j` |
| `q8` | prefix `react.js` |
| `q9` | prefix `reactj` |
| `q10` | prefix `reactjs` |
| `q11` | prefix `a` |
| `q12` | prefix `an` |
| `q13` | prefix `ang` |
| `q14` | prefix `angu` |
| `q15` | prefix `angul` |
| `q16` | prefix `angula` |
| `q17` | prefix `angular` |
| `q18` | prefix `v` |
| `q19` | prefix `vu` |
| `q20` | prefix `vue` |
| `q21` | prefix `n` |
| `q22` | prefix `no` |
| `q23` | prefix `nod` |
| `q24` | prefix `node` |
| `q25` | prefix `node.` |
| `q26` | prefix `node.j` |
| `q27` | prefix `node.js` |
| `q28` | prefix `nodej` |
| `q29` | prefix `nodejs` |
| `q30` | prefix `d` |
| `q31` | prefix `dj` |
| `q32` | prefix `dja` |
| `q33` | prefix `djan` |
| `q34` | prefix `djang` |
| `q35` | prefix `django` |
| `q36` | prefix `s` |
| `q37` | prefix `sp` |
| `q38` | prefix `spr` |
| `q39` | prefix `spri` |
| `q40` | prefix `sprin` |
| `q41` | prefix `spring` |
| `q42` | prefix `spring␣` |
| `q43` | prefix `spring␣b` |
| `q44` | prefix `spring␣bo` |
| `q45` | prefix `spring␣boo` |
| `q46` | prefix `spring␣boot` |
| `q47` | prefix `p` |
| `q48` | prefix `pa` |
| `q49` | prefix `pan` |
| `q50` | prefix `pand` |
| `q51` | prefix `panda` |
| `q52` | prefix `pandas` |
| `q53` | prefix `nu` |
| `q54` | prefix `num` |
| `q55` | prefix `nump` |
| `q56` | prefix `numpy` |
| `q57` | prefix `sc` |
| `q58` | prefix `sci` |
| `q59` | prefix `scik` |
| `q60` | prefix `sciki` |
| `q61` | prefix `scikit` |
| `q62` | prefix `scikit-` |
| `q63` | prefix `scikit-l` |
| `q64` | prefix `scikit-le` |
| `q65` | prefix `scikit-lea` |
| `q66` | prefix `scikit-lear` |
| `q67` | prefix `scikit-learn` |
| `q68` | prefix `scikit␣` |
| `q69` | prefix `scikit␣l` |
| `q70` | prefix `scikit␣le` |
| `q71` | prefix `scikit␣lea` |
| `q72` | prefix `scikit␣lear` |
| `q73` | prefix `scikit␣learn` |
| `q74` | prefix `scikitl` |
| `q75` | prefix `scikitle` |
| `q76` | prefix `scikitlea` |
| `q77` | prefix `scikitlear` |
| `q78` | prefix `scikitlearn` |
| `q79` | prefix `sk` |
| `q80` | prefix `skl` |
| `q81` | prefix `skle` |
| `q82` | prefix `sklea` |
| `q83` | prefix `sklear` |
| `q84` | prefix `sklearn` |
| `q85` | prefix `t` |
| `q86` | prefix `te` |
| `q87` | prefix `ten` |
| `q88` | prefix `tens` |
| `q89` | prefix `tenso` |
| `q90` | prefix `tensor` |
| `q91` | prefix `tensorf` |
| `q92` | prefix `tensorfl` |
| `q93` | prefix `tensorflo` |
| `q94` | prefix `tensorflow` |
| `q95` | prefix `tensor␣` |
| `q96` | prefix `tensor␣f` |
| `q97` | prefix `tensor␣fl` |
| `q98` | prefix `tensor␣flo` |
| `q99` | prefix `tensor␣flow` |
| `q100` | prefix `py` |
| `q101` | prefix `pyt` |
| `q102` | prefix `pyto` |
| `q103` | prefix `pytor` |
| `q104` | prefix `pytorc` |
| `q105` | prefix `pytorch` |
| `q106` | prefix `py␣` |
| `q107` | prefix `py␣t` |
| `q108` | prefix `py␣to` |
| `q109` | prefix `py␣tor` |
| `q110` | prefix `py␣torc` |
| `q111` | prefix `py␣torch` |
| `q112` | prefix `ap` |
| `q113` | prefix `apa` |
| `q114` | prefix `apac` |
| `q115` | prefix `apach` |
| `q116` | prefix `apache` |
| `q117` | prefix `apache␣` |
| `q118` | prefix `apache␣s` |
| `q119` | prefix `apache␣sp` |
| `q120` | prefix `apache␣spa` |
| `q121` | prefix `apache␣spar` |
| `q122` | prefix `apache␣spark` |
| `q123` | prefix `spa` |
| `q124` | prefix `spar` |
| `q125` | prefix `spark` |
| `q126` | prefix `apache␣a` |
| `q127` | prefix `apache␣ai` |
| `q128` | prefix `apache␣air` |
| `q129` | prefix `apache␣airf` |
| `q130` | prefix `apache␣airfl` |
| `q131` | prefix `apache␣airflo` |
| `q132` | prefix `apache␣airflow` |
| `q133` | prefix `ai` |
| `q134` | prefix `air` |
| `q135` | prefix `airf` |
| `q136` | prefix `airfl` |
| `q137` | prefix `airflo` |
| `q138` | prefix `airflow` |
| `qf` | accepting state (end marker read) |

### Transition relation δ and output relation ω

`δ(state, input)` is the column *To*, and `ω(state, input)` is the column *Output*.

| From | Input | To | Output |
| :--- | :---: | :--- | :--- |
| `q0` | `r` | `q1` | `ε` |
| `q1` | `e` | `q2` | `ε` |
| `q2` | `a` | `q3` | `ε` |
| `q3` | `c` | `q4` | `ε` |
| `q4` | `t` | `q5` | `ε` |
| `q5` | `#` | `qf` | `REACT` |
| `q5` | `.` | `q6` | `ε` |
| `q6` | `j` | `q7` | `ε` |
| `q7` | `s` | `q8` | `ε` |
| `q8` | `#` | `qf` | `REACT` |
| `q5` | `j` | `q9` | `ε` |
| `q9` | `s` | `q10` | `ε` |
| `q10` | `#` | `qf` | `REACT` |
| `q0` | `a` | `q11` | `ε` |
| `q11` | `n` | `q12` | `ε` |
| `q12` | `g` | `q13` | `ε` |
| `q13` | `u` | `q14` | `ε` |
| `q14` | `l` | `q15` | `ε` |
| `q15` | `a` | `q16` | `ε` |
| `q16` | `r` | `q17` | `ε` |
| `q17` | `#` | `qf` | `ANGULAR` |
| `q0` | `v` | `q18` | `ε` |
| `q18` | `u` | `q19` | `ε` |
| `q19` | `e` | `q20` | `ε` |
| `q20` | `#` | `qf` | `VUE` |
| `q0` | `n` | `q21` | `ε` |
| `q21` | `o` | `q22` | `ε` |
| `q22` | `d` | `q23` | `ε` |
| `q23` | `e` | `q24` | `ε` |
| `q24` | `.` | `q25` | `ε` |
| `q25` | `j` | `q26` | `ε` |
| `q26` | `s` | `q27` | `ε` |
| `q27` | `#` | `qf` | `NODE_JS` |
| `q24` | `j` | `q28` | `ε` |
| `q28` | `s` | `q29` | `ε` |
| `q29` | `#` | `qf` | `NODE_JS` |
| `q0` | `d` | `q30` | `ε` |
| `q30` | `j` | `q31` | `ε` |
| `q31` | `a` | `q32` | `ε` |
| `q32` | `n` | `q33` | `ε` |
| `q33` | `g` | `q34` | `ε` |
| `q34` | `o` | `q35` | `ε` |
| `q35` | `#` | `qf` | `DJANGO` |
| `q0` | `s` | `q36` | `ε` |
| `q36` | `p` | `q37` | `ε` |
| `q37` | `r` | `q38` | `ε` |
| `q38` | `i` | `q39` | `ε` |
| `q39` | `n` | `q40` | `ε` |
| `q40` | `g` | `q41` | `ε` |
| `q41` | `␣` | `q42` | `ε` |
| `q42` | `b` | `q43` | `ε` |
| `q43` | `o` | `q44` | `ε` |
| `q44` | `o` | `q45` | `ε` |
| `q45` | `t` | `q46` | `ε` |
| `q46` | `#` | `qf` | `SPRING_BOOT` |
| `q0` | `p` | `q47` | `ε` |
| `q47` | `a` | `q48` | `ε` |
| `q48` | `n` | `q49` | `ε` |
| `q49` | `d` | `q50` | `ε` |
| `q50` | `a` | `q51` | `ε` |
| `q51` | `s` | `q52` | `ε` |
| `q52` | `#` | `qf` | `PANDAS` |
| `q21` | `u` | `q53` | `ε` |
| `q53` | `m` | `q54` | `ε` |
| `q54` | `p` | `q55` | `ε` |
| `q55` | `y` | `q56` | `ε` |
| `q56` | `#` | `qf` | `NUMPY` |
| `q36` | `c` | `q57` | `ε` |
| `q57` | `i` | `q58` | `ε` |
| `q58` | `k` | `q59` | `ε` |
| `q59` | `i` | `q60` | `ε` |
| `q60` | `t` | `q61` | `ε` |
| `q61` | `-` | `q62` | `ε` |
| `q62` | `l` | `q63` | `ε` |
| `q63` | `e` | `q64` | `ε` |
| `q64` | `a` | `q65` | `ε` |
| `q65` | `r` | `q66` | `ε` |
| `q66` | `n` | `q67` | `ε` |
| `q67` | `#` | `qf` | `SCIKIT_LEARN` |
| `q61` | `␣` | `q68` | `ε` |
| `q68` | `l` | `q69` | `ε` |
| `q69` | `e` | `q70` | `ε` |
| `q70` | `a` | `q71` | `ε` |
| `q71` | `r` | `q72` | `ε` |
| `q72` | `n` | `q73` | `ε` |
| `q73` | `#` | `qf` | `SCIKIT_LEARN` |
| `q61` | `l` | `q74` | `ε` |
| `q74` | `e` | `q75` | `ε` |
| `q75` | `a` | `q76` | `ε` |
| `q76` | `r` | `q77` | `ε` |
| `q77` | `n` | `q78` | `ε` |
| `q78` | `#` | `qf` | `SCIKIT_LEARN` |
| `q36` | `k` | `q79` | `ε` |
| `q79` | `l` | `q80` | `ε` |
| `q80` | `e` | `q81` | `ε` |
| `q81` | `a` | `q82` | `ε` |
| `q82` | `r` | `q83` | `ε` |
| `q83` | `n` | `q84` | `ε` |
| `q84` | `#` | `qf` | `SCIKIT_LEARN` |
| `q0` | `t` | `q85` | `ε` |
| `q85` | `e` | `q86` | `ε` |
| `q86` | `n` | `q87` | `ε` |
| `q87` | `s` | `q88` | `ε` |
| `q88` | `o` | `q89` | `ε` |
| `q89` | `r` | `q90` | `ε` |
| `q90` | `f` | `q91` | `ε` |
| `q91` | `l` | `q92` | `ε` |
| `q92` | `o` | `q93` | `ε` |
| `q93` | `w` | `q94` | `ε` |
| `q94` | `#` | `qf` | `TENSORFLOW` |
| `q90` | `␣` | `q95` | `ε` |
| `q95` | `f` | `q96` | `ε` |
| `q96` | `l` | `q97` | `ε` |
| `q97` | `o` | `q98` | `ε` |
| `q98` | `w` | `q99` | `ε` |
| `q99` | `#` | `qf` | `TENSORFLOW` |
| `q47` | `y` | `q100` | `ε` |
| `q100` | `t` | `q101` | `ε` |
| `q101` | `o` | `q102` | `ε` |
| `q102` | `r` | `q103` | `ε` |
| `q103` | `c` | `q104` | `ε` |
| `q104` | `h` | `q105` | `ε` |
| `q105` | `#` | `qf` | `PYTORCH` |
| `q100` | `␣` | `q106` | `ε` |
| `q106` | `t` | `q107` | `ε` |
| `q107` | `o` | `q108` | `ε` |
| `q108` | `r` | `q109` | `ε` |
| `q109` | `c` | `q110` | `ε` |
| `q110` | `h` | `q111` | `ε` |
| `q111` | `#` | `qf` | `PYTORCH` |
| `q11` | `p` | `q112` | `ε` |
| `q112` | `a` | `q113` | `ε` |
| `q113` | `c` | `q114` | `ε` |
| `q114` | `h` | `q115` | `ε` |
| `q115` | `e` | `q116` | `ε` |
| `q116` | `␣` | `q117` | `ε` |
| `q117` | `s` | `q118` | `ε` |
| `q118` | `p` | `q119` | `ε` |
| `q119` | `a` | `q120` | `ε` |
| `q120` | `r` | `q121` | `ε` |
| `q121` | `k` | `q122` | `ε` |
| `q122` | `#` | `qf` | `SPARK` |
| `q37` | `a` | `q123` | `ε` |
| `q123` | `r` | `q124` | `ε` |
| `q124` | `k` | `q125` | `ε` |
| `q125` | `#` | `qf` | `SPARK` |
| `q117` | `a` | `q126` | `ε` |
| `q126` | `i` | `q127` | `ε` |
| `q127` | `r` | `q128` | `ε` |
| `q128` | `f` | `q129` | `ε` |
| `q129` | `l` | `q130` | `ε` |
| `q130` | `o` | `q131` | `ε` |
| `q131` | `w` | `q132` | `ε` |
| `q132` | `#` | `qf` | `AIRFLOW` |
| `q11` | `i` | `q133` | `ε` |
| `q133` | `r` | `q134` | `ε` |
| `q134` | `f` | `q135` | `ε` |
| `q135` | `l` | `q136` | `ε` |
| `q136` | `o` | `q137` | `ε` |
| `q137` | `w` | `q138` | `ε` |
| `q138` | `#` | `qf` | `AIRFLOW` |

Any pair (state, input) that is not in the table has no transition, so the input is rejected.

## M_DB — Databases

```text
M_DB = (Q, Σ, Γ, δ, ω, q0, F)

Q  = { q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, qf }
     |Q| = 20
Σ  = { e, g, l, n, o, p, q, r, s, t, # }
     |Σ| = 11
Γ  = { POSTGRESQL, NOSQL, SQL }
     |Γ| = 3
q0 = q0
F  = { qf }
```

Number of transitions: 22.

Diagram: `diagrams/fst/m_db.svg` (source: `diagrams/fst/m_db.dot`).

### States

| State | Meaning |
| :--- | :--- |
| `q0` | prefix ε (nothing read) |
| `q1` | prefix `p` |
| `q2` | prefix `po` |
| `q3` | prefix `pos` |
| `q4` | prefix `post` |
| `q5` | prefix `postg` |
| `q6` | prefix `postgr` |
| `q7` | prefix `postgre` |
| `q8` | prefix `postgres` |
| `q9` | prefix `postgresq` |
| `q10` | prefix `postgresql` |
| `q11` | prefix `n` |
| `q12` | prefix `no` |
| `q13` | prefix `nos` |
| `q14` | prefix `nosq` |
| `q15` | prefix `nosql` |
| `q16` | prefix `s` |
| `q17` | prefix `sq` |
| `q18` | prefix `sql` |
| `qf` | accepting state (end marker read) |

### Transition relation δ and output relation ω

`δ(state, input)` is the column *To*, and `ω(state, input)` is the column *Output*.

| From | Input | To | Output |
| :--- | :---: | :--- | :--- |
| `q0` | `p` | `q1` | `ε` |
| `q1` | `o` | `q2` | `ε` |
| `q2` | `s` | `q3` | `ε` |
| `q3` | `t` | `q4` | `ε` |
| `q4` | `g` | `q5` | `ε` |
| `q5` | `r` | `q6` | `ε` |
| `q6` | `e` | `q7` | `ε` |
| `q7` | `s` | `q8` | `ε` |
| `q8` | `q` | `q9` | `ε` |
| `q9` | `l` | `q10` | `ε` |
| `q10` | `#` | `qf` | `POSTGRESQL` |
| `q8` | `#` | `qf` | `POSTGRESQL` |
| `q0` | `n` | `q11` | `ε` |
| `q11` | `o` | `q12` | `ε` |
| `q12` | `s` | `q13` | `ε` |
| `q13` | `q` | `q14` | `ε` |
| `q14` | `l` | `q15` | `ε` |
| `q15` | `#` | `qf` | `NOSQL` |
| `q0` | `s` | `q16` | `ε` |
| `q16` | `q` | `q17` | `ε` |
| `q17` | `l` | `q18` | `ε` |
| `q18` | `#` | `qf` | `SQL` |

Any pair (state, input) that is not in the table has no transition, so the input is rejected.

## M_TOOLS — Tools and technologies

```text
M_TOOLS = (Q, Σ, Γ, δ, ω, q0, F)

Q  = { q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36, q37, q38, q39, q40, q41, q42, q43, q44, q45, q46, q47, q48, q49, q50, q51, q52, q53, q54, q55, q56, q57, q58, q59, q60, q61, q62, q63, q64, q65, q66, q67, q68, q69, q70, q71, q72, q73, q74, q75, q76, q77, q78, q79, q80, q81, q82, q83, q84, q85, q86, q87, qf }
     |Q| = 89
Σ  = { ␣, /, a, b, c, d, e, g, h, i, k, l, m, n, o, p, r, s, t, u, w, x, # }
     |Σ| = 23
Γ  = { GIT, DOCKER, KUBERNETES, NMAP, LINUX, TCP_IP, NETWORKING, ETL, ELT, DATA_PIPELINE, DATA_WAREHOUSING }
     |Γ| = 11
q0 = q0
F  = { qf }
```

Number of transitions: 106.

Diagram: `diagrams/fst/m_tools.svg` (source: `diagrams/fst/m_tools.dot`).

### States

| State | Meaning |
| :--- | :--- |
| `q0` | prefix ε (nothing read) |
| `q1` | prefix `g` |
| `q2` | prefix `gi` |
| `q3` | prefix `git` |
| `q4` | prefix `d` |
| `q5` | prefix `do` |
| `q6` | prefix `doc` |
| `q7` | prefix `dock` |
| `q8` | prefix `docke` |
| `q9` | prefix `docker` |
| `q10` | prefix `k` |
| `q11` | prefix `ku` |
| `q12` | prefix `kub` |
| `q13` | prefix `kube` |
| `q14` | prefix `kuber` |
| `q15` | prefix `kubern` |
| `q16` | prefix `kuberne` |
| `q17` | prefix `kubernet` |
| `q18` | prefix `kubernete` |
| `q19` | prefix `kubernetes` |
| `q20` | prefix `n` |
| `q21` | prefix `nm` |
| `q22` | prefix `nma` |
| `q23` | prefix `nmap` |
| `q24` | prefix `l` |
| `q25` | prefix `li` |
| `q26` | prefix `lin` |
| `q27` | prefix `linu` |
| `q28` | prefix `linux` |
| `q29` | prefix `t` |
| `q30` | prefix `tc` |
| `q31` | prefix `tcp` |
| `q32` | prefix `tcp/` |
| `q33` | prefix `tcp/i` |
| `q34` | prefix `tcp/ip` |
| `q35` | prefix `tcp␣` |
| `q36` | prefix `tcp␣i` |
| `q37` | prefix `tcp␣ip` |
| `q38` | prefix `tcp␣/` |
| `q39` | prefix `tcp␣/␣` |
| `q40` | prefix `tcp␣/␣i` |
| `q41` | prefix `tcp␣/␣ip` |
| `q42` | prefix `tcp␣/i` |
| `q43` | prefix `tcp␣/ip` |
| `q44` | prefix `tcp/␣` |
| `q45` | prefix `tcp/␣i` |
| `q46` | prefix `tcp/␣ip` |
| `q47` | prefix `tcpi` |
| `q48` | prefix `tcpip` |
| `q49` | prefix `ne` |
| `q50` | prefix `net` |
| `q51` | prefix `netw` |
| `q52` | prefix `netwo` |
| `q53` | prefix `networ` |
| `q54` | prefix `network` |
| `q55` | prefix `networki` |
| `q56` | prefix `networkin` |
| `q57` | prefix `networking` |
| `q58` | prefix `e` |
| `q59` | prefix `et` |
| `q60` | prefix `etl` |
| `q61` | prefix `el` |
| `q62` | prefix `elt` |
| `q63` | prefix `da` |
| `q64` | prefix `dat` |
| `q65` | prefix `data` |
| `q66` | prefix `data␣` |
| `q67` | prefix `data␣p` |
| `q68` | prefix `data␣pi` |
| `q69` | prefix `data␣pip` |
| `q70` | prefix `data␣pipe` |
| `q71` | prefix `data␣pipel` |
| `q72` | prefix `data␣pipeli` |
| `q73` | prefix `data␣pipelin` |
| `q74` | prefix `data␣pipeline` |
| `q75` | prefix `data␣pipelines` |
| `q76` | prefix `data␣w` |
| `q77` | prefix `data␣wa` |
| `q78` | prefix `data␣war` |
| `q79` | prefix `data␣ware` |
| `q80` | prefix `data␣wareh` |
| `q81` | prefix `data␣wareho` |
| `q82` | prefix `data␣warehou` |
| `q83` | prefix `data␣warehous` |
| `q84` | prefix `data␣warehouse` |
| `q85` | prefix `data␣warehousi` |
| `q86` | prefix `data␣warehousin` |
| `q87` | prefix `data␣warehousing` |
| `qf` | accepting state (end marker read) |

### Transition relation δ and output relation ω

`δ(state, input)` is the column *To*, and `ω(state, input)` is the column *Output*.

| From | Input | To | Output |
| :--- | :---: | :--- | :--- |
| `q0` | `g` | `q1` | `ε` |
| `q1` | `i` | `q2` | `ε` |
| `q2` | `t` | `q3` | `ε` |
| `q3` | `#` | `qf` | `GIT` |
| `q0` | `d` | `q4` | `ε` |
| `q4` | `o` | `q5` | `ε` |
| `q5` | `c` | `q6` | `ε` |
| `q6` | `k` | `q7` | `ε` |
| `q7` | `e` | `q8` | `ε` |
| `q8` | `r` | `q9` | `ε` |
| `q9` | `#` | `qf` | `DOCKER` |
| `q0` | `k` | `q10` | `ε` |
| `q10` | `u` | `q11` | `ε` |
| `q11` | `b` | `q12` | `ε` |
| `q12` | `e` | `q13` | `ε` |
| `q13` | `r` | `q14` | `ε` |
| `q14` | `n` | `q15` | `ε` |
| `q15` | `e` | `q16` | `ε` |
| `q16` | `t` | `q17` | `ε` |
| `q17` | `e` | `q18` | `ε` |
| `q18` | `s` | `q19` | `ε` |
| `q19` | `#` | `qf` | `KUBERNETES` |
| `q0` | `n` | `q20` | `ε` |
| `q20` | `m` | `q21` | `ε` |
| `q21` | `a` | `q22` | `ε` |
| `q22` | `p` | `q23` | `ε` |
| `q23` | `#` | `qf` | `NMAP` |
| `q0` | `l` | `q24` | `ε` |
| `q24` | `i` | `q25` | `ε` |
| `q25` | `n` | `q26` | `ε` |
| `q26` | `u` | `q27` | `ε` |
| `q27` | `x` | `q28` | `ε` |
| `q28` | `#` | `qf` | `LINUX` |
| `q0` | `t` | `q29` | `ε` |
| `q29` | `c` | `q30` | `ε` |
| `q30` | `p` | `q31` | `ε` |
| `q31` | `/` | `q32` | `ε` |
| `q32` | `i` | `q33` | `ε` |
| `q33` | `p` | `q34` | `ε` |
| `q34` | `#` | `qf` | `TCP_IP` |
| `q31` | `␣` | `q35` | `ε` |
| `q35` | `i` | `q36` | `ε` |
| `q36` | `p` | `q37` | `ε` |
| `q37` | `#` | `qf` | `TCP_IP` |
| `q35` | `/` | `q38` | `ε` |
| `q38` | `␣` | `q39` | `ε` |
| `q39` | `i` | `q40` | `ε` |
| `q40` | `p` | `q41` | `ε` |
| `q41` | `#` | `qf` | `TCP_IP` |
| `q38` | `i` | `q42` | `ε` |
| `q42` | `p` | `q43` | `ε` |
| `q43` | `#` | `qf` | `TCP_IP` |
| `q32` | `␣` | `q44` | `ε` |
| `q44` | `i` | `q45` | `ε` |
| `q45` | `p` | `q46` | `ε` |
| `q46` | `#` | `qf` | `TCP_IP` |
| `q31` | `i` | `q47` | `ε` |
| `q47` | `p` | `q48` | `ε` |
| `q48` | `#` | `qf` | `TCP_IP` |
| `q20` | `e` | `q49` | `ε` |
| `q49` | `t` | `q50` | `ε` |
| `q50` | `w` | `q51` | `ε` |
| `q51` | `o` | `q52` | `ε` |
| `q52` | `r` | `q53` | `ε` |
| `q53` | `k` | `q54` | `ε` |
| `q54` | `i` | `q55` | `ε` |
| `q55` | `n` | `q56` | `ε` |
| `q56` | `g` | `q57` | `ε` |
| `q57` | `#` | `qf` | `NETWORKING` |
| `q54` | `#` | `qf` | `NETWORKING` |
| `q0` | `e` | `q58` | `ε` |
| `q58` | `t` | `q59` | `ε` |
| `q59` | `l` | `q60` | `ε` |
| `q60` | `#` | `qf` | `ETL` |
| `q58` | `l` | `q61` | `ε` |
| `q61` | `t` | `q62` | `ε` |
| `q62` | `#` | `qf` | `ELT` |
| `q4` | `a` | `q63` | `ε` |
| `q63` | `t` | `q64` | `ε` |
| `q64` | `a` | `q65` | `ε` |
| `q65` | `␣` | `q66` | `ε` |
| `q66` | `p` | `q67` | `ε` |
| `q67` | `i` | `q68` | `ε` |
| `q68` | `p` | `q69` | `ε` |
| `q69` | `e` | `q70` | `ε` |
| `q70` | `l` | `q71` | `ε` |
| `q71` | `i` | `q72` | `ε` |
| `q72` | `n` | `q73` | `ε` |
| `q73` | `e` | `q74` | `ε` |
| `q74` | `#` | `qf` | `DATA_PIPELINE` |
| `q74` | `s` | `q75` | `ε` |
| `q75` | `#` | `qf` | `DATA_PIPELINE` |
| `q66` | `w` | `q76` | `ε` |
| `q76` | `a` | `q77` | `ε` |
| `q77` | `r` | `q78` | `ε` |
| `q78` | `e` | `q79` | `ε` |
| `q79` | `h` | `q80` | `ε` |
| `q80` | `o` | `q81` | `ε` |
| `q81` | `u` | `q82` | `ε` |
| `q82` | `s` | `q83` | `ε` |
| `q83` | `e` | `q84` | `ε` |
| `q84` | `#` | `qf` | `DATA_WAREHOUSING` |
| `q83` | `i` | `q85` | `ε` |
| `q85` | `n` | `q86` | `ε` |
| `q86` | `g` | `q87` | `ε` |
| `q87` | `#` | `qf` | `DATA_WAREHOUSING` |

Any pair (state, input) that is not in the table has no transition, so the input is rejected.

## M_OTHER — Other qualifications

```text
M_OTHER = (Q, Σ, Γ, δ, ω, q0, F)

Q  = { q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36, q37, q38, q39, q40, q41, q42, q43, q44, q45, q46, q47, q48, q49, q50, q51, q52, q53, q54, q55, q56, q57, q58, q59, q60, q61, q62, q63, q64, q65, q66, q67, q68, q69, q70, q71, q72, q73, q74, q75, q76, q77, q78, q79, q80, q81, q82, q83, q84, q85, q86, q87, q88, q89, q90, q91, q92, q93, q94, q95, q96, q97, q98, q99, q100, q101, q102, q103, q104, q105, q106, q107, q108, q109, q110, q111, q112, q113, q114, q115, q116, q117, q118, q119, q120, q121, q122, q123, q124, q125, q126, q127, q128, q129, q130, q131, q132, q133, q134, q135, qf }
     |Q| = 137
Σ  = { ␣, -, a, b, c, d, e, g, h, i, l, m, n, o, p, r, s, t, u, v, y, # }
     |Σ| = 22
Γ  = { MACHINE_LEARNING, ML_MODEL_DEVELOPMENT, REST_API, VULNERABILITY_ASSESSMENT, CYBERSECURITY, SECURITY_AUTOMATION }
     |Γ| = 6
q0 = q0
F  = { qf }
```

Number of transitions: 145.

Diagram: `diagrams/fst/m_other.svg` (source: `diagrams/fst/m_other.dot`).

### States

| State | Meaning |
| :--- | :--- |
| `q0` | prefix ε (nothing read) |
| `q1` | prefix `m` |
| `q2` | prefix `ma` |
| `q3` | prefix `mac` |
| `q4` | prefix `mach` |
| `q5` | prefix `machi` |
| `q6` | prefix `machin` |
| `q7` | prefix `machine` |
| `q8` | prefix `machine␣` |
| `q9` | prefix `machine␣l` |
| `q10` | prefix `machine␣le` |
| `q11` | prefix `machine␣lea` |
| `q12` | prefix `machine␣lear` |
| `q13` | prefix `machine␣learn` |
| `q14` | prefix `machine␣learni` |
| `q15` | prefix `machine␣learnin` |
| `q16` | prefix `machine␣learning` |
| `q17` | prefix `machine-` |
| `q18` | prefix `machine-l` |
| `q19` | prefix `machine-le` |
| `q20` | prefix `machine-lea` |
| `q21` | prefix `machine-lear` |
| `q22` | prefix `machine-learn` |
| `q23` | prefix `machine-learni` |
| `q24` | prefix `machine-learnin` |
| `q25` | prefix `machine-learning` |
| `q26` | prefix `machine␣learning␣` |
| `q27` | prefix `machine␣learning␣m` |
| `q28` | prefix `machine␣learning␣mo` |
| `q29` | prefix `machine␣learning␣mod` |
| `q30` | prefix `machine␣learning␣mode` |
| `q31` | prefix `machine␣learning␣model` |
| `q32` | prefix `machine␣learning␣model␣` |
| `q33` | prefix `machine␣learning␣model␣d` |
| `q34` | prefix `machine␣learning␣model␣de` |
| `q35` | prefix `machine␣learning␣model␣dev` |
| `q36` | prefix `machine␣learning␣model␣deve` |
| `q37` | prefix `machine␣learning␣model␣devel` |
| `q38` | prefix `machine␣learning␣model␣develo` |
| `q39` | prefix `machine␣learning␣model␣develop` |
| `q40` | prefix `machine␣learning␣model␣developm` |
| `q41` | prefix `machine␣learning␣model␣developme` |
| `q42` | prefix `machine␣learning␣model␣developmen` |
| `q43` | prefix `machine␣learning␣model␣development` |
| `q44` | prefix `machine-learning␣` |
| `q45` | prefix `machine-learning␣m` |
| `q46` | prefix `machine-learning␣mo` |
| `q47` | prefix `machine-learning␣mod` |
| `q48` | prefix `machine-learning␣mode` |
| `q49` | prefix `machine-learning␣model` |
| `q50` | prefix `machine-learning␣model␣` |
| `q51` | prefix `machine-learning␣model␣d` |
| `q52` | prefix `machine-learning␣model␣de` |
| `q53` | prefix `machine-learning␣model␣dev` |
| `q54` | prefix `machine-learning␣model␣deve` |
| `q55` | prefix `machine-learning␣model␣devel` |
| `q56` | prefix `machine-learning␣model␣develo` |
| `q57` | prefix `machine-learning␣model␣develop` |
| `q58` | prefix `machine-learning␣model␣developm` |
| `q59` | prefix `machine-learning␣model␣developme` |
| `q60` | prefix `machine-learning␣model␣developmen` |
| `q61` | prefix `machine-learning␣model␣development` |
| `q62` | prefix `r` |
| `q63` | prefix `re` |
| `q64` | prefix `res` |
| `q65` | prefix `rest` |
| `q66` | prefix `rest␣` |
| `q67` | prefix `rest␣a` |
| `q68` | prefix `rest␣ap` |
| `q69` | prefix `rest␣api` |
| `q70` | prefix `rest␣apis` |
| `q71` | prefix `v` |
| `q72` | prefix `vu` |
| `q73` | prefix `vul` |
| `q74` | prefix `vuln` |
| `q75` | prefix `vulne` |
| `q76` | prefix `vulner` |
| `q77` | prefix `vulnera` |
| `q78` | prefix `vulnerab` |
| `q79` | prefix `vulnerabi` |
| `q80` | prefix `vulnerabil` |
| `q81` | prefix `vulnerabili` |
| `q82` | prefix `vulnerabilit` |
| `q83` | prefix `vulnerability` |
| `q84` | prefix `vulnerability␣` |
| `q85` | prefix `vulnerability␣a` |
| `q86` | prefix `vulnerability␣as` |
| `q87` | prefix `vulnerability␣ass` |
| `q88` | prefix `vulnerability␣asse` |
| `q89` | prefix `vulnerability␣asses` |
| `q90` | prefix `vulnerability␣assess` |
| `q91` | prefix `vulnerability␣assessm` |
| `q92` | prefix `vulnerability␣assessme` |
| `q93` | prefix `vulnerability␣assessmen` |
| `q94` | prefix `vulnerability␣assessment` |
| `q95` | prefix `c` |
| `q96` | prefix `cy` |
| `q97` | prefix `cyb` |
| `q98` | prefix `cybe` |
| `q99` | prefix `cyber` |
| `q100` | prefix `cybers` |
| `q101` | prefix `cyberse` |
| `q102` | prefix `cybersec` |
| `q103` | prefix `cybersecu` |
| `q104` | prefix `cybersecur` |
| `q105` | prefix `cybersecuri` |
| `q106` | prefix `cybersecurit` |
| `q107` | prefix `cybersecurity` |
| `q108` | prefix `cyber␣` |
| `q109` | prefix `cyber␣s` |
| `q110` | prefix `cyber␣se` |
| `q111` | prefix `cyber␣sec` |
| `q112` | prefix `cyber␣secu` |
| `q113` | prefix `cyber␣secur` |
| `q114` | prefix `cyber␣securi` |
| `q115` | prefix `cyber␣securit` |
| `q116` | prefix `cyber␣security` |
| `q117` | prefix `s` |
| `q118` | prefix `se` |
| `q119` | prefix `sec` |
| `q120` | prefix `secu` |
| `q121` | prefix `secur` |
| `q122` | prefix `securi` |
| `q123` | prefix `securit` |
| `q124` | prefix `security` |
| `q125` | prefix `security␣` |
| `q126` | prefix `security␣a` |
| `q127` | prefix `security␣au` |
| `q128` | prefix `security␣aut` |
| `q129` | prefix `security␣auto` |
| `q130` | prefix `security␣autom` |
| `q131` | prefix `security␣automa` |
| `q132` | prefix `security␣automat` |
| `q133` | prefix `security␣automati` |
| `q134` | prefix `security␣automatio` |
| `q135` | prefix `security␣automation` |
| `qf` | accepting state (end marker read) |

### Transition relation δ and output relation ω

`δ(state, input)` is the column *To*, and `ω(state, input)` is the column *Output*.

| From | Input | To | Output |
| :--- | :---: | :--- | :--- |
| `q0` | `m` | `q1` | `ε` |
| `q1` | `a` | `q2` | `ε` |
| `q2` | `c` | `q3` | `ε` |
| `q3` | `h` | `q4` | `ε` |
| `q4` | `i` | `q5` | `ε` |
| `q5` | `n` | `q6` | `ε` |
| `q6` | `e` | `q7` | `ε` |
| `q7` | `␣` | `q8` | `ε` |
| `q8` | `l` | `q9` | `ε` |
| `q9` | `e` | `q10` | `ε` |
| `q10` | `a` | `q11` | `ε` |
| `q11` | `r` | `q12` | `ε` |
| `q12` | `n` | `q13` | `ε` |
| `q13` | `i` | `q14` | `ε` |
| `q14` | `n` | `q15` | `ε` |
| `q15` | `g` | `q16` | `ε` |
| `q16` | `#` | `qf` | `MACHINE_LEARNING` |
| `q7` | `-` | `q17` | `ε` |
| `q17` | `l` | `q18` | `ε` |
| `q18` | `e` | `q19` | `ε` |
| `q19` | `a` | `q20` | `ε` |
| `q20` | `r` | `q21` | `ε` |
| `q21` | `n` | `q22` | `ε` |
| `q22` | `i` | `q23` | `ε` |
| `q23` | `n` | `q24` | `ε` |
| `q24` | `g` | `q25` | `ε` |
| `q25` | `#` | `qf` | `MACHINE_LEARNING` |
| `q16` | `␣` | `q26` | `ε` |
| `q26` | `m` | `q27` | `ε` |
| `q27` | `o` | `q28` | `ε` |
| `q28` | `d` | `q29` | `ε` |
| `q29` | `e` | `q30` | `ε` |
| `q30` | `l` | `q31` | `ε` |
| `q31` | `␣` | `q32` | `ε` |
| `q32` | `d` | `q33` | `ε` |
| `q33` | `e` | `q34` | `ε` |
| `q34` | `v` | `q35` | `ε` |
| `q35` | `e` | `q36` | `ε` |
| `q36` | `l` | `q37` | `ε` |
| `q37` | `o` | `q38` | `ε` |
| `q38` | `p` | `q39` | `ε` |
| `q39` | `m` | `q40` | `ε` |
| `q40` | `e` | `q41` | `ε` |
| `q41` | `n` | `q42` | `ε` |
| `q42` | `t` | `q43` | `ε` |
| `q43` | `#` | `qf` | `ML_MODEL_DEVELOPMENT` |
| `q25` | `␣` | `q44` | `ε` |
| `q44` | `m` | `q45` | `ε` |
| `q45` | `o` | `q46` | `ε` |
| `q46` | `d` | `q47` | `ε` |
| `q47` | `e` | `q48` | `ε` |
| `q48` | `l` | `q49` | `ε` |
| `q49` | `␣` | `q50` | `ε` |
| `q50` | `d` | `q51` | `ε` |
| `q51` | `e` | `q52` | `ε` |
| `q52` | `v` | `q53` | `ε` |
| `q53` | `e` | `q54` | `ε` |
| `q54` | `l` | `q55` | `ε` |
| `q55` | `o` | `q56` | `ε` |
| `q56` | `p` | `q57` | `ε` |
| `q57` | `m` | `q58` | `ε` |
| `q58` | `e` | `q59` | `ε` |
| `q59` | `n` | `q60` | `ε` |
| `q60` | `t` | `q61` | `ε` |
| `q61` | `#` | `qf` | `ML_MODEL_DEVELOPMENT` |
| `q0` | `r` | `q62` | `ε` |
| `q62` | `e` | `q63` | `ε` |
| `q63` | `s` | `q64` | `ε` |
| `q64` | `t` | `q65` | `ε` |
| `q65` | `␣` | `q66` | `ε` |
| `q66` | `a` | `q67` | `ε` |
| `q67` | `p` | `q68` | `ε` |
| `q68` | `i` | `q69` | `ε` |
| `q69` | `#` | `qf` | `REST_API` |
| `q69` | `s` | `q70` | `ε` |
| `q70` | `#` | `qf` | `REST_API` |
| `q0` | `v` | `q71` | `ε` |
| `q71` | `u` | `q72` | `ε` |
| `q72` | `l` | `q73` | `ε` |
| `q73` | `n` | `q74` | `ε` |
| `q74` | `e` | `q75` | `ε` |
| `q75` | `r` | `q76` | `ε` |
| `q76` | `a` | `q77` | `ε` |
| `q77` | `b` | `q78` | `ε` |
| `q78` | `i` | `q79` | `ε` |
| `q79` | `l` | `q80` | `ε` |
| `q80` | `i` | `q81` | `ε` |
| `q81` | `t` | `q82` | `ε` |
| `q82` | `y` | `q83` | `ε` |
| `q83` | `␣` | `q84` | `ε` |
| `q84` | `a` | `q85` | `ε` |
| `q85` | `s` | `q86` | `ε` |
| `q86` | `s` | `q87` | `ε` |
| `q87` | `e` | `q88` | `ε` |
| `q88` | `s` | `q89` | `ε` |
| `q89` | `s` | `q90` | `ε` |
| `q90` | `m` | `q91` | `ε` |
| `q91` | `e` | `q92` | `ε` |
| `q92` | `n` | `q93` | `ε` |
| `q93` | `t` | `q94` | `ε` |
| `q94` | `#` | `qf` | `VULNERABILITY_ASSESSMENT` |
| `q0` | `c` | `q95` | `ε` |
| `q95` | `y` | `q96` | `ε` |
| `q96` | `b` | `q97` | `ε` |
| `q97` | `e` | `q98` | `ε` |
| `q98` | `r` | `q99` | `ε` |
| `q99` | `s` | `q100` | `ε` |
| `q100` | `e` | `q101` | `ε` |
| `q101` | `c` | `q102` | `ε` |
| `q102` | `u` | `q103` | `ε` |
| `q103` | `r` | `q104` | `ε` |
| `q104` | `i` | `q105` | `ε` |
| `q105` | `t` | `q106` | `ε` |
| `q106` | `y` | `q107` | `ε` |
| `q107` | `#` | `qf` | `CYBERSECURITY` |
| `q99` | `␣` | `q108` | `ε` |
| `q108` | `s` | `q109` | `ε` |
| `q109` | `e` | `q110` | `ε` |
| `q110` | `c` | `q111` | `ε` |
| `q111` | `u` | `q112` | `ε` |
| `q112` | `r` | `q113` | `ε` |
| `q113` | `i` | `q114` | `ε` |
| `q114` | `t` | `q115` | `ε` |
| `q115` | `y` | `q116` | `ε` |
| `q116` | `#` | `qf` | `CYBERSECURITY` |
| `q0` | `s` | `q117` | `ε` |
| `q117` | `e` | `q118` | `ε` |
| `q118` | `c` | `q119` | `ε` |
| `q119` | `u` | `q120` | `ε` |
| `q120` | `r` | `q121` | `ε` |
| `q121` | `i` | `q122` | `ε` |
| `q122` | `t` | `q123` | `ε` |
| `q123` | `y` | `q124` | `ε` |
| `q124` | `␣` | `q125` | `ε` |
| `q125` | `a` | `q126` | `ε` |
| `q126` | `u` | `q127` | `ε` |
| `q127` | `t` | `q128` | `ε` |
| `q128` | `o` | `q129` | `ε` |
| `q129` | `m` | `q130` | `ε` |
| `q130` | `a` | `q131` | `ε` |
| `q131` | `t` | `q132` | `ε` |
| `q132` | `i` | `q133` | `ε` |
| `q133` | `o` | `q134` | `ε` |
| `q134` | `n` | `q135` | `ε` |
| `q135` | `#` | `qf` | `SECURITY_AUTOMATION` |

Any pair (state, input) that is not in the table has no transition, so the input is rejected.

## M_ACAD — Academic qualifications

```text
M_ACAD = (Q, Σ, Γ, δ, ω, q0, F)

Q  = { q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36, q37, q38, q39, q40, q41, q42, q43, q44, q45, q46, q47, q48, q49, q50, q51, q52, q53, q54, q55, q56, q57, q58, q59, q60, q61, q62, q63, q64, q65, q66, q67, q68, q69, q70, q71, q72, q73, q74, q75, q76, q77, q78, q79, q80, q81, q82, q83, q84, q85, q86, q87, q88, q89, q90, q91, q92, q93, q94, q95, q96, q97, q98, q99, q100, q101, q102, q103, q104, q105, qf }
     |Q| = 107
Σ  = { ␣, ', ., a, b, c, d, e, f, g, h, i, l, m, n, o, p, r, s, t, u, w, y, # }
     |Σ| = 24
Γ  = { BACHELOR, MASTER, PHD, COMPUTER_SCIENCE, SOFTWARE_ENGINEERING, SYSTEMS_ENGINEERING, DATA_SCIENCE }
     |Γ| = 7
q0 = q0
F  = { qf }
```

Number of transitions: 125.

Diagram: `diagrams/fst/m_acad.svg` (source: `diagrams/fst/m_acad.dot`).

### States

| State | Meaning |
| :--- | :--- |
| `q0` | prefix ε (nothing read) |
| `q1` | prefix `b` |
| `q2` | prefix `ba` |
| `q3` | prefix `bac` |
| `q4` | prefix `bach` |
| `q5` | prefix `bache` |
| `q6` | prefix `bachel` |
| `q7` | prefix `bachelo` |
| `q8` | prefix `bachelor` |
| `q9` | prefix `bachelor'` |
| `q10` | prefix `bachelor's` |
| `q11` | prefix `bs` |
| `q12` | prefix `bsc` |
| `q13` | prefix `bsc.` |
| `q14` | prefix `b.` |
| `q15` | prefix `b.s` |
| `q16` | prefix `b.sc` |
| `q17` | prefix `b.sc.` |
| `q18` | prefix `m` |
| `q19` | prefix `ma` |
| `q20` | prefix `mas` |
| `q21` | prefix `mast` |
| `q22` | prefix `maste` |
| `q23` | prefix `master` |
| `q24` | prefix `master'` |
| `q25` | prefix `master's` |
| `q26` | prefix `ms` |
| `q27` | prefix `msc` |
| `q28` | prefix `msc.` |
| `q29` | prefix `m.` |
| `q30` | prefix `m.s` |
| `q31` | prefix `m.sc` |
| `q32` | prefix `m.sc.` |
| `q33` | prefix `p` |
| `q34` | prefix `ph` |
| `q35` | prefix `phd` |
| `q36` | prefix `phd.` |
| `q37` | prefix `ph.` |
| `q38` | prefix `ph.d` |
| `q39` | prefix `ph.d.` |
| `q40` | prefix `c` |
| `q41` | prefix `co` |
| `q42` | prefix `com` |
| `q43` | prefix `comp` |
| `q44` | prefix `compu` |
| `q45` | prefix `comput` |
| `q46` | prefix `compute` |
| `q47` | prefix `computer` |
| `q48` | prefix `computer␣` |
| `q49` | prefix `computer␣s` |
| `q50` | prefix `computer␣sc` |
| `q51` | prefix `computer␣sci` |
| `q52` | prefix `computer␣scie` |
| `q53` | prefix `computer␣scien` |
| `q54` | prefix `computer␣scienc` |
| `q55` | prefix `computer␣science` |
| `q56` | prefix `s` |
| `q57` | prefix `so` |
| `q58` | prefix `sof` |
| `q59` | prefix `soft` |
| `q60` | prefix `softw` |
| `q61` | prefix `softwa` |
| `q62` | prefix `softwar` |
| `q63` | prefix `software` |
| `q64` | prefix `software␣` |
| `q65` | prefix `software␣e` |
| `q66` | prefix `software␣en` |
| `q67` | prefix `software␣eng` |
| `q68` | prefix `software␣engi` |
| `q69` | prefix `software␣engin` |
| `q70` | prefix `software␣engine` |
| `q71` | prefix `software␣enginee` |
| `q72` | prefix `software␣engineer` |
| `q73` | prefix `software␣engineeri` |
| `q74` | prefix `software␣engineerin` |
| `q75` | prefix `software␣engineering` |
| `q76` | prefix `sy` |
| `q77` | prefix `sys` |
| `q78` | prefix `syst` |
| `q79` | prefix `syste` |
| `q80` | prefix `system` |
| `q81` | prefix `systems` |
| `q82` | prefix `systems␣` |
| `q83` | prefix `systems␣e` |
| `q84` | prefix `systems␣en` |
| `q85` | prefix `systems␣eng` |
| `q86` | prefix `systems␣engi` |
| `q87` | prefix `systems␣engin` |
| `q88` | prefix `systems␣engine` |
| `q89` | prefix `systems␣enginee` |
| `q90` | prefix `systems␣engineer` |
| `q91` | prefix `systems␣engineeri` |
| `q92` | prefix `systems␣engineerin` |
| `q93` | prefix `systems␣engineering` |
| `q94` | prefix `d` |
| `q95` | prefix `da` |
| `q96` | prefix `dat` |
| `q97` | prefix `data` |
| `q98` | prefix `data␣` |
| `q99` | prefix `data␣s` |
| `q100` | prefix `data␣sc` |
| `q101` | prefix `data␣sci` |
| `q102` | prefix `data␣scie` |
| `q103` | prefix `data␣scien` |
| `q104` | prefix `data␣scienc` |
| `q105` | prefix `data␣science` |
| `qf` | accepting state (end marker read) |

### Transition relation δ and output relation ω

`δ(state, input)` is the column *To*, and `ω(state, input)` is the column *Output*.

| From | Input | To | Output |
| :--- | :---: | :--- | :--- |
| `q0` | `b` | `q1` | `ε` |
| `q1` | `a` | `q2` | `ε` |
| `q2` | `c` | `q3` | `ε` |
| `q3` | `h` | `q4` | `ε` |
| `q4` | `e` | `q5` | `ε` |
| `q5` | `l` | `q6` | `ε` |
| `q6` | `o` | `q7` | `ε` |
| `q7` | `r` | `q8` | `ε` |
| `q8` | `#` | `qf` | `BACHELOR` |
| `q8` | `'` | `q9` | `ε` |
| `q9` | `s` | `q10` | `ε` |
| `q10` | `#` | `qf` | `BACHELOR` |
| `q1` | `s` | `q11` | `ε` |
| `q11` | `c` | `q12` | `ε` |
| `q12` | `#` | `qf` | `BACHELOR` |
| `q12` | `.` | `q13` | `ε` |
| `q13` | `#` | `qf` | `BACHELOR` |
| `q1` | `.` | `q14` | `ε` |
| `q14` | `s` | `q15` | `ε` |
| `q15` | `c` | `q16` | `ε` |
| `q16` | `#` | `qf` | `BACHELOR` |
| `q16` | `.` | `q17` | `ε` |
| `q17` | `#` | `qf` | `BACHELOR` |
| `q0` | `m` | `q18` | `ε` |
| `q18` | `a` | `q19` | `ε` |
| `q19` | `s` | `q20` | `ε` |
| `q20` | `t` | `q21` | `ε` |
| `q21` | `e` | `q22` | `ε` |
| `q22` | `r` | `q23` | `ε` |
| `q23` | `#` | `qf` | `MASTER` |
| `q23` | `'` | `q24` | `ε` |
| `q24` | `s` | `q25` | `ε` |
| `q25` | `#` | `qf` | `MASTER` |
| `q18` | `s` | `q26` | `ε` |
| `q26` | `c` | `q27` | `ε` |
| `q27` | `#` | `qf` | `MASTER` |
| `q27` | `.` | `q28` | `ε` |
| `q28` | `#` | `qf` | `MASTER` |
| `q18` | `.` | `q29` | `ε` |
| `q29` | `s` | `q30` | `ε` |
| `q30` | `c` | `q31` | `ε` |
| `q31` | `#` | `qf` | `MASTER` |
| `q31` | `.` | `q32` | `ε` |
| `q32` | `#` | `qf` | `MASTER` |
| `q0` | `p` | `q33` | `ε` |
| `q33` | `h` | `q34` | `ε` |
| `q34` | `d` | `q35` | `ε` |
| `q35` | `#` | `qf` | `PHD` |
| `q35` | `.` | `q36` | `ε` |
| `q36` | `#` | `qf` | `PHD` |
| `q34` | `.` | `q37` | `ε` |
| `q37` | `d` | `q38` | `ε` |
| `q38` | `#` | `qf` | `PHD` |
| `q38` | `.` | `q39` | `ε` |
| `q39` | `#` | `qf` | `PHD` |
| `q0` | `c` | `q40` | `ε` |
| `q40` | `o` | `q41` | `ε` |
| `q41` | `m` | `q42` | `ε` |
| `q42` | `p` | `q43` | `ε` |
| `q43` | `u` | `q44` | `ε` |
| `q44` | `t` | `q45` | `ε` |
| `q45` | `e` | `q46` | `ε` |
| `q46` | `r` | `q47` | `ε` |
| `q47` | `␣` | `q48` | `ε` |
| `q48` | `s` | `q49` | `ε` |
| `q49` | `c` | `q50` | `ε` |
| `q50` | `i` | `q51` | `ε` |
| `q51` | `e` | `q52` | `ε` |
| `q52` | `n` | `q53` | `ε` |
| `q53` | `c` | `q54` | `ε` |
| `q54` | `e` | `q55` | `ε` |
| `q55` | `#` | `qf` | `COMPUTER_SCIENCE` |
| `q0` | `s` | `q56` | `ε` |
| `q56` | `o` | `q57` | `ε` |
| `q57` | `f` | `q58` | `ε` |
| `q58` | `t` | `q59` | `ε` |
| `q59` | `w` | `q60` | `ε` |
| `q60` | `a` | `q61` | `ε` |
| `q61` | `r` | `q62` | `ε` |
| `q62` | `e` | `q63` | `ε` |
| `q63` | `␣` | `q64` | `ε` |
| `q64` | `e` | `q65` | `ε` |
| `q65` | `n` | `q66` | `ε` |
| `q66` | `g` | `q67` | `ε` |
| `q67` | `i` | `q68` | `ε` |
| `q68` | `n` | `q69` | `ε` |
| `q69` | `e` | `q70` | `ε` |
| `q70` | `e` | `q71` | `ε` |
| `q71` | `r` | `q72` | `ε` |
| `q72` | `i` | `q73` | `ε` |
| `q73` | `n` | `q74` | `ε` |
| `q74` | `g` | `q75` | `ε` |
| `q75` | `#` | `qf` | `SOFTWARE_ENGINEERING` |
| `q56` | `y` | `q76` | `ε` |
| `q76` | `s` | `q77` | `ε` |
| `q77` | `t` | `q78` | `ε` |
| `q78` | `e` | `q79` | `ε` |
| `q79` | `m` | `q80` | `ε` |
| `q80` | `s` | `q81` | `ε` |
| `q81` | `␣` | `q82` | `ε` |
| `q82` | `e` | `q83` | `ε` |
| `q83` | `n` | `q84` | `ε` |
| `q84` | `g` | `q85` | `ε` |
| `q85` | `i` | `q86` | `ε` |
| `q86` | `n` | `q87` | `ε` |
| `q87` | `e` | `q88` | `ε` |
| `q88` | `e` | `q89` | `ε` |
| `q89` | `r` | `q90` | `ε` |
| `q90` | `i` | `q91` | `ε` |
| `q91` | `n` | `q92` | `ε` |
| `q92` | `g` | `q93` | `ε` |
| `q93` | `#` | `qf` | `SYSTEMS_ENGINEERING` |
| `q0` | `d` | `q94` | `ε` |
| `q94` | `a` | `q95` | `ε` |
| `q95` | `t` | `q96` | `ε` |
| `q96` | `a` | `q97` | `ε` |
| `q97` | `␣` | `q98` | `ε` |
| `q98` | `s` | `q99` | `ε` |
| `q99` | `c` | `q100` | `ε` |
| `q100` | `i` | `q101` | `ε` |
| `q101` | `e` | `q102` | `ε` |
| `q102` | `n` | `q103` | `ε` |
| `q103` | `c` | `q104` | `ε` |
| `q104` | `e` | `q105` | `ε` |
| `q105` | `#` | `qf` | `DATA_SCIENCE` |

Any pair (state, input) that is not in the table has no transition, so the input is rejected.

## M_EXP — Professional experience

```text
M_EXP = (Q, Σ, Γ, δ, ω, q0, F)

Q  = { q0, q1, q2, qf }
     |Q| = 4
Σ  = { ␣, +, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, # }
     |Σ| = 39
Γ  = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }
     |Γ| = 10
q0 = q0
F  = { qf }
```

Number of transitions: 87.

Diagram: `diagrams/fst/m_exp.svg` (source: `diagrams/fst/m_exp.dot`).

### States

| State | Meaning |
| :--- | :--- |
| `q0` | nothing has been read |
| `q1` | reading the number of years (the digits are copied) |
| `q2` | reading the rest of the expression (everything is erased) |
| `qf` | accepting state (end marker read) |

### Transition relation δ and output relation ω

`δ(state, input)` is the column *To*, and `ω(state, input)` is the column *Output*.

| From | Input | To | Output |
| :--- | :---: | :--- | :--- |
| `q0` | `0` | `q1` | `0` |
| `q1` | `0` | `q1` | `0` |
| `q2` | `0` | `q2` | `ε` |
| `q0` | `1` | `q1` | `1` |
| `q1` | `1` | `q1` | `1` |
| `q2` | `1` | `q2` | `ε` |
| `q0` | `2` | `q1` | `2` |
| `q1` | `2` | `q1` | `2` |
| `q2` | `2` | `q2` | `ε` |
| `q0` | `3` | `q1` | `3` |
| `q1` | `3` | `q1` | `3` |
| `q2` | `3` | `q2` | `ε` |
| `q0` | `4` | `q1` | `4` |
| `q1` | `4` | `q1` | `4` |
| `q2` | `4` | `q2` | `ε` |
| `q0` | `5` | `q1` | `5` |
| `q1` | `5` | `q1` | `5` |
| `q2` | `5` | `q2` | `ε` |
| `q0` | `6` | `q1` | `6` |
| `q1` | `6` | `q1` | `6` |
| `q2` | `6` | `q2` | `ε` |
| `q0` | `7` | `q1` | `7` |
| `q1` | `7` | `q1` | `7` |
| `q2` | `7` | `q2` | `ε` |
| `q0` | `8` | `q1` | `8` |
| `q1` | `8` | `q1` | `8` |
| `q2` | `8` | `q2` | `ε` |
| `q0` | `9` | `q1` | `9` |
| `q1` | `9` | `q1` | `9` |
| `q2` | `9` | `q2` | `ε` |
| `q1` | `a` | `q2` | `ε` |
| `q2` | `a` | `q2` | `ε` |
| `q1` | `b` | `q2` | `ε` |
| `q2` | `b` | `q2` | `ε` |
| `q1` | `c` | `q2` | `ε` |
| `q2` | `c` | `q2` | `ε` |
| `q1` | `d` | `q2` | `ε` |
| `q2` | `d` | `q2` | `ε` |
| `q1` | `e` | `q2` | `ε` |
| `q2` | `e` | `q2` | `ε` |
| `q1` | `f` | `q2` | `ε` |
| `q2` | `f` | `q2` | `ε` |
| `q1` | `g` | `q2` | `ε` |
| `q2` | `g` | `q2` | `ε` |
| `q1` | `h` | `q2` | `ε` |
| `q2` | `h` | `q2` | `ε` |
| `q1` | `i` | `q2` | `ε` |
| `q2` | `i` | `q2` | `ε` |
| `q1` | `j` | `q2` | `ε` |
| `q2` | `j` | `q2` | `ε` |
| `q1` | `k` | `q2` | `ε` |
| `q2` | `k` | `q2` | `ε` |
| `q1` | `l` | `q2` | `ε` |
| `q2` | `l` | `q2` | `ε` |
| `q1` | `m` | `q2` | `ε` |
| `q2` | `m` | `q2` | `ε` |
| `q1` | `n` | `q2` | `ε` |
| `q2` | `n` | `q2` | `ε` |
| `q1` | `o` | `q2` | `ε` |
| `q2` | `o` | `q2` | `ε` |
| `q1` | `p` | `q2` | `ε` |
| `q2` | `p` | `q2` | `ε` |
| `q1` | `q` | `q2` | `ε` |
| `q2` | `q` | `q2` | `ε` |
| `q1` | `r` | `q2` | `ε` |
| `q2` | `r` | `q2` | `ε` |
| `q1` | `s` | `q2` | `ε` |
| `q2` | `s` | `q2` | `ε` |
| `q1` | `t` | `q2` | `ε` |
| `q2` | `t` | `q2` | `ε` |
| `q1` | `u` | `q2` | `ε` |
| `q2` | `u` | `q2` | `ε` |
| `q1` | `v` | `q2` | `ε` |
| `q2` | `v` | `q2` | `ε` |
| `q1` | `w` | `q2` | `ε` |
| `q2` | `w` | `q2` | `ε` |
| `q1` | `x` | `q2` | `ε` |
| `q2` | `x` | `q2` | `ε` |
| `q1` | `y` | `q2` | `ε` |
| `q2` | `y` | `q2` | `ε` |
| `q1` | `z` | `q2` | `ε` |
| `q2` | `z` | `q2` | `ε` |
| `q1` | `+` | `q2` | `ε` |
| `q2` | `+` | `q2` | `ε` |
| `q1` | `␣` | `q2` | `ε` |
| `q2` | `␣` | `q2` | `ε` |
| `q2` | `#` | `qf` | `ε` |

Any pair (state, input) that is not in the table has no transition, so the input is rejected.
