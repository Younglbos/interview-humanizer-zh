"""Build a self-contained Doubao chat prompt from the maintained skill sources."""

from pathlib import Path
import re


def build(root):
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    skill = re.sub(r"\A---\n.*?\n---\n", "", skill, count=1, flags=re.S)
    skill = skill.replace(
        "阅读 [采访体裁指南](references/interview-writing.md) 的对应部分",
        "按下文“采访体裁指南”的对应部分处理",
    ).replace(
        "每次润色或成稿都阅读 [Humanizer-zh 表达检查](references/humanizer-base.md)",
        "每次润色或成稿都按下文“Humanizer-zh 表达检查”核对",
    ).replace("来源及许可见 [NOTICE.md](NOTICE.md)。", "来源及许可声明见本文末尾。")
    writing = (root / "references/interview-writing.md").read_text(encoding="utf-8")
    base = (root / "references/humanizer-base.md").read_text(encoding="utf-8")
    base = base[base.index("# Humanizer-zh\n"):]
    license_text = (root / "LICENSE").read_text(encoding="utf-8").strip()
    intro = """# 豆包采访写作助手 · 小苹果树专用

你是为小苹果树提供中文采访稿写作帮助的助手。按下列规则处理用户随后提供的材料；不假装已完成真实采访、事实调查或文件操作。

本文件包含完整规则，不依赖仓库文件读取、联网工具或其他客户端配置。没有文件工具时在对话中交付文本；只有在实际具备能力并按用户请求操作成功后，才声称已读取附件、修改文件或生成文件。

用户尚未提供任务或材料时，简短请用户发送稿件或采访记录，不把本规则改写成文章。已提供材料时直接执行，优先保留事实、引语、归因和确定程度。

"""
    source = """# 来源与许可声明

本文件由 interview-humanizer-zh 的规则文件合并生成，上游 Humanizer-zh 的 31 项检查完整保留。
项目：https://github.com/Younglbos/interview-humanizer-zh
上游：https://github.com/op7418/Humanizer-zh
上游基准提交：f4518a8eab97b8bfebc66a89d34320a89bef6930。
以下为分发本文件时需保留的 MIT 声明，不属于稿件正文。

"""
    return intro + skill.strip() + "\n\n" + writing.strip() + "\n\n# Humanizer-zh 表达检查\n\n" + base.strip() + "\n\n" + source + license_text + "\n"


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    target = root / "DOUBAO_PROMPT.md"
    target.write_text(build(root), encoding="utf-8")
    print(f"Generated {target.name}")
