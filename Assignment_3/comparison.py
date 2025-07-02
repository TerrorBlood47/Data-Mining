
def read_dataset(filename):
    filepath = "/home/faiak/Desktop/Academic/Data-Mining/Assignemnt_3/Datasets/" + filename
    with open(filepath, 'r') as file:
        # Read the file and split each transaction by spaces
        transactions = [[int(item) for item in line.strip().split()] for line in file.readlines()]
    return transactions


## APIRORI



from collections import defaultdict

def find_frequent_1_itemsets(transactions, min_sup):
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in set(transaction):  # Ensure that we count unique items
            item_count[item] += 1
    
    L1 = set()
    for item, count in item_count.items():
        if count >= min_sup:
            L1.add(tuple([item]))  # Create a frozenset of the frequent items
    

    return sorted(list(L1), key=lambda x: sorted(x))


import copy


def has_infrequent_subset(candidate, prev_frequent_itemsets):
    # print(f"candidate : {candidate}")
    # print(f"prev_freq_itemsets: {prev_frequent_itemsets}")
    for item in candidate:
        subset = copy.deepcopy(candidate)
        subset.remove(item)
        # if subset not in prev_frequent_itemsets:
        #     return True  # If any subset is not frequent, return True

        if not any(set(subset).issubset(set(sublist)) for sublist in prev_frequent_itemsets):
            return True
        
    return False  # Otherwise, return False


def apriori_gen(Lk_minus_1 : list[list[str]], k_1:int):
    candidates = []
    Lk_minus_1 = sorted(Lk_minus_1)
    # Lk_minus_1 = [sorted(row) for row in Lk_minus_1]

    # print(f"Lk_minus_1: {Lk_minus_1}")

    for i in range(len(Lk_minus_1)):
        for j in range(i + 1, len(Lk_minus_1)):
            l1 = list(Lk_minus_1[i])
            l2 = list(Lk_minus_1[j])

            # print(f"l1: {l1}, l2: {l2}")

            if l1[:k_1-1] == l2[:k_1-1] and l1[k_1-1] < l2[k_1-1]:
                candidate = sorted(l1[:k_1-1] + [l1[k_1-1]] + [l2[k_1-1]])

                # print(f"Candidate: {candidate}")

                if not has_infrequent_subset(candidate, Lk_minus_1):
                    candidates.append(candidate)
    return candidates

def count_support(transactions, itemset):
    count = 0
    itemset = set(itemset)
    for transaction in transactions:
        transaction_set = set(transaction)
        if itemset.issubset(transaction_set):
            count += 1
    return count

def APRIORI_ALGO(Transactions, min_sup):
    L = []

    L1 = find_frequent_1_itemsets(Transactions, min_sup)

    total_patterns = 0

    # print(L1)

    # print("Frequent 1-itemsets:")
    # for itemset in L1:
    #     print(itemset)
    # The output will show the frequent 1-itemsets found in the dataset

    L.append(L1)
    Lk_minus_1 = L1

    total_patterns += len(L1)

    k = 2

    # Ck = apriori_gen(Lk_minus_1, k - 1)
    # print(f"Candidates for {k}-itemsets: {Ck}")
    while Lk_minus_1:
        # print(f"k : {k}")
        Ck = apriori_gen(Lk_minus_1, k - 1)

        # print(f"len(Ck) : {len(Ck)}")
        # print(f"Candidates for {k}-itemsets: {Ck}")
        Lk = []
        for candidate in Ck:
            if count_support(Transactions, candidate) >= min_sup:
                Lk.append(list(sorted(candidate)))
        if not Lk:
            break
        L.append(Lk)

        # print(f"len(Lk) : {len(Lk)}")
        total_patterns += len(Lk)

        Lk_minus_1 = Lk
        
        # print(f"#####  Frequent {k}-itemsets: {Lk}")

        k += 1

    print(f"L : {L}")
    print(f"length of frequent itemsets in APRIORI : {total_patterns}")



### FP_GROWTH


from collections import defaultdict

class Node:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link_next= None


    def display(self, ind=1):
        print('  ' * ind, f'{self.item}: {self.count}')
        for child in self.children.values():
            child.display(ind + 1)


def BUILD_TREE(transactions, min_support):
    header_table = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            header_table[item] += 1
    header_table = {k: v for k, v in header_table.items() if v >= min_support}
    if not header_table:
        return None, None
    for key in header_table:
        header_table[key] = [header_table[key], None]
    root = Node(None, 1, None)
    for transaction in transactions:
        filtered_transaction = [item for item in transaction if item in header_table]
        filtered_transaction.sort(key=lambda x: header_table[x][0], reverse=True)
        insert_tree(filtered_transaction, root, header_table)
    return root, header_table

def insert_tree(items, node, header_table):
    if items:
        first_item = items[0]
        if first_item in node.children:
            node.children[first_item].count += 1
        else:
            new_node = Node(first_item, 1, node)
            node.children[first_item] = new_node
            if header_table[first_item][1] is None:
                header_table[first_item][1] = new_node
            else:
                current = header_table[first_item][1]
                while current.link_next is not None:
                    current = current.link_next
                current.link_next= new_node
        insert_tree(items[1:], node.children[first_item], header_table)


def MINE_TREE(header_table, min_support, prefix, frequent_itemsets):
    sorted_items = sorted(header_table.items(), key=lambda x: x[1][0])
    for base_item, (count, node) in sorted_items:
        new_prefix = prefix.copy()
        new_prefix.add(base_item)
        frequent_itemsets.append((new_prefix, count))
        conditional_pattern_base = []
        while node is not None:
            path = []
            parent = node.parent
            while parent is not None and parent.item is not None:
                path.append(parent.item)
                parent = parent.parent
            path.reverse()
            for _ in range(node.count):
                conditional_pattern_base.append(path)
            node = node.link_next
        conditional_tree, conditional_header = BUILD_TREE(conditional_pattern_base, min_support)
        if conditional_header is not None:
            # print(f"\nConditional FP-tree for prefix {new_prefix}:")
            # conditional_tree.display()
            MINE_TREE(conditional_header, min_support, new_prefix, frequent_itemsets)

def FP_TREE_ALGO(Transactions, min_sup):
    root, header_table = BUILD_TREE(Transactions, min_sup)
    frequent_itemsets = []
    if root is not None:
        MINE_TREE(header_table, min_sup, set(), frequent_itemsets)

    print(f"length of frequent itemsets in FP_GROWTH : {len(frequent_itemsets)}")
    # print(frequent_itemsets)




######## MAIN CODE ###################3
import math
import sys, os

if __name__ == "__main__":
    # os.makedirs('./Output', exist_ok=True)  # ✅ Creates the folder if it doesn't exist
    output_file = "/home/faiak/Desktop/Academic/Data-Mining/Assignemnt_3/Output/output.txt"
    sys.stdout = open(output_file, 'w')

    filename = 'sample.txt'
    Transactions = read_dataset(filename) 
    min_sup = math.ceil(0.25 * len(Transactions))

    APRIORI_ALGO(Transactions=Transactions, min_sup=min_sup)

    FP_TREE_ALGO(Transactions=Transactions, min_sup=min_sup)