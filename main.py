from tools import build_default_tools
import os
from llm import create_llm
from dotenv import load_dotenv
from agent.loop import plan_and_execute

load_dotenv()

def main():
    # 获取模型配置
    api_key = os.environ.get("API_KEY")
    base_url = os.environ.get("BASE_URL")
    model = os.environ.get("MODEL")
    if not api_key:
        raise ValueError("未找到 API_KEY，请在 .env 文件中配置。")
    if not base_url:
        raise ValueError("未找到 BASE_URL，请在 .env 文件中配置。")
    if not model:
        raise ValueError("未找到 MODEL，请在 .env 文件中配置。")

    # 创建一个llm调用函数
    llm = create_llm(
        api_key,
        base_url,
        model,
        system_prompt=(
            "You are a Plan-and-Execute agent assistant. "
            "When planning, output numbered steps one per line. "
            "When executing or summarizing, use the same language as the task."
        )
    )

    # 获取提供给llm调用的工具信息
    tools = build_default_tools()

    # 测试案例
    prompt = "查看当前日期，把当前日期所有的数字求和，并返回结果。"
    print(f"user prompt: {prompt}\n")
    result = plan_and_execute(prompt, llm, tools, max_replans=2, verbose=True)
    print(f"\nFinal Result: {result}")


if __name__ == '__main__':
    main()
