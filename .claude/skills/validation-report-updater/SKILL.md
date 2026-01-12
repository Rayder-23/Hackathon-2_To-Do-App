---
name: validation-report-updater
description: Read skill validation reports and systematically apply all recommendations to update skills. Use this skill when you have validation reports with recommendations that need to be implemented in skills, ensuring all priority levels (high, medium, low) are addressed.
---

# Validation Report Updater

## Overview

This skill provides a systematic approach to reading skill validation reports and applying all recommendations to update skills. It ensures that all priority levels (high, medium, low) are considered and implemented, not just high-priority items. The skill helps transform validation feedback into concrete improvements in skill implementations.

## When to Use This Skill

Use this skill when:
- You have received validation reports for skills with recommendations
- You need to systematically apply all recommendations (high, medium, low priority)
- You want to ensure comprehensive skill improvement based on validation feedback
- You're performing routine skill maintenance and quality improvements
- You need to track implementation of validation report recommendations

## Required Clarifications

1. What validation report needs to be processed? (Path to validation report file)
2. Which skill needs to be updated based on the report? (Skill name/path)
3. What specific recommendations from the report need attention? (Priority levels to focus on)
4. Are there any constraints on the type of changes that can be made? (Permissions, timeline, dependencies)

## Workflow

### Step 1: Analyze Validation Report

Read and analyze the validation report to identify all recommendations:

1. **Extract all recommendations** from the report
2. **Categorize by priority level** (High, Medium, Low)
3. **Identify critical issues** that must be addressed
4. **Note strengths** to preserve during updates

### Step 2: Prioritize Implementation

Create an implementation plan that addresses all priority levels:

```
IMPLEMENTATION PLAN:
- High Priority: [List all high priority items to address first]
- Medium Priority: [List all medium priority items to address second]
- Low Priority: [List all low priority items to address last]
- Critical Issues: [List any critical issues that require immediate attention]
```

### Step 3: Apply All Recommendations

Systematically implement recommendations in priority order:

1. **Start with high priority** recommendations
2. **Continue with medium priority** items
3. **Address low priority** improvements
4. **Document status** of each recommendation as [COMPLETED], [PARTIALLY COMPLETED], or [PENDING]

### Step 4: Verification

Verify that all recommendations have been addressed:

```
VERIFICATION CHECKLIST:
- [ ] All high priority recommendations implemented
- [ ] All medium priority recommendations addressed
- [ ] All low priority recommendations considered
- [ ] Critical issues resolved
- [ ] Skill functionality maintained
- [ ] No regressions introduced
- [ ] Updated skill validated again (if needed)
```

## Best Practices

### Comprehensive Coverage
- Address ALL recommendations, not just high-priority ones
- Track the status of each recommendation individually
- Update validation reports to reflect completed actions

### Systematic Approach
- Work through recommendations in priority order
- Make incremental changes and verify after each set
- Preserve skill functionality while improving quality

### Documentation
- Mark completed recommendations with [COMPLETED]
- Note partially completed items as [PARTIALLY COMPLETED]
- Document reasons for any items marked [PENDING]
- Update validation reports with implementation status

## Implementation Guidelines

### For High Priority Items
- These should be implemented immediately
- Usually address critical structural or functional issues
- May prevent the skill from working properly

### For Medium Priority Items
- These improve usability or maintainability
- Can be implemented after high priority items
- Often relate to user experience or workflow improvements

### For Low Priority Items
- These are enhancement suggestions
- May improve long-term maintainability
- Good for polishing and refinement

## Quality Gates

Before considering the update complete:
- All high priority recommendations must be implemented
- Medium priority recommendations should be addressed
- Low priority recommendations should be considered and either implemented or documented as deferred
- The updated skill should maintain its core functionality
- No new issues should be introduced during the update process

## Output Specification

After applying this skill, you should produce:
1. Updated skill files with all recommendations implemented
2. Updated validation report reflecting completed actions
3. Summary of changes made and recommendations status
4. Any new validation reports if the skill was re-validated