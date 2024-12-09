import pandas as pd
from collections import defaultdict

class MindDataset:
    def __init__(self, data_path, num_users=500, leaf_node_capacity=50, min_history=5):
        self.data_path = data_path
        self.num_users = num_users
        self.leaf_node_capacity = leaf_node_capacity
        self.news_columns = ["NewsID", "Category", "Subcategory", "NewsTitle", "NewsAbstrct", "NewsUrl",
                          "EntitiesinNewsTitle", "EntitiesinNewsAbstract"]
        self.user_columns = ["Impression ID", "User ID", "Impression Time", "User Click History", "Impression News"]
        self.news_data = pd.read_csv(self.data_path + '/news.tsv', sep='\t', names=self.news_columns)
        self.user_behavior = pd.read_csv(self.data_path + '/behaviors.tsv', sep='\t', names=self.user_columns)
        self._process_user_behavior(min_history)
        self.subcate_item_dict = defaultdict(set)
        self.Category_dict = defaultdict(set)
        self.Category_set = set()

    def _process_user_behavior(self, min_history):
        def cal_len(s):
            return len(str(s).split(' '))

        self.user_behavior['User Click Length'] = self.user_behavior.apply(
            lambda x: cal_len(x['User Click History']), axis=1
        )
        self.user_behavior_filtered = self.user_behavior[self.user_behavior['User Click Length'] >= min_history]
        self.user_sampled = self.user_behavior_filtered.sample(n=self.num_users, random_state=2)

    def negative_sampling(self):
        for impressionList in self.user_sampled['Impression News']:
            impressionList = impressionList.split(' ')
            for impression in impressionList:
                newsID, label = impression.split('-')
                cate_name = self.news_data[self.news_data['NewsID'] == newsID]['Category'].iloc[0]
                subcate_name = self.news_data[self.news_data['NewsID'] == newsID]['Subcategory'].iloc[0]
                self.Category_dict[cate_name].add(subcate_name)
                self.Category_set.add(cate_name)
                if label == '1':
                    newsTitle = self.news_data[self.news_data['NewsID'] == newsID]['NewsTitle'].iloc[0]
                    self.subcate_item_dict[subcate_name].add((newsID, newsTitle))

        for impressionList in self.user_sampled['Impression News']:
            impressionList = impressionList.split(' ')
            for impression in impressionList:
                newsID, label = impression.split('-')
                cate_name = self.news_data[self.news_data['NewsID'] == newsID]['Category'].iloc[0]
                subcate_name = self.news_data[self.news_data['NewsID'] == newsID]['Subcategory'].iloc[0]
                self.Category_dict[cate_name].add(subcate_name)
                self.Category_set.add(cate_name)
                if label == '0':
                    newsTitle = self.news_data[self.news_data['NewsID'] == newsID]['NewsTitle'].iloc[0]
                    if len(self.subcate_item_dict[subcate_name]) < self.leaf_node_capacity:
                        self.subcate_item_dict[subcate_name].add((newsID, newsTitle))

    def get_category_dict(self):
        return self.Category_dict

    def get_subcategory_item_dict(self):
        return self.subcate_item_dict

    def get_category_set(self):
        return self.Category_set


# Usage example:
# data_path = './data/MINDsmall_dev'
# mind_dataset = MindDataset(data_path, num_users=500, leaf_node_capacity=50)
#
# mind_dataset.negative_sampling()
#
# category_dict = mind_dataset.get_category_dict()
# subcate_item_dict = mind_dataset.get_subcategory_item_dict()
# category_set = mind_dataset.get_category_set()
