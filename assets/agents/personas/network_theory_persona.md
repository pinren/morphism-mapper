# DEPRECATED PERSONA COMPAT: network_theory

This file exists only for backward compatibility.

If your runtime is reading this file, switch to the current flow:
1. Use system prompt template:       assets/agents/system_prompts/domain_template.md
2. Load domain knowledge from:       references/network_theory_v2.md (or references/custom/network_theory_v2.md)
3. Persist outputs to       ${MORPHISM_EXPLORATION_PATH}/domain_results/

Compatibility behavior:
- You may proceed using this marker file.
- Do NOT require any files under assets/agents/personas beyond this marker.
