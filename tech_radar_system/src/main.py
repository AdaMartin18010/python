# tech_radar_system/src/main.py

from processor import process_multiple

# 定义一个要监控的技术列表
# 格式: (github_owner, github_repo_name, pypi_package_name)
TECHNOLOGIES_TO_TRACK = [
    ("tiangolo", "fastapi", "fastapi"),
    ("pallets", "flask", "flask"),
    ("django", "django", "django"),
    ("pandas-dev", "pandas", "pandas"),
    ("numpy", "numpy", "numpy"),
    ("scikit-learn", "scikit-learn", "scikit-learn"),
    ("langchain-ai", "langchain", "langchain"),
    ("pydantic", "pydantic", "pydantic"),
    ("encode", "httpx", "httpx"),
    ("polars", "polars", "polars"),
]

def main():
    """
    主函数，用于执行技术雷达数据处理流程。
    """
    print("Starting technology radar data processing...")
    
    # 请确保已设置 GITHUB_TOKEN 环境变量
    
    results_df = process_multiple(TECHNOLOGIES_TO_TRACK)
    
    if not results_df.empty:
        print("\n--- Processing Complete ---")
        print("Data collected and processed successfully:")
        print(results_df.to_markdown(index=False))

        # 将结果保存到CSV文件
        output_path = "tech_radar_results.csv"
        results_df.to_csv(output_path, index=False)
        print(f"\nResults saved to {output_path}")
    else:
        print("\n--- Processing Complete ---")
        print("No data was processed. Please check logs for errors.")

if __name__ == "__main__":
    main() 