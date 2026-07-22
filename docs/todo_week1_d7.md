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

[week1_baselines 03ffa49] AWO: patch, todo and branch to week1.
3 files changed, 58 insertions(+), 1 deletion(-)
create mode 100644 docs/todo_week1_d7.md

-----------

[week1_baselines f6c357d] AWO: add, new journey as update and patch, optional run with --prompt option
17 files changed, 1566 insertions(+), 3 deletions(-)
create mode 120000 _docs
create mode 100644 week0_explore/boukensha/journeys/mud-journeys-2026-07-18_v1.md
create mode 100644 week1_baseline/log_viz/__pycache__/server.cpython-313.pyc
create mode 100644 week1_baseline/log_viz/server.py
create mode 100644 week1_baseline/mud-mcp/.gitignore
create mode 100644 week1_baseline/mud-mcp/README.md
create mode 100644 week1_baseline/mud-mcp/credentials.example.json
create mode 100644 week1_baseline/mud-mcp/mud_mcp/__init__.py
create mode 100644 week1_baseline/mud-mcp/mud_mcp/server.py
create mode 100644 week1_baseline/mud-mcp/mud_mcp/session.py
create mode 100644 week1_baseline/mud-mcp/pyproject.toml
create mode 100644 week1_baseline/mud-mcp/scripts/smoke_test.py
create mode 100644 week1_baseline/mud-mcp/uv.lock

[week1_baselines 64d87c4] AWO: patch, finish week0 and commit.
1 file changed, 1 insertion(+), 1 deletion(-)

-----------

[week1_baselines fa43d68] AWO: init, week1 data's from repo and main-structure.
240 files changed, 19126 insertions(+)
create mode 100644 week0_explore/explore_architecture/03c_subagent_sdk/.gitignore
create mode 100644 week0_explore/explore_architecture/03c_subagent_sdk/data/world.md
create mode 100644 week0_explore/explore_architecture/03c_subagent_sdk/references/commands.md
create mode 100644 week0_explore/explore_architecture/03c_subagent_sdk/requirements.txt
create mode 100755 week0_explore/explore_architecture/03c_subagent_sdk/scripts/mud_client.py
create mode 100755 week0_explore/explore_architecture/03c_subagent_sdk/scripts/run_agent.py
create mode 100644 week0_explore/explore_architecture/03c_subagent_sdk/scripts/run_agent_ollama.py
create mode 100644 week0_explore/explore_architecture/04_n8n/readme.md
create mode 100644 week1_baseline/python/00_config/README.md
create mode 100644 week1_baseline/python/00_config/boukensha/__init__.py
create mode 100644 week1_baseline/python/00_config/boukensha/config.py
create mode 100644 week1_baseline/python/00_config/boukensha/py.typed
create mode 100644 week1_baseline/python/00_config/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/00_config/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/00_config/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/00_config/examples/example.py
create mode 100644 week1_baseline/python/00_config/prompts/system.md
create mode 100644 week1_baseline/python/00_config/pyproject.toml
create mode 100644 week1_baseline/python/01_struct_skeleton/README.md
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/__init__.py
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/config.py
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/context.py
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/message.py
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/py.typed
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/01_struct_skeleton/boukensha/tool.py
create mode 100644 week1_baseline/python/01_struct_skeleton/examples/example.py
create mode 100644 week1_baseline/python/01_struct_skeleton/pyproject.toml
create mode 100644 week1_baseline/python/02_the_registry/README.md
create mode 100644 week1_baseline/python/02_the_registry/boukensha/__init__.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/config.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/context.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/errors.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/message.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/py.typed
create mode 100644 week1_baseline/python/02_the_registry/boukensha/registry.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/02_the_registry/boukensha/tool.py
create mode 100644 week1_baseline/python/02_the_registry/examples/example.py
create mode 100644 week1_baseline/python/02_the_registry/pyproject.toml
create mode 100644 week1_baseline/python/03_prompt_builder/README.md
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/__init__.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/backends/__init__.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/backends/anthropic.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/backends/base.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/backends/gemini.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/backends/mammouth.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/backends/ollama.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/backends/ollama_cloud.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/backends/openai.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/config.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/context.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/errors.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/message.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/prompt_builder.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/py.typed
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/registry.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/03_prompt_builder/boukensha/tool.py
create mode 100644 week1_baseline/python/03_prompt_builder/examples/example.py
create mode 100644 week1_baseline/python/03_prompt_builder/prompts/system.md
create mode 100644 week1_baseline/python/03_prompt_builder/pyproject.toml
create mode 100644 week1_baseline/python/04_api_client/README.md
create mode 100644 week1_baseline/python/04_api_client/boukensha/__init__.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/backends/__init__.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/backends/anthropic.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/backends/base.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/backends/gemini.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/backends/mammouth.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/backends/ollama.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/backends/ollama_cloud.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/backends/openai.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/client.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/config.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/context.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/errors.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/message.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/prompt_builder.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/py.typed
create mode 100644 week1_baseline/python/04_api_client/boukensha/registry.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/04_api_client/boukensha/tool.py
create mode 100644 week1_baseline/python/04_api_client/examples/example.py
create mode 100644 week1_baseline/python/04_api_client/prompts/system.md
create mode 100644 week1_baseline/python/04_api_client/pyproject.toml
create mode 100644 week1_baseline/python/05_agent_loop/README.md
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/__init__.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/agent.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/backends/__init__.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/backends/anthropic.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/backends/base.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/backends/gemini.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/backends/mammouth.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/backends/ollama.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/backends/ollama_cloud.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/backends/openai.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/client.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/config.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/context.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/errors.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/message.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/prompt_builder.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/py.typed
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/registry.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/05_agent_loop/boukensha/tool.py
create mode 100644 week1_baseline/python/05_agent_loop/examples/example.py
create mode 100644 week1_baseline/python/05_agent_loop/prompts/system.md
create mode 100644 week1_baseline/python/05_agent_loop/pyproject.toml
create mode 100644 week1_baseline/python/06_the_logger/README.md
create mode 100644 week1_baseline/python/06_the_logger/boukensha/__init__.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/agent.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/backends/__init__.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/backends/anthropic.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/backends/base.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/backends/gemini.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/backends/mammouth.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/backends/ollama.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/backends/ollama_cloud.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/backends/openai.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/client.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/config.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/context.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/errors.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/logger.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/message.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/prompt_builder.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/py.typed
create mode 100644 week1_baseline/python/06_the_logger/boukensha/registry.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/06_the_logger/boukensha/tool.py
create mode 100644 week1_baseline/python/06_the_logger/examples/example.py
create mode 100644 week1_baseline/python/06_the_logger/prompts/system.md
create mode 100644 week1_baseline/python/06_the_logger/pyproject.toml
create mode 100644 week1_baseline/python/07_the_run_dsl/README.md
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/__init__.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/agent.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/backends/__init__.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/backends/anthropic.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/backends/base.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/backends/gemini.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/backends/mammouth.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/backends/ollama.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/backends/ollama_cloud.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/backends/openai.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/client.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/config.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/context.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/errors.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/logger.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/message.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/prompt_builder.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/py.typed
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/registry.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/run_dsl.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/07_the_run_dsl/boukensha/tool.py
create mode 100644 week1_baseline/python/07_the_run_dsl/examples/example.py
create mode 100644 week1_baseline/python/07_the_run_dsl/prompts/system.md
create mode 100644 week1_baseline/python/07_the_run_dsl/pyproject.toml
create mode 100644 week1_baseline/python/08_the_repl_loop/README.md
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/__init__.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/agent.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/backends/__init__.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/backends/anthropic.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/backends/base.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/backends/gemini.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/backends/mammouth.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/backends/ollama.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/backends/ollama_cloud.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/backends/openai.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/client.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/config.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/context.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/errors.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/logger.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/message.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/prompt_builder.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/py.typed
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/registry.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/repl.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/run_dsl.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/tool.py
create mode 100644 week1_baseline/python/08_the_repl_loop/boukensha/version.py
create mode 100644 week1_baseline/python/08_the_repl_loop/examples/example.py
create mode 100644 week1_baseline/python/08_the_repl_loop/prompts/system.md
create mode 100644 week1_baseline/python/08_the_repl_loop/pyproject.toml
create mode 100644 week1_baseline/python/09_global_executable/README.md
create mode 100755 week1_baseline/python/09_global_executable/bin/boukensha
create mode 100644 week1_baseline/python/09_global_executable/boukensha/__init__.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/agent.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/backends/__init__.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/backends/anthropic.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/backends/base.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/backends/gemini.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/backends/mammouth.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/backends/ollama.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/backends/ollama_cloud.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/backends/openai.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/client.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/config.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/context.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/errors.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/logger.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/message.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/prompt_builder.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/py.typed
create mode 100644 week1_baseline/python/09_global_executable/boukensha/registry.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/repl.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/run_dsl.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/tasks/__init__.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/tasks/base.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/tasks/player.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/tool.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha/version.py
create mode 100644 week1_baseline/python/09_global_executable/boukensha_loader.py
create mode 100644 week1_baseline/python/09_global_executable/prompts/system.md
create mode 100644 week1_baseline/python/09_global_executable/pyproject.toml
create mode 100644 week1_baseline/python/INTERACTIONS_GERMAN.md
create mode 100644 week1_baseline/python/INTERACTIONS_PART_GER.md
create mode 100644 week1_baseline/ruby/INTERACTIONS_GERMAN.md
create mode 100644 week1_baseline/ruby/ITERATIONS.md

-----------