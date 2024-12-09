import os
from stream_processing import simulate_stream, stream_handler, aggregate_results
from threading import Thread
import time

def start_streaming():
    """
    Starts the streaming process by simulating data stream, handling it, 
    and aggregating results, while launching the Streamlit dashboard.
    """
    dataset_path = "data/portugal_listings.csv"
    output_path = "data/aggregated_results.csv"

    os.makedirs("data", exist_ok=True)

    Thread(target=simulate_stream, args=(dataset_path,), daemon=True).start()
    Thread(target=stream_handler, daemon=True).start()
    Thread(target=aggregate_results, args=(output_path,), daemon=True).start()

    os.system("streamlit run dashboard.py")

if __name__ == "__main__":
    start_streaming()
