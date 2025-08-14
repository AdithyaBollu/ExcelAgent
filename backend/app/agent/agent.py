"""Run this model in Python

> pip install openai
"""
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
# import gradio as gr
import tempfile

import logging

from .tools.nutrition import get_nutrition_info
from .tools.weather import get_weather_data
from .tools.fileIO import read_file, create_file
from .tools.excelIO import create_excel_file, create_new_sheet, read_excel_file, add_formula_to_excel, write_to_cell


logging.basicConfig(level=logging.INFO)
# from openpyxl.pivot.table import PivotTable
# from openpyxl.chart import Reference


# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

load_dotenv()
client = OpenAI(
    api_key = os.environ["OPENAI_API_KEY"],
)


# def create_excel_pivot_table(file_path, pivot_table_name, data_range, row_fields, column_fields, value_fields):
#     wb = openpyxl.load_workbook(file_path)
#     sheet = wb.active  # or wb['Sheet1']

#     pivot_table = PivotTable(
#         name=pivot_table_name,
#         data=Reference(sheet, range_string=data_range),
#         rows=row_fields,
#         columns=column_fields,
#         values=value_fields
#     )

#     sheet.add_pivot_table(pivot_table)

#     wb.save("./createdFiles/" + os.path.basename(file_path))
#     return f"Pivot table '{pivot_table_name}' created in {file_path}", f"./createdFiles/{os.path.basename(file_path)}"

