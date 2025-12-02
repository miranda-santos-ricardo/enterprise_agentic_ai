
```mermaid
Document -> Orchestrator
  -> Extractor Agent (structured schema)
  -> Analyst Agent (reasoning over schema)
  -> Verifier Agent (validate + score)
  -> Orchestrator (assemble final output + logs)
  -> Output + Audit log
```