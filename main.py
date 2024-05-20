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


# Usage example:
file_name = 'file.txt'
text_file = 'links.txt'  # Replace this with your actual text file name

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

def search_word(word_file_map, word):
    # Return the list of files for the given word, or an empty list if the word is not found
    return word_file_map.get(word, [])

def search_page_rank(word):
    file_path = "page-rank.txt"
    files = search_word(load_word_file_map(file_path),word)
    text_file = 'links.txt'
    ans = []
    for file_name in files:
        temp = find_link_info(file_name, text_file)
        if len(temp) != 0 :
            ans.append({"url": temp[0], "name": temp[1]},)

    return ans

def search_tf_idf(word):
    file_path = "tf-idf.txt"
    files = search_word(load_word_file_map(file_path), word)
    text_file = 'links.txt'
    ans = []
    for file_name in files:
        temp = find_link_info(file_name, text_file)
        if len(temp) != 0:
            ans.append({"url": temp[0], "name": temp[1]}, )

    return ans

def search_inverted_index(word):
    file_path = "inverted-index.txt"
    files = search_word(load_word_file_map(file_path), word)
    text_file = 'links.txt'
    ans = []
    for file_name in files:
        temp = find_link_info(file_name, text_file)
        if len(temp) != 0:
            ans.append({"url": temp[0], "name": temp[1]}, )

    return ans

def main():
    st.title("Word Link Search")

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
