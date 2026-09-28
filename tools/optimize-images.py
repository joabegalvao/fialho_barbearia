#!/usr/bin/env python3
"""Gera as imagens otimizadas da landing page a partir dos arquivos originais.

Uso (na raiz do projeto):
    python3 tools/optimize-images.py

Requer Pillow (pip install pillow). Os originais nunca são alterados.
Para trocar uma foto, substitua o arquivo de origem ou edite a lista PHOTOS
e rode o script novamente.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"

# As fotos recebidas têm cerca de 665 px de largura. Nada é ampliado: a maior
# versão gerada é a do tamanho original.
WIDTHS = (360, 520)
LOGO_BG = (13, 12, 13)  # #0D0C0D, fundo do logo e fundo escuro da página

# nome de saída -> arquivo original (na raiz do projeto)
PHOTOS = {
    "toalha-quente": "Screenshot 2026-09-28 153120.png",
    "barbeiro-e-cliente-mirim": "Screenshot 2026-09-28 153138.png",
    "placa-barbearia-aberta": "Screenshot 2026-09-28 153147.png",
    "geladeira-bebidas": "Screenshot 2026-09-28 153208.png",
    "salao-poltronas": "Screenshot 2026-09-28 153218.png",
    "barbeiro-em-atendimento": "Screenshot 2026-09-28 153238.png",
}

# Fotos de perfil das avaliações: nome de saída -> arquivo na raiz do projeto
AVATARS = {
    "avaliacao-richard-derner": "Richard_Derner.png",
    "avaliacao-ronny-matheus": "Ronny_Matheus.png",
    "avaliacao-jose-gerdes": "Jose_Gerdes.png",
}

# Recorte aplicado a todas as fotos (esquerda, topo, direita, base), em pixels.
# As capturas de tela trazem uma linha irregular nas bordas.
TRIM = (2, 2, 2, 2)

# Recortes extras por arquivo, somados ao TRIM. Use quando o original trouxer
# faixas nas extremidades.
CROPS = {}


def open_source(source: str) -> Image.Image:
    im = Image.open(ROOT / source).convert("RGB")
    extra = CROPS.get(source, (0, 0, 0, 0))
    left, top, right, bottom = (a + b for a, b in zip(TRIM, extra))
    return im.crop((left, top, im.width - right, im.height - bottom))


def resize_to_width(im: Image.Image, width: int) -> Image.Image:
    if im.width <= width:
        return im.copy()
    height = round(im.height * width / im.width)
    return im.resize((width, height), Image.LANCZOS)


def build_photos() -> None:
    for name, source in PHOTOS.items():
        im = open_source(source)
        for width in WIDTHS:
            resize_to_width(im, width).save(
                OUT / f"{name}-{width}.webp", "WEBP", quality=80, method=6
            )
        im.save(OUT / f"{name}-{im.width}.webp", "WEBP", quality=82, method=6)
        # fallback JPEG para navegadores sem WebP
        im.save(
            OUT / f"{name}-{im.width}.jpg", "JPEG", quality=82, optimize=True, progressive=True
        )
        print(f"{name}: {im.width}x{im.height}")


def build_logo() -> None:
    """O logo original tem 447x447 px. Nada é redesenhado: o script limpa o
    ruído de compressão JPEG do fundo, que passa a ter a cor exata LOGO_BG
    (a mesma do fundo escuro da página), e torna transparente a área fora do
    círculo."""
    logo = Image.open(ROOT / "fialho_barbearia.jpg").convert("RGB")
    size = logo.width

    pixels = logo.load()
    for y in range(size):
        for x in range(size):
            r, g, b = pixels[x, y]
            if abs(r - LOGO_BG[0]) + abs(g - LOGO_BG[1]) + abs(b - LOGO_BG[2]) <= 14:
                pixels[x, y] = LOGO_BG

    # máscara circular com suavização de borda
    scale = 4
    mask = Image.new("L", (size * scale, size * scale), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * scale - 1, size * scale - 1), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)

    badge = logo.convert("RGBA")
    badge.putalpha(mask)

    for width in (size, 176):
        out = badge if width == size else badge.resize((width, width), Image.LANCZOS)
        out.save(OUT / f"logo-fialho-{width}.png", optimize=True)
        out.save(OUT / f"logo-fialho-{width}.webp", "WEBP", quality=92, method=6)
    print(f"logo-fialho: {size}x{size}")

    # Ícones
    for name, width in (("favicon-32", 32), ("apple-touch-icon", 180), ("icon-192", 192)):
        icon = badge.resize((width, width), Image.LANCZOS)
        if name == "apple-touch-icon":
            # o iOS não aceita transparência: fundo na cor do logo
            flat = Image.new("RGB", icon.size, LOGO_BG)
            flat.paste(icon, mask=icon.getchannel("A"))
            icon = flat
        icon.save(OUT / f"{name}.png", optimize=True)


def build_avatars() -> None:
    """Mantém o tamanho e a transparência originais (72x72 px)."""
    for name, source in AVATARS.items():
        im = Image.open(ROOT / source).convert("RGBA")
        im.save(OUT / f"{name}.png", optimize=True)
        im.save(OUT / f"{name}.webp", "WEBP", quality=90, method=6)
        print(f"{name}: {im.width}x{im.height}")


def build_social_card() -> None:
    """Imagem de compartilhamento (1200x630): logo à esquerda e foto à direita,
    sem ampliar nenhum dos dois."""
    card = Image.new("RGB", (1200, 630), LOGO_BG)

    photo = open_source(PHOTOS["toalha-quente"])
    photo = ImageOps.fit(photo, (480, 630), Image.LANCZOS, centering=(0.5, 0.45))
    card.paste(photo, (720, 0))

    logo = Image.open(OUT / "logo-fialho-447.png").convert("RGBA")
    logo = logo.resize((400, 400), Image.LANCZOS)
    card.paste(logo, ((720 - 400) // 2, (630 - 400) // 2), logo)

    card.save(OUT / "compartilhamento.jpg", "JPEG", quality=86, optimize=True, progressive=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_photos()
    build_logo()
    build_avatars()
    build_social_card()
    total = sum(f.stat().st_size for f in OUT.iterdir())
    print(f"{len(list(OUT.iterdir()))} arquivos, {total / 1024:.0f} KB no total")
