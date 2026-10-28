# Personal Ops Agent: self-assessment rubric

Score each row 0 (missing), 1 (partial) or 2 (demonstrated), for 10 points. Write one command or observed artifact beside every score. The README acceptance criteria define the project-specific behavior.

| Area | Evidence for 2 points |
|---|---|
| Working path | Your starter implementation executes the real pipeline and passes its acceptance test. |
| Evidence and correctness | Run every eval.jsonl case; inspect answers or results before scoring independently expected facts. Report every failed case. |
| Permissions and limits | Demonstrate the relevant denial/exhaustion test and explain which host check enforces it. |
| Explanation | Explain the architecture diagram, one failure and its fix, and why this abstraction is appropriate. |
| Reproducibility | Another learner can run your documented commands with no keys in offline mode; live evidence is labelled separately. |

**Ready to extend:** at least 8/10, no failed ownership/write-permission checks, and no concealed factual failures. A reference solution is a teaching baseline; its presence does not waive the quality bar. The corrected Support Copilot passes its offline policy cases; this does not replace live-model and human validation.

**Stretch review:** complete one extension, add a new independent test case, and document whether the measured result improved, stayed the same or regressed.
