#!/bin/bash
# Script to package the mcp-doc-grounding skill into a distributable format

SKILL_NAME="mcp-doc-grounding"
SKILL_DIR=".claude/skills/${SKILL_NAME}"
OUTPUT_DIR="${SKILL_DIR}/dist"

echo "Packaging ${SKILL_NAME} skill..."

# Create output directory
mkdir -p "${OUTPUT_DIR}"

# Create the skill package as a zip file
cd "${SKILL_DIR}" || exit 1
zip -r "${OUTPUT_DIR}/${SKILL_NAME}.skill" . -x "dist/*" "*/__pycache__/*" "*.pyc" "*.pyo" ".git/*" ".DS_Store"

echo "Skill packaged successfully as ${OUTPUT_DIR}/${SKILL_NAME}.skill"

# Validate the package structure
echo ""
echo "Validating package structure..."
if [ -f "${OUTPUT_DIR}/${SKILL_NAME}.skill" ]; then
    echo "✓ Package file created successfully"

    # Check if required files are present by examining the zip contents
    if zipinfo -1 "${OUTPUT_DIR}/${SKILL_NAME}.skill" | grep -q "SKILL.md"; then
        echo "✓ SKILL.md found in package"
    else
        echo "✗ SKILL.md not found in package"
    fi

    if zipinfo -1 "${OUTPUT_DIR}/${SKILL_NAME}.skill" | grep -q "scripts/"; then
        echo "✓ Scripts directory found in package"
    else
        echo "✓ No scripts directory (optional)"
    fi

    echo "Package validation complete!"
else
    echo "✗ Package creation failed"
    exit 1
fi