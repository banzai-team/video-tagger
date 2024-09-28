import pandas as pd
import re
from llama_index.core import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import Settings
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.indices import VectorStoreIndex
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.schema import MetadataMode



def make_view_name_from_tags(tags_str, max_level):
    tag_list = tags_str.split(', ')
    final_tag_list = []
    for tag in tag_list:
        tags = tag.split(": ")
        tags = tags[:min(len(tags), max_level)]
        final_tag_list.append(' -> '.join(tags))
    return final_tag_list


def split_tags(tag_list):
    final_tag_list = []
    for tag in tag_list:
        tags = tag.split(": ")
        if len(tags) == 3:
            final_tag_list.append(tags[0])
            final_tag_list.append(tags[0] + ": " + tags[1])
            final_tag_list.append(tags[0]+ ": " + tags[1] + ": " + tags[2])
        elif len(tags) == 2:
            final_tag_list.append(tags[0])
            final_tag_list.append(tags[0] + ": " + tags[1])
        elif len(tags) == 1:
            final_tag_list.append(tags[0])
        else:
            print("NOT IMPLEMENTED!!!!", tag)
    return final_tag_list

def join_tag_with_subtags(tag_list):
    return ": ".join(tag_list)


def create_docs(df):
    documents = []
    for _, row in df.iterrows():
        metadata = {
            "video_id": row.video_id,
            "Название видео": row.title,
            "tags": row.tags,
            "expand_tags": split_tags(row.tags.split(', '))
        }
        documents.append(
            Document(
                text=row.description[:min(len(row.description), 512)], 
                metadata=metadata, 
                excluded_embed_metadata_keys=["video_id", "tags"],
                metadata_template="{key}:\n---\n{value}\n---\n",
                text_template="{metadata_str}Описание видео:\n---\n{content}\n---\n"
            )
        )

    return documents


def read_data(filepath_csv):
    df = pd.read_csv(filepath_csv)
    df.dropna(inplace=True)
    return df


def load_embedder(model_name="intfloat/multilingual-e5-base"):
    Settings.embed_model = HuggingFaceEmbedding(model_name)


def make_retrieve_prompt(title, description):
    return (
        f'Название видео:\n---\n{title}\n---\n'
        f'Описание видео:\n---\n{description[:min(len(description), 512)]}\n---\n'
    )


class FixedMetaTokenTextSplitter(TokenTextSplitter):
    def _get_metadata_str(self, node) -> str:
        """Helper function to get the proper metadata str for splitting."""
        embed_metadata_str = node.get_metadata_str(mode=MetadataMode.EMBED)
        return embed_metadata_str


def build_few_shot_index(train_filepath_csv, model_name="intfloat/multilingual-e5-base") -> VectorStoreIndex:
    df = read_data(train_filepath_csv)
    docs = create_docs(df)
    load_embedder(model_name=model_name)
    index = VectorStoreIndex.from_documents(
        documents=docs, 
        show_progress=True,
        transformations=[
            FixedMetaTokenTextSplitter(
                separator=" ", chunk_size=1024, chunk_overlap=64,
                include_metadata=True,
            )
        ],
    )
    return index
