# 目录结构
```text
plan-execute-agent/
├── main.py              # 程序入口
├── agent/
│   ├── types.py         # HistoryItem 定义
│   ├── planner.py       # plan
│   ├── loop.py          # plan_and_execute（核心）
│   ├── executor.py      # execute（ReAct 单步执行器）
│   ├── react_loop.py    # ReAct 循环 + Tool execution 日志
│   └── prompt.py        # ReAct 提示词 / Action 解析
├── tools/
│   ├── calculator.py
│   ├── current_time.py
│   ├── word_count.py
│   └── types.py             # Tool 定义
├── llm.py                   # 模型调用 + JSON 日志 + print_message / print_messages
├── requirements.txt
└── .env.example
```

# 配置apikey
```bash
cp .env.example .env
```

# 运行
```bash
pip install -r requirements.txt
```

```bash
python main.py
```