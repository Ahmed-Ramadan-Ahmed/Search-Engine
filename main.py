import os
import streamlit as st
import re
from urllib.parse import urlparse
# Directory containing your files
folder_path = "All files"
file_map = {}

# Function to extract link from the first line of a file
def extract_link(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        first_line = file.readline().strip()
        return first_line


with open('final.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # Split the line by comma
        parts = line.strip().split(', ')

        # Extract filename and link
        filename = parts[0]
        link = parts[1]

        # Map the filename to the link
        file_map[filename] = link

# with open("final.txt", "w", encoding='utf-8') as file:
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         if os.path.isfile(file_path):  # Check if it's a file
#             link = extract_link(file_path)
#             file_map[filename] = link
#             match =  re.search(r'https://([^/]+)', link)
#             if(match): word_between_http_and_dot = match.group(1)
#             else: word_between_http_and_dot=""
#             file.write(filename + ", " + link + ", " + word_between_http_and_dot+ "\n")

def create_link_dictionary(file_path, word_to_search, file_map):
    link_dict = {}
    with open(file_path, "r", encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 2:
                word = parts[0].strip()
                # Check if the start of 'word' matches 'word_to_search'
                if not word.startswith(word_to_search):
                    continue
                file_names = [file_map[file.strip()] for file in parts[1].split(",") if file.strip() in file_map]
                if word_to_search not in link_dict:
                    link_dict[word_to_search] = []
                for ff in file_names:
                   link_dict[word_to_search].append(ff)
    return link_dict

def search_word(word, link_dict):
    if word in link_dict:
        return link_dict[word]
    else:
        return "Word not found in the file."

# Streamlit app
st.title("Word Search Engine")

linkedin_url = r"https://www.linkedin.com/in/ahmed-ramadan-348264225/"
github_url = r"https://github.com/Ahmed-Ramadan-Ahmed"
leetcode_url = r"https://leetcode.com/u/A_Ramadan_A/"
codeforces_url = r"https://codeforces.com/profile/Master_by2025"
email = "aramadan442000@gmail.com"
st.sidebar.image(r"Ahmed.jpg", width=100)
# Create a sidebar
with st.sidebar:
    with st.sidebar.container():
        st.write("Connect with me:")
        # Mail
        st.markdown(f"[![Email](https://img.shields.io/badge/Email-Contact-informational)](mailto:{email})")
        # GitHub badge
        st.markdown(f"[![GitHub](https://img.shields.io/badge/GitHub-Profile-green)]({github_url})")
        # LinkedIn badge
        st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue)]({linkedin_url})")
        # LeetCode badge
        st.markdown(f"[![LeetCode](https://img.shields.io/badge/LeetCode-Profile-red)]({leetcode_url})")
        # Codeforces badge
        st.markdown(f"[![Codeforces](https://img.shields.io/badge/Codeforces-Profile-purple)]({codeforces_url})")



search_method = st.selectbox("Choose Search Method:", ["By Page Rank", "By TF-IDF", "By inverted-index"])
word = st.text_input("Enter a word:")

if st.button("Search"):
    if search_method == "By Page Rank":
        file_path = "page-rank.txt"
    elif search_method == "By TF-IDF":
        file_path = "tf-idf.txt"
    elif search_method == "By inverted-index":
        file_path = "inverted-index.txt"

    if word:
        link_dict = create_link_dictionary(file_path, word, file_map)
        result = search_word(word, link_dict)

        if result != "Word not found in the file.":
            for link in result:
                st.markdown(f"- [{link}]({link})")
        else:
            st.error(f"The word '{word}' was not found in the links.")
    else:
        st.warning("Please enter a word to search.")
