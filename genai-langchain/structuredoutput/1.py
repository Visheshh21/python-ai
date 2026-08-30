from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal

load_dotenv()

model = ChatGroq(model_name='openai/gpt-oss-20b',temperature=0.5,max_tokens=None)

# Simple TypedDict
# class review(TypedDict):
#     summary: str 
#     sentiment: str

#Annotated TypedDict
class review(TypedDict):
    summary: Annotated[str,"A brief Summary of the review under 100 words"]
    sentiment: Annotated[Literal["Positive","Negative"],"Sentiment of the review (positive/negative)"]
    rating: Annotated[str,"Rating of the review (1-5)"]  
    pros: Annotated[Optional[list[str]],"Write down all the pros inside a list"]
    cons: Annotated[Optional[list[str]],"Write down all the cons inside a list, If they are explicitly mentioned in the review"]

structured_model=model.with_structured_output(review)

result=structured_model.invoke("""I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast–whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera–the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware–why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful

""")

print(result)
 