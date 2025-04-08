#include <bits/stdc++.h>

using namespace std;
#define fast_cin() ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL)

#define     all(x)      x.begin(), x.end() 

typedef long long int ll;



typedef set<string> ItemSet;
typedef vector<ItemSet> List_of_ItemSets;
typedef vector<vector<string>> Transactions;


ostream& operator<<(ostream& os ,ItemSet& itemSet){
    os<<"{";

    for(auto it=itemSet.begin(); it!=itemSet.end(); ++it){
        os<< (*it) <<" ";
    }

    os <<"}";

    return os;
}


ostream& operator<<(ostream& os, List_of_ItemSets& L){

    os<<"[";

    for(ItemSet itemSet : L){
        os<<itemSet;
        os<<endl;
    }

    os<<"]";

    return os;
}


List_of_ItemSets find_frequent_1_itemSet(vector<vector<string>> &D,int min_sup){
    ItemSet set;

    for(int i=0; i<D.size(); i++){
        for(string s: D[i]){
            set.insert(s);
        }
    }

    List_of_ItemSets L1;

    for(string s : set){
        int count = 0;

        // cout<<s<<": "<<endl;
        for(int i=0; i<D.size(); i++){
            if(find(D[i].begin(), D[i].end() ,s) != D[i].end()){
                count++;
            }
        }

        // cout<<count<<endl;

        if(count >= min_sup){
            ItemSet itemSet;
            itemSet.insert(s);
            L1.push_back(itemSet);
        }
    }

    // for(string s : set){
    //     cout<<s<<endl;
    // }

    sort(all(L1));

    return L1;
}


ItemSet join(ItemSet &l1, ItemSet &l2, int k_1) {
    auto it1 = l1.begin();
    auto it2 = l2.begin();

    ItemSet c;

    for (int i = 0; i < k_1 - 1; ++i, ++it1, ++it2) {
        if (*it1 != *it2) {
            return {}; 
        }
        c.insert(*it1); 
    }

    c.insert(*it1);
    c.insert(*it2);

    return c;
}



bool has_infrequent_subset(ItemSet c, List_of_ItemSets Lk_1){
    for(auto it=c.begin();it!=c.end(); ++it){
        ItemSet subset = c;
        subset.erase(*it);


        if (find(Lk_1.begin(), Lk_1.end(), subset) == Lk_1.end()) {
            return true; // found an infrequent subset
        }
    }

    return false;
}


List_of_ItemSets apriori_gen(List_of_ItemSets Lk_1, int k_1) {
    List_of_ItemSets Ck;


    for (size_t i = 0; i < Lk_1.size(); ++i) {
        for (size_t j = i + 1; j < Lk_1.size(); ++j) {
            ItemSet l1 = Lk_1[i];
            ItemSet l2 = Lk_1[j];

            auto it1 = l1.begin();
            auto it2 = l2.begin();

            bool mismatch = false;
            for (int k = 0; k < k_1 - 1; ++k, ++it1, ++it2) {
                if (*it1 != *it2) {
                    mismatch = true;
                    break;
                }
            }

            if (mismatch) continue;

            // Check last element to avoid duplicate joins

            auto last1 = *prev(l1.end());
            auto last2 = *prev(l2.end());

            if (last1 >= last2) continue;

            ItemSet c = join(l1, l2, k_1);

            if (!has_infrequent_subset(c, Lk_1)) {
                Ck.push_back(c);
            }
        }
    }

    return Ck;
}

int Counter(Transactions D, ItemSet c){
    int count = 0;
    
    for(int i=0; i<D.size(); i++){
        bool not_found = false;

        for(string s : c){

            if(find(D[i].begin(), D[i].end(), s) == D[i].end()){
                not_found = true;
                break;
            }
        }

        if(!not_found){
            count++;
        }
    }

    return count;
}

Transactions DatasetCreation(void){
    string filepath = "Datasets/retail.dat.txt";
    Transactions D;
    ifstream file(filepath);
    string line;

    while (getline(file, line)) {
        istringstream iss(line);
        vector<string> transaction;
        string item;

        while (iss >> item) {
            transaction.push_back(item);
        }

        D.push_back(transaction);
    }

    file.close();
    cout<< "File read complete"<<endl;
    return D;
}

void solve(void){

    // a database of transaction
    // Transactions D = {
    //     {"I1", "I2", "I5"},
    //     {"I2", "I4"},
    //     {"I2", "I3"},
    //     {"I1", "I2", "I4"},
    //     {"I1", "I3"},
    //     {"I2", "I3"},
    //     {"I1", "I3"},
    //     {"I1", "I2", "I3", "I5"},
    //     {"I1", "I2", "I3"}
    // }; 


    Transactions D = DatasetCreation();

    // const uint32_t min_sup = 2; //min support count

    // List_of_ItemSets L1 = find_frequent_1_itemSet(D, min_sup);

    // for(ItemSet itemSet : L1){
    //     cout<< itemSet << endl;
    // }

    // List_of_ItemSets Lk_1 = L1;

    // for(int k=2;k<4 ;k++){
    //     List_of_ItemSets Ck = apriori_gen(Lk_1, k-1);
    
    // if(Ck.size() == 0){
    //     cout<<"break"<<endl;
    //     break;
    // }

    // cout<<"Ck"<<endl;
    // cout<<Ck<<endl;
    
    // List_of_ItemSets Lk;

    // for(ItemSet itemSet : Ck){
    //     int count = Counter(D, itemSet);

    //     if(count >= min_sup) {
    //         Lk.push_back(itemSet);
    //     }
    // }

    // cout<<"Lk"<<endl;
    // cout<<Lk<<endl;

    // Lk_1 = Lk;

    // }

}

int main() {
fast_cin();


solve();



return 0;
}