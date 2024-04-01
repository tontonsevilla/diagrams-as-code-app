from diagrams import Cluster, Diagram
from diagrams.azure.general import Managementgroups
from diagrams.azure.general import Subscriptions
from diagrams.azure.identity import ActiveDirectory
 
with Diagram("Azure Tenant Design", show=False, direction="TB"):
    tenant = ActiveDirectory("Tenant AD")  
    topGroup = Managementgroups("Main\r\nManagement Group")
    sandbox = Subscriptions("Sandbox\r\nSubscription")
 
    with Cluster("Business Units"):
        with Cluster("Unit1"):
          mainGroup = Managementgroups("Unit1\r\nManagement Group")
          topGroup >> mainGroup
          with Cluster("Project1"):
            group = Managementgroups("Project1\r\nManagement Group")
            sub = [Subscriptions("Project1\r\nDev/Test\r\nSubscription"), Subscriptions("Project1\r\nProduction\r\nSubscription")]
            group - sub
            mainGroup >> group
 
          with Cluster("Project2"):
            group = Managementgroups("Project2\r\nManagement Group")
            sub = [Subscriptions("Project2\r\nDev/Test\r\nSubscription"), Subscriptions("Project2\r\nProduction\r\nSubscription")]
            group - sub
            mainGroup >> group
 
        with Cluster("Infrastructure"):
          group = Managementgroups("Infrastructure\r\nManagement Group")
          sub = [Subscriptions("Test\r\nSubscription"), Subscriptions("Infrastructure\r\nProduction\r\nSubscription")]
          group - sub
          topGroup >> group
 
    tenant >> topGroup >> sandbox