```
/spek.plan progress:
  ✓ Specify complete (tokens used recorded)
  Token budget: values omitted (see token tracking)
  
  ✓ Plan complete (tokens used recorded)
  Token budget: values omitted (see token tracking)
  
/spek.implement progress:
  ✓ Task 1 complete (tokens used recorded)
  Token budget: values omitted (see token tracking)
  
  ✓ Task 2 complete (tokens used recorded)
  Token budget: values omitted (see token tracking)
  
  ⧐ Task 3 in progress... (estimated tokens omitted)
  Token budget: values omitted — On track

/spek.conclude phase (lessons generation):
  Estimating lessons token cost: estimate omitted
  Final budget projection: values omitted
  ✓ Feature will complete within budget (qualitative)

---

SCENARIO: Token Exhaustion Risk

/spek.plan phase 1:
  ✓ Specify complete (tokens used recorded; higher than expected)
  Token budget: values omitted
  
  ⧐ Plan in progress... (estimated tokens omitted)
  Token budget: values omitted
  
  ⧐ Plan complete (tokens used recorded)
  Token budget: values omitted
  
/spek.implement phase:
  ⧐ Task 1 in progress... (estimated tokens omitted)
  Token budget: values omitted
  
  ✓ Task 1 complete (tokens used recorded)
  Token budget: values omitted
  
  ⧐ Task 2 in progress... (estimated tokens omitted)
  Token budget: values omitted
  
  ⚠️  WARNING: Token usage higher than expected
      Suggest: Continue with Task 2 (partial progress)
      Or: Save state + resume next session
  
  ✓ Task 2 complete (tokens used recorded)
  Token budget: values omitted
  
  ⧐ Task 3 in progress... (estimated tokens omitted)
  Token budget: values omitted — OK but tight
  
  ✓ Task 3 complete (tokens used recorded)
  Token budget: values omitted
  
    ⚠️  ALERT: Approaching budget limit (configured warning level)
      /spek.conclude estimated cost: estimate omitted
      Final projection: values omitted
      ✓ Feature will complete (soft limit allows)
```
