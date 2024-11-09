boost = '''
Parse the given text as a CV file, put weights on the motivations you extracted, according to the SDT. Please give in the following format:
"motivations": {
    "autonomy": {
      "personal_growth": {
        "weight": "int",
        "description": "str"
      },
      "value_driven": {
        "weight": "int",
        "description": "str"
      }
    },
    "competence": {
      "strategic_impact": {
        "weight": "int",
        "description": "str"
      }
    },
    "relatedness": {
      "community_impact": {
        "weight": "int",
        "description": "str"
      }
    },
    "extrinsic": {
      "financial_focus": {
        "weight": "int",
        "description": "str"
      }
    }

return JSON only
'''