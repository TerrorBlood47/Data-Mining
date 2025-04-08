import pandas as pd
from itertools import combinations
from collections import defaultdict

def read_dataset(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    transactions = []
    for line in lines:
        transaction = line.strip().split()
        transactions.append(transaction)
    
    print("File read complete")
    return transactions

def find_frequent_1_itemsets(transactions, min_sup):
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in set(transaction):  # using set to avoid duplicates in one transaction
            item_count[item] += 1
    
    L1 = []
    for item, count in item_count.items():
        if count >= min_sup:
            L1.append(frozenset([item]))
    
    return sorted(L1, key=lambda x: sorted(x))

def has_infrequent_subset(candidate, prev_frequent_itemsets):
    for item in candidate:
        subset = candidate - frozenset([item])
        if subset not in prev_frequent_itemsets:
            return True
    return False

def apriori_gen(Lk_minus_1, k):
    candidates = []
    Lk_minus_1 = list(Lk_minus_1)

    for i in range(len(Lk_minus_1)):
        for j in range(i + 1, len(Lk_minus_1)):
            l1 = list(Lk_minus_1[i])
            l2 = list(Lk_minus_1[j])

            if l1[:k-1] == l2[:k-1]:
                candidate = Lk_minus_1[i] | Lk_minus_1[j]
                if not has_infrequent_subset(candidate, Lk_minus_1):
                    candidates.append(candidate)
    return candidates

def count_support(transactions, itemset):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    return count

def apriori(transactions, min_sup):
    transactions = list(map(set, transactions))
    L = []
    
    L1 = find_frequent_1_itemsets(transactions, min_sup)
    L.append(L1)
    k = 2
    Lk_minus_1 = set(L1)

    while Lk_minus_1:
        Ck = apriori_gen(Lk_minus_1, k - 1)
        Lk = []
        for candidate in Ck:
            if count_support(transactions, candidate) >= min_sup:
                Lk.append(candidate)
        if not Lk:
            break
        L.append(Lk)
        Lk_minus_1 = set(Lk)
        k += 1

        print(f"Candidates for {k}-itemsets: {Ck}")
        print(f"Frequent {k}-itemsets: {Lk}")

    return L

def print_itemsets(L):
    for k, itemsets in enumerate(L):
        print(f"Frequent {k+1}-itemsets:")
        for itemset in itemsets:
            print(sorted(itemset))
        print()

# Example usage
if __name__ == "__main__":
    filepath = "Datasets/retail.dat.txt"
    transactions = read_dataset(filepath)
    min_support = 2
    L = apriori(transactions, min_support)
    print_itemsets(L)
