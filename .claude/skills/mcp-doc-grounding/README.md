# MCP Documentation Grounding Skill

This skill ensures all external documentation usage is grounded in authoritative MCP sources (Better Auth for auth-related, Context7 for general library/framework docs). It queries appropriate MCP servers for official, up-to-date documentation, extracts documented behaviors, flags undocumented areas, and prohibits hallucinated APIs or behaviors.

## Overview

The MCP Documentation Grounding skill addresses the critical need to verify that all external library and framework documentation comes from authoritative sources rather than internal knowledge or assumptions. It systematically queries MCP servers to access the most current and accurate documentation.

## Components

- **SKILL.md**: Main skill definition with usage instructions
- **scripts/mcp_doc_grounding.py**: Core implementation logic
- **references/mcp_usage_guide.md**: Detailed MCP tool usage information
- **examples/usage_examples.md**: Practical usage examples

## When to Use

Use this skill when:
- You need documentation for a library, framework, or API
- Implementing features that require external library usage
- There's uncertainty about API behavior, configuration, or constraints
- You want to ensure documentation is up-to-date and authoritative
- Working with authentication systems or general frameworks

## Key Features

1. Automatic categorization of requests (auth vs general)
2. Selection of appropriate MCP server based on request type
3. Extraction of only documented behaviors
4. Clear flagging of undocumented areas and ambiguities
5. Prevention of hallucinated information
6. Proper citation of authoritative sources