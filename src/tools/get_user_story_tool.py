import os
from dotenv import load_dotenv
load_dotenv()
from langchain.tools import Tool
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.work_item_tracking.models import Wiql
organization_url = os.getenv('AZURE_ORG_URL', 'https://dev.azure.com/yourorg')
personal_access_token = os.getenv('AZURE_DEVOPS_PERSONAL_ACCESS_TOKEN', 'your-pat-token')
project_name = os.getenv('PROJECT_NAME', 'YourProject')

class AzureDevOpsConnector:
    """Connect to Azure DevOps and retrieve user stories"""
    
    def __init__(self, organization_url, personal_access_token, project_name):
        """
        Initialize Azure DevOps connection
        
        Args:
            organization_url: Azure DevOps organization URL (e.g., 'https://dev.azure.com/yourorg')
            personal_access_token: Personal Access Token for authentication
            project_name: Name of the Azure DevOps project
        """
        self.organization_url = organization_url
        self.project_name = project_name
        
        # Create authentication credentials
        credentials = BasicAuthentication('', personal_access_token)
        self.connection = Connection(base_url=organization_url, creds=credentials)
        
        # Get work item tracking client
        self.wit_client = self.connection.clients.get_work_item_tracking_client()
    
    def get_work_items(self, work_item_types=['User Story', 'Task', 'Epic'], max_results=50):
        """
        Retrieve work items from Azure DevOps
        
        Args:
            work_item_types: List of work item types to retrieve (default: User Story, Task, Epic)
            max_results: Maximum number of work items to retrieve
            
        Returns:
            List of work item dictionaries
        """
        # Build the work item type filter
        type_filter = " OR ".join([f"[System.WorkItemType] = '{wit}'" for wit in work_item_types])
        
        # WIQL query to get work items
        wiql_query = f"""
        SELECT [System.Id], [System.Title], [System.State], 
               [System.AssignedTo], [System.Description], [System.Tags], [System.WorkItemType]
        FROM WorkItems
        WHERE [System.TeamProject] = '{self.project_name}'
        AND ({type_filter})
        ORDER BY [System.CreatedDate] DESC
        """
        
        # Execute query
        wiql = Wiql(query=wiql_query)
        query_results = self.wit_client.query_by_wiql(wiql, top=max_results).work_items
        
        if not query_results:
            return []
        
        # Get full work item details
        work_item_ids = [item.id for item in query_results]
        work_items = self.wit_client.get_work_items(
            ids=work_item_ids,
            expand='All'
        )
        
        # Format work items
        work_items_list = []
        for item in work_items:
            fields = item.fields
            work_items_list.append({
                'id': item.id,
                'type': fields.get('System.WorkItemType', ''),
                'title': fields.get('System.Title', ''),
                'state': fields.get('System.State', ''),
                'assigned_to': fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned'),
                'description': fields.get('System.Description', ''),
                'tags': fields.get('System.Tags', ''),
                'created_date': str(fields.get('System.CreatedDate', '')),
                'url': item.url
            })
        
        return work_items_list


def create_work_items_tool():
    """
    Create a LangChain tool for retrieving Azure DevOps work items (User Stories, Tasks, Epics)
    
    Args:
        organization_url: Azure DevOps organization URL
        personal_access_token: Personal Access Token
        project_name: Project name
        
    Returns:
        LangChain Tool object
    """
    connector = AzureDevOpsConnector(
        organization_url=organization_url,
        personal_access_token=personal_access_token,
        project_name=project_name
    )
    
    def get_work_items_func(query: str = "") -> str:
        """Get work items (User Stories, Tasks, Epics) from Azure DevOps"""
        try:
            items = connector.get_work_items(work_item_types=['User Story', 'Task', 'Epic'], max_results=50)
            if not items:
                return "No work items found."
            
            # Group by type for better readability
            grouped_items = {}
            for item in items:
                item_type = item['type']
                if item_type not in grouped_items:
                    grouped_items[item_type] = []
                grouped_items[item_type].append(item)
            
            result = f"Found {len(items)} work items:\n\n"
            
            for item_type, items_of_type in grouped_items.items():
                result += f"=== {item_type}s ({len(items_of_type)}) ===\n\n"
                for item in items_of_type:
                    result += f"ID: {item['id']}\n"
                    result += f"Title: {item['title']}\n"
                    result += f"State: {item['state']}\n"
                    result += f"Assigned To: {item['assigned_to']}\n"
                    result += f"Created: {item['created_date']}\n"
                    if item['tags']:
                        result += f"Tags: {item['tags']}\n"
                    result += f"URL: {item['url']}\n"
                    result += "---\n"
                    result += f"{item['description']}\n"
                result += "\n"
            
            return result
        except Exception as e:
            return f"Error retrieving work items: {str(e)}"
    
    tool = Tool(
        name="GetAzureDevOpsWorkItems",
        func=get_work_items_func,
        description="Retrieves work items (User Stories, Tasks, and Epics) from Azure DevOps. Returns ID, type, title, state, assignee, and other details."
    )
    
    return tool

# def main():
#     """Example usage"""
    
#     # Create the tool
#     user_story_tool = create_work_items_tool()
    
#     # Use the tool
#     print("=== Fetching User Stories ===\n")
#     result = user_story_tool.run("")
#     print(result)


# if __name__ == "__main__":
#     main()