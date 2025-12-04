
```mermaid
graph TD;
    Document --> Orchestrator;

    Orchestrator -->|extract| ExtractorAgent;
    ExtractorAgent -->|structured data| Orchestrator;

    Orchestrator -->|analyze| AnalystAgent;
    AnalystAgent -->|analysis result| Orchestrator;

    Orchestrator -->|verify| VerifierAgent;
    VerifierAgent -->|verification + confidence| Orchestrator;

    Orchestrator -->|log decision| GovernanceLog;
    GovernanceLog --> AuditTrail;

    Orchestrator -->|approved| Output;
    Orchestrator -->|rejected| FailureReport;
```

### Failure and Control Model
The orchestrator acts as the single control point of the system.  
If verification thresholds are not met, execution is halted and a failure report is generated instead of an output.

This design prevents uncontrolled AI decisions and ensures that every result can be traced, reviewed, and justified.
