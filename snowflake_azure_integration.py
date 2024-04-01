from diagrams import Cluster, Diagram, Edge
import diagrams.azure.database as azDb
import diagrams.azure.web as web
from diagrams.custom import Custom
import diagrams.saas.analytics

diagram_graph_attr = {
    "fontsize": "45",
    "bgcolor": "white",
    "splines": "spline"
}

cluster_grapth_attr = {
    "fontsize": "25"
}

with Diagram("Snowflake and Azure Integration", direction="TB", show=False, graph_attr=diagram_graph_attr):
    with Cluster("Snowflake", graph_attr=cluster_grapth_attr) as sfCluster:
        dwDatabase = azDb.SQLDatawarehouse("DW Database")
        loadStagingToRawTask = Custom("Task \n Load Staging \n to \n Raw Table", "resources\\task_icon.png")
        loadRawToCleanTask = Custom("Task \n Load Raw \n to \n Clean Dynamic Table", "resources\\task_icon.png")
        loadCleanToConsumptionTask = Custom("Task \n Load Clean \n to \n Consumption \n Dynamic Table", "resources\\task_icon.png")
        sfBlobStorage = azDb.BlobStorage("CSV Storage")
        sfPipe = Custom("Snowpipe \n Integraion to Azure", "resources\\snowpipe.png")

        with Cluster("Schemas", graph_attr=cluster_grapth_attr):
            schemaRaw = Custom("Raw", "resources\\schema_icon.png")
            schemaClean = Custom("Clean", "resources\\schema_icon.png")
            schemaConsumption = Custom("Consumption", "resources\\schema_icon.png")
            schemas = [schemaRaw, schemaClean, schemaConsumption]

        dwDatabase << schemas
        schemaRaw << loadStagingToRawTask
        schemaRaw << Edge() >> loadRawToCleanTask >> schemaClean
        schemaClean >> Edge() << loadCleanToConsumptionTask >> schemaConsumption
        loadStagingToRawTask << Edge() >> sfBlobStorage << sfPipe

    with Cluster("Azure", graph_attr=cluster_grapth_attr) as azCluster:
        azSqlDatabase = azDb.SQLDatabases("OLTP Database")
        azDataFoctory = azDb.DataFactory("Azure Data factory")
        azTriggerEvent = Custom("Event Trigger \n to Execute \n Data Factory Pipeline", "resources\\azure_trigger.png")
        azBlobStorage = azDb.BlobStorage("CSV Storage")
        azQueueNotifcation = web.NotificationHubNamespaces("Queue Notification \n to Snowpipe")

        azSqlDatabase << Edge(label="Fetch start on trigger") >> azDataFoctory << azTriggerEvent
        azDataFoctory >> Edge(label="Save newly created CSV") << azBlobStorage      
        azBlobStorage << Edge(label="Check if has new created file") >> azQueueNotifcation

        azQueueNotifcation >> sfPipe
        azBlobStorage >> \
            Edge(label="Fetch once notified by Azure") << sfPipe
