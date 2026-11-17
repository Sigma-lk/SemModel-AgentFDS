from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

def main():
    # Diagram nodes aggregate related responsibilities to keep the overview at ten.
    OUT = Path(__file__).parent
    W, H = 3000, 2380
    im = Image.new('RGB', (W, H), '#FFFFFF')
    d = ImageDraw.Draw(im)
    FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
    def font(n):
        return ImageFont.truetype(FONT, n)

    INK = '#17324D'
    MUTED = '#52677C'
    LINE = '#637B91'
    def text(x, y, s, size=32, fill=INK, anchor='mm'):
        d.text((x, y), s, font=font(size), fill=fill, anchor=anchor)

    def lines(cx, ys, ss, sizes=None, colors=None):
        for i, (y, s) in enumerate(zip(ys, ss)):
            text(cx, y, s, (sizes or [36]*len(ss))[i],
                 (colors or [INK]*len(ss))[i])

    def label(x, y, ss, size=29):
        ss = ss.split('\n')
        widths = [d.textbbox((0, 0), s, font=font(size))[2] for s in ss]
        height = len(ss) * (size + 10)
        d.rounded_rectangle((x-max(widths)/2-12, y-height/2-6,
                             x+max(widths)/2+12, y+height/2+6),
                            radius=8, fill='white')
        for i, s in enumerate(ss):
            text(x, y+(i-(len(ss)-1)/2)*(size+10), s, size, MUTED)

    def arrow(points, both=False):
        d.line(points, fill=LINE, width=4)
        def head(a, b):
            dx, dy = b[0]-a[0], b[1]-a[1]
            length = math.hypot(dx, dy)
            ux, uy = dx/length, dy/length
            p = (b[0]-19*ux, b[1]-19*uy)
            d.polygon([b, (p[0]+8*uy, p[1]-8*ux),
                       (p[0]-8*uy, p[1]+8*ux)], fill=LINE)
        head(points[-2], points[-1])
        if both:
            head(points[1], points[0])

    # Layer bands are backgrounds, not system components.
    for y1, y2, name, bg in [
        (45, 410, '交互', '#F4F7FD'),
        (490, 1370, '应用服务', '#F4F9F9'),
        (1435, 1825, '执行与适配', '#F8F6FC'),
        (1880, 2270, '存储', '#FAF8F2'),
    ]:
        d.rounded_rectangle((48, y1, 2952, y2), radius=24, fill=bg)
        text(86, y1+44, name, 27, MUTED, 'lm')

    # Interactive components: identical blue rounded rectangles.
    for cx, name in [
        (1050, 'Agent'),
        (1950, '用户前端'),
    ]:
        d.rounded_rectangle((cx-280, 115, cx+280, 325), radius=38,
                            fill='#E0ECFF', outline='#507DB6', width=3)
        text(cx, 220, name, 46)

    # Application services: identical teal rectangles.
    for cx, name in [
        (600, '统一查询层'),
        (2400, '连接器层'),
    ]:
        d.rectangle((cx-285, 830, cx+285, 1100), fill='#DDF2EE',
                    outline='#368B7E', width=3)
        text(cx, 965, name, 44)

    # Data concepts are modeled inside the model-management component.
    d.rectangle((1075, 625, 1925, 1315), fill='#DDF2EE',
                outline='#368B7E', width=3)
    text(1500, 676, '模型管理层', 44)

    # Peer data categories use identical document shapes and colors.
    for y, title in [
        (725, '模型元数据'),
        (910, '运行时模型'),
        (1095, '观测数据'),
    ]:
        d.polygon([(1200, y), (1760, y), (1800, y+40), (1800, y+145),
                   (1200, y+145)], fill='#EFE6FA', outline='#8C6EB1', width=3)
        d.line([(1760, y), (1760, y+40), (1800, y+40)],
               fill='#8C6EB1', width=3)
        text(1500, y+72, title, 33)

    # One aggregated infrastructure node.
    d.polygon([(339, 1510), (2661, 1510), (2685, 1534), (2685, 1766),
               (2661, 1790), (339, 1790), (315, 1766), (315, 1534)],
              fill='#EDE5FA', outline='#8C6EB1', width=3)
    text(1500, 1650, '执行引擎与存储适配', 44)

    # Storage media: four identical gold cylinders.
    for cx, name in [
        (600, 'PostgreSQL'),
        (1200, 'Neo4j'),
        (1800, 'Elasticsearch'),
        (2400, 'Prometheus'),
    ]:
        x1, x2, y1, y2, e = cx-242, cx+242, 1985, 2220, 54
        d.ellipse((x1, y2-e, x2, y2), fill='#FAEAC3', outline='#B58A35', width=3)
        d.rectangle((x1, y1+e/2, x2, y2-e/2), fill='#FAEAC3')
        d.line((x1, y1+e/2, x1, y2-e/2), fill='#B58A35', width=3)
        d.line((x2, y1+e/2, x2, y2-e/2), fill='#B58A35', width=3)
        d.ellipse((x1, y1, x2, y1+e), fill='#FFF3D7', outline='#B58A35', width=3)
        text(cx, 2116, name, 36)

    # Every relation has a concise label. Orthogonal segments never cross.
    arrow([(1330, 220), (1670, 220)], both=True)
    label(1500, 220, '提问\n调查结果')
    arrow([(850, 325), (850, 380), (600, 380), (600, 830)], both=True)
    label(600, 462, '对象、拓扑、证据')
    arrow([(1750, 325), (1750, 452), (825, 452), (825, 830)], both=True)
    label(1250, 452, '对象、拓扑、证据')
    arrow([(1950, 325), (1950, 540), (1500, 540), (1500, 625)], both=True)
    label(1710, 540, '定义维护、人工登记')
    arrow([(2115, 965), (1925, 965)])
    label(2020, 907, '发现、更新\n存在确认', 25)

    arrow([(600, 1100), (600, 1510)], both=True)
    label(600, 1413, '绑定计划、结果\n元数据读取')
    arrow([(1500, 1315), (1500, 1510)], both=True)
    label(1500, 1413, '受控读写\n同步提交')
    arrow([(2400, 1100), (2400, 1510)])
    label(2400, 1413, '观测接入\nHTTP JSON')

    for cx, s in [
        (600, 'SQL\n模型、观测'),
        (1200, 'Cypher\n图读写'),
        (1800, 'DSL 查询\n观测写入'),
        (2400, 'PromQL 查询\n指标写入'),
    ]:
        arrow([(cx, 1790), (cx, 1985)], both=True)
        label(cx, 1890, s)

    text(1500, 2330, 'SemModel-AgentFDS 总体架构图', 35)
    im.save(OUT / 'semmodel-agentfds-architecture.png', dpi=(180, 180))
    print(OUT / 'semmodel-agentfds-architecture.png')


if __name__ == "__main__":
    main()
