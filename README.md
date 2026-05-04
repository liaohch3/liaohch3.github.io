# liaohch3.github.io

个人博客，基于 [Hugo](https://gohugo.io/) + [Stack](https://github.com/CaiJimmy/hugo-theme-stack) 主题搭建。

📖 https://liaohch3.com/

## 发布前检查

发布 workflow 会先运行敏感信息扫描，避免把高置信度 secret、个人身份信息或图片元数据发布到公网：

```bash
python3 scripts/check_sensitive_info.py
```

如果某一行确实需要公开，可以在该行加入 `sensitive-ok` 作为显式豁免。
