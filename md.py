"""Modified version to generate Markdown files with GitHub-hosted images"""
import logging
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg
import pandas as pd
from tqdm import tqdm
import os
from datetime import datetime

from download_to_csv import main_download_csv, get_distinct_tokens

logger = logging.getLogger(__name__)

# Set figure aesthetics for better visualization
plt.style.use('ggplot')

# Set higher DPI for sharper in-notebook display
plt.rcParams['figure.dpi'] = 100
folder = 'chart_images'
markdown_folder = 'reports'

# GitHub repository configuration
GITHUB_REPO_URL = "https://raw.githubusercontent.com/VaporFund/weekly-reports/main"
GITHUB_IMAGES_PATH = f"{GITHUB_REPO_URL}/{folder}"

def ensure_folders_exist():
    """Create necessary folders if they don't exist."""
    os.makedirs(folder, exist_ok=True)
    os.makedirs(markdown_folder, exist_ok=True)

def basic_charts(token: str, csv_source: str, basic_chart_figure: str) -> pd.DataFrame:
    """
    Basic Line Charts
    Let's create two separate line charts for the token amount and USDC return.
    """
    # Load the CSV data
    df = pd.read_csv(csv_source)

    # Display the first few rows to verify data loading
    print(f"Total rows: {len(df)}")

    # Data preprocessing
    # Convert timestamp to datetime
    df['quoted_at'] = pd.to_datetime(df['quoted_at'], format='ISO8601')

    # Convert ua_token_amount from string to float (it's in wei format with 18 decimals)
    df['output_amount'] = df['output_amount'].astype(float)

    # Convert to a more readable format (divide by 10^18 to get the actual token amount)
    df['output_amount_readable'] = df['output_amount'] / 1e18

    # Convert ua_token_amount from string to float (it's in wei format with 18 decimals)
    df['input_amount'] = df['input_amount'].astype(float)

    # Convert to a more readable format (divide by 10^18 to get the actual token amount)
    df['input_amount_readable'] = df['input_amount'] / 1e18

    # Sort by timestamp to ensure proper chronological order
    df = df.sort_values('quoted_at')

    # Basic Line Charts
    # Let's create two separate line charts for the token amount and USDC return.
    # Set up the figure with two subplots (one for each metric)
    plt.figure(figsize=(14, 10))

    # Plot 1: ua_token_amount over time
    plt.subplot(2, 1, 1)
    plt.plot(df['quoted_at'], df['output_amount_readable'], color='blue', linewidth=2)
    plt.title(f'{token} Token Amount Over Time', fontsize=16)
    plt.ylabel('Token Amount', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Format the x-axis to show nice time labels
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    # Plot 2: odos_usdc_return over time
    plt.subplot(2, 1, 2)
    plt.plot(df['quoted_at'], df['output_amount_formatted'], color='green', linewidth=2)
    plt.title('USDC Return Value Over Time', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('USDC Value', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Format the x-axis to show nice time labels
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    # Adjust layout
    plt.tight_layout()
    # Save as image file
    plt.savefig(basic_chart_figure, dpi=300, bbox_inches='tight')
    plt.clf()
    return df


def trend_lines(token: str, df: pd.DataFrame, trend_lines_figure: str):
    """
    Enhanced Visualization with Trend Lines
    Now let's create more detailed visualizations with trend lines and annotations.
    """
    # Enhanced visualization with additional insights
    plt.figure(figsize=(16, 12))

    # Plot with more detailed formatting
    # 1. ua_token_amount with trend line
    plt.subplot(2, 1, 1)
    plt.plot(df['quoted_at'], df['output_amount_readable'], color='blue', linewidth=2, label='Token Amount')

    # Add trend line
    z = np.polyfit(range(len(df)), df['output_amount_readable'], 1)
    p = np.poly1d(z)
    plt.plot(df['quoted_at'], p(range(len(df))), "r--", linewidth=1, label='Trend Line')

    plt.title(f'{token} Token Amount Over Time', fontsize=16)
    plt.ylabel('Token Amount', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Add annotations for min and max values
    max_token_idx = df['output_amount_readable'].idxmax()
    min_token_idx = df['output_amount_readable'].idxmin()

    plt.annotate(f'Max: {df.loc[max_token_idx, "output_amount_readable"]:.2f}',
                 xy=(df.loc[max_token_idx, 'quoted_at'], df.loc[max_token_idx, 'output_amount_readable']),
                 xytext=(10, 10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    plt.annotate(f'Min: {df.loc[min_token_idx, "output_amount_readable"]:.2f}',
                 xy=(df.loc[min_token_idx, 'quoted_at'], df.loc[min_token_idx, 'output_amount_readable']),
                 xytext=(10, -20), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    # 2. odos_usdc_return with trend line
    plt.subplot(2, 1, 2)
    plt.plot(df['quoted_at'], df['output_amount_formatted'], color='green', linewidth=2, label='USDC Return')

    # Add trend line
    z = np.polyfit(range(len(df)), df['output_amount_formatted'], 1)
    p = np.poly1d(z)
    plt.plot(df['quoted_at'], p(range(len(df))), "r--", linewidth=1, label='Trend Line')

    plt.title('USDC Return Value Over Time', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('USDC Value', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Add annotations for min and max values
    max_usdc_idx = df['output_amount_formatted'].idxmax()
    min_usdc_idx = df['output_amount_formatted'].idxmin()

    plt.annotate(f'Max: {df.loc[max_usdc_idx, "output_amount_formatted"]:.2f}',
                 xy=(df.loc[max_usdc_idx, 'quoted_at'], df.loc[max_usdc_idx, 'output_amount_formatted']),
                 xytext=(10, 10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    plt.annotate(f'Min: {df.loc[min_usdc_idx, "output_amount_formatted"]:.2f}',
                 xy=(df.loc[min_usdc_idx, 'quoted_at'], df.loc[min_usdc_idx, 'output_amount_formatted']),
                 xytext=(10, -20), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    plt.tight_layout()
    # Save as image file
    plt.savefig(trend_lines_figure, dpi=300, bbox_inches='tight')
    plt.clf()


def correlation_analysis(token: str, df: pd.DataFrame, correlation_analysis_figure: str):
    """
    Correlation Analysis
    Let's analyze the relationship between token amount and USDC return. 
    We'll create a scatter plot to visualize their relationship and calculate the correlation coefficient.
    """
    # Correlation analysis
    correlation = df['input_amount_readable'].corr(df['output_amount_formatted'])
    print(f"Correlation between token amount and USDC return: {correlation:.4f}")

    # Display basic statistics
    print(f"\nStatistics for {token} Token Amount:")
    print(df['input_amount_readable'].describe())

    print("\nStatistics for USDC Return:")
    print(df['output_amount_formatted'].describe())

    # Plot the relationship between token amount and USDC return
    plt.figure(figsize=(10, 6))
    plt.scatter(df['input_amount_readable'], df['output_amount_formatted'], alpha=0.5)
    plt.title('Relationship Between Token Amount and USDC Return', fontsize=16)
    plt.xlabel('Token Amount', fontsize=14)
    plt.ylabel('USDC Return', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Add trend line
    z = np.polyfit(df['input_amount_readable'], df['output_amount_formatted'], 1)
    p = np.poly1d(z)
    plt.plot(df['input_amount_readable'], p(df['output_amount_formatted']), "r--")

    plt.tight_layout()
    # Save as image file
    plt.savefig(correlation_analysis_figure, dpi=300, bbox_inches='tight')
    plt.clf()

    return correlation


def generate_markdown_report(symbol, basic_chart_figure, trend_lines_figure, correlation_analysis_figure, df, correlation):
    """Generate markdown report with GitHub-hosted images."""
    
    # Get image filenames for GitHub URLs
    basic_chart_filename = os.path.basename(basic_chart_figure)
    trend_lines_filename = os.path.basename(trend_lines_figure)
    correlation_filename = os.path.basename(correlation_analysis_figure)
    
    # Generate timestamp for the report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate statistics
    token_stats = df['input_amount_readable'].describe()
    usdc_stats = df['output_amount_formatted'].describe()
    
    markdown_content = f"""# {symbol} Price Analysis Report

Generated on: {timestamp}

## Overview

This report provides a comprehensive analysis of {symbol} token price data including:
- Basic price trend visualization
- Enhanced trend analysis with annotations
- Correlation analysis between token amount and USDC return
- Statistical summary

## Key Metrics

| Metric | Value |
|--------|-------|
| **Data Points** | {len(df)} |
| **Correlation Coefficient** | {correlation:.4f} |
| **Token Amount Range** | {token_stats['min']:.2f} - {token_stats['max']:.2f} |
| **USDC Return Range** | {usdc_stats['min']:.2f} - {usdc_stats['max']:.2f} |

## Basic Price Charts

The following charts show the basic price trends for {symbol} token amount and USDC return over time.

![{symbol} Basic Price Charts]({GITHUB_IMAGES_PATH}/{basic_chart_filename})

## Enhanced Trend Analysis

These enhanced visualizations include trend lines and annotations highlighting minimum and maximum values.

![{symbol} Enhanced Trend Charts]({GITHUB_IMAGES_PATH}/{trend_lines_filename})

## Correlation Analysis

The scatter plot below shows the relationship between token amount and USDC return, with a correlation coefficient of **{correlation:.4f}**.

![{symbol} Correlation Analysis]({GITHUB_IMAGES_PATH}/{correlation_filename})

## Statistical Summary

### {symbol} Token Amount Statistics
- **Count**: {token_stats['count']:.0f}
- **Mean**: {token_stats['mean']:.4f}
- **Standard Deviation**: {token_stats['std']:.4f}
- **Minimum**: {token_stats['min']:.4f}
- **25th Percentile**: {token_stats['25%']:.4f}
- **Median**: {token_stats['50%']:.4f}
- **75th Percentile**: {token_stats['75%']:.4f}
- **Maximum**: {token_stats['max']:.4f}

### USDC Return Statistics
- **Count**: {usdc_stats['count']:.0f}
- **Mean**: {usdc_stats['mean']:.4f}
- **Standard Deviation**: {usdc_stats['std']:.4f}
- **Minimum**: {usdc_stats['min']:.4f}
- **25th Percentile**: {usdc_stats['25%']:.4f}
- **Median**: {usdc_stats['50%']:.4f}
- **75th Percentile**: {usdc_stats['75%']:.4f}
- **Maximum**: {usdc_stats['max']:.4f}

## Interpretation

{"### Strong Correlation" if abs(correlation) > 0.7 else "### Moderate Correlation" if abs(correlation) > 0.3 else "### Weak Correlation"}

The correlation coefficient of {correlation:.4f} indicates a {"strong" if abs(correlation) > 0.7 else "moderate" if abs(correlation) > 0.3 else "weak"} {"positive" if correlation > 0 else "negative"} relationship between token amount and USDC return.

---


*Report generated by VaporFund Analytics*
"""
    

    # Get current date in dd/mm/yyyy format for filename (use dashes since slashes aren't allowed in filenames)
    current_date = datetime.now().strftime("%d-%m-%Y")
    markdown_filename = f"{markdown_folder}/{current_date}/{symbol}_analysis_report.md"

    # Save markdown file
    markdown_filename = f"{markdown_folder}/{symbol}_analysis_report.md"
    with open(markdown_filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Markdown report saved: {markdown_filename}")
    return markdown_filename


def generate_index_markdown(processed_tokens):
    """Generate an index markdown file listing all reports."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    index_content = f"""# Price Analysis Reports Index

Generated on: {timestamp}

## Available Reports

This index contains links to all generated price analysis reports.

| Token | Report Link | Charts |
|-------|-------------|--------|
"""
    
    for token in processed_tokens:
        report_link = f"[{token} Analysis Report](./{token}_analysis_report.md)"
        charts_link = f"[Charts]({GITHUB_IMAGES_PATH})"
        index_content += f"| **{token}** | {report_link} | {charts_link} |\n"
    
    index_content += f"""

## Summary

- **Total Tokens Analyzed**: {len(processed_tokens)}
- **Reports Generated**: {len(processed_tokens)}
- **Charts Repository**: [GitHub Images Folder]({GITHUB_IMAGES_PATH})

---

*Generated by VaporFund Analytics*
"""

    index_filename = f"{markdown_folder}/README.md"
    with open(index_filename, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"Index file saved: {index_filename}")
    return index_filename


def remove_temp_files():
    """Remove temporary CSV files but keep images and markdown files."""
    import glob
    
    # Remove all CSV files
    csv_files = glob.glob("price_snapshots_*.csv")
    for file in csv_files:
        os.remove(file)
        print(f"Removed: {file}")


def main():
    """Main function to process all tokens and generate reports."""
    ensure_folders_exist()
    
    print(f"GitHub images will be referenced from: {GITHUB_IMAGES_PATH}")
    print(f"Make sure to push the '{folder}' folder to your GitHub repository!")
    
    symbols = get_distinct_tokens()
    processed_tokens = []
    
    for token_symbol in tqdm(symbols, desc="Processing tokens"):
        try:
            # Download to CSV
            main_download_csv(token_symbol=token_symbol)
            output_csv_file = f"quotes_{token_symbol}.csv"

            # Define image file paths
            BASIC_CHART_FIGURE = f'{folder}/{token_symbol}_price_charts.png'
            TREND_LINES_FIGURE = f'{folder}/{token_symbol}_price_charts_with_trend.png'
            CORRELATION_ANALYSIS_FIGURE = f'{folder}/{token_symbol}_relationship_chart.png'

            # Generate charts
            df = basic_charts(token=token_symbol, csv_source=output_csv_file, basic_chart_figure=BASIC_CHART_FIGURE)
            trend_lines(token=token_symbol, df=df, trend_lines_figure=TREND_LINES_FIGURE)
            correlation = correlation_analysis(token=token_symbol, df=df, correlation_analysis_figure=CORRELATION_ANALYSIS_FIGURE)
            
            # Generate markdown report
            generate_markdown_report(
                symbol=token_symbol,
                basic_chart_figure=BASIC_CHART_FIGURE,
                trend_lines_figure=TREND_LINES_FIGURE,
                correlation_analysis_figure=CORRELATION_ANALYSIS_FIGURE,
                df=df,
                correlation=correlation
            )
            
            processed_tokens.append(token_symbol)
            
        except numpy.linalg.LinAlgError:
            logger.error(f"ERROR: Linear algebra error for token: {token_symbol}")
        except FileNotFoundError:
            logger.error(f"ERROR: File not found for token: {token_symbol}")
        except Exception as e:
            logger.error(f"ERROR: Error processing token {token_symbol}: {str(e)}")
    
    # Generate index file
    if processed_tokens:
        generate_index_markdown(processed_tokens)
    
    # Clean up temporary files
    # remove_temp_files()
    
    print(f"\n✅ Processing complete!")
    print(f"📊 Generated reports for {len(processed_tokens)} tokens")
    print(f"📁 Chart images saved in: {folder}/")
    print(f"📄 Markdown reports saved in: {markdown_folder}/")
    print(f"\n🔗 Don't forget to:")
    print(f"   1. Update GITHUB_REPO_URL with your actual GitHub repository")
    print(f"   2. Push the '{folder}' folder to GitHub")
    print(f"   3. Push the '{markdown_folder}' folder to GitHub")


if __name__ == "__main__":
    main()