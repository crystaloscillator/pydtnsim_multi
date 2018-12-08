def load_X11_colors(file):
    color_pallete = dict()
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('!'):
                continue
            color, name = line.split('\t\t')
            r, g, b = color.split()
            color_pallete[name] = (r,g,b)
    return color_pallete
color_pallete = load_X11_colors('/usr/share/X11/rgb.txt')
print(color_pallete)
