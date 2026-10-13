from typing import Callable, Dict, Any
from tools.types import Tool
from agent.planner import plan, plan_prompt, replan_prompt
from agent.executor import execute



def plan_and_execute(
    task: str,
    llm: Callable[[str], str],
    tools: Dict[str, Tool],
    max_replans: int = 2,
    verbose: bool = False,
) -> str:
    # 生成执行计划
    steps = plan(llm, plan_prompt(task))
    if verbose:
        print("\n=== Plan ===")
        for i, st in enumerate(steps, 1):
            print(f"  {i}. {st}")
        print()

    # 子任务执行的状态
    state: Dict[str, Any] = {}
    for attempt in range(max_replans + 1):
        # 逐步执行
        for i, st in enumerate(steps):
            if verbose:
                print(f"\n--- Executing step {i + 1}: {st} ---")
            try:
                out = execute(st, state, tools, llm, verbose=verbose)
                state[f"step_{i}"] = out
                if verbose:
                    print(f"Result: {out}\n")
            except Exception as e:
                # 某一个步骤执行过程中出现异常触发下面逻辑
                if verbose:
                    print(f"Step failed: {e}. Replanning...\n")
                # 重新进行一次任务规划
                steps = plan(llm, replan_prompt(task, st, e))
                if verbose:
                    print("\n=== Replanned ===")
                    for j, new_st in enumerate(steps, 1):
                        print(f"  {j}. {new_st}")
                    print()
                break
        else:
            summary_prompt = f"Summarize final result based on: {state}"
            return llm(summary_prompt)

    return "Failed after replanning."
