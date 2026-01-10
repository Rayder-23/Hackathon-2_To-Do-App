---
name: mcp-doc-grounding
description: Ensures all external documentation usage is grounded in authoritative MCP sources (Better Auth for auth-related, Context7 for general library/framework docs). Queries appropriate MCP servers for official, up-to-date documentation, extracts documented behaviors, flags undocumented areas, and prohibits hallucinated APIs or behaviors.
---

# MCP Documentation Grounding Skill

This skill ensures all external documentation usage is grounded in authoritative MCP sources. It systematically queries MCP servers for official, up-to-date documentation while prohibiting inferred, assumed, or hallucinated APIs or behaviors.

## Purpose

When users need documentation for libraries, frameworks, or APIs, this skill ensures that information comes from authoritative sources rather than internal knowledge or assumptions. It uses MCP servers to access the most current and accurate documentation.

## When to Use This Skill

- When you need documentation for a library, framework, or API
- When implementing features that require external library usage
- When there's uncertainty about API behavior, configuration, or constraints
- When you want to ensure documentation is up-to-date and authoritative
- When working with authentication systems (Better Auth) or general frameworks (Context7)

## Procedure

### 1. Identify Documentation Need

Determine the specific documentation need or question, such as:
- Library usage patterns
- Configuration options
- API behavior and parameters
- Framework constraints or requirements

### 2. Categorize the Request

Determine whether the request is:
- **Authentication-related**: Any query about authentication, authorization, user sessions, JWT, OAuth, etc.
- **General framework/library documentation**: Any query about general libraries, frameworks, or APIs

### 3. Select the Appropriate MCP Server

Based on the categorization:
- **Better Auth MCP**: For authentication-related documentation
- **Context7 MCP**: For all other official documentation (general frameworks, libraries, APIs)

### 4. Query the Selected MCP Server

Execute the appropriate query based on the categorization:

#### For Authentication-Related (Better Auth MCP):
- Use the Better Auth search tool for specific authentication queries
- Use the Better Auth chat tool for complex authentication scenarios
- Use the Better Auth list_files/get_file tools to access specific documentation

#### For General Framework/Library (Context7 MCP):
- First resolve the library name to a Context7-compatible library ID using resolve-library-id
- Then query the documentation using query-docs with the resolved library ID

### 5. Extract and Summarize Documented Behaviors

- Extract only confirmed, documented behaviors from the MCP responses
- Identify APIs, parameters, and constraints that are explicitly documented
- Note any version-specific information or deprecated features

### 6. Flag Undocumented Areas and Ambiguities

Explicitly flag:
- Areas where documentation is incomplete or missing
- Ambiguities in the documentation
- Any gaps between the requirement and available documentation

### 7. Prohibit Hallucinated Information

- Do not infer, assume, or hallucinate APIs or behaviors
- If required documentation is unavailable or unclear, report the gap instead of guessing
- Always cite the authoritative source (MCP server) used

## Output Format

The skill output should include:

### Documentation Source
- Clearly cite which MCP server was used (Better Auth or Context7)

### Confirmed Documentation
- List of APIs, behaviors, and constraints that are confirmed in documentation

### Open Questions
- Areas where documentation is unclear, incomplete, or missing

### Recommendations
- Next steps for addressing any documentation gaps
- Whether to proceed with implementation based on available documentation

## Examples

### Example 1: Authentication Query
```
User: "How do I implement JWT authentication with Better Auth?"

Process:
1. Identify as authentication-related
2. Select Better Auth MCP server
3. Query Better Auth documentation for JWT implementation
4. Extract documented JWT configuration options
5. Flag any unclear areas
6. Provide confirmed implementation approach
```

### Example 2: Framework Query
```
User: "How do I use React hooks for state management?"

Process:
1. Identify as general framework documentation
2. Select Context7 MCP server
3. Resolve "React" to appropriate library ID
4. Query React documentation for hooks
5. Extract documented hook patterns
6. Flag any unclear areas
7. Provide confirmed usage patterns
```

## Error Handling

- If MCP server is unavailable, report the unavailability
- If no relevant documentation is found, clearly state this
- If multiple interpretations exist, present options and recommend verification
- If documentation conflicts with known implementation, flag the discrepancy

## Validation Checklist

Before completing a documentation request, verify:
- [ ] Appropriate MCP server was selected based on request type
- [ ] Documentation is from authoritative source (not assumed)
- [ ] Undocumented areas are clearly flagged
- [ ] No hallucinated APIs or behaviors were provided
- [ ] Output is suitable for implementation or specification writing
- [ ] Sources are clearly cited