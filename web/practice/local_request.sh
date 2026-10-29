#!/bin/bash
# Reader-run only, after official Ollama installation and explicit model pull.
# This is local inference, not an OpenAI API call. No credentials.
curl --disable --noproxy '*' --connect-timeout 5 --max-time 120 \
  --silent --show-error --include \
  http://127.0.0.1:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3:0.6b",
    "messages": [{"role":"user","content":"只根据虚构材料输出两行，格式为事项｜负责人｜日期｜依据。缺失值写待确认，不补猜。材料：[L1]小林确认2026-10-30提交海报。[L2]场地报价还没收到，负责人和日期未定。 /no_think"}],
    "stream": false,
    "options": {"num_predict": 160},
    "keep_alive": 0
  }'
curl_status=$?
printf '\ncurl exit=%s；HTTP 状态另看上面的响应头。若超时，按教程停止本地模型。没有自动重试。\n' "$curl_status"
exit "$curl_status"
