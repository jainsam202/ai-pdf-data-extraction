
import chainlit as cl
from app.rag.service import RAGService


@cl.on_chat_start
async def start():
    files = await cl.AskFileMessage(
        content="Upload a PDF to begin.",
        accept=["application/pdf"],
        max_size_mb=20,
        timeout=180,
    ).send()

    if files:
        pdf = files[0]

        await cl.Message(
            content=f"Uploaded: {pdf.name}"
        ).send()

        # Next step:
        # Send the PDF to your FastAPI upload endpoint
        # for document processing.


@cl.on_message
async def main(message: cl.Message):

    question = message.content
    result = RAGService.ask(question=question)
    source_text = ""

    if result["sources"]:
        source_text = "\n\n### Sources\n"

        for source in result["sources"]:
            source_text += (
                f"- Document: "
                f"{source.get('document_id')}\n"
            )

            source_text += (
                f"  Chunk: "
                f"{source.get('chunk_id')}\n"
            )

            source_text += (
                f"  Score: "
                f"{source.get('score')}\n"
            )

    await cl.Message(
        content=result["answer"] + source_text
    ).send()
