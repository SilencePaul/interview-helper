# Interview Prep Agent - Project Spec (for Claude Code)

## Goal
Build a local interview-prep assistant that helps me:
1) Review CS fundamentals notes (八股) in markdown
2) Practice algorithms in an interview-style workflow (prompt -> my answer -> grading)
3) Track weak points and schedule spaced repetition
4) (Optional) generate/replace missing figures with mermaid diagrams

This project should be a real usable AI-agent product, not just scripts.

## Non-goals / Constraints
- Do NOT reproduce copyrighted content verbatim from external sites.
- Use my existing markdown notes as the source of truth.
- If a note references a missing image, replace it with:
  - a Mermaid diagram, or
  - a compact table, or
  - a short text schematic
- Keep everything runnable locally.

## Repo Structure (expected)
/notes/                     # my pasted 八股 markdown notes (grouped by topic)
/patterns/                  # algorithm patterns (small set, high quality)
/problems/                  # algorithm problem bank (structured)
/mistakes/                  # my retrospectives after mock interviews
/assets/                    # screenshots or images I add manually
/prompts/                   # system prompts / role prompts
/app/                       # executable app (CLI or minimal web)
/data/                      # progress, scores, spaced repetition schedule

## Data Formats
### Notes
- Markdown files in /notes

### Algorithm Problems (JSON)
Each problem file should include:
{
  "id": "lc_3",
  "title": "Longest Substring Without Repeating Characters",
  "url": "...",
  "tags": ["sliding_window", "hashmap"],
  "trigger_words": ["longest", "substring", "without repeating"],
  "difficulty": "medium",
  "time_limit_min": 20,
  "rubric": {
    "recognize_pattern": 3,
    "correctness": 4,
    "complexity": 2,
    "edge_cases": 1
  },
  "solution_outline": [
    "Use sliding window with hashmap last_seen",
    "Move left pointer when duplicate inside window",
    "Update max length"
  ],
  "common_mistakes": [
    "left pointer update wrong",
    "forget to use max(left, last_seen+1)"
  ]
}

### Patterns (Markdown)
Each pattern doc must include:
- When to use (trigger words + constraints)
- Template (pseudocode)
- Edge cases checklist
- Complexity
- 3 representative problems (ids)

## Agent Roles
### Tutor
- Explain concepts, then ask 2-3 follow-up questions.
- Explain my questions.
- Use my notes as grounding; if missing, mention me and add the missing part for in the notes

### Interviewer
- Only asks questions.
- Enforces time limit and follow-up probing.
- No solutions given.

### Grader
- Grades my answer using rubric.
- Outputs:
  - score breakdown
  - what I missed
  - a model answer structure (not necessarily full code)
  - next-step drills (link to patterns + problems)

## Core Features (MVP)
1) Topic review:
- pick a topic -> ask me active recall questions -> grade -> log results -> record mistakes 

2) Algorithm mock:
- pick a problem by tag/difficulty -> interview mode -> grade -> store mistakes

3) Spaced repetition:
- schedule next review based on performance (simple SM-2 or lightweight heuristic)

4) Figure completion:
- scan notes for image missing and generate mermaid diagrams where possible

## Output / UX
Pick one:
- CLI (recommended first): `python -m app`
- Minimal local web (optional later)

CLI commands:
- review topic <topic>
- mock algo --tag sliding_window --difficulty medium
- stats
- fix-figures

## Tech Choices
Prefer Python:
- Typer or Click for CLI
- Pydantic for schemas
- SQLite for progress (or JSON if simplest)

## Acceptance Criteria
- I can run the app locally and complete:
  - 1 topic review session
  - 1 algorithm mock session
  - see grading + saved results
  - see next scheduled review
- Placeholders in notes can be detected and converted to mermaid diagrams.

## First Tasks for Claude Code
1) Scaffold the repo structure and minimal CLI
2) Implement schemas for Problem/Result/ReviewPlan
3) Implement Interviewer + Grader loop for algorithm problems
4) Add 3 patterns + 5 problems as examples
5) Implement a figure placeholder scanner and mermaid generator (basic)