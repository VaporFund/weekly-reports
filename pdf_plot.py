"""Original version from https://github.com/Chonlakant/MetaQuote/blob/main/plot_uLINK.ipynb"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

from download_to_csv import main_download_csv

# Set figure aesthetics for better visualization
plt.style.use('ggplot')

# Set higher DPI for sharper in-notebook display
plt.rcParams['figure.dpi'] = 100
CSV_SOURCE = 'price_snapshots_usol.csv'
folder = 'pdf_plot_output_figures'
BASIC_CHART_FIGURE = f'{folder}/uLINK_price_charts.png'
TREND_LINES_FIGURE = f'{folder}/uLINK_price_charts_with_trend.png'
CORRELATION_ANALYSIS_FIGURE = f'{folder}/uLINK_relationship_chart.png'


def basic_charts() -> pd.DataFrame:
    """
    Basic Line Charts
    Let's create two separate line charts for the token amount and USDC return.
    """
    # Load the CSV data
    df = pd.read_csv(CSV_SOURCE)

    # Display the first few rows to verify data loading
    print(f"Total rows: {len(df)}")

    # Data preprocessing
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Convert ua_token_amount from string to float (it's in wei format with 18 decimals)
    df['ua_token_amount'] = df['ua_token_amount'].astype(float)

    # Convert to a more readable format (divide by 10^18 to get the actual token amount)
    df['ua_token_amount_readable'] = df['ua_token_amount'] / 1e18

    # Sort by timestamp to ensure proper chronological order
    df = df.sort_values('timestamp')

    # Basic Line Charts
    # Let's create two separate line charts for the token amount and USDC return.
    # Set up the figure with two subplots (one for each metric)
    plt.figure(figsize=(14, 10))

    # Plot 1: ua_token_amount over time
    plt.subplot(2, 1, 1)
    plt.plot(df['timestamp'], df['ua_token_amount_readable'], color='blue', linewidth=2)
    plt.title('uLINK Token Amount Over Time', fontsize=16)
    plt.ylabel('Token Amount', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Format the x-axis to show nice time labels
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    # Plot 2: odos_usdc_return over time
    plt.subplot(2, 1, 2)
    plt.plot(df['timestamp'], df['odos_usdc_return'], color='green', linewidth=2)
    plt.title('USDC Return Value Over Time', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('USDC Value', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Format the x-axis to show nice time labels
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    # Adjust layout
    plt.tight_layout()
    # Optional: save as image file
    plt.savefig(BASIC_CHART_FIGURE, dpi=300)
    plt.clf()
    return df


def trend_lines(df: pd.DataFrame):
    """
    Enhanced Visualization with Trend Lines
    Now let's create more detailed visualizations with trend lines and annotations.
    """
    # Enhanced visualization with additional insights
    plt.figure(figsize=(16, 12))

    # Plot with more detailed formatting
    # 1. ua_token_amount with trend line
    plt.subplot(2, 1, 1)
    plt.plot(df['timestamp'], df['ua_token_amount_readable'], color='blue', linewidth=2, label='Token Amount')

    # Add trend line
    z = np.polyfit(range(len(df)), df['ua_token_amount_readable'], 1)
    p = np.poly1d(z)
    plt.plot(df['timestamp'], p(range(len(df))), "r--", linewidth=1, label='Trend Line')

    plt.title('uLINK Token Amount Over Time', fontsize=16)
    plt.ylabel('Token Amount', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Add annotations for min and max values
    max_token_idx = df['ua_token_amount_readable'].idxmax()
    min_token_idx = df['ua_token_amount_readable'].idxmin()

    plt.annotate(f'Max: {df.loc[max_token_idx, "ua_token_amount_readable"]:.2f}',
                 xy=(df.loc[max_token_idx, 'timestamp'], df.loc[max_token_idx, 'ua_token_amount_readable']),
                 xytext=(10, 10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    plt.annotate(f'Min: {df.loc[min_token_idx, "ua_token_amount_readable"]:.2f}',
                 xy=(df.loc[min_token_idx, 'timestamp'], df.loc[min_token_idx, 'ua_token_amount_readable']),
                 xytext=(10, -20), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    # 2. odos_usdc_return with trend line
    plt.subplot(2, 1, 2)
    plt.plot(df['timestamp'], df['odos_usdc_return'], color='green', linewidth=2, label='USDC Return')

    # Add trend line
    z = np.polyfit(range(len(df)), df['odos_usdc_return'], 1)
    p = np.poly1d(z)
    plt.plot(df['timestamp'], p(range(len(df))), "r--", linewidth=1, label='Trend Line')

    plt.title('USDC Return Value Over Time', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('USDC Value', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Add annotations for min and max values
    max_usdc_idx = df['odos_usdc_return'].idxmax()
    min_usdc_idx = df['odos_usdc_return'].idxmin()

    plt.annotate(f'Max: {df.loc[max_usdc_idx, "odos_usdc_return"]:.2f}',
                 xy=(df.loc[max_usdc_idx, 'timestamp'], df.loc[max_usdc_idx, 'odos_usdc_return']),
                 xytext=(10, 10), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    plt.annotate(f'Min: {df.loc[min_usdc_idx, "odos_usdc_return"]:.2f}',
                 xy=(df.loc[min_usdc_idx, 'timestamp'], df.loc[min_usdc_idx, 'odos_usdc_return']),
                 xytext=(10, -20), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    plt.tight_layout()
    # Optional: save as image file
    plt.savefig(TREND_LINES_FIGURE, dpi=300)
    plt.clf()


def correlation_analysis(df: pd.DataFrame):
    """
    Correlation Analysis
    Let's analyze the relationship between token amount and USDC return. We'll create a scatter plot to visualize their relationship and calculate the correlation coefficient.
    """
    from IPython.display import display
    # Correlation analysis
    correlation = df['ua_token_amount_readable'].corr(df['odos_usdc_return'])
    print(f"Correlation between token amount and USDC return: {correlation:.4f}")

    # Display basic statistics
    print("\nStatistics for uLINK Token Amount:")
    display(df['ua_token_amount_readable'].describe())

    print("\nStatistics for USDC Return:")
    display(df['odos_usdc_return'].describe())

    # Plot the relationship between token amount and USDC return
    plt.figure(figsize=(10, 6))
    plt.scatter(df['ua_token_amount_readable'], df['odos_usdc_return'], alpha=0.5)
    plt.title('Relationship Between Token Amount and USDC Return', fontsize=16)
    plt.xlabel('Token Amount', fontsize=14)
    plt.ylabel('USDC Return', fontsize=14)
    plt.grid(True, alpha=0.3)

    # Add trend line
    z = np.polyfit(df['ua_token_amount_readable'], df['odos_usdc_return'], 1)
    p = np.poly1d(z)
    plt.plot(df['ua_token_amount_readable'], p(df['ua_token_amount_readable']), "r--")

    plt.tight_layout()
    # Optional: save as image file
    plt.savefig(CORRELATION_ANALYSIS_FIGURE, dpi=300)
    plt.clf()


def make_pdf():
    """Use markdown and generate the pdf."""
    pdf = MarkdownPdf(toc_level=2, optimize=True)
    basic_chart = f"<img src='{BASIC_CHART_FIGURE}'/>"
    trend_lines_chart = f"<img src='{TREND_LINES_FIGURE}'/>"
    correlation_analysis_chart = f"<img src='{CORRELATION_ANALYSIS_FIGURE}'/>"

    # This is bug. Must no ident in the content lines.
    content = f"""
### Figure
{basic_chart}
{trend_lines_chart}
{correlation_analysis_chart}
    """
    pdf.add_section(Section(content, toc=False))

    pdf.meta["title"] = "price chart"
    pdf.meta["author"] = "VapourFund"
    pdf.save("price_chart.pdf")


def main():
    # download to CSV
    main_download_csv()

    df = basic_charts()
    trend_lines(df)
    correlation_analysis(df)
    make_pdf()


if __name__ == "__main__":
    main()
