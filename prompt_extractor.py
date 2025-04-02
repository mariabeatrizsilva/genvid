import os
import pandas as pd

class PromptExtractor:
    def __init__(self, dataframe, file_beginnings):
        """
        Initializes the PromptExtractor with a dataframe containing UUIDs and prompts.

        Args:
            dataframe (pd.DataFrame): DataFrame with 'uuid' and 'prompt' columns.
        """
        self.dd = dataframe
        self.ff = file_beginnings
        
    def prompt_from_id(self, video_id):
        """
        Given a video_id (uuid), return the corresponding prompt from the dataframe.
        """
        entry = self.dd[self.dd['uuid'] == video_id]
        if not entry.empty:
            return entry['prompt'].values[0], int(entry.index[0])  # Return the prompt and its index in the dataframe
        else:
            return None
        
    def process_video_files(self, video_files,csv_path='processed_video_data.csv'):
        """
        Processes video files, extracts UUIDs, prefixes, and associated prompts,
        and stores them in a structured data format.

        Args:
            video_files (list): A list of video file names.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing UUID, prefix, and prompt.
        """

        data = []  # Initialize an empty list to store the structured data
        processed_count = 0
        total_videos = len(video_files)

        for file in video_files:
            # print ("Processing file: {file}")
            for prefix in self.ff:
                if file.startswith(prefix):
                    uuid = file[len(prefix):].split('.')[0]  # Remove prefix and file extension
                    print(uuid)

                    prompt_info = self.prompt_from_id(uuid)
                    if prompt_info:
                        prompt, index = prompt_info
                        data.append({
                            "uuid": uuid,
                            "prefix": prefix,
                            "prompt": prompt
                        })
                        # print(f"Found prompt for uuid: {uuid} with prefix: {prefix}. Prompt: {prompt}")
                    else:
                        data.append({
                            "uuid": uuid,
                            "prefix": prefix,
                            "prompt": None
                        })
                        print(f"No prompt found for uuid: {uuid}")

                    break  # Move to the next file after finding a matching prefix
            processed_count += 1
            if processed_count % 20 == 0 or processed_count == total_videos:
                percentage = (processed_count / total_videos) * 100
                print(f"Processed {processed_count}/{total_videos} videos ({percentage:.2f}%)")

        # save data to csv and return
        data_df = pd.DataFrame(data)
        data_df.to_csv(csv_path, index=False)  # Save to CSV for future use
        return data_df

    @staticmethod
    def list_video_files(folder):
        """
        List all video files in the given folder.
        """
        if not os.path.exists(folder):
            print(f"Folder {folder} does not exist.")
            return []

        files = os.listdir(folder)
        video_files = [f for f in files if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        return video_files
    
    @staticmethod
    def list_video_files_multi(folders):
        """
        List all video files in the given folder(s).

        Args:
            folders: A string (single folder path) or a list of strings (multiple folder paths).

        Returns:
            A list of strings, where each string is the full path to a video file.
        """

        all_video_files = []

        if isinstance(folders, str):  # Single folder
            folders = [folders]  # Make it a list for consistent processing

        for folder in folders:
            print(f"Listing video files in folder: {folder}")
            all_video_files.extend(PromptExtractor.list_video_files(folder))  # Call the single-folder function

        return all_video_files
