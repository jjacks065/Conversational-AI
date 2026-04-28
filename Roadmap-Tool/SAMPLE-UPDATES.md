# Sample Roadmap Updates

This file shows examples of common roadmap updates you might make to the `roadmap-data.json` file.

## Example 1: Adding a New Metric

To add a new strategic metric to the Overview section:

```json
{
  "sections": {
    "overview": {
      "metrics": [
        // Existing metrics...
        {
          "type": "uptime",
          "value": "99.9%",
          "label": "Platform Uptime",
          "icon": "⚡"
        }
      ]
    }
  }
}
```

## Example 2: Adding a Q2 Feature

To add a new feature to an existing Q2 card:

```json
{
  "sections": {
    "q2-details": {
      "cards": [
        {
          "title": "🏗️ Cost Optimization Foundation",
          "features": [
            // Existing features...
            {
              "name": "Advanced Caching Layer",
              "description": "Redis-based caching system for frequently accessed data to reduce API calls"
            }
          ]
        }
      ]
    }
  }
}
```

## Example 3: Adding a New Q2 Card

To add a completely new Q2 implementation area:

```json
{
  "sections": {
    "q2-details": {
      "cards": [
        // Existing cards...
        {
          "title": "🔒 Security Enhancement",
          "color": "#9c88ff", 
          "target": "Zero security incidents",
          "features": [
            {
              "name": "OAuth 2.0 Implementation",
              "description": "Secure authentication and authorization framework"
            },
            {
              "name": "Data Encryption",
              "description": "End-to-end encryption for sensitive customer data"
            }
          ]
        }
      ]
    }
  }
}
```

## Example 4: Updating Quarter Objectives

To modify Q3 objectives:

```json
{
  "sections": {
    "q3-q1-roadmap": {
      "quarters": [
        {
          "quarter": "Q3 2026",
          "theme": "Intelligence & Optimization",
          "subtitle": "Advanced AI Integration", 
          "objectives": [
            "Machine Learning Cost Optimization",
            "Advanced Analytics Platform", 
            "Agent Experience Excellence",
            "Predictive Scaling Implementation"  // New objective
          ]
        }
      ]
    }
  }
}
```

## Example 5: Adding Success Metrics

To add new KPIs to the metrics section:

```json
{
  "sections": {
    "metrics": {
      "agentExperience": {
        "metrics": [
          // Existing metrics...
          {
            "type": "training-time",
            "label": "Agent Training Time",
            "value": "<2 hours",
            "detail": "New agent onboarding",
            "icon": "🎓"
          }
        ]
      }
    }
  }
}
```

## Example 6: Updating the Transformation Description

To modify the strategic transformation narrative:

```json
{
  "sections": {
    "overview": {
      "transformation": {
        "title": "Strategic Transformation 2.0",
        "description": "Transform <strong>CSR Chat (aka. Minerva)</strong> from single customer platform to <strong>multi-tenant SaaS solution</strong> achieving profitable unit economics while maintaining enterprise-grade performance and premium agent experience."
      }
    }
  }
}
```

## Example 7: Updating Logo Path

To update the logo reference (e.g., after moving the logo file):

```json
{
  "metadata": {
    "logoPath": "./new-logo-filename.png"
  }
}
```

**Important**: When updating the logo path, you need to update it in TWO places:
1. In `roadmap-data.json` for external loading
2. In the embedded fallback data within the HTML template file

## Example 8: Adding Risk Mitigation

To add new risks and mitigation strategies:

```json
{
  "sections": {
    "metrics": {
      "riskMitigation": {
        "risks": [
          // Existing risks...
          {
            "title": "Technical Debt Accumulation",
            "mitigation": "Dedicated 20% capacity allocation for refactoring and technical debt reduction in each sprint"
          }
        ]
      }
    }
  }
}
```

## Best Practices

1. **Validate After Changes**: Always run `python3 validate-roadmap.py` after making updates
2. **Consistent Formatting**: Keep consistent emoji usage and color schemes
3. **Meaningful Icons**: Choose emojis that clearly represent the metric or feature
4. **Concise Descriptions**: Keep feature descriptions to 1-2 lines for readability
5. **Color Coordination**: Use colors that work well with the blue gradient background

## Quick Validation

After making changes:

```bash
# Validate the JSON structure
python3 validate-roadmap.py

# Open the presentation to see changes
open Minerva-Platform-Roadmap-Template.html
```