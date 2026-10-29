"""Reader-run only. No SDK. One documented HTTPS request; never auto-retries."""
import json
import os
import sys
import urllib.error
import urllib.request

URL = 'https://api.openai.com/v1/responses'
PAYLOAD = {
    'model': 'gpt-5.4-mini-2026-03-17',
    'reasoning': {'effort': 'none'},
    'input': '只根据虚构材料输出两行，格式为“事项｜负责人｜日期｜依据”。缺失值写“待确认”，不补猜。材料：[L1]小林确认2026-10-30提交海报。[L2]场地报价还没收到，负责人和日期未定。',
    'max_output_tokens': 160,
    'store': False,
}


def text_parts(response):
    """Do not assume the first output item is a text message."""
    if not isinstance(response, dict):
        return []
    output = response.get('output')
    if not isinstance(output, list):
        return []
    parts = []
    for item in output:
        if not isinstance(item, dict) or item.get('type') != 'message':
            continue
        content = item.get('content')
        if not isinstance(content, list):
            continue
        for part in content:
            if (isinstance(part, dict) and part.get('type') == 'output_text'
                    and isinstance(part.get('text'), str)):
                parts.append(part['text'])
    return parts


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward credentials to a redirected destination.


def main():
    if sys.argv[1:] != ['--send-once']:
        print('未发送。读完费用/隐私说明后，才可加 --send-once。')
        return 2
    key = os.environ.get('OPENAI_API_KEY', '').strip()
    if not key:
        print('未发送：当前终端未设置 OPENAI_API_KEY。不要把密钥写入此文件。')
        return 2
    request = urllib.request.Request(
        URL, data=json.dumps(PAYLOAD, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key},
        method='POST')
    # No proxy auto-discovery in this teaching script. Do not bypass workplace policy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(request, timeout=60) as result:
            response = json.load(result)
            print('HTTP', result.status)
            print('request_id:', result.headers.get('x-request-id', '未返回'))
    except urllib.error.HTTPError as error:
        print('HTTP', error.code, 'request_id:', error.headers.get('x-request-id', '未返回'))
        print('Retry-After:', error.headers.get('Retry-After', '未返回'))
        # Error messages can echo credentials. Redact the exact supplied key before display.
        print(error.read(8192).decode('utf-8', errors='replace').replace(key, '[REDACTED]'))
        print('已停止，没有自动重试。按教程检查 error.code。')
        return 1
    except (urllib.error.URLError, TimeoutError, OSError):
        print('网络/TLS/超时错误。结果未知；不要立刻重发。检查用量后再决定。')
        return 1
    except (ValueError, TypeError):
        print('响应不是预期 JSON。已停止；不自动重试。')
        return 1
    if not isinstance(response, dict):
        print('响应不是预期 JSON 对象。已停止；不自动重试。')
        return 1
    print('status:', response.get('status'))
    print('incomplete_details:', response.get('incomplete_details'))
    print('usage:', json.dumps(response.get('usage'), ensure_ascii=False))
    parts = text_parts(response)
    print('TEXT:\n' + '\n'.join(parts))
    if response.get('status') != 'completed' or not parts:
        print('尚未通过：未完成或没有文本。不要把 HTTP 200 当作练习成功。')
        return 1
    print('传输完成；仍需人工逐行核对内容。没有继续发送。')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
