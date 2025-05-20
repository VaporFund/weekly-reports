from fpdf import FPDF
from fpdf.enums import XPos, YPos

pdf = FPDF()
pdf.add_page()
pdf.set_font('helvetica', 'B', size=23)
pdf.cell(0, 15, "Liquidity Discovery Weekly Analysis #2", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('helvetica', '', size=16)
pdf.cell(0, 10, "Universal Assets Arbitrage Strategy: Cross-DEX Opportunities", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.image("img/1-click-arb-agent.png", x=10, y=None, w=100)
pdf.set_font('helvetica', 'B', size=17)
pdf.cell(0, 10, "The Cross-DEX Arbitrage Opportunity in 1-click", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('helvetica', 'B', size=13)
pdf.cell(0, 10, "Background", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font('helvetica', '', size=11)
pdf.multi_cell(0, 6, "Vaporfund had been running crypto business for two years but always felt one step behind the market. After months of research, she discovered a pattern in the pricing of Universal's tokenized assets across different DEXs.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output("hello_report.pdf")
