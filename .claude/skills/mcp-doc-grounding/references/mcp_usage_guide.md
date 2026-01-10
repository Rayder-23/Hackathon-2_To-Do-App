# MCP Documentation Grounding - Reference Guide

This reference guide provides detailed information on how to properly use MCP tools for documentation grounding.

## Better Auth MCP Tools

The Better Auth MCP provides specialized tools for authentication-related documentation:

### Search Tool
- Purpose: Perform semantic search across Better Auth's knowledge base
- Usage: For finding specific authentication information, API details, or configuration options
- Parameters:
  - query: Natural language search query
  - mode: Search depth (fast/balanced/deep)
  - limit: Number of results (1-100)

### Chat Tool
- Purpose: Engage in conversational interactions about authentication concepts
- Usage: For complex authentication scenarios that require contextual understanding
- Parameters:
  - messages: Array of message objects for conversation history

### List Files Tool
- Purpose: Browse available files in Better Auth's knowledge repository
- Usage: To understand what documentation is available before searching

### Get File Tool
- Purpose: Retrieve specific file contents by ID
- Usage: For accessing detailed documentation files identified through list_files

## Context7 MCP Tools

The Context7 MCP provides tools for general framework and library documentation:

### Resolve Library ID Tool
- Purpose: Resolves a package/product name to a Context7-compatible library ID
- Usage: Call this BEFORE using query-docs to get the correct library identifier
- Parameters:
  - libraryName: Name of the library to search for
  - query: User's original question (used for ranking results)

### Query Docs Tool
- Purpose: Retrieves and queries up-to-date documentation from Context7
- Usage: After resolving library ID, to get specific documentation
- Parameters:
  - libraryId: Exact Context7-compatible library ID
  - query: Specific question about the library

## Best Practices for Documentation Grounding

### 1. Always Verify Authority
- Prioritize MCP tools over internal knowledge
- Confirm documentation comes from official sources
- Cross-reference when multiple sources are available

### 2. Handle Missing Documentation Gracefully
- If documentation is unavailable, clearly state this
- Do not extrapolate or assume undocumented behaviors
- Recommend alternative approaches when documentation is insufficient

### 3. Flag Uncertainties
- Clearly mark areas where documentation is ambiguous
- Note version differences that may affect implementation
- Identify deprecated features or practices

### 4. Follow the Proper Sequence
- For authentication: Use Better Auth MCP tools directly
- For general libraries: First resolve library ID, then query docs
- Always cite the source of information

## Common Patterns

### Authentication Documentation Query Pattern:
```
1. Identify as authentication-related
2. Use mcp__better-auth__search for initial discovery
3. Use mcp__better-auth__chat for complex scenarios
4. Extract only documented behaviors
5. Flag any uncertainties
```

### General Library Documentation Query Pattern:
```
1. Identify as general library/framework
2. Use mcp__context7__resolve-library-id to get proper ID
3. Use mcp__context7__query-docs with resolved ID
4. Extract only documented behaviors
5. Flag any uncertainties
```

## Error Handling

### MCP Server Unavailable
- Report the unavailability immediately
- Suggest alternatives if possible
- Do not proceed with assumptions

### No Relevant Documentation Found
- Clearly state that no relevant documentation was found
- Do not invent or assume API behaviors
- Suggest contacting maintainers or seeking alternative sources

### Ambiguous Documentation
- Highlight specific areas of ambiguity
- Explain the impact on implementation
- Recommend verification steps

## Quality Checks

Before considering documentation complete, verify:
- [ ] Information comes from authoritative MCP sources
- [ ] No undocumented APIs or behaviors are suggested
- [ ] Uncertainties are clearly flagged
- [ ] Sources are properly cited
- [ ] Information is current and up-to-date