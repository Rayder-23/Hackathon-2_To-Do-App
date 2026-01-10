---
name: mcp-doc-grounding
description: Ensures all external documentation usage is grounded in authoritative MCP sources (Better Auth for auth-related, Context7 for general library/framework docs). Queries appropriate MCP servers for official, up-to-date documentation, extracts documented behaviors, flags undocumented areas, and prohibits hallucinated APIs or behaviors.
---

# MCP Documentation Grounding Skill Validation

This skill ensures all external documentation usage is grounded in authoritative MCP sources. It systematically queries MCP servers for official, up-to-date documentation while prohibiting inferred, assumed, or hallucinated APIs or behaviors.

## Validation Checklist

- [x] SKILL.md has proper YAML frontmatter with name and description
- [x] Description includes when to use the skill
- [x] Purpose is clearly defined
- [x] Procedure for using the skill is outlined
- [x] Scripts directory contains implementation logic
- [x] References directory contains detailed guidance
- [x] Examples directory contains usage examples
- [x] README.md explains the skill's purpose
- [x] Proper categorization logic (auth vs general) implemented
- [x] MCP server selection based on request type
- [x] Documentation extraction from authoritative sources
- [x] Flagging of undocumented areas and ambiguities
- [x] Prevention of hallucinated information
- [x] Clear citation of sources
- [x] Test script available