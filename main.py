from LLMTreeRec import LLMTreeRec
from dataloader import MindDataset

data_path = './data/MINDsmall_dev'
minddataset = MindDataset(data_path, num_users=500, leaf_node_capacity=50, min_history=5)
LLMTreeRec = LLMTreeRec(minddataset, first_level_k=5, recall_num=20, recall_subset=4, sleep_time=20, log_file="log.json")
users = minddataset.user_sampled

for index, row in users.iterrows():
    user_id = row['User ID']
    print("Recommend for user: ", user_id)
    LLMTreeRec.run_user(user_id)