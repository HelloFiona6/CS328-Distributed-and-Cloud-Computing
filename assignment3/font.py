# # 查询当前系统所有字体
# from matplotlib.font_manager import FontManager
# import subprocess

# mpl_fonts = set(f.name for f in FontManager().ttflist)

# print('all font list get from matplotlib.font_manager:')
# for f in sorted(mpl_fonts):
#     print('\t' + f)
    
    
    
# from matplotlib.font_manager import findfont, FontProperties

# print(findfont(FontProperties(family="WenQuanYi Zen Hei")))

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
font_prop = fm.FontProperties(fname=font_path)

plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['axes.unicode_minus'] = False
