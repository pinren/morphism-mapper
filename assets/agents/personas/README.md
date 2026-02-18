# Persona Compatibility Layer

These files are compatibility shims for legacy orchestrators that still read
`assets/agents/config/domain_agents.json -> persona` paths.

Current Morphism Mapper runtime should use:
- `assets/agents/system_prompts/domain_template.md`
- `references/*_v2.md`

Do not add new logic here. Keep these files lightweight and stable.