SYSTEM_PROMPT = {
        "role": "system",
        "content": '''You are a nutrition expert well-versed in dietary plans and nutritional information. Provide users with:
        1. Tailored dietary recommendations for specific goals, including cutting, bulking, keto, or Mediterranean diets.
        2. Macronutrient breakdowns (e.g., protein, carbs, fat) for any food item and adjustments based on specific dietary needs.
        3. Use the get_nutrition_info Tool when you need to look up nutritional info for any food item.
        4. Use the read_file tool when users upload files or reference file paths.
        5. Use the get_weather_data tool when users ask for weather information for cities or locations.
        IMPORTANT: when using functions:
        1. Please ensure you use the correct parameters as defined in the function's description.
    
        IMPORTANT: When a user asks you to modify a file:
        1. First use read_file to get the file contents
        2. Then generate the new content based on the user's request
        3. Use create_file to write the new content to the file

        IMPORTANT: When a user asks you to read a file and get weather data for cities in that file:
        1. First use read_file to get the file contents
        2. Parse the cities from the file content
        3. Then use get_weather_data for EACH city found in the file
        4. Provide a complete weather report for all cities
        
        #IMPORTANT When user asks anything to do with an excel file:
        1. Use read_excel_file to read the file and get valuable cells
        2. If the user asks to add a formula, use add_formula_to_excel with the provided parameters
            1. For the formula_template argument, the arg is "forumla_template" not "formula_template=".
            2. Make sure both start_row and end_row are provided.
        3. If the user asks to create a new column use write_to_cell to write the title of the column
        4. If the user asks to write a value to a specific cell, use write_to_cell with the provided parameters
        5. If the user asks to create a new sheet, use create_new_sheet with the provided parameters
        
        # IMPORTANT If asked to create an Excel File or store to an Excel File:
        1. Use create_excel_file to create the file
        2. READ THE EXCEL FILE USING read_excel_file
        3. If the user asks to add a formula, use add_formula_to_excel with the provided parameters
            1. For the formula_template argument, the arg is "forumla_template" not "formula_template=".
            2. Make sure both start_row and end_row are provided.
        4. If the user asks to create a new column use write_to_cell to write the title of the column
        5. If the user asks to write a value to a specific cell, use write_to_cell with the provided parameters
        6. If the user asks to create a new sheet, use create_new_sheet with the provided parameters
        
        

        You have access to real-time weather data through the get_weather_data function. Always use this tool when weather information is requested.
        
        # Steps:
        # 1. Understand the user's dietary goal or query, such as food macros or diet-specific recommendations.
        # 2. If asking about food macros, provide specific values for protein, carbohydrates, and fat for the given food.
        # 3. If asking for dietary recommendations, list foods or meals that align with the user's diet and goal.
        # 4. If a file is mentioned or uploaded, use read_file to access its contents.
        # 5. If weather data is requested, use get_weather_data for the specified location(s).
        # 6. Present all information clearly and concisely.

        ## Examples:
        # - "What macros are in chicken breast for a keto diet?"
        # - "Can you recommend meals for bulking?"
        # - "Read the uploaded file and tell me about the cities"
        # - "What's the weather like in New York?"
        # - "Read the cities file and get weather data for each city"
        # 
        # Output Format:
        # Provide responses in clear, user-friendly text. For macro breakdown requests, use this structure:
        # - Food: [Food Name]
        # - Protein: [Value in grams]
        # - Carbohydrates: [Value in grams]
        # - Fats: [Value in grams]
        # 
        # For dietary recommendations:
        # - Goal: [Diet Goal]
        # - Recommendations: [Meal or food items]
        #
        # For weather data:
        # - City: [City Name]
        # - Temperature: [Current temperature]
        # - Conditions: [Weather conditions]
        # - Additional details as available''',
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_nutrition_info",
            "description": "Gets the nutritional information in the food provided. Use any time you need to look up the nutritional value of a food in a query. Example: is Salmon hleahty? what macors does salmon have?",
            "parameters": {
                "type": "object",
                "properties": {
                    "food_name": {
                        "type": "string",
                        "description": "The name of the food item to get nutrition info for"
                    }
                },
                "additionalProperties": False,
                "required": [
                    "food_name"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a file uploaded by the user. Use this to process any files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read. This should be a valid file path on the server where the model is running."
                    }
                },
                "additionalProperties": False,
                "required": [
                    "file_path"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_data",
            "description": "gets the current weather data for a given location. Use this to provide weather information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get weather data for. This can be a city name, state, or country."
                    }
                },
                "additionalProperties": False,
                "required": [
                    "location"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Creates a new file with the specified content. Use this to create new files based on user requests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to create. This should be a valid file name without extension."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the new file. This will be the initial content of the file."
                    },
                    "extension": {
                        "type": "string",
                        "description": "The file extension to use for the created file. This should be a valid file extension (e.g., .txt, .json) make sure the extension is prefixed with a '.' ."
                    }
                },
                "additionalProperties": False,
                "required": [
                    "file_name",
                    "content",
                    "extension"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_excel_file",
            "description": "Creates a new excel file with the specified name, use this to create new Excel files",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the new excel file to be created"
                    }
                },
                "additionalProperties": False,
                "required": [
                    "file_name"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_excel_file",
            "description": "reads an Excel file and returns the valuable cells with their coordinates. Use this to process Excel files.",
            "parameters": {
                "type": "object",
                "properties": {
                   "file_path": {
                        "type": "string",
                        "description": "The path to the Excel file to read. This should be a valid file path on the server where the model is running."
                    }
                },
                "additionalProperties": False,
                "required": [
                    "file_path"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "add_formula_to_excel",
            "description": "Adds a formula to a specified column in an Excel file. Use this to apply formulas to Excel files.",
            "parameters": {
                "type": "object",
                "properties": {
                   "file_path": {
                        "type": "string",
                        "description": "The path to the Excel file to read. This should be a valid file path on the server where the model is running."
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "The name of the sheet in the Excel file to modify."
                    },
                    "column_letter": {
                        "type": "string",
                        "description": "The letter of the column to which the formula will be applied (e.g., 'A', 'B', etc.)."
                    },
                    "formula_template": {
                        "type": "string",
                        "description": "The formula template to apply. Use {row} to refer to the current row number. Example: '=SUM(A{row}:B{row})' will sum the values in columns A and B for each row."
                    },
                    "start_row": {
                        "type": "integer",
                        "description": "The starting row number for applying the formula."
                    },
                    "end_row": {
                        "type": "integer",
                        "description": "The ending row number for applying the formula. If not provided, the formula will be applied to all rows starting from start_row to the last row with data."
                    }

                },
                "additionalProperties": False,
                "required": [
                    "file_path",
                    "sheet_name",
                    "column_letter",
                    "formula_template",
                    "start_row",
                    "end_row"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_to_cell",
            "description": "Writes a value to a specific cell in an Excel file. Use this to modify specific cells in Excel files. Example: Adding a title to a column, adding a titile to total below,  etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the Excel file to modify. This should be a valid file path on the server where the model is running."
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "The name of the sheet in the Excel file to modify."
                    },
                    "column": {
                        "type": "string",
                        "description": "The letter of the column where the value will be written (e.g., 'A', 'B', etc.)."
                    },
                    "row": {
                        "type": "integer",
                        "description": "The row number where the value will be written."
                    },
                    "value": {
                        "type": "string",
                        "description": "The value to write to the specified cell."
                    }
                },
                "additionalProperties": False,
                "required": [
                    "file_path",
                    "sheet_name",
                    "column",
                    "row",
                    "value"
                ]
            }
        }
    }, 
    {
        "type": "function",
        "function": {
            "name": "create_new_sheet",
            "description": "Creates a new sheet in an Excel file. Use this to add new sheets to Excel files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the Excel file to modify. This should be a valid file path on the server where the model is running."
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "The name of the new sheet to create."
                    }
                },
                "additionalProperties": False,
                "required": [
                    "file_path",
                    "sheet_name"
                ]
            }
        }
    }

]


def chat_with_nutrition_bot(message, history):
    messages = [SYSTEM_PROMPT]
    file_path_to_return = None
    file_name_to_return = None


    # Update previous messages
    for msg in history:
        if msg["role"] == "user":
            messages.append({"role": "user", "content": msg["content"]})
        elif msg["role"] == "assistant":
            messages.append({"role": "assistant", "content": msg["content"]})
    
    # Append current message
    messages.append({"role": "user", "content": message})
    bot_response = ""


    max_iterations = 20
    iteration = 0

    tool_processed = False

    file_path = None

    while iteration < max_iterations and not tool_processed:
        iteration += 1
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
            tools=tools,
            temperature=0.7,
            top_p=1
        )

        # Handle Tool calls
        if response.choices[0].message.tool_calls:
            # Add assistant message with tool calls
            messages.append(response.choices[0].message)
            
            # yield "🔧 Processing tools..."
            # Process each tool
            # print("Tool calls detected:" + str(response.choices[0].message.tool_calls))
            for i, tool_call in enumerate(response.choices[0].message.tool_calls):
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)


                # yield f"🔧 Calling {function_name} ({i+1}/{len(response.choices[0].message.tool_calls)})..."

                print(f"Tool call: {function_name} with args: {function_args}")
                result = None

                if function_name == "get_nutrition_info":
                    result = get_nutrition_info(function_args["food_name"])   

                elif function_name == "read_file":
                    result = read_file(function_args["file_path"])

                elif function_name == "create_file":
                    result = create_file(function_args["file_name"], function_args["content"], function_args["extension"])
                    file_path_to_return = result
                    file_name_to_return = f"{function_args['file_name']}{function_args['extension']}"
                    logging.info(f"File path to return: {file_path_to_return}")
                    result = json.dumps({"message": "File created successfully", "file_path": result})
                elif function_name == "get_weather_data":
                    result = get_weather_data(function_args["location"])
                    if result is None:
                        result = json.dumps({"error": "Weather data not found for the specified location."})
                    else:
                        result = json.dumps(result)
                
                elif function_name == "create_excel_file":
                    result = create_excel_file(function_args["file_name"])
                    file_path = result
                    file_path_to_return = result
                    file_name_to_return = f"{function_args['file_name']}.xlsx"
                    result = json.dumps({"message": "Excel File created successfully", "file_path": result})
                elif function_name == "read_excel_file":
                    result = read_excel_file(function_args["file_path"])
                
                elif function_name == "add_formula_to_excel":
                    result, file_path = add_formula_to_excel(
                        file_path if file_path else function_args["file_path"],
                        function_args["sheet_name"],
                        function_args["column_letter"],
                        function_args["formula_template"],
                        function_args["start_row"],
                        function_args["end_row"],
                    )

                    file_path_to_return= file_path
                    file_name_to_return = os.path.basename(file_path) if file_path else None
                
                elif function_name == "write_to_cell":
                    result, file_path = write_to_cell(
                        file_path if file_path else function_args["file_path"],
                        function_args["sheet_name"],
                        function_args["column"],
                        function_args["row"],
                        function_args["value"]
                    )
                    file_path_to_return= file_path
                    file_name_to_return = os.path.basename(file_path) if file_path else None
                
                elif function_name == "create_new_sheet":
                    result, file_path = create_new_sheet(
                        file_path if file_path else function_args["file_path"],
                        function_args["sheet_name"]
                    )
                    file_path_to_return= file_path
                    file_name_to_return = os.path.basename(file_path) if file_path else None
                
                messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result if result else json.dumps({"error": "Function returned no result"})
                    })

            continue
        else:
            print("break: ", iteration)
            tool_processed = True
            break

    # Make streaming call for final response
    final_response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        temperature=0.7,
        top_p=1,
        stream=False  # Enable streaming
    )

    bot_response = final_response.choices[0].message.content

    # if file_path_to_return:
        # bot_response += f"\n\nFile created at: (/file={file_path_to_return})"

    if iteration >= max_iterations:
        bot_response += "\n\n⚠️ Warning: Maximum iterations reached. The response may be incomplete."

    file_info = None
    if file_path_to_return:
        file_info = {
            "path": file_path_to_return,
            "name": file_name_to_return,
        }

    return bot_response, file_info



# def clear_history():
#     return []


# with gr.Blocks(title="Nutrition Expert Bot", theme=gr.themes.Soft()) as demo:
#     gr.Markdown(
#         """
#         # Nutrition Expert Bot
        
#         Ask me about nutrition facts, macros, diet recommendations, and more!
#         I can look up nutritional information for specific foods and provide dietary advice.
        
#         **Examples:**
#         - "What are the macros in chicken breast?"
#         - "Give me some keto-friendly meal ideas"
#         - "How much protein is in 100g of salmon?"
#         - "What foods are good for bulking?"
#         """
#     )

#     # File upload tool
#     # download_file = gr.File(label="Download Generated File", interactive=False)

#     chatbot = gr.Chatbot(
#         value=[],
#         height=800,
#         type="messages"
#     )
    

#     with gr.Row():
#         msg = gr.Textbox(
#             placeholder="Ask me about nutrition, macros, or diet reccomendations...",
#             container=False,
#             scale=7,
#             label="Your Question"
#         )

#         submit_btn = gr.Button("Send", scale=1, variant="primary")

#     with gr.Row():
#         clear_btn = gr.Button("Clear History", variant="secondary")
    
#     file_upload = gr.File(
#         label="Upload a file (e.g., food log, meal plan, or nutrition data)",
#         file_count="single",
#         type="filepath"
#     )
    
    

#     def respond(message, chat_history, file_path):
#         if not message.strip():
#             yield "", chat_history, None
#             return
#         # If a file is uploaded, you can process it here (e.g., parse nutrition data)
#         enhanced_message = message
#         if file_path:
#             print(f"File uploaded: {file_path}")
#             enhanced_message = f"{message}. There is an uploaded file at path: {file_path}. Please read this file first."
        
#         chat_history.append({"role": "user", "content": enhanced_message})
        
#         file_to_download = None
#         bot_message = ""


#         for response_chunk in chat_with_nutrition_bot(enhanced_message, chat_history):
#             bot_message = response_chunk

#             current_history = chat_history + [{"role": "assistant", "content": bot_message}]
#             yield "", current_history, None
        
        
#         chat_history.append({"role": "assistant", "content": bot_message})
#         # Return None for file_upload to clear it
#         print(chat_history)
#         yield "", chat_history, None


#     # Submit on button click
#     submit_btn.click(
#         respond,
#         inputs=[msg, chatbot, file_upload],
#         outputs=[msg, chatbot, file_upload],
#         queue=True
#     )

#     # Submit on Enter key
#     msg.submit(
#         respond,
#         inputs=[msg, chatbot, file_upload],
#         outputs=[msg, chatbot, file_upload],
#         queue=True
#     )

#     # Clear history
#     clear_btn.click(
#         lambda: [],
#         outputs=[chatbot],
#         queue=False
#     )



# # Launch the app
# if __name__ == "__main__":
#     print(tempfile.gettempdir())
#     demo.launch(
#         share=True,  # Set to True if you want a public link
#         server_name="127.0.0.1",
#         server_port=7860,
#         show_error=True,
#         debug=True,
#         allowed_paths=[tempfile.gettempdir()]
#     )


# response_format = {
#     "type": "text"
# }

# while True:
#     response = client.chat.completions.create(
#         messages = messages,
#         model = "gpt-4o-mini",
#         tools = tools,
#         response_format = response_format,
#         temperature = 1,
#         top_p = 1,
#     )

#     if response.choices[0].message.tool_calls:
#         print(response.choices[0].message.tool_calls)
#         messages.append(response.choices[0].message)
#         for tool_call in response.choices[0].message.tool_calls:
#             function_name = tool_call.function.name
#             function_args = json.loads(tool_call.function.arguments)
#             result = ""

#             if  function_name == "get_nutrition_info":
#                 result = get_nutrition_info(function_args["food_name"])

#             messages.append({
#                 "role": "tool",
#                 "tool_call_id": tool_call.id,
#                 "content": result,
#             })
#     else:
#         print("[Model Response] " + response.choices[0].message.content)
#         user_input = input("\nYour question: ")
#         if user_input.lower() in ['quit', 'exit', 'bye']:
#             break
#         messages.append({
#             "role": "user",
#             "content": user_input
#         })
