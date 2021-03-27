__version__ = "0.1.0"

import cairo

to_point = 2.83465


def norm_col(*args):
    args = list(args)
    for i, a in enumerate(args):
        args[i] = a / 255.0
    return tuple(args)


cbackground = norm_col(254, 246, 228)
cmajor = norm_col(208, 210, 211)
lmajor = 0.8
cminor = norm_col(239, 223, 215)

lpminor = 0.8
apminor = 0.8

lsminor = 0.6
asminor = 0.4


def hor(ctx, off, margin, twidth, height, grid):
    pos = off
    while pos < height:
        ctx.move_to(margin, pos)
        ctx.line_to(twidth, pos)
        pos += grid * 2


def vert(ctx, off, margin, twidth, height, grid):
    pos = margin + off
    while pos < twidth:
        ctx.move_to(pos, 0)
        ctx.line_to(pos, height)
        pos += grid * 2


def page_mm(margin, width, height, grid):
    margin = float(margin) * to_point
    width = float(width) * to_point
    height = float(height) * to_point
    grid = float(grid) * to_point
    return page(margin, width, height, grid)


def page(margin, width, height, grid):
    twidth = margin + width
    with cairo.SVGSurface("paper.svg", twidth, height) as srf:
        page_srf(srf, margin, twidth, height, grid)
    with cairo.PDFSurface("paper.pdf", twidth, height) as srf:
        page_srf(srf, margin, twidth, height, grid)


def page_srf(srf, margin, twidth, height, grid):
    ctx = cairo.Context(srf)
    ctx.set_source_rgb(*cbackground)
    ctx.rectangle(0, 0, twidth, height)
    ctx.fill()

    ctx.set_source_rgb(*cmajor)
    ctx.set_line_width(lmajor)
    hor(ctx, 0, margin, twidth, height, grid)
    ctx.stroke()

    ctx.set_source_rgba(*cminor, apminor)
    ctx.set_line_width(lpminor)
    vert(ctx, 0, margin, twidth, height, grid)
    ctx.stroke()

    ctx.set_source_rgba(*cminor, asminor)
    ctx.set_line_width(lsminor)
    vert(ctx, grid, margin, twidth, height, grid)
    hor(ctx, grid, margin, twidth, height, grid)
    ctx.stroke()
