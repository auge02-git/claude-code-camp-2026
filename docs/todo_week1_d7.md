[main 7b8b945] AWO: patch, logging on datetime of session on start-site.
11 files changed, 1621 insertions(+), 3 deletions(-)
create mode 100644 week0_explore/boukensha/journeys/erfahrung_durchlaeufe_v10_1.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v10.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-15_v11.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-16_v1.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-16_v2.md
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-16_v3.md
create mode 100644 week0_explore/boukensha/references/commands.md


### claudeCodeCamp/week0_explore/boukensha/boukensha/cli.py

[week0_tests bfb018a] AWO: patch, after dsl can agent prompting.
12 files changed, 226 insertions(+), 68 deletions(-)
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-16_v3.md

boukensha --prompt "schau"
boukensha --prompt "schau" --prompt "geh norden"
boukensha --dsl journeys/start.txt --prompt "inventar"

uv run boukensha --llm-base-url http://localhost:1234 --model google/gemma-4-12b-qat --max-steps 30 --dsl ./journeys/mud-journeys-2026-07-16_v3.md --prompt "level schneller und toede wenn es geht"

[main b5c67e1] AWO: add, prompting option into dsl-running session.
2 files changed, 24 insertions(+), 1 deletion(-)

-----------

Andre.Wolff@MB-J3XNPGKM94 claudeCodeCamp % git switch week1_baselines
A       docs/todo_week0_d5.md
M       week0_explore/boukensha/boukensha/__pycache__/cli.cpython-313.pyc
M       week0_explore/boukensha/boukensha/cli.py
branch 'week1_baselines' set up to track 'origin/week1_baselines'.
Switched to a new branch 'week1_baselines'