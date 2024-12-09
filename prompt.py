def generate_prompt_interest(news_list):
    """Stage 1: Generate interest summary prompt based on user's clicked news"""
    prompt = "A user's clicked news are:\n"
    prompt += '\n'.join(news_list)  # Efficient way to join list of strings
    prompt += "\nSummarize the interested topics, from the most important to the least important."
    return prompt


def generate_prompt_category_selection(category_list):
    """Stage 2: Generate prompt for category selection based on user interests"""
    message = "Select some topic categories based on the user's interest from the provided list"
    message += " from the most important to the least important without explanation:\n"
    message += ', '.join(category_list)  # Join categories with a comma for better readability
    message += '.'
    return message


def build_prompt_subcategory(category_list, category_dict, k):
    """Stage 3: Generate prompt for subcategory selection based on user interests"""
    prompt = f"Provide a ranked list of top {k} subcategories based on the user's interest from the provided list, without offering any explanations."
    prompt += " Please do not change the format of titles during the output process.\n"
    prompt += "Here is the category and subcategory list:\n"

    # Efficiently add categories and subcategories
    count = 1
    for cate in category_list:
        cate_lower = cate.lower()
        if cate_lower in category_dict:
            for subcate in category_dict[cate_lower]:
                prompt += f"{count}. {subcate}\n"
                count += 1

    prompt += "\n"
    return prompt


def build_prompt_top_k_news(subcategory, k, news_dict):
    """Stage 4: Generate prompt to select top K news from the list based on user interest"""
    prompt = f"Select top {k} news based on the user's interest from the following candidate news about {subcategory} without explanation."
    prompt += " Please do not change the format of titles during the output process.\n"
    prompt += "Here is the news list:\n"

    # Efficiently add news items from the dictionary
    if subcategory in news_dict:
        news_list = news_dict[subcategory]
        for i, (ID, title) in enumerate(news_list, start=1):
            prompt += f"{i}. {title}\n"

    return prompt


def build_prompt_rerank(news_title_list):
    """Stage 5: Generate prompt to rerank pre-selected news based on recommendation"""
    prompt = "Rank these pre-selected news based on the degree of recommendation to the user. Be aware of ranking diversity.\n"

    # Efficiently add news items with their subcategory
    index = 1
    for subcate, newslist in news_title_list:
        for news in newslist:
            prompt += f"{index}: {news}\n"
            index += 1

    return prompt
