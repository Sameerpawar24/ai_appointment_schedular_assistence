# from openai import AsyncOpenAI
# from groq import AsyncGroq
# from langchain_groq import ChatGroq
# # from test.tool.tools import add,add_appointment,check_doctor_availability,get_current_datetime_ist
# from test.tool.tools import add,book_appointment,add_appointment,view_appointments,view_doctor_schedule
# from test.llm.prompt import prompt
# from langchain_core.messages import HumanMessage, AIMessage, ToolMessage,SystemMessage
# import os
# from test.core.config import settings



# # Initialize Groq model
# llm = ChatGroq(
#     model=settings.CHAT_MODEL,
#     groq_api_key=settings.GROQ_API_KEY,
#     temperature=0
# )

# # Bind tools
# # llm_with_tools = llm.bind_tools([ check_doctor_availability,
# #     add_appointment,
# #     get_current_datetime_ist])

# llm_with_tools = llm.bind_tools([add_appointment,view_appointments,view_doctor_schedule])


# async def generate_response(memory):

#     # Insert system message once (convert to proper message object)
#     if not any(isinstance(msg, SystemMessage) for msg in memory):
#         memory.insert(0, SystemMessage(
#             content=prompt
#         ))
        
#     #OPTION 1
#     # # First LLM call (with tools enabled)
#     # response = await llm_with_tools.ainvoke(memory)

#     # # Add assistant response to memory
#     # memory.append(response)

#     # # If tool was triggered
#     # if response.tool_calls:
#     #     tool_call = response.tool_calls[0]

#     #     if tool_call["name"] == "add_appointment":
#     #         # Execute tool
#     #         result = add_appointment.invoke(tool_call["args"])
#     #     elif tool_call["name"] == "view_appointments":
#     #         result = view_appointments.invoke(tool_call["args"])
#     #     elif tool_call["name"] == "view_doctor_schedule":
#     #         result = view_doctor_schedule.invoke(tool_call["args"])
#     #     else:
#     #         result = "Unknown tool"

#     #         # Append proper ToolMessage with correct ID
#     #         memory.append(
#     #             ToolMessage(
#     #                 content=str(result),
#     #                 tool_call_id=tool_call["id"]   # MUST match actual id
#     #             )
#     #         )

#     #         # Second LLM call (to generate final user-facing message)
#     #         final_response = await llm_with_tools.ainvoke(memory)

#     #         return final_response.content

#     # # If no tool triggered
#     # return response.content

#     #OPTION 2
#     # response = await llm_with_tools.ainvoke(memory)
#     # memory.append(response)

#     # while response.tool_calls:

#     #     for tool_call in response.tool_calls:

#     #         if tool_call["name"] == "book_appointment":
#     #             result = book_appointment.invoke(tool_call["args"])
#     #         elif tool_call["name"] == "view_appointments":
#     #             result = view_appointments.invoke(tool_call["args"])
#     #         else:
#     #             result = "Unknown tool"

#     #         memory.append(
#     #             ToolMessage(
#     #                 content=str(result),
#     #                 tool_call_id=tool_call["id"]
#     #             )
#     #         )

#     #     # Call model again after tool execution
#     #     response = await llm_with_tools.ainvoke(memory)
#     #     memory.append(response)

#     # # Only return non-empty content
#     # return response.content if response.content else "Your appointment has been successfully scheduled."


#     #OPTION 3
#     response = await llm_with_tools.ainvoke(memory)
#     memory.append(response)

#     if response.tool_calls:
#         tool_call = response.tool_calls[0]

#         # if tool_call["name"] == "add_appointment":
#         #     result = add_appointment.invoke(tool_call["args"])
#         # elif tool_call["name"] == "get_current_datetime_ist":
#         #     result = get_current_datetime_ist.invoke(tool_call["args"])
#         # elif tool_call["name"] == "check_doctor_availability":
#         #     result = check_doctor_availability.invoke(tool_call["args"])
#         # else:
#         #     result = f"Unknown tool: {tool_call['name']}

#     if response.tool_calls:
#         tool_call = response.tool_calls[0]

#         if tool_call["name"] == "add_appointment":
#             result = add_appointment.invoke(tool_call["args"])
#         elif tool_call["name"] == "view_appointments":
#             result = view_appointments.invoke(tool_call["args"])
#         elif tool_call["name"] == "view_doctor_schedule":
#             result = view_doctor_schedule.invoke(tool_call["args"])
#         else:
#             result = f"Unknown tool: {tool_call['name']}"

 
#         return str(result)

#     # If no tool triggered
#     return response.content


#___________________________________________________________________________________________________________


from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, ToolMessage
from test.tool.tools import (
    check_doctor_availability,
    add_appointment,
    reschedule_appointment
)

from test.llm.prompt import prompt
from test.core.config import settings


# -----------------------------
# Initialize LLM
# -----------------------------

llm = ChatGroq(
    model=settings.CHAT_MODEL,
    groq_api_key=settings.GROQ_API_KEY,
    temperature=0,
)


# bind tools
llm_with_tools = llm.bind_tools([
    check_doctor_availability,
    add_appointment,
    reschedule_appointment
])


# -----------------------------
# Generate Response
# -----------------------------

async def generate_response(memory):

    if not any(isinstance(msg, SystemMessage) for msg in memory):
        memory.insert(0, SystemMessage(content=prompt))


    response = await llm_with_tools.ainvoke(memory)

    memory.append(response)


    # -----------------------------
    # TOOL EXECUTION
    # -----------------------------

    while response.tool_calls:

        tool_call = response.tool_calls[0]


        # if tool_call["name"] == "check_doctor_availability":
        #     result = check_doctor_availability.invoke(tool_call["args"])
        args = tool_call["args"]

        if tool_call["name"] == "check_doctor_availability":

            if not all(k in args for k in ["doctor_name","date","time"]):
                return "Please provide doctor name date and time."

            result = check_doctor_availability.invoke(args)

        elif tool_call["name"] == "add_appointment":
            result = add_appointment.invoke(tool_call["args"])

        elif tool_call["name"] == "reschedule_appointment":
            result = reschedule_appointment.invoke(tool_call["args"])
            

        else:
            result = "TOOL_ERROR"


        memory.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
        )


        response = await llm_with_tools.ainvoke(memory)

        memory.append(response)


    return response.content