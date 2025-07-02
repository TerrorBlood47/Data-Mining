import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("/home/faiak/Desktop/Academic/Data-Mining/Assignment_9/jamal/benchmarks/benchmark_results.csv")  # Replace with the actual path if needed

# Extract necessary columns
datasets = df['Dataset']
dt_acc = df['DT_Accuracy']
nb_acc = df['NB_Accuracy']

# Plotting
x = range(len(datasets))
width = 0.35

plt.figure(figsize=(12, 6))
plt.bar(x, dt_acc, width=width, label='Decision Tree', color='skyblue')
plt.bar([i + width for i in x], nb_acc, width=width, label='Naive Bayes', color='lightgreen')

# Add labels and title
plt.xlabel("Dataset")
plt.ylabel("Accuracy")
plt.title("Accuracy Comparison: Decision Tree vs Naive Bayes")
plt.xticks([i + width / 2 for i in x], datasets, rotation=45, ha='right')
plt.ylim(0, 1.1)
plt.legend()
plt.tight_layout()

# Save the figure
plt.savefig("./accuracy_comparison.png", dpi=300)
print("✅ Plot saved as 'accuracy_comparison.png'.")


# Show the plot
plt.show()
