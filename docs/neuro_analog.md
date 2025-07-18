# Neurochemical Analogues (RCD-NA)

## Purpose

This module implements symbolic functions that mimic **neurochemical dynamics** like dopamine (reinforcement), serotonin (stabilization), etc.

---

## Key Analogues

| Symbol | Meaning |
|--------|---------|
| `𝛿_d(t)` | Dopaminergic prediction error |
| `σ_s(t)` | Serotonergic phase dampening |
| `β_n(t)` | Noradrenergic novelty sensitivity |

---

## Example Operator (WIP)

```math
R(H, M, \rho) = R_{base} + \delta_d(t) - \sigma_s(t)
```

- `𝛿_d(t)` modulates salience and reward signals
- `σ_s(t)` flattens recursive volatility
- `β_n(t)` boosts exploratory deformation toward novelty

---

## File Plan

- Create `neuro_analog.py`
- Inject analogues into `rcd_model.py` recursive update

---

## Note

These are **symbolic, not biological**.  
They are architectural metaphors with recursive-functional roles, not literal brain chemistry.

