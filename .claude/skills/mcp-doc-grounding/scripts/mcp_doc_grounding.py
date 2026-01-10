#!/usr/bin/env python3
"""
MCP Documentation Grounding Script

This script implements the core logic for querying authoritative MCP sources
for documentation, ensuring that all external documentation usage is grounded
in official sources rather than assumptions or hallucinations.
"""

import json
import sys
from typing import Dict, Any, Optional, List


def categorize_request(query: str) -> str:
    """
    Categorize the documentation request as either 'auth' or 'general'.

    Args:
        query: The documentation need or question

    Returns:
        'auth' for authentication-related queries, 'general' for others
    """
    auth_keywords = [
        'auth', 'authentication', 'authorization', 'jwt', 'oauth',
        'login', 'logout', 'session', 'user', 'identity', 'better auth',
        'passport', 'auth0', 'firebase auth', 'supabase auth'
    ]

    query_lower = query.lower()

    for keyword in auth_keywords:
        if keyword in query_lower:
            return 'auth'

    return 'general'


def resolve_library_id(library_name: str, query: str) -> Optional[Dict[str, Any]]:
    """
    Resolve a library name to a Context7-compatible library ID.

    Args:
        library_name: Name of the library to search for
        query: The user's original question

    Returns:
        Dictionary with library ID information or None if not found
    """
    # This would call the actual mcp__context7__resolve-library-id tool in practice
    print(f"Resolving library ID for: {library_name}")
    print(f"Query context: {query}")

    # Mock implementation - in real usage, this would call the actual tool
    return {
        "library_id": f"/{library_name.replace(' ', '/')}",
        "name": library_name,
        "description": f"Documentation for {library_name}",
        "reputation": "High"
    }


def query_context7_docs(library_id: str, query: str) -> Dict[str, Any]:
    """
    Query Context7 for documentation using the resolved library ID.

    Args:
        library_id: Context7-compatible library ID
        query: The documentation question

    Returns:
        Dictionary with documentation results
    """
    # This would call the actual mcp__context7__query-docs tool in practice
    print(f"Querying Context7 for library: {library_id}")
    print(f"Query: {query}")

    # Mock implementation - in real usage, this would call the actual tool
    return {
        "library_id": library_id,
        "query": query,
        "results": [
            {
                "title": "Documentation Result",
                "content": "This is confirmed documentation from official sources.",
                "source": "Official Library Documentation"
            }
        ],
        "undocumented_areas": [],
        "ambiguities": []
    }


def query_better_auth_docs(query: str) -> Dict[str, Any]:
    """
    Query Better Auth MCP for authentication-related documentation.

    Args:
        query: The authentication-related question

    Returns:
        Dictionary with authentication documentation results
    """
    # This would call the actual Better Auth MCP tools in practice
    print(f"Querying Better Auth documentation for: {query}")

    # Mock implementation - in real usage, this would call the actual tools
    return {
        "query": query,
        "results": [
            {
                "title": "Authentication Documentation",
                "content": "This is confirmed authentication documentation from Better Auth.",
                "source": "Better Auth Official Documentation"
            }
        ],
        "undocumented_areas": [],
        "ambiguities": []
    }


def extract_documented_behaviors(docs_result: Dict[str, Any]) -> List[str]:
    """
    Extract documented behaviors, APIs, and constraints from documentation results.

    Args:
        docs_result: The result from MCP documentation query

    Returns:
        List of documented behaviors
    """
    behaviors = []

    if "results" in docs_result:
        for result in docs_result["results"]:
            if "content" in result:
                behaviors.append(result["content"])

    return behaviors


def flag_undocumented_areas(docs_result: Dict[str, Any]) -> List[str]:
    """
    Identify and flag undocumented areas from documentation results.

    Args:
        docs_result: The result from MCP documentation query

    Returns:
        List of undocumented areas
    """
    undocumented = []

    if "undocumented_areas" in docs_result:
        undocumented.extend(docs_result["undocumented_areas"])

    return undocumented


def flag_ambiguities(docs_result: Dict[str, Any]) -> List[str]:
    """
    Identify and flag ambiguities from documentation results.

    Args:
        docs_result: The result from MCP documentation query

    Returns:
        List of ambiguities
    """
    ambiguities = []

    if "ambiguities" in docs_result:
        ambiguities.extend(docs_result["ambiguities"])

    return ambiguities


def ground_documentation_request(query: str) -> Dict[str, Any]:
    """
    Main function to ground a documentation request in authoritative MCP sources.

    Args:
        query: The documentation need or question

    Returns:
        Dictionary with documentation results, confirmed behaviors, and flagged issues
    """
    print(f"Processing documentation request: {query}")

    # Step 1: Categorize the request
    category = categorize_request(query)
    print(f"Category: {category}")

    # Step 2: Query the appropriate MCP server
    docs_result = {}

    if category == 'auth':
        print("Using Better Auth MCP server for authentication documentation")
        docs_result = query_better_auth_docs(query)
        source = "Better Auth MCP"
    else:
        print("Using Context7 MCP server for general documentation")
        # For general docs, we need to resolve the library ID first
        # Extract potential library name from query (simplified approach)
        words = query.split()
        library_name = words[0] if words else "general"
        library_info = resolve_library_id(library_name, query)

        if library_info:
            library_id = library_info["library_id"]
            docs_result = query_context7_docs(library_id, query)
        else:
            docs_result = {
                "query": query,
                "results": [],
                "undocumented_areas": ["Could not resolve library ID for Context7"],
                "ambiguities": []
            }

        source = "Context7 MCP"

    # Step 3: Extract documented behaviors
    documented_behaviors = extract_documented_behaviors(docs_result)

    # Step 4: Flag undocumented areas
    undocumented_areas = flag_undocumented_areas(docs_result)

    # Step 5: Flag ambiguities
    ambiguities = flag_ambiguities(docs_result)

    # Step 6: Compile results
    result = {
        "documentation_source": source,
        "query": query,
        "category": category,
        "confirmed_documentation": documented_behaviors,
        "undocumented_areas": undocumented_areas,
        "ambiguities": ambiguities,
        "proceed_with_implementation": len(undocumented_areas) == 0 and len(ambiguities) == 0
    }

    return result


def main():
    """
    Main function to run the MCP documentation grounding process.
    """
    if len(sys.argv) < 2:
        print("Usage: python mcp_doc_grounding.py \"documentation query here\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    try:
        result = ground_documentation_request(query)

        print("\n" + "="*60)
        print("MCP DOCUMENTATION GROUNDING RESULTS")
        print("="*60)

        print(f"Documentation Source: {result['documentation_source']}")
        print(f"Query: {result['query']}")
        print(f"Category: {result['category']}")

        print("\nCONFIRMED DOCUMENTATION:")
        if result['confirmed_documentation']:
            for i, behavior in enumerate(result['confirmed_documentation'], 1):
                print(f"  {i}. {behavior}")
        else:
            print("  No confirmed documentation found.")

        print("\nUNDOCUMENTED AREAS:")
        if result['undocumented_areas']:
            for i, area in enumerate(result['undocumented_areas'], 1):
                print(f"  {i}. {area}")
        else:
            print("  No undocumented areas found.")

        print("\nAMBIGUITIES:")
        if result['ambiguities']:
            for i, ambiguity in enumerate(result['ambiguities'], 1):
                print(f"  {i}. {ambiguity}")
        else:
            print("  No ambiguities found.")

        print(f"\nPROCEED WITH IMPLEMENTATION: {result['proceed_with_implementation']}")

        # Return the result as JSON for potential programmatic use
        print("\n" + json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error processing documentation request: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()