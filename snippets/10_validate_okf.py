import frontmatter

def validate_okf():
    invalid = [str(p) for p in OKF.rglob("*.md")
               if p.name != "log.md" and not frontmatter.load(p).get("type")]
    print("✅ Valid OKF" if not invalid else f"❌ Missing 'type': {invalid}")

validate_okf()
