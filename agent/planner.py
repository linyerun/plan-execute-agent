from typing import Callable, List
import re

def plan_prompt(task: str) -> str:
    return (
        "Break the task into 3-7 concrete steps.Return ONE step per line.\n"
        f"Task: {task}"
    )


def replan_prompt(task: str, step: str, e: Exception) -> str:
    return (
        f"Task: {task}\n"
        f"Failed step: {step}\n"
        f"Error: {e}\n"
        "Give a new plan."
    )


def _parse_steps(text: str) -> List[str]:
    result = []
    for s in text.splitlines():
        s = s.strip()
        if not s:
            continue
        # 匹配行首：数字. 或者 - ，一次性删掉
        s = re.sub(r'^(\d+\.|-)', '', s)
        result.append(s.strip())
    return result


def plan(llm: Callable[[str], str], prompt: str) -> List[str]:
    text = llm(prompt)
    steps = _parse_steps(text)
    return steps
