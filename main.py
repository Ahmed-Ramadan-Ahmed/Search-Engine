import streamlit as st
import os

# Directory containing your files
folder_path = "All_Files"
file_map = {}


# Function to extract link from the first line of a file
def extract_link(file_path):
    with open(file_path, "r") as file:
        first_line = file.readline().strip()
        return first_line


# Iterate over files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):  # Check if it's a file
        link = extract_link(file_path)
        file_map[filename] = link


def create_link_dictionary(file_path, word_to_search):
    link_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 2:
                word = parts[0].strip()
                if word != word_to_search:
                    continue
                file_names = [file_map[file.strip()] for file in parts[1].split(",")]
                link_dict[word] = file_names
                break
    return link_dict


def search_word(word, link_dict):
    if word in link_dict:
        return link_dict[word]
    else:
        return "Word not found in the file."


def search_page_rank(word):
    file_path = "page-rank.txt"
    link_dict = create_link_dictionary(file_path, word)
    return search_word(word, link_dict)


def search_tf_idf(word):
    file_path = "tf-idf.txt"
    link_dict = create_link_dictionary(file_path, word)
    return search_word(word, link_dict)


def search_inverted_index(word):
    file_path = "inverted-index.txt"
    link_dict = create_link_dictionary(file_path, word)
    return search_word(word, link_dict)


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

            if result == "Word not found in the file.":
                st.error(f"The word '{word}' was not found in the links.")
            else:
                st.text_area("Links found:", "\n".join(result))
        else:
            st.warning("Please enter a word to search.")


if __name__ == "__main__":
    main()







