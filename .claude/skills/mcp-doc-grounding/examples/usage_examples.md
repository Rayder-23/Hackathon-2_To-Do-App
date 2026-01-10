# MCP Documentation Grounding - Usage Examples

This file provides practical examples of how to use the MCP Documentation Grounding skill.

## Example 1: Authentication Query

**User Query**: "How do I implement JWT authentication with Better Auth?"

**Process**:
1. The skill identifies this as an authentication-related query
2. It selects the Better Auth MCP server
3. It queries the Better Auth documentation for JWT implementation
4. It extracts documented JWT configuration options
5. It flags any unclear areas
6. It provides a confirmed implementation approach

**Expected Output**:
- Documentation Source: Better Auth MCP
- Confirmed Documentation: JWT configuration patterns, token handling, session management
- Undocumented Areas: Any gaps in JWT implementation details
- Recommendation: Proceed with documented approach

## Example 2: General Framework Query

**User Query**: "How do I use React hooks for state management?"

**Process**:
1. The skill identifies this as a general framework documentation query
2. It selects the Context7 MCP server
3. It resolves "React" to the appropriate library ID
4. It queries React documentation for hooks
5. It extracts documented hook patterns
6. It flags any unclear areas
7. It provides confirmed usage patterns

**Expected Output**:
- Documentation Source: Context7 MCP
- Confirmed Documentation: useState, useEffect, useContext patterns
- Undocumented Areas: Any deprecated or experimental hooks
- Recommendation: Use documented hook patterns

## Example 3: Library Usage Query

**User Query**: "What are the configuration options for Express.js middleware?"

**Process**:
1. The skill identifies this as a general library documentation query
2. It selects the Context7 MCP server
3. It resolves "Express.js" to the appropriate library ID
4. It queries Express documentation for middleware configuration
5. It extracts documented configuration options
6. It flags any unclear areas
7. It provides confirmed usage patterns

**Expected Output**:
- Documentation Source: Context7 MCP
- Confirmed Documentation: Middleware configuration options, app.use() patterns
- Undocumented Areas: Any experimental features
- Recommendation: Use documented middleware patterns

## Example 4: Complex Integration Query

**User Query**: "How do I integrate Next.js with Supabase authentication?"

**Process**:
1. The skill identifies this as involving authentication (Supabase auth)
2. It could use either server depending on focus:
   - For auth aspects: Better Auth MCP
   - For general integration: Context7 MCP
3. It queries appropriate documentation
4. It extracts documented integration patterns
5. It flags any unclear areas
6. It provides confirmed implementation approach

**Expected Output**:
- Documentation Source: Mix of Better Auth MCP (auth) and Context7 MCP (framework)
- Confirmed Documentation: Integration patterns, session handling
- Undocumented Areas: Any complex edge cases
- Recommendation: Follow documented integration patterns

## When to Stop and Report Gaps

The skill will stop and report if:

1. MCP servers are unavailable
2. No relevant documentation is found
3. Critical implementation details are missing
4. Documentation conflicts with known best practices

In these cases, it will clearly report the gap instead of making assumptions.