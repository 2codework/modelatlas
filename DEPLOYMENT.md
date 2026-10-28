# GitHub Pages

静态站点地址：https://2codework.github.io/modelatlas/ 。

`python scripts/build.py` 生成 `dist/` 并同步到 Pages 使用的 `docs/`；保留 `.nojekyll` 与相对资源路径。`python scripts/check_pages.py` 检查两目录字节一致、严格 JSON 及本地链接。

`.github/workflows/checks.yml` 在 push/PR 执行离线构建、Python 与 Node 测试，并检查生成文件是否最新。该工作流不部署、不访问外部模型，也不安装项目第三方依赖。线上版本以对应提交的 Actions 与 Pages 结果为准。

发布前检查数据来源、许可、安全与浏览器可访问性。发布后核对实际 URL、子路径资源、CSP、数据计数与生效提交。构建成功不等于已发布。
