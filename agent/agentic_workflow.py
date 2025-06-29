from utils.model_loader import ModelLoader
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from prompt_library.prompt import SYSTEM_PROMPT

class GraphBuilder:
    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()

        self.tools = []

        self.weather_tools = WeatherInfoTool()

        self.tools.extend([* self.weather_tools.weather_tool_list])

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None

        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        # response = self.llm.invoke(input_question) # without tool bind it works directly.
        return {"messages": [response]}


    def build_graph(self):
        """
        Build a graph based on the input data using the loaded LLM.
        This is a placeholder for the actual graph building logic.
        """
        graph_builder = StateGraph(MessagesState)

        # create nodes
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        # create edges and conditions
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition) 
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    
    def __call__(self, *args, **kwds):
        return self.build_graph()

        

