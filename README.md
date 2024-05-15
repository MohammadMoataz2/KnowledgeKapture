# KnowledgeKapture: Information Retrieval System

 Made by [Masa Aladwan](https://github.com/MasaAladwan) and [Mohammad Moataz](https://github.com/MohammadMoataz2)

### Crawling And Search

## Overview
KnowledgeKapture is an information retrieval system and search engine designed to enable users to efficiently search through PDF, Word, and TXT files and crawling them. Leveraging Natural Language Processing (NLP) techniques, it preprocesses both files and queries to enhance search accuracy and crawling Process. The system ranks search results using a similarity ranking method for effective information retrieval. Additionally, a user-friendly interface built with tkinter facilitates easy query input and result display.


![image](https://github.com/MohammadMoataz2/KnowledgeKapture/assets/123085286/25aa0469-5554-4405-b81d-94976ee735e6)

## Features
- **Versatile Search:** Supports searching across diverse file formats including PDF, Word, and TXT.
- **NLP Preprocessing:** Utilizes NLTK preprocessing techniques for both files and queries.
- **Similarity Ranking:** Implements a similarity ranking method to deliver accurate and relevant search results.
- **User Interface:** Developed with tkinter for a seamless interaction experience.
- **File Crawling:** Conducts crawling to create an inverse index for efficient searching.

## Achievements
- Designed and implemented a versatile search engine for diverse file formats, enhancing information retrieval efficiency.
- Leveraged NLTK preprocessing and similarity ranking methods to deliver accurate and relevant search results.
- Developed an intuitive user interface for seamless interaction with the search engine.




## Pipeline

![image](https://github.com/MohammadMoataz2/KnowledgeKapture/assets/123085286/6bfc87d2-39fc-43ad-92d1-3441c11d6e51)

The KnowledgeKapture system follows the following pipeline:

1. **Add File:** Users can add files in PDF, Word, or TXT formats to the system.
2. **Crawling:** The system conducts crawling to gather data from added files.
3. **Inverted Index:** It then creates an inverted index from the crawled data for efficient searching.
4. **Query:** Users input their query through the user-friendly interface.
5. **Search:** The system searches through the inverted index using NLP techniques.
6. **Retrieve Document:** Relevant documents matching the query are retrieved and displayed to the user.



## Technologies Used
- **Python:** Utilizes pandas and NumPy for data manipulation.
- **Natural Language Processing (NLP):** Employs NLTK for preprocessing.
- **User Interface:** tkinter for GUI development.
- **Crawling:** Implements crawling techniques for creating an inverse index.
- **File Formats:** Supports PDF, Word, and TXT.


![image](https://github.com/MohammadMoataz2/KnowledgeKapture/assets/123085286/565f1c82-036b-45a0-8bf4-6e75bde8f261)

## Installation
1. Clone the repository:

git clone https://github.com/MohammadMoataz2/KnowledgeKapture.git

2. Install dependencies:

pip install -r requirements.txt

## Usage
1. Run the application:

python KnowledgeKapture.py

2. Input your query in the provided interface.
3. View the search results displayed.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

