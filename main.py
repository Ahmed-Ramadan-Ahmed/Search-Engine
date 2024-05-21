import streamlit as st
import os

def find_link_info(file_name, text_file):
    with open(text_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split(', ')
        if parts[0] == file_name:
            return [parts[1], parts[2]]
    return None

def load_word_file_map(filename):
    word_file_map = {}

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Split the line into word and file names
            word, files = line.split(': ')
            # Remove trailing newlines and split the file names into a list
            file_list = files.strip().split(', ')
            # Add the word and corresponding file list to the dictionary
            word_file_map[word] = file_list

    return word_file_map

def get_file_names(word, file_path):
    # Read the file and split lines
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Create a dictionary to store file names and frequencies
    file_freq = []
    for line in lines:
        Word, parts = line.split('\t')
        if(Word != word):
            continue

        parts = parts.split(';')
        for part in parts:
            if(len(part.split(':'))<2):
                continue
            file = part.split(':')[0]
            freq = int(part.split(':')[1])
            file_freq.append((file,int(freq)))

    # Sort the dictionary based on frequencies in descending order
    sorted_files = sorted(file_freq, key=lambda x: x[1], reverse=True)
    # Return a sorted list of file names

    return sorted_files


def search_word(word_file_map, word):
    # Return the list of files for the given word, or an empty list if the word is not found
    return word_file_map.get(word, [])

def search_page_rank(word):
    file_path = "page-rank.txt"
    files = search_word(load_word_file_map(file_path),word)
    text_file = 'Links.txt'
    ans = []
    for file_name in files:
        temp = find_link_info(file_name, text_file)
        if len(temp) != 0 :
            ans.append({"url": temp[0], "name": temp[1]},)

    return ans

def search_tf_idf(word):
    file_path = "tf-idf.txt"
    files = search_word(load_word_file_map(file_path), word)
    text_file = 'Links.txt'
    ans = []
    for file_name in files:
        temp = find_link_info(file_name, text_file)
        if len(temp) != 0:
            ans.append({"url": temp[0], "name": temp[1]}, )

    return ans

def search_inverted_index(word):
    file_path = "inverted-index.txt"
    files = get_file_names(word,file_path)
    text_file = 'Links.txt'
    ans = []
    for file_name, freq in files:
        file_name = file_name + ".txt"
        temp = find_link_info(file_name, text_file)
        ans.append({"url": temp[0], "name": temp[1]})

    return ans

def main():
    # search_inverted_index("mo")
    # return
    st.title("Search Engine")

    linkedin_url = "https://www.linkedin.com/in/ahmed-ramadan-348264225/"
    github_url = "https://github.com/Ahmed-Ramadan-Ahmed"
    leetcode_url = "https://leetcode.com/u/A_Ramadan_A/"
    codeforces_url = "https://codeforces.com/profile/Master_by2025"
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

    search_method = st.selectbox("Choose Search Method:", ["By Page Rank", "By TF-IDF", "inverted-index"])
    word = st.text_input("Enter a word:")

    if st.button("Search"):
        if word:
            if search_method == "By Page Rank":
                result = search_page_rank(word)
            elif search_method == "By TF-IDF":
                result = search_tf_idf(word)
            elif search_method == "inverted-index":
                result = search_inverted_index(word)

            if len(result) == 0 :
                st.error(f"The word '{word}' was not found in the links.")
            else:

                for key, value in enumerate(result):
                    url = value["url"]
                    name = value["name"]
                    st.markdown(f"[**{name}**]({url})")
                    # st.text_area("Links found:", "".join(f"[{name}]({url})"))
        else:
            st.warning("Please enter a word to search.")


if __name__ == "__main__":
    main()
