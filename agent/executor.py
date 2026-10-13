from typing import Callable, Dict, Any
from tools.types import Tool
from agent.react import react_loop


def execute(
    step: str,
    state: Dict[str, Any],
    tools: Dict[str, Tool],
    llm: Callable[[str], str],
    verbose: bool = False,
) -> str:
    """以 ReAct 作为单步执行器，结合已有 state 完成当前步骤。"""
    context = "\n".join(f"- {k}: {v}" for k, v in state.items()) or "(none)"
    question = (
        f"Complete this step only:\n{step}\n\n"
        f"Prior step results:\n{context}\n\n"
        "Use tools if needed, then give Final Answer succinctly."
    )
    return react_loop(question, tools, llm, max_steps=4, verbose=verbose)
