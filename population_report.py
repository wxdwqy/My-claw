# -*- coding: utf-8 -*-
"""
人口结构变化对产业影响分析报告 - PDF生成脚本
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 注册中文字体
try:
    pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
    pdfmetrics.registerFont(TTFont('Microsoft YaHei', 'C:/Windows/Fonts/msyh.ttc'))
    CHINESE_FONT = 'SimHei'
    CHINESE_FONT_BODY = 'SimSun'
except:
    CHINESE_FONT = 'Helvetica'
    CHINESE_FONT_BODY = 'Helvetica'

# 颜色定义
COLOR_DARK = HexColor('#1a1a2e')
COLOR_RED = HexColor('#c0392b')
COLOR_GREEN = HexColor('#27ae60')
COLOR_BLUE = HexColor('#2980b9')
COLOR_ORANGE = HexColor('#e67e22')
COLOR_PURPLE = HexColor('#8e44ad')
COLOR_GRAY = HexColor('#7f8c8d')
COLOR_LIGHT_RED = HexColor('#fdecea')
COLOR_LIGHT_GREEN = HexColor('#eafaf1')
COLOR_LIGHT_BLUE = HexColor('#ebf5fb')
COLOR_LIGHT_ORANGE = HexColor('#fef9e7')
COLOR_LIGHT_PURPLE = HexColor('#f5eef8')
COLOR_BG = HexColor('#f5f6fa')
COLOR_BORDER = HexColor('#dcdde1')

W = A4[0]
H = A4[1]

def create_styles():
    styles = getSampleStyleSheet()
    base_font = CHINESE_FONT
    body_font = CHINESE_FONT_BODY

    styles.add(ParagraphStyle(
        'ReportTitle',
        fontName=base_font,
        fontSize=22,
        leading=30,
        alignment=TA_CENTER,
        textColor=white,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'ReportSubtitle',
        fontName=base_font,
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=HexColor('#bdc3c7'),
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        'ReportMeta',
        fontName=body_font,
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=HexColor('#95a5a6'),
        spaceAfter=20,
    ))
    styles.add(ParagraphStyle(
        'SectionHeader',
        fontName=base_font,
        fontSize=15,
        leading=20,
        textColor=white,
        spaceBefore=8,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        'SubHeader',
        fontName=base_font,
        fontSize=12,
        leading=16,
        textColor=COLOR_DARK,
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'SubHeaderRed',
        fontName=base_font,
        fontSize=12,
        leading=16,
        textColor=COLOR_RED,
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'SubHeaderGreen',
        fontName=base_font,
        fontSize=12,
        leading=16,
        textColor=COLOR_GREEN,
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'SubHeaderBlue',
        fontName=base_font,
        fontSize=12,
        leading=16,
        textColor=COLOR_BLUE,
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'SubHeaderOrange',
        fontName=base_font,
        fontSize=12,
        leading=16,
        textColor=COLOR_ORANGE,
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'SubHeaderPurple',
        fontName=base_font,
        fontSize=12,
        leading=16,
        textColor=COLOR_PURPLE,
        spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        'BodyText2',
        fontName=body_font,
        fontSize=9.5,
        leading=14,
        textColor=HexColor('#2c3e50'),
        spaceBefore=2,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        'BulletText',
        fontName=body_font,
        fontSize=9.5,
        leading=14,
        textColor=HexColor('#2c3e50'),
        spaceBefore=1,
        spaceAfter=1,
        leftIndent=12,
        bulletIndent=0,
    ))
    styles.add(ParagraphStyle(
        'TableHeader',
        fontName=base_font,
        fontSize=9,
        leading=12,
        textColor=white,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        fontName=body_font,
        fontSize=8.5,
        leading=12,
        textColor=HexColor('#2c3e50'),
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        fontName=base_font,
        fontSize=8.5,
        leading=12,
        textColor=HexColor('#1a1a2e'),
    ))
    styles.add(ParagraphStyle(
        'Footnote',
        fontName=body_font,
        fontSize=8,
        leading=11,
        textColor=COLOR_GRAY,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'SummaryBox',
        fontName=body_font,
        fontSize=10,
        leading=15,
        textColor=HexColor('#2c3e50'),
        spaceBefore=4,
        spaceAfter=4,
    ))
    return styles

def section_banner(title, color, styles):
    """创建彩色标题横幅"""
    data = [[Paragraph(title, styles['SectionHeader'])]]
    t = Table(data, colWidths=[W - 4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    return t

def stock_table(headers, rows, bg_color, styles):
    """创建股票表格"""
    col_widths = [3.2*cm, 2.2*cm, 6.8*cm, 4.3*cm]
    header_row = [Paragraph(h, styles['TableHeader']) for h in headers]

    table_data = [header_row]
    for row in rows:
        table_data.append([
            Paragraph(row[0], styles['TableCellBold']),
            Paragraph(row[1], styles['TableCell']),
            Paragraph(row[2], styles['TableCell']),
            Paragraph(row[3], styles['TableCell']),
        ])

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bg_color),
        ('BACKGROUND', (0, 1), (-1, -1), white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, bg_color),
    ]))
    return t

def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
    )

    styles = create_styles()
    story = []

    # ===== 封面 ===== #
    # 顶部色带
    cover_top = Table([['']], colWidths=[W - 4*cm], rowHeights=[0.8*cm])
    cover_top.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_DARK),
    ]))
    story.append(cover_top)

    story.append(Spacer(1, 0.8*cm))

    # 主标题
    story.append(Paragraph('人口结构变化', styles['ReportTitle']))
    story.append(Paragraph('对产业格局的影响分析报告', styles['ReportTitle']))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('——出生率持续下降背景下的投资机遇与风险', styles['ReportSubtitle']))
    story.append(Spacer(1, 0.6*cm))

    # 分隔线
    story.append(HRFlowable(width='80%', thickness=1, color=HexColor('#4a4a6a'), spaceAfter=0.4*cm))

    # 元信息
    story.append(Paragraph('报告日期：2026年4月5日（清明节）', styles['ReportMeta']))
    story.append(Paragraph('报告分析：云爪 | 数据来源：公开市场信息综合整理', styles['ReportMeta']))
    story.append(Spacer(1, 0.8*cm))

    # 核心数据卡片
    core_data = [
        ['2025年出生人口', '2025年死亡人口', '人口自然增长率', '60岁以上人口'],
        ['约792万人', '约1131万人', '-2.4‰', '突破3亿'],
        ['同比继续下降', '持续增长', '连续多年负增长', '占总人口21%+'],
    ]
    cd_table = Table(core_data, colWidths=[(W-4*cm)/4]*4)
    cd_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#34495e')),
        ('BACKGROUND', (0, 2), (-1, 2), HexColor('#3d4f5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('TEXTCOLOR', (0, 1), (-1, 1), HexColor('#f39c12')),
        ('TEXTCOLOR', (0, 2), (-1, 2), HexColor('#bdc3c7')),
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, 1), 13),
        ('FONTSIZE', (0, 2), (-1, 2), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#1a1a2e')),
    ]))
    story.append(cd_table)

    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(
        '数据来源：国家统计局2025年人口数据公报 | 注：以上数据为根据公开信息整理的参考数据',
        styles['Footnote']
    ))

    story.append(PageBreak())

    # ===== 正文 ===== #

    # ---- 第一部分：总体框架 ---- #
    story.append(section_banner('第一部分：分析框架与核心逻辑', COLOR_DARK, styles))
    story.append(Spacer(1, 0.4*cm))

    framework_text = [
        '中国人口结构正在经历历史性转折。2025年数据显示：出生人口约792万，死亡人口约1131万，',
        '人口自然增长率连续多年为负。根据人口学规律，未来十年这一趋势几乎不可逆转。',
        '',
        '这一人口结构变化将从三个维度重塑产业格局：',
        '',
        '  1. 需求萎缩：直接面向婴幼儿的教育、消费需求断崖式减少',
        '  2. 需求爆发：老龄人口激增带动养老、医疗、健康需求井喷式增长',
        '  3. 需求迁移：从"生"到"老"的消费重心转移，催生全新赛道',
        '',
        '本报告从"受损产业"、"受益产业"、"新兴赛道"三个维度展开分析，并附加A股',
        '相关上市公司参考，帮助投资者理解人口变局下的产业走向。',
    ]
    for line in framework_text:
        story.append(Paragraph(line, styles['BodyText2']))
    story.append(Spacer(1, 0.3*cm))

    story.append(PageBreak())

    # ---- 第二部分：受损产业 ---- #
    story.append(section_banner('第二部分：受损产业分析（谨慎规避）', COLOR_RED, styles))
    story.append(Spacer(1, 0.4*cm))

    # 2.1 教育产业
    story.append(Paragraph('2.1 教育产业 — 受冲击最早、最直接', styles['SubHeaderRed']))
    story.append(Paragraph(
        '出生人口减少意味着潜在生源持续萎缩。教育产业链从学前到高考全线承压，',
        styles['BodyText2']))
    story.append(Paragraph(
        '且随着时间推移，影响将从学前逐步传导至K12、高等教育。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    edu_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['中公教育', '002607.SZ', '公职考试培训', '考生总量减少，竞争加剧，需求萎缩直接传导至培训市场'],
        ['学大教育', '000526.SZ', 'K12一对一培训', 'K12阶段学生数量持续下滑，教培需求结构性减少'],
        ['凯文教育', '002659.SZ', '国际教育/K12', '出生率下降→生源减少→学校运营压力加大'],
        ['豆神教育', '300010.SZ', '语文教育/直播带货', '教育主业受双减+人口双重冲击，业务转型压力大'],
        ['行动教育', '605098.SH', '企业管理培训', '成人培训相对稳定，但高端客户群体扩张受限'],
    ]
    story.append(stock_table(edu_data[0], edu_data[1:], COLOR_RED, styles))
    story.append(Spacer(1, 0.4*cm))

    # 2.2 婴幼儿消费
    story.append(Paragraph('2.2 婴幼儿消费产业 — 消费人群持续萎缩', styles['SubHeaderRed']))
    story.append(Paragraph(
        '婴幼儿奶粉、服装、玩具、尿布等消费总量随出生人口下降而减少，龙头企业',
        styles['BodyText2']))
    story.append(Paragraph(
        '虽可通过高端化、出口对冲部分压力，但行业天花板整体下移已成定局。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    baby_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['贝因美', '002570.SZ', '婴幼儿配方奶粉', '国产奶粉龙头，出生率下降直接导致市场总量萎缩'],
        ['伊利股份', '600887.SH', '乳制品（含婴幼儿配方奶）', '婴幼儿配方奶业务占比受出生率影响，成人奶成新增长点'],
        ['西部牧业', '300106.SZ', '乳制品加工', '新疆区域乳企，婴幼儿奶源需求下滑影响营收结构'],
        ['孩子王', '301078.SZ', '母婴童用品零售', '门店覆盖母婴全品类，消费人群减少冲击营收'],
        ['安奈儿', '002875.SZ', '中高端童装', '童装龙头，消费者减少直接压缩市场空间'],
    ]
    story.append(stock_table(baby_data[0], baby_data[1:], HexColor('#a93226'), styles))
    story.append(Spacer(1, 0.4*cm))

    # 2.3 房地产
    story.append(Paragraph('2.3 房地产 — 三四线城市率先崩塌', styles['SubHeaderRed']))
    story.append(Paragraph(
        '人口净流出地区住房需求萎缩，而人口持续流入的核心城市相对抗压。',
        styles['BodyText2']))
    story.append(Paragraph(
        '长期看，"刚需减少+老龄化遗产释放"双重叠加，房价承压。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    house_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['华夏幸福', '600340.SH', '产业新城/房地产', '项目集中三四线，人口流出叠加需求萎缩，债务危机延续'],
        ['阳光城', '000671.SZ', '房地产开发', '高杠杆房企，人口减少叠加地产下行周期，偿债压力大'],
        ['蓝光发展', '600466.SH', '房地产开发', '已陷入债务困境，人口结构变化加剧去化难度'],
        ['绿地控股', '600606.SH', '地产/基建', '商办综合体受人口减少冲击，大基建对冲有限'],
        ['中南建设', '000961.SZ', '房地产开发', '布局三四线为主，受人口流失影响较大'],
    ]
    story.append(stock_table(house_data[0], house_data[1:], HexColor('#922b21'), styles))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        '注：万科A（000002.SZ）、保利发展（600048.SH）、招商蛇口（001979.SZ）等龙头央企/国企',
        styles['Footnote']))
    story.append(Paragraph(
        '相对抗压，因其主要布局核心城市，且具备资源整合能力，但行业整体β仍然向下。',
        styles['Footnote']))

    story.append(PageBreak())

    # ---- 第三部分：受益产业 ---- #
    story.append(section_banner('第三部分：受益产业分析（重点关注）', COLOR_GREEN, styles))
    story.append(Spacer(1, 0.4*cm))

    # 3.1 养老产业
    story.append(Paragraph('3.1 养老产业 — 最确定的长期成长赛道', styles['SubHeaderGreen']))
    story.append(Paragraph(
        '中国60岁以上人口已突破3亿，预计2035年超4亿。养老服务供给严重不足，政策',
        styles['BodyText2']))
    story.append(Paragraph(
        '全面支持银发经济，产业进入黄金发展期，市场规模超10万亿元。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    old_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['南京新百', '600682.SH', '养老服务/商业', '旗下安康通为国内最大养老服务运营商之一，直接受益老龄化'],
        ['珠江股份', '600684.SH', '养老社区运营', '转型养老产业，运营多个高端养老社区项目'],
        ['新华锦', '600735.SH', '养老地产/贸易', '爱丁堡系列养老公寓，高端养老服务布局清晰'],
        ['凤凰股份', '600716.SH', '养老社区建设', 'A股养老核心标的，长三角养老社区建设标杆'],
        ['双箭股份', '002381.SZ', '养老院运营/TPPE', '长三角养老社区布局领跑，医疗服务持续扩张'],
        ['中关村', '000931.SZ', '养老服务/医药', '华素制药+久久泰和养老，双主业布局老龄化需求'],
    ]
    story.append(stock_table(old_data[0], old_data[1:], COLOR_GREEN, styles))
    story.append(Spacer(1, 0.4*cm))

    # 3.2 医疗健康
    story.append(Paragraph('3.2 医疗健康产业 — 老龄化的刚性需求', styles['SubHeaderGreen']))
    story.append(Paragraph(
        '心脑血管疾病、肿瘤、骨科等老年高发疾病的诊疗需求持续扩大。医疗器械、',
        styles['BodyText2']))
    story.append(Paragraph(
        '创新药、慢病管理构成三大成长方向，叠加国产替代加速，龙头企业迎来黄金期。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    health_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['迈瑞医疗', '300760.SZ', '医疗器械龙头', '监护仪、呼吸机等ICU设备直接受益老龄化手术及危重病人增加'],
        ['乐心医疗', '300562.SZ', '慢病管理设备', '聚焦心脑血管慢病管理，远程健康监测需求爆发'],
        ['鱼跃医疗', '002223.SZ', '家用医疗器械', '制氧机、血压计、轮椅等老年家庭必备器械需求稳健'],
        ['心脉医疗', '688016.SH', '血管介入器械', '外周血管支架等高端介入器械，老年患者高发适应症'],
        ['三诺生物', '300298.SZ', '血糖监测', '糖尿病患者超1.4亿，血糖仪及试纸需求随老龄化扩大'],
    ]
    story.append(stock_table(health_data[0], health_data[1:], HexColor('#1e8449'), styles))
    story.append(Spacer(1, 0.4*cm))

    # 3.3 保险与财富管理
    story.append(Paragraph('3.3 保险与养老金融 — 老龄化催生理财刚需', styles['SubHeaderGreen']))
    story.append(Paragraph(
        '寿险、重疾险、年金险等与老年风险高度相关的产品持续增长。养老目标基金、',
        styles['BodyText2']))
    story.append(Paragraph(
        '个人养老金账户政策落地，保险+资产管理双轮驱动。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    insurance_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['中国平安', '601318.SH', '寿险/健康险/资产管理', '国内最大寿险公司，健康险+养老金融双轮驱动老龄化需求'],
        ['中国人寿', '601628.SH', '人寿保险', '寿险龙头，长期护理保险布局加速，直接受益老龄化'],
        ['友邦保险', '601628.SH（沪）', '高端寿险/健康险', '高端客户养老及健康保障需求，溢价能力强'],
        ['新华保险', '601336.SH', '人寿保险/养老社区', '养老社区+保险协同布局，契合老龄化需求'],
        ['中国太保', '601601.SH', '寿险/健康险/养老社区', '太保家园养老社区+保险产品协同发展'],
    ]
    story.append(stock_table(insurance_data[0], insurance_data[1:], HexColor('#196f3d'), styles))

    story.append(PageBreak())

    # ---- 第四部分：新兴赛道 ---- #
    story.append(section_banner('第四部分：新兴赛道分析（高潜力蓝海）', COLOR_BLUE, styles))
    story.append(Spacer(1, 0.4*cm))

    # 4.1 银发科技
    story.append(Paragraph('4.1 银发科技（AgeTech）— AI+老龄化的最大交汇点', styles['SubHeaderBlue']))
    story.append(Paragraph(
        '陪伴机器人、远程医疗、无障碍智能家居——技术进步与老龄化需求形成历史性交汇。',
        styles['BodyText2']))
    story.append(Paragraph(
        '工信部2025年已公布32个智能养老机器人试点项目，产业从概念走向落地。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    age_tech_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['科大讯飞', '002230.SZ', 'AI/语音智能', 'AI大模型+适老化智能家居，陪伴机器人语音交互核心供应商'],
        ['机器人概念股\n（行业汇总）', '多只', '工业/服务机器人', '老年陪护机器人、助行机器人、护理机器人等新物种涌现'],
        ['信隆健康', '002105.SZ', '康复辅具/AI影像', '轮椅、助行器等康复辅具龙头，AI医疗影像设备布局'],
        ['奥佳华', '002614.SZ', '按摩器械/健康家居', '高端按摩椅满足老年健康需求，智能家居入口价值'],
        ['延华智能', '002178.SZ', '智慧城市/智能建筑', '适老化智能楼宇改造，智慧社区养老解决方案'],
    ]
    story.append(stock_table(age_tech_data[0], age_tech_data[1:], COLOR_BLUE, styles))
    story.append(Spacer(1, 0.4*cm))

    # 4.2 辅助生殖
    story.append(Paragraph('4.2 辅助生殖 — 政策催化的刚需赛道', styles['SubHeaderBlue']))
    story.append(Paragraph(
        '不孕率上升+平均生育年龄推迟+政策支持（部分省市已纳入医保），辅助生殖',
        styles['BodyText2']))
    story.append(Paragraph(
        '市场年增速超15%，渗透率仍有巨大提升空间（国内vs发达国家差距明显）。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    art_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['长春高新', '000661.SZ', '生长激素/辅助生殖', '旗下金赛药业生殖产品线，辅助生殖领域核心布局'],
        ['通策医疗', '600763.SH', '口腔+辅助生殖', '昆明波恩生殖中心，试管婴儿技术国内领先'],
        ['丽珠集团', '000513.SZ', '生殖药物', '丽申宝（尿促卵泡素）等辅助生殖药物市占率领先'],
        ['麦迪科技', '603990.SH', '医疗IT+辅助生殖', '收购玛丽医院，辅助生殖服务领域持续扩张'],
        ['昌红科技', '300151.SZ', '辅助生殖耗材', '试管婴儿耗材（培养皿、移液管等）细分龙头'],
    ]
    story.append(stock_table(art_data[0], art_data[1:], HexColor('#1a6f9c'), styles))
    story.append(Spacer(1, 0.4*cm))

    # 4.3 死亡经济
    story.append(Paragraph('4.3 死亡经济（身后事服务）— 被忽视的蓝海', styles['SubHeaderBlue']))
    story.append(Paragraph(
        '死亡人口每年超1100万并持续增加，殡葬需求刚性。传统行业暴利但分散，',
        styles['BodyText2']))
    story.append(Paragraph(
        '数字化、绿色殡葬、数字永生等新概念正在重塑这个古老行业。',
        styles['BodyText2']))
    story.append(Spacer(1, 0.2*cm))

    death_data = [
        ['公司名称', '股票代码', '主营业务', '关联性说明'],
        ['福成股份', '600965.SH', '殡葬服务', 'A股殡葬服务稀缺标的，殡葬业务毛利率维持80%以上'],
        ['福寿园', '01448.HK（港股）', '高端陵园/数字殡葬', '中国殡葬行业龙头，探索元宇宙祭扫+数字遗产区块链存证'],
        ['永安林业', '000663.SZ', '林业/生态陵园', '生态陵园建设，绿色殡葬概念布局'],
        ['数字遗产概念\n（行业汇总）', '多家', '账号继承/数据保存', '微信、支付宝、 游戏账号等数字资产继承需求催生新服务'],
        ['AI"复活"服务\n（新兴探索）', '行业早期', 'AI数字人/记忆存储', '通过AI技术还原逝者音容笑貌，已有商业化案例（争议中成长）'],
    ]
    story.append(stock_table(death_data[0], death_data[1:], HexColor('#1f618d'), styles))

    story.append(PageBreak())

    # ---- 第五部分：总结 ---- #
    story.append(section_banner('第五部分：总结与投资逻辑', COLOR_ORANGE, styles))
    story.append(Spacer(1, 0.5*cm))

    # 总结表格
    summary_table_data = [
        ['产业类型', '代表公司（部分）', '核心逻辑', '确定性'],
        ['教育产业', '中公教育、学大教育', '生源减少+政策压制', '高'],
        ['婴幼儿消费', '贝因美、伊利股份', '消费人群持续萎缩', '高'],
        ['房地产（三四线）', '华夏幸福、阳光城', '需求萎缩叠加债务压力', '高'],
        ['养老产业', '南京新百、凤凰股份', '老龄人口持续增加+政策支持', '极高'],
        ['医疗健康', '迈瑞医疗、鱼跃医疗', '老年病高发+国产替代', '极高'],
        ['保险与财富管理', '中国平安、中国人寿', '养老金融产品需求爆发', '高'],
        ['银发科技', '科大讯飞、机器人概念股', 'AI技术×老龄化需求交汇', '中高'],
        ['辅助生殖', '长春高新、通策医疗', '政策支持+渗透率提升', '中高'],
        ['死亡经济', '福成股份、福寿园（港）', '死亡人口增加+消费升级', '中'],
    ]

    col_widths_sum = [3.5*cm, 5.5*cm, 5.5*cm, 2*cm]
    sum_table_data = [[Paragraph(c, styles['TableHeader']) for c in summary_table_data[0]]]
    for row in summary_table_data[1:]:
        sum_table_data.append([
            Paragraph(row[0], styles['TableCellBold']),
            Paragraph(row[1], styles['TableCell']),
            Paragraph(row[2], styles['TableCell']),
            Paragraph(row[3], styles['TableCell']),
        ])

    sum_t = Table(sum_table_data, colWidths=col_widths_sum, repeatRows=1)
    sum_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ORANGE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#fef9e7')]),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),
        ('FONTNAME', (3, 1), (3, -1), CHINESE_FONT),
    ]))
    story.append(sum_t)
    story.append(Spacer(1, 0.5*cm))

    # 核心结论
    story.append(Paragraph('核心结论', styles['SubHeaderOrange']))
    conclusions = [
        '1. 人口结构变化是未来10-20年最确定的宏观趋势，不可逆且正在加速。',
        '2. "老的越来越多"比"小的越来越少"更确定——养老、医疗、健康保险是最优先受益方向。',
        '3. 教育、婴幼儿消费的衰退已经发生，不必等待确认，现在就要规避。',
        '4. 银发科技（AgeTech）是目前最被低估的新赛道，AI+老龄化的交叉领域想象空间最大。',
        '5. 辅助生殖在政策催化下进入快速成长期，但注意短期估值压力。',
        '6. 死亡经济虽显沉重，却是真实存在的蓝海市场，数字化升级空间广阔。',
        '7. 以上上市公司仅作产业关联性参考，不构成投资建议，投资需审慎评估基本面。',
    ]
    for c in conclusions:
        story.append(Paragraph(c, styles['BulletText']))
    story.append(Spacer(1, 0.5*cm))

    story.append(HRFlowable(width='100%', thickness=0.5, color=COLOR_BORDER, spaceAfter=0.3*cm))
    story.append(Paragraph(
        '免责声明：本报告仅供信息参考，不构成任何投资建议。股票市场有风险，投资需谨慎。',
        styles['Footnote']))
    story.append(Paragraph(
        '报告生成工具：云爪 AI助手 | 数据来源：公开市场信息综合整理 | 截至2026年4月',
        styles['Footnote']))

    doc.build(story)
    print(f"PDF报告已生成: {output_path}")

if __name__ == '__main__':
    output_file = r'C:\Users\wxd\WorkBuddy\Claw\人口结构变化产业影响分析报告.pdf'
    build_pdf(output_file)
