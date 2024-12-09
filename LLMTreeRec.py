import json
import difflib
from dataloader import MindDataset
from OpenAILLM import OpenAILLM
from utils import *
from prompt import *


class LLMTreeRec:
    def __init__(self, dataset: MindDataset, first_level_k=5, recall_num=20, recall_subset=4, log_file="log.json"):
        self.dataset = dataset
        self.first_level_k = first_level_k
        self.recall_num = recall_num
        self.recall_subset = recall_subset
        self.log_file = log_file
        system_prompt = "You need to act as a recommendation system, summarizing user interests and suggesting relevant content."
        self.conversation = OpenAILLM(system_prompt)
        self.log_data = {}  # To store all logs

    def convert_set_to_list(self, data):
        """Recursively convert sets to lists."""
        if isinstance(data, set):
            return list(data)
        elif isinstance(data, dict):
            return {key: self.convert_set_to_list(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_set_to_list(item) for item in data]
        else:
            return data

    def save_log(self):
        self.log_data = self.convert_set_to_list(self.log_data)
        with open(self.log_file, "w", encoding='utf-8') as f:
            json.dump(self.log_data, f, ensure_ascii=False, indent=4)

    def log_stage(self, user_log, stage, input_data, prompt, output_data, additional_data=None):
        """Log the information for each stage, converting sets to lists."""
        if additional_data:
            additional_data = self.convert_set_to_list(additional_data)
        stage_info = {
            'stage': stage,
            'input': input_data,
            'prompt': prompt,
            'output': output_data
        }
        if additional_data:
            stage_info.update(additional_data)

        # Add or update the user's log
        if user_log['user_id'] not in self.log_data:
            self.log_data[user_log['user_id']] = {'stages': []}

        self.log_data[user_log['user_id']]['stages'].append(stage_info)

    def calculate_recall_rate(self, user_ID, recall_news_title):
        user_pos_news = get_pos_news(self.dataset.news_data, user_ID, self.dataset.user_behavior)
        recall_pos = 0
        for subcate, l in recall_news_title:
            for news in l:
                news_match = ""
                for item_match in difflib.get_close_matches(news, user_pos_news, cutoff=0.8):
                    news_match = item_match
                    break
                if news_match != "":
                    recall_pos += 1
        recall_rate = recall_pos / len(user_pos_news) if user_pos_news else 0  # 防止除以零
        return recall_rate

    def run_user(self, user_ID):
        # Initialize log for this user
        user_log = {
            'user_id': user_ID,
            'stages': []
        }

        # Retrieve the list of news that the user clicked
        newsIDList = \
        self.dataset.user_behavior[self.dataset.user_behavior["User ID"] == user_ID]["User Click History"].iloc[
            0].split(' ')
        newsIDList = newsIDList[-50:]
        newsList = [self.dataset.news_data[self.dataset.news_data['NewsID'] == newsID]['NewsTitle'].iloc[0] for newsID
                    in newsIDList]

        # Stage 1: Generate Interest-based Prompt
        prompt = generate_prompt_interest(newsList)
        response = self.conversation.generate(prompt, 1)
        self.log_stage(user_log, 'Interest Summarization', newsList, prompt, response)

        # Stage 2: Category Selection
        prompt_2 = generate_prompt_category_selection(self.dataset.Category_set)
        response_2 = self.conversation.generate(prompt_2, 2)
        category_list = get_cate(response_2)
        self.log_stage(user_log, 'Category Selection', self.dataset.Category_set, prompt_2, response_2,
                       {'category_list': category_list})

        # Stage 3: Subcategory Selection and News Retrieval
        prompt_3 = build_prompt_subcategory(category_list[:self.first_level_k],
                                            self.dataset.Category_dict, self.first_level_k)
        response_3 = self.conversation.generate(prompt_3, 2)
        subcategory_list = get_subcate(response_3)
        self.log_stage(user_log, 'Subcategory Selection', category_list[:self.first_level_k], prompt_3, response_3,
                       {'subcategory_list': subcategory_list})

        # Stage 4: Recall Top-K News from Subcategories
        recall_news_title = []
        for subcate in subcategory_list:
            if len(self.dataset.subcate_item_dict[subcate]) == 0:
                continue
            num = self.recall_subset if self.recall_subset <= len(self.dataset.subcate_item_dict[subcate]) else len(
                self.dataset.subcate_item_dict[subcate])
            prompt_4 = build_prompt_top_k_news(subcate, num, self.dataset.subcate_item_dict)
            message_4 = self.conversation.generate(prompt_4, 2)
            recall_news_title.append((subcate, get_news_title(message_4)))
            self.log_stage(user_log, 'Recall From Leaf Nodes', subcategory_list, prompt_4, message_4,
                           {'recall_news_title': recall_news_title})

        # Evaluation: Calculate recall rate based on user behavior
        recall_rate = self.calculate_recall_rate(user_ID, recall_news_title)
        self.log_stage(user_log, 'Evaluation', user_ID, "", "", {'recall_rate': recall_rate})
        self.save_log()
