# tech_radar_system/src/processor.py

import pandas as pd

def process_data(github_data, pypi_data):
    """
    Processes raw data and calculates initial metrics.
    For the prototype, this is a simple combination and placeholder for a scoring model.
    """
    if not github_data or not pypi_data:
        return None

    # 简单的社区活跃度评分（示例）
    # 这里的权重是任意选择的，用于演示目的
    activity_score = (
        github_data.get("stars", 0) * 0.6 +
        github_data.get("forks", 0) * 0.3 +
        github_data.get("watchers", 0) * 0.1
    )

    processed_record = {
        **github_data,
        **pypi_data,
        "activity_score": round(activity_score, 2),
    }

    return processed_record

def process_multiple(tech_list):
    """
    Processes a list of technologies, collecting and processing their data.
    
    :param tech_list: A list of tuples, where each tuple is (repo_owner, repo_name, pypi_package_name)
    :return: A pandas DataFrame with the processed data.
    """
    # 动态导入以避免循环依赖问题，并保持collector的独立性
    from .collector import get_github_data, get_pypi_data

    processed_data = []
    for repo_owner, repo_name, pypi_package in tech_list:
        print(f"--- Processing {repo_name} ---")
        
        gh_data = get_github_data(repo_owner, repo_name)
        if not gh_data:
            print(f"Skipping {repo_name} due to lack of GitHub data.")
            continue
            
        py_data = get_pypi_data(pypi_package)
        if not py_data:
            print(f"Skipping {repo_name} due to lack of PyPI data.")
            continue
            
        record = process_data(gh_data, py_data)
        if record:
            record["name"] = repo_name
            processed_data.append(record)

    df = pd.DataFrame(processed_data)
    # 重新排列列的顺序以便于查看
    if not df.empty:
        cols = ['name', 'version', 'stars', 'forks', 'watchers', 'activity_score', 'summary', 'last_updated', 'author', 'open_issues']
        # 确保所有预期的列都存在
        existing_cols = [col for col in cols if col in df.columns]
        df = df[existing_cols]

    return df 