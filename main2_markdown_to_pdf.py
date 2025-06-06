from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

pdf = MarkdownPdf(toc_level=2, optimize=True)

weekly_analysis_no_2_markdown = """
## Weekly Analysis #2
Universal Assets Arbitrage Strategy: Cross-DEX Opportunities
<img src="img/1-click-arb-agent.png" alt="1-click-arb-agent" width="50%">

## The Cross-DEX Arbitrage Opportunity in 1-click

### Background

VaporFund had been running crypto business for two years but always felt one step behind the market. After months of research, she discovered a pattern in the pricing of Universal's tokenized assets across different DEXs.

Arbi wallet:

[https://basescan.org/address/0xbd392784638d10a6cef2193e32edbd658739f4af#tokentxns](https://basescan.org/address/0xbd392784638d10a6cef2193e32edbd658739f4af#tokentxns)

### The Discovery

On a quiet Friday afternoon in May 2025, Arbi noticed something peculiar. While monitoring prices of uSOL across multiple exchanges, he spotted a consistent price discrepancy:

- On Odos (Base network): uSOL trading at $165.23
- On Universal Assets DEX: uSOL trading at $163.57
- Buy tx: [https://basescan.org/tx/0xc596528089f668befde8a1e08567117c6cdb049e2ec04da2173d68580d629a0f](https://basescan.org/tx/0xc596528089f668befde8a1e08567117c6cdb049e2ec04da2173d68580d629a0f)
- Sell tx: [https://basescan.org/tx/0x5e7e54fa8fc4d78f8da2b8114d5ebdf28516252847424f5e90ac7ecf23b570cb](https://basescan.org/tx/0x5e7e54fa8fc4d78f8da2b8114d5ebdf28516252847424f5e90ac7ecf23b570cb)
- Result: +$1.5 (Profit)

The differences might seem minimal to casual traders, but to Arbi, ther represented a clear arbitrage opportunity. With uSOL's high trading volume and relatively deep liquidity, these small percentage differences could translate to meaningful profits when executed at scale.

### Setting Up the Strategy

Arbi's approach was methodical:

1. **Infrastructure Setup:** He configured a 1-click arbitrage application at [https://arbi.VaporFund.com/](https://arbi.VaporFund.com/)
1. **Auto-check setting:** Arbi use this setting for checking arbitrage opportunities
    * Input amount: 1000 USDC
    * Minimum profit threshold: 1.0%
    * Slippage Tolerance: 0.1%
1. **Monitoring System:** He developed a simple bot that monitored price discrepancies between the two exchanges, triggering alerts when spreads exceeded 1.0%.
1. **Gas Optimization:** Arbi created a gas strategy that adjusted based on network congestion, ensuring transactions would go through during profitable windows without overpaying.

### The First Trade

The opportunity came faster than expected. On Monday morning, Arbi's alert system pinged—uSEI was trading 1.2% lower on Universal Assets DEX compared to Kyberswap.

### Trade Execution:
<img src="img/trade_execution.png">

For her $300 position, the profit after gas and slippage came to approximately $1.23 return in less than 10 minutes.

### The uSUI Opportunity but Lost
* On Kyberswap (Base network): uSOL trading at $165.23
* On Universal Assets DEX: uSOL trading at $163.57
* Buy tx: [https://basescan.org/tx/0xcd307d959e95ceacc0cc23797f7b0f66c19223a619b193a0649f7f21963beb20](https://basescan.org/tx/0xcd307d959e95ceacc0cc23797f7b0f66c19223a619b193a0649f7f21963beb20)
* Sell tx: [https://basescan.org/tx/0x9ab0e11876e7163af22562e4603361255db96957e4c2cf90554fcd4a574d70ff](https://basescan.org/tx/0x9ab0e11876e7163af22562e4603361255db96957e4c2cf90554fcd4a574d70ff)
* Result: -$0.64 (Lost) because the price changes during the trade execution.

## Risk Management

Arbi recognized the risks in her strategy:

1. **Slippage Risk:** There was always a small slippage on Kyberswap when swapping assets between multiple DEXs since Kyberswap is an aggregator.
1. **Divergence Risk:** If the underlying asset (e.g., native SOL) experienced a sudden price movement, the arbitrage window could close before execution completed.
1. **Liquidity Risk:** Larger positions could face slippage, especially on newly launched assets.

To mitigate these risks, Arbi implemented position sizing rules based on available liquidity which capture significant data from [https://wallet.VaporFund.com/liquidity-discovery](https://wallet.VaporFund.com/liquidity-discovery) and maintained reserve capital on each network to avoid unnecessary cross-chain transfers.

### The Technology Edge

Arbi's competitive advantage came from optimization:

1. Creating direct transaction routing that bypassed aggregators for lower gas fees
1. Implementing a prioritized execution system that could simultaneously prepare transactions on multiple networks
1. Setting up faster swap execution for her larger trades to avoid being frontrun

### Key Takeaways from Arbi's Experience
1. **Market Inefficiencies:** Despite the mature state of DeFi in 2025, cross-DEX and cross-chain inefficiencies still existed, particularly for newer tokenized assets.
1. **Institutional Advantage:** Universal's deep connection with Coinbase provided exceptional price stability for their wrapped assets, making arbitrage less risky than with algorithmic stablecoins or synthetic assets.
1. **Infrastructure Matters:** Low-latency connections and optimized execution were as important as identifying the opportunities themselves.
1. **Liquidity Assessment:** The most profitable trades weren't always on the largest assets—sometimes newer assets with growing but imbalanced liquidity offered better opportunities.
1. **Expanding Ecosystem:** As Universal continually added new wrapped assets, each launch created temporary pricing inefficiencies that could be captured by prepared traders.

While the specific numbers and profits detailed in ther narrative are illustrative, they represent the types of opportunities that emerge in cross-chain, multi-DEX environments—especially around institutional-grade wrapped assets like those provided by Universal.

"""
pdf.add_section(Section(weekly_analysis_no_2_markdown, toc=False))

pdf.meta["title"] = "Weekly Analysis No.2"
pdf.meta["author"] = "VaporFund"

pdf.save("weekly_analysis_no2.pdf")
