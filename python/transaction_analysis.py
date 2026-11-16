import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the cleaned data (Assuming exported from SQL or provided as CSV)
# df = pd.read_csv('../data/cleaned_transactions.csv')

# Creating mock data for demonstration purposes
data = {
    'transaction_id': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8'],
    'transaction_date': ['2023-10-01', '2023-10-01', '2023-10-02', '2023-10-02', '2023-10-03', '2023-10-03', '2023-10-04', '2023-10-04'],
    'transaction_hour': [14, 18, 19, 10, 18, 19, 11, 18],
    'amount': [150.00, 200.00, 50.00, 300.00, 120.00, 450.00, 80.00, 200.00],
    'payment_method': ['Credit Card', 'UPI', 'Credit Card', 'Debit Card', 'UPI', 'Credit Card', 'Net Banking', 'Credit Card'],
    'gateway': ['Gateway_A', 'Gateway_B', 'Gateway_A', 'Gateway_A', 'Gateway_B', 'Gateway_A', 'Gateway_C', 'Gateway_A'],
    'status': ['Success', 'Success', 'Failed', 'Success', 'Failed', 'Failed', 'Success', 'Failed'],
    'error_code': ['No Error', 'No Error', 'Timeout', 'No Error', 'Insufficient Funds', 'Timeout', 'No Error', 'Timeout']
}
df = pd.DataFrame(data)

# 2. Analyze Success/Failure Rates by Gateway
gateway_stats = df.groupby('gateway').agg(
    total_transactions=('transaction_id', 'count'),
    failed_transactions=('status', lambda x: (x == 'Failed').sum())
).reset_index()

gateway_stats['failure_rate'] = (gateway_stats['failed_transactions'] / gateway_stats['total_transactions']) * 100
print("--- Gateway Failure Rates ---")
print(gateway_stats.sort_values(by='failure_rate', ascending=False).to_string(index=False))

# 3. Identify Unusual Patterns: Failures by Hour and Payment Method
# Filter only failed transactions
failed_df = df[df['status'] == 'Failed']

# Pattern 1: Failure count by Payment Method
plt.figure(figsize=(10, 5))
sns.countplot(data=failed_df, x='payment_method', order=failed_df['payment_method'].value_counts().index, palette='Reds')
plt.title('Transaction Failures by Payment Method')
plt.xlabel('Payment Method')
plt.ylabel('Number of Failures')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../data/failures_by_payment_method.png', dpi=300)
print("\n[Saved] Plot: failures_by_payment_method.png")

# Pattern 2: Failure count by Hour of Day (Peak Hour Analysis)
plt.figure(figsize=(10, 5))
sns.countplot(data=failed_df, x='transaction_hour', palette='Oranges')
plt.title('Transaction Failures by Hour of Day')
plt.xlabel('Hour of Day (24h)')
plt.ylabel('Number of Failures')
plt.tight_layout()
plt.savefig('../data/failures_by_hour.png', dpi=300)
print("[Saved] Plot: failures_by_hour.png")

# 4. Export aggregated data for Excel Validation
validation_df = df.groupby(['payment_method', 'status']).size().unstack(fill_value=0)
validation_df.to_csv('../data/excel_validation_summary.csv')
print("\n[Saved] Excel validation summary exported to: excel_validation_summary.csv")
