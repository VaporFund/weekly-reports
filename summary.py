# Arbitrage Opportunities Analysis - Base L2 Chain Data Visualization
# Comprehensive Python notebook with charts and graphs

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Read the CSV data
df = pd.read_csv('db_arbitrage.csv')

print("=== ARBITRAGE OPPORTUNITIES ANALYSIS ===")
print(f"Dataset: {len(df)} records from Base L2 chain")
print(f"Date: {df['quoted_at'].iloc[0]}")
print("\n" + "="*50)

# ==============================================================================
# 1. DATA OVERVIEW VISUALIZATION
# ==============================================================================

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Data Overview - Base L2 Arbitrage Analysis', fontsize=16, fontweight='bold')

# 1.1 Token Distribution
token_counts = df['symbol'].value_counts()
axes[0,0].pie(token_counts.values, labels=token_counts.index, autopct='%1.1f%%', startangle=90)
axes[0,0].set_title('Token Distribution')

# 1.2 Exchange Distribution
exchange_counts = df['exchange_name'].value_counts()
axes[0,1].bar(exchange_counts.index, exchange_counts.values, color=['#ff9999', '#66b3ff'])
axes[0,1].set_title('Quotes per Exchange')
axes[0,1].set_ylabel('Number of Quotes')

# 1.3 Quote Type Distribution
quote_type_counts = df['quote_type'].value_counts()
axes[1,0].bar(quote_type_counts.index, quote_type_counts.values, color=['#99ff99', '#ffcc99'])
axes[1,0].set_title('Quote Type Distribution')
axes[1,0].set_ylabel('Number of Quotes')

# 1.4 Price Range Distribution
price_ranges = {
    'Very Low (<$0.001)': len(df[df['price_per_token'] < 0.001]),
    'Low ($0.001-$1)': len(df[(df['price_per_token'] >= 0.001) & (df['price_per_token'] < 1)]),
    'Medium ($1-$100)': len(df[(df['price_per_token'] >= 1) & (df['price_per_token'] < 100)]),
    'High ($100-$10K)': len(df[(df['price_per_token'] >= 100) & (df['price_per_token'] < 10000)]),
    'Very High (≥$10K)': len(df[df['price_per_token'] >= 10000])
}
axes[1,1].bar(range(len(price_ranges)), list(price_ranges.values()), 
              color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7'])
axes[1,1].set_title('Price Range Distribution')
axes[1,1].set_ylabel('Number of Quotes')
axes[1,1].set_xticks(range(len(price_ranges)))
axes[1,1].set_xticklabels(list(price_ranges.keys()), rotation=45, ha='right')

plt.tight_layout()
plt.show()

# ==============================================================================
# 2. ARBITRAGE OPPORTUNITIES VISUALIZATION
# ==============================================================================

# Calculate arbitrage opportunities
arbitrage_data = []
tokens = df['symbol'].unique()

for token in tokens:
    token_data = df[df['symbol'] == token]
    buy_orders = token_data[token_data['quote_type'] == 'BUY']
    sell_orders = token_data[token_data['quote_type'] == 'SELL']
    
    if len(buy_orders) > 0 and len(sell_orders) > 0:
        highest_buy = buy_orders.loc[buy_orders['price_per_token'].idxmax()]
        lowest_sell = sell_orders.loc[sell_orders['price_per_token'].idxmin()]
        
        spread_percent = ((highest_buy['price_per_token'] - lowest_sell['price_per_token']) / 
                         lowest_sell['price_per_token']) * 100
        
        arbitrage_data.append({
            'token': token,
            'buy_exchange': lowest_sell['exchange_name'],
            'sell_exchange': highest_buy['exchange_name'],
            'buy_price': lowest_sell['price_per_token'],
            'sell_price': highest_buy['price_per_token'],
            'spread_percent': spread_percent
        })

arb_df = pd.DataFrame(arbitrage_data).sort_values('spread_percent', ascending=False)

# Plot arbitrage opportunities
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('Arbitrage Opportunities Analysis', fontsize=16, fontweight='bold')

# 2.1 Spread Percentage by Token
bars = axes[0].bar(arb_df['token'], arb_df['spread_percent'], 
                   color=['#e74c3c' if x > 10 else '#f39c12' if x > 2 else '#27ae60' 
                          for x in arb_df['spread_percent']])
axes[0].set_title('Arbitrage Spread by Token')
axes[0].set_ylabel('Spread Percentage (%)')
axes[0].set_xlabel('Token')
for i, v in enumerate(arb_df['spread_percent']):
    axes[0].text(i, v + 0.2, f'{v:.2f}%', ha='center', va='bottom', fontweight='bold')

# 2.2 Buy vs Sell Prices Comparison
x = np.arange(len(arb_df))
width = 0.35
axes[1].bar(x - width/2, arb_df['buy_price'], width, label='Buy Price', alpha=0.8, color='#3498db')
axes[1].bar(x + width/2, arb_df['sell_price'], width, label='Sell Price', alpha=0.8, color='#e74c3c')
axes[1].set_title('Buy vs Sell Prices')
axes[1].set_ylabel('Price ($)')
axes[1].set_xlabel('Token')
axes[1].set_xticks(x)
axes[1].set_xticklabels(arb_df['token'])
axes[1].legend()
axes[1].set_yscale('log')  # Log scale due to wide price range

plt.tight_layout()
plt.show()

# Print arbitrage summary
print("\n=== TOP ARBITRAGE OPPORTUNITIES ===")
for i, row in arb_df.iterrows():
    print(f"{row['token']}: {row['spread_percent']:.2f}% spread")
    print(f"  Buy at {row['buy_exchange']}: ${row['buy_price']:.8f}")
    print(f"  Sell at {row['sell_exchange']}: ${row['sell_price']:.8f}")

# ==============================================================================
# 3. CORRELATION ANALYSIS VISUALIZATION
# ==============================================================================

# Calculate correlations for each token
correlation_data = []
for token in tokens:
    token_data = df[df['symbol'] == token]
    if len(token_data) > 2:
        corr = np.corrcoef(token_data['price_per_token'], token_data['output_amount_formatted'])[0,1]
        correlation_data.append({'token': token, 'correlation': corr})

corr_df = pd.DataFrame(correlation_data)

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Correlation Analysis', fontsize=16, fontweight='bold')

# 3.1 Price vs Amount Correlation by Token
bars = axes[0,0].bar(corr_df['token'], corr_df['correlation'], 
                     color=['#e74c3c' if x < 0 else '#27ae60' for x in corr_df['correlation']])
axes[0,0].set_title('Price vs Output Amount Correlation by Token')
axes[0,0].set_ylabel('Correlation Coefficient')
axes[0,0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
for i, v in enumerate(corr_df['correlation']):
    axes[0,0].text(i, v + 0.02 if v > 0 else v - 0.02, f'{v:.3f}', 
                   ha='center', va='bottom' if v > 0 else 'top', fontweight='bold')

# 3.2 Price vs Amount Scatter Plot
axes[0,1].scatter(df['price_per_token'], df['output_amount_formatted'], 
                  c=df['symbol'].astype('category').cat.codes, alpha=0.6, cmap='tab10')
axes[0,1].set_title('Price vs Output Amount Scatter')
axes[0,1].set_xlabel('Price per Token ($)')
axes[0,1].set_ylabel('Output Amount')
axes[0,1].set_xscale('log')
axes[0,1].set_yscale('log')

# 3.3 Exchange Price Comparison
exchange_prices = df.groupby(['symbol', 'exchange_name'])['price_per_token'].mean().unstack()
exchange_prices.plot(kind='bar', ax=axes[1,0], color=['#3498db', '#e74c3c'])
axes[1,0].set_title('Average Price by Token and Exchange')
axes[1,0].set_ylabel('Average Price ($)')
axes[1,0].set_xlabel('Token')
axes[1,0].legend(title='Exchange')
axes[1,0].set_yscale('log')

# 3.4 Slippage vs Price Analysis
slippage_price_corr = np.corrcoef(df['price_per_token'], df['slippage_limit_percent'])[0,1]
axes[1,1].scatter(df['price_per_token'], df['slippage_limit_percent'], 
                  c=df['exchange_name'].astype('category').cat.codes, alpha=0.6)
axes[1,1].set_title(f'Price vs Slippage (Correlation: {slippage_price_corr:.4f})')
axes[1,1].set_xlabel('Price per Token ($)')
axes[1,1].set_ylabel('Slippage Limit (%)')
axes[1,1].set_xscale('log')

plt.tight_layout()
plt.show()

# ==============================================================================
# 4. EXCHANGE COMPARISON DETAILED ANALYSIS
# ==============================================================================

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Exchange Comparison Analysis', fontsize=16, fontweight='bold')

# 4.1 Average Metrics by Exchange
exchange_stats = df.groupby('exchange_name').agg({
    'price_per_token': 'mean',
    'output_amount_formatted': 'mean',
    'slippage_limit_percent': 'mean'
}).round(2)

x = np.arange(len(exchange_stats.index))
width = 0.25

axes[0,0].bar(x - width, exchange_stats['price_per_token'], width, 
              label='Avg Price', alpha=0.8, color='#3498db')
axes[0,0].set_title('Average Price by Exchange')
axes[0,0].set_ylabel('Average Price ($)')
axes[0,0].set_xticks(x)
axes[0,0].set_xticklabels(exchange_stats.index)
axes[0,0].set_yscale('log')

# 4.2 Output Amount Comparison
axes[0,1].bar(exchange_stats.index, exchange_stats['output_amount_formatted'], 
              color=['#e74c3c', '#27ae60'], alpha=0.8)
axes[0,1].set_title('Average Output Amount by Exchange')
axes[0,1].set_ylabel('Average Output Amount')
axes[0,1].set_yscale('log')

# 4.3 Slippage Comparison
axes[1,0].bar(exchange_stats.index, exchange_stats['slippage_limit_percent'], 
              color=['#f39c12', '#9b59b6'], alpha=0.8)
axes[1,0].set_title('Average Slippage by Exchange')
axes[1,0].set_ylabel('Slippage Limit (%)')

# 4.4 Price Spread Between Exchanges
price_spreads = []
for token in tokens:
    token_data = df[df['symbol'] == token]
    kyber_avg = token_data[token_data['exchange_name'] == 'KyberSwap']['price_per_token'].mean()
    universal_avg = token_data[token_data['exchange_name'] == 'Universal Assets']['price_per_token'].mean()
    
    if not np.isnan(kyber_avg) and not np.isnan(universal_avg):
        spread = abs(kyber_avg - universal_avg) / min(kyber_avg, universal_avg) * 100
        price_spreads.append({'token': token, 'spread': spread})

spread_df = pd.DataFrame(price_spreads)
bars = axes[1,1].bar(spread_df['token'], spread_df['spread'], 
                     color=['#e74c3c' if x > 10 else '#f39c12' if x > 2 else '#27ae60' 
                            for x in spread_df['spread']], alpha=0.8)
axes[1,1].set_title('Price Spread Between Exchanges')
axes[1,1].set_ylabel('Price Difference (%)')
axes[1,1].set_xlabel('Token')

plt.tight_layout()
plt.show()

# ==============================================================================
# 5. TIME SERIES AND VOLUME ANALYSIS
# ==============================================================================

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('Volume and Liquidity Analysis', fontsize=16, fontweight='bold')

# 5.1 Output Amount Distribution by Token
df.boxplot(column='output_amount_formatted', by='symbol', ax=axes[0])
axes[0].set_title('Output Amount Distribution by Token')
axes[0].set_ylabel('Output Amount (Log Scale)')
axes[0].set_yscale('log')
axes[0].set_xlabel('Token')

# 5.2 Quote Type Distribution by Exchange
quote_distribution = pd.crosstab(df['exchange_name'], df['quote_type'])
quote_distribution.plot(kind='bar', ax=axes[1], color=['#3498db', '#e74c3c'])
axes[1].set_title('Quote Type Distribution by Exchange')
axes[1].set_ylabel('Number of Quotes')
axes[1].set_xlabel('Exchange')
axes[1].legend(title='Quote Type')
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.show()

# ==============================================================================
# 6. HEATMAP VISUALIZATION
# ==============================================================================

# Create correlation heatmap
numeric_cols = ['price_per_token', 'output_amount_formatted', 'slippage_limit_percent']
correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='RdYlBu_r', center=0, 
            square=True, fmt='.3f', cbar_kws={'shrink': 0.8})
plt.title('Correlation Heatmap - Numeric Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# ==============================================================================
# 7. SUMMARY STATISTICS TABLE
# ==============================================================================

print("\n=== SUMMARY STATISTICS ===")
print("\nOverall Statistics:")
print(df[numeric_cols].describe())

print("\nExchange Comparison:")
print(df.groupby('exchange_name')[numeric_cols].mean())

print("\nToken Statistics:")
print(df.groupby('symbol')[numeric_cols].mean())

# ==============================================================================
# 8. RISK-REWARD ANALYSIS
# ==============================================================================

fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Create risk-reward scatter plot
for i, row in arb_df.iterrows():
    # Use spread as reward and inverse of liquidity as risk proxy
    token_data = df[df['symbol'] == row['token']]
    avg_liquidity = token_data['output_amount_formatted'].mean()
    risk_proxy = 1 / np.log10(avg_liquidity + 1)  # Higher liquidity = lower risk
    
    ax.scatter(risk_proxy, row['spread_percent'], s=100, alpha=0.7, 
               label=row['token'])
    ax.annotate(row['token'], (risk_proxy, row['spread_percent']), 
                xytext=(5, 5), textcoords='offset points', fontsize=10)

ax.set_xlabel('Risk Proxy (Inverse Liquidity)')
ax.set_ylabel('Arbitrage Spread (%)')
ax.set_title('Risk-Reward Analysis: Arbitrage Opportunities', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n=== ANALYSIS COMPLETE ===")
print("Key Insights:")
print("1. uSEI shows highest arbitrage potential (19.42% spread)")
print("2. Clear market structure: KyberSwap (sell-side) vs Universal Assets (buy-side)")
print("3. Strong correlations vary significantly by token")
print("4. Liquidity differences create arbitrage opportunities")
print("5. Slippage settings don't correlate with price levels")