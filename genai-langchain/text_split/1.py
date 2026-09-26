#text splitting aloows us to process documents that would otherwise exceed the model's context limit. 
##length based
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(r"D:\python_ai\genai-langchain\Document_Loaders\2025341478.pdf")

docs=loader.load()

text="""The technology job market is undergoing a profound structural evolution, moving past the pandemic-era hiring booms and subsequent corporate corrections into a landscape defined by selective specialization and intense integration of artificial intelligence. While headline-grabbing layoffs at major tech conglomerates once dominated economic news, the broader ecosystem has stabilized, revealing a market that is simultaneously more demanding and deeply opportunistic for professionals with the right skill sets.

At the center of this transformation is the artificial intelligence and machine learning boom. Roles focusing on AI engineering, machine learning pipelines, and data architecture are experiencing unprecedented demand. Companies across sectors—ranging from healthcare and finance to traditional manufacturing—are racing to operationalize generative AI models, retrieval-augmented generation architectures, and automated agent workflows. Consequently, engineers who can bridge the gap between core software development and advanced data infrastructure command top-tier compensation and face a deeply competitive recruitment market.

Simultaneously, traditional software development roles have experienced a shift toward quality over quantity. The era of speculative hiring for generalist junior positions has largely receded, replaced by an emphasis on practical execution, system scalability, and domain-specific expertise. Employers increasingly look for candidates who demonstrate mastery over modern development stacks, cloud-native orchestration tools like Kubernetes and Docker, and rigorous security protocols. Cybersecurity and cloud infrastructure management remain exceptionally resilient areas, driven by an escalating threat landscape and the continuous migration of enterprise workloads to hybrid environments.

Geographically and structurally, tech employment has also decentralized. Traditional tech hubs like Silicon Valley and Seattle face competition from emerging regional ecosystems and fully remote or hybrid employment models. Non-tech enterprises—often referred to as "traditional" industries—now absorb a vast share of digital talent as every modern business transforms into a software-reliant organization. This diffusion cushions tech workers against localized industry contractions, opening diverse avenues outside of big tech.

For job seekers, the contemporary market rewards adaptability and continuous upskilling. The widespread adoption of AI-assisted coding tools has redefined productivity expectations, elevating the baseline technical proficiency required for entry- and mid-level roles. Professionals who pair foundational computer science principles with specialized competencies in data pipelines, secure coding, and intelligent agent development are finding themselves exceptionally well-positioned to navigate the shifting demands of the modern digital economy."""

text_splitter=CharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=10,
    separator=""
)

# For Document objects from loader.load(), use split_documents:
split_docs = text_splitter.split_documents(docs)
print(f"Split into {len(split_docs)} document chunks:")
for i, d in enumerate(split_docs):
    print(f"--- Chunk {i+1} ---")
    print(d.page_content[:100], "...")