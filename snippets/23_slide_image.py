import base64
from openai import OpenAI

openai_client = OpenAI()

def make_slide(arch, png, filename="proposal_slide.png", quality="medium"):   # "low" to save money in class
    """Turns the diagram into a 16:9 proposal slide with the pricing table. Returns the PNG path."""
    totals = cost_totals(arch)
    lines = "\n".join(f"- {c.item}: USD {c.usd:,.0f}" + (" / mes" if c.kind == "aws_monthly" else "")
                      for c in arch.costs)
    prompt = f"""Turn this AWS architecture diagram into a sales proposal slide, 16:9 format,
clean and professional style, white background. All text on the slide must be in Spanish.
Keep the same AWS icons, services and arrows from the diagram. Do not add or remove services.
On the right, add a pricing table with exactly these lines:
{lines}
Total consultoría (una vez): USD {totals['consulting']:,.0f}
Total AWS estimado ilustrativo: USD {totals['aws_monthly']:,.0f} / mes
Title: {arch.title}. Provider: NubeAndina Consulting."""
    with open(png, "rb") as diagram:
        res = openai_client.images.edit(       # edits from the diagram: keeps icons and arrows
            model=IMAGE_MODEL,
            image=diagram,
            prompt=prompt,
            size="1536x1024",                  # landscape, slide-like
            quality=quality,
        )
    with open(filename, "wb") as f:
        f.write(base64.b64decode(res.data[0].b64_json))
    return filename

slide = make_slide(arch, png)
display(Image(slide))
# Without an input diagram: inside make_slide use openai_client.images.generate(model=IMAGE_MODEL, prompt=prompt, size="1536x1024")
