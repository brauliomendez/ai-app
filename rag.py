import streamlit as st
from openai import OpenAI

from translator import translate

VECTOR_STORE_ID = "vs_68f6050871e08191af5917a15a37b40d"


def get_client() -> OpenAI:
    api_key = st.session_state.get("openai_api_key")
    if not api_key:
        raise ValueError(translate("rag.missing_api_key"))
    return OpenAI(api_key=api_key)


def stream_vector_search(chat_history, placeholder):
    """Stream the assistant response with markdown updates."""
    text_chunks = []
    try:
        client = get_client()
        with client.responses.stream(
            model="gpt-5-mini",
            input=chat_history,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [VECTOR_STORE_ID],
                }
            ],
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    text_chunks.append(event.delta)
                    placeholder.markdown("".join(text_chunks))
                elif event.type == "response.completed":
                    return event.response.output_text
    except ValueError as missing_key_err:
        placeholder.error(str(missing_key_err))
        return None
    except Exception as exc:
        placeholder.error(translate("rag.error_message", error=str(exc)))
        return None

    return "".join(text_chunks)


def upload_and_index_file(file):
    client = get_client()
    uploaded_file = client.files.create(
        file=file,
        purpose="assistants"
    )
    client.vector_stores.files.create(
        vector_store_id=VECTOR_STORE_ID,
        file_id=uploaded_file.id
    )


def get_indexed_files():
    client = get_client()
    files = client.vector_stores.files.list(vector_store_id=VECTOR_STORE_ID)
    if len(files.data) == 0:
        return []

    filenames = []
    for file in files.data:
        file_info = client.files.retrieve(file.id)
        filenames.append({
            "id": file.id,
            "name": file_info.filename
        })

    return filenames


def delete_file(file_id):
    client = get_client()
    deleted_vs_file = client.vector_stores.files.delete(
        vector_store_id=VECTOR_STORE_ID,
        file_id=file_id
    )
    if deleted_vs_file:
        deleted_file = client.files.delete(file_id)
        return deleted_file.deleted
    else:
        return False


def reset_chat_history():
    st.session_state.chat_history_rag = [
        {"role": "assistant", "content": translate("rag.default_assistant_message")}
    ]


if "chat_history_rag" not in st.session_state:
    reset_chat_history()

# UI

if not st.session_state.get("openai_api_key"):
    st.info(translate("rag.missing_api_key"))
    st.stop()

st.title(translate("rag.title"))
st.divider()

st.header(translate("rag.upload_header"))

if "uploader_version" not in st.session_state:
    st.session_state.uploader_version = 0

files = st.file_uploader(
    translate("rag.uploader_help"),
    type=["pdf"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_version}"
)

if files:
    if st.button(translate("rag.index_button"), type="primary", key="index"):
        for file in files:
            with st.spinner(translate("rag.indexing_spinner")):
                upload_and_index_file(file)
        st.session_state.uploader_version += 1
        st.toast(translate("rag.file_indexed_toast", filename=file.name))
        st.rerun()

st.write(translate("rag.indexed_files_label"))
with st.spinner(translate("rag.loading_spinner")):
    files = get_indexed_files()

if len(files) == 0:
    st.badge(translate("rag.empty_badge"), color="grey")
else:
    col1, col2 = st.columns(2)
    for file in files:
        with col1:
            st.write(f" - {file['name']}")
        with col2:
            if st.button(translate("rag.remove_button"), key=f"remove_{file['id']}"):
                with st.spinner(translate("rag.deleting_spinner")):
                    success = delete_file(file["id"])
                if success:
                    st.toast(translate("rag.file_deleted_toast", filename=file["name"]))
                    st.rerun()
                else:
                    st.toast(translate("rag.file_error_toast", filename=file["name"]))

st.divider()

col3, col4 = st.columns(2)
with col3:
    st.header(translate("rag.chat_header"))
with col4:
    if st.button(translate("rag.clear_history_button")):
        reset_chat_history()

for message in st.session_state.chat_history_rag:
    st.chat_message(message["role"]).markdown(message["content"])

if prompt := st.chat_input(translate("rag.chat_input_placeholder")):
    st.session_state.chat_history_rag.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    assistant_message = st.chat_message("assistant")
    placeholder = assistant_message.empty()

    response = stream_vector_search(st.session_state.chat_history_rag, placeholder)

    if response:
        st.session_state.chat_history_rag.append({"role": "assistant", "content": response})
