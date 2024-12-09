import pandas as pd
import time
import queue
import os
import logging

pd.options.mode.chained_assignment = None

logging.basicConfig(
    filename="stream_processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

stream_queue = queue.Queue()
all_data_processed = False

aggregated_data = pd.DataFrame()


def simulate_stream(dataset_path: str, batch_size: int = 10):
    """
    Simulates streaming by reading a dataset in batches and adding records to a queue.
    """
    try:
        if not os.path.exists(dataset_path):
            logging.error(f"Dataset `{dataset_path}` not found.")
            return

        logging.info(f"Simulating stream from dataset: {dataset_path}")
        df = pd.read_csv(dataset_path)

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]
            for _, record in batch.iterrows():
                stream_queue.put(record.to_dict())
            logging.info(f"Streamed {len(batch)} records to the queue.")
            time.sleep(1)
        
        global all_data_processed
        all_data_processed = True
        logging.info("All data has been streamed.")
    except Exception as e:
        logging.error(f"Error during streaming simulation: {e}")


def process_batch(batch_df):
    """
    Processes a batch of records, applying filtering and grouping logic.
    """
    try:
        filtered = batch_df[
            (batch_df["Price"] >= 50000) | (batch_df["LivingArea"] >= 20)
        ]
        
        filtered.loc[:, "Avg_Price_per_Sqm"] = filtered.apply(
            lambda x: x["Price"] / x["LivingArea"] if x["LivingArea"] > 0 else float('nan'),
            axis=1
        )

        grouped = filtered.groupby(["District", "Type"]).agg(
            Avg_Price=("Price", "mean"),
            Avg_Area=("LivingArea", "mean"),
            Count=("Price", "count"),
            Avg_Price_per_Sqm=("Avg_Price_per_Sqm", "mean")
        ).reset_index()

        grouped = grouped.rename(columns={"Type": "Property_Type"})

        return grouped
    except Exception as e:
        logging.error(f"Error processing batch: {e}")
        return pd.DataFrame()


def stream_handler():
    """
    Handles records from the stream queue for processing.
    Continuously fetches records from the queue, processes them, and updates aggregated results.
    """
    global aggregated_data
    try:
        logging.info("Stream handler started.")
        buffer = []
        while not (all_data_processed and stream_queue.empty()):
            try:
                record = stream_queue.get(timeout=1)
                buffer.append(record)

                if len(buffer) >= 10 or (all_data_processed and len(buffer) > 0):
                    batch_df = pd.DataFrame(buffer)
                    processed_batch = process_batch(batch_df)

                    aggregated_data = pd.concat([aggregated_data, processed_batch])
                    aggregated_data = aggregated_data.groupby(
                        ["District", "Property_Type"]
                    ).agg(
                        Avg_Price=("Avg_Price", "mean"),
                        Avg_Area=("Avg_Area", "mean"),
                        Count=("Count", "sum"),
                        Avg_Price_per_Sqm=("Avg_Price_per_Sqm", "mean")
                    ).reset_index()

                    buffer.clear()
                    logging.info("Processed a batch of records and updated aggregates.")

                stream_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logging.exception(f"Error in stream_handler: {e}")

        logging.info("Stream handler finished processing.")
    except Exception as e:
        logging.error(f"Error initializing stream_handler: {e}")


def aggregate_results(output_path: str):
    """
    Saves aggregated results to a file every 30 seconds.
    """
    try:
        logging.info(f"Starting aggregation to `{output_path}`")
        while not (all_data_processed and stream_queue.empty()):
            if not aggregated_data.empty:
                if os.path.exists(output_path):
                    aggregated_data.to_csv(output_path, mode='a', header=False, index=False)
                    logging.info(f"Aggregated data appended to `{output_path}`.")
                else:
                    aggregated_data.to_csv(output_path, mode='w', header=True, index=False)
                    logging.info(f"Aggregated data saved to `{output_path}`.")
            time.sleep(30)

        logging.info("Final aggregation completed.")
    except Exception as e:
        logging.error(f"Error during aggregation: {e}")
