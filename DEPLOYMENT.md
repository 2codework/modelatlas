# GitHub Pages 部署准备（尚未执行）

目标候选：`2codework/ModelAtlas`；仓库名与组织权限由发布者核实。本地版本不调用 GitHub，不自动创建或推送，不开通付费服务。

1. 审核数据来源与许可归属，确认公开授权；检查仓库不含秘密、个人数据或受限评测资料。
2. 按 README 构建及运行全部测试。浏览器验收桌面/手机/键盘/进度导入导出；该验收尚未由本地测试证明。
3. 创建公开仓库并推送受审核源码。选定 Pages 发布方式。
4. 推荐将 `dist/` 作为静态发布内容；保留 `.nojekyll` 和相对路径。若采用分支目录发布，可把 dist 内容放入独立发布分支根目录。不要发布整个工作区。
5. `ci-drafts/check.yml.disabled` 是未启用草案。只有经授权后才移动为 `.github/workflows/check.yml`。草案只校验，不部署；任何 Pages workflow 权限和 action 固定提交需单独审核，不照抄未知 action。
6. 预期项目地址形如 `https://2codework.github.io/ModelAtlas/`，这只是预期格式，**不是已部署链接**。发布后检查实际 URL、子路径资源、CSP、生效提交和数据计数；成功后才能报告上线。

构建无网络依赖，无 npm/pip 安装。运行 Python 静态服务器只供本地预览；不作为公开生产服务器。
