from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma


class VectorDb:
    def __init__(self):
        data = open("./data/project_data_카카오싱크.txt", 'r').read().strip()
        self.db = self.insert(data)

    def insert(self, text, chunk_size=1000):
        splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        splitted_text = splitter.split_text(text)
        embeddings = OpenAIEmbeddings()
        return Chroma.from_texts(
            splitted_text, embeddings, metadatas=[{"source": str(i)} for i in range(len(splitted_text))]
        )

    def query(self, q, number=3):
        return self.db.as_retriever(search_kwargs={'k': number}).get_relevant_documents(q)
