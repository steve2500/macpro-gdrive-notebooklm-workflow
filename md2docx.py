import markdown
import os

def convert_md_to_html(md_file_path):
    """将 Markdown 文件转换为包含 Meta 信息的完整 HTML 字符串"""
    if not os.path.exists(md_file_path):
        print(f"错误: 找不到文件 {md_file_path}")
        return None

    with open(md_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 使用 'extra' 扩展以支持表格、代码块、任务列表等高级语法
    # 使用 'toc' 扩展可以自动生成目录结构（如果需要）
    html_content = markdown.markdown(text, extensions=['extra', 'codehilite', 'toc'])

    # 包装成完整的 HTML 文档格式，确保 Google Drive 识别编码
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """
    
    # 将结果保存为本地文件供预览
    output_path = md_file_path.replace('.md', '.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    print(f"转换成功！HTML 文件已生成: {output_path}")
    return full_html

# 使用示例
# convert_md_to_html('test.md')