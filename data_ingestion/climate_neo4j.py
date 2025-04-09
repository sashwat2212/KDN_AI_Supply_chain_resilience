from py2neo import Graph, Node, Relationship
import json

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "Sashwat@22"))

# Load JSON data
with open("/Users/kdn_aisashwat/Desktop/supply_chain_resillience/satellite_data/climate_risk_data.json", "r") as file:
    data = json.load(file)

timestamp = data["timestamp"]
event_node = Node("Event", timestamp=timestamp)
graph.merge(event_node, "Event", "timestamp")

for climate_entry in data["nasa_climate_data"]:
    bbox = climate_entry["bbox"]
    source = climate_entry["source"]
    geometry = climate_entry["climate_data"]["geometry"]
    properties = climate_entry["climate_data"]["properties"]["parameter"]

    # Extract coordinates
    lon, lat = geometry["coordinates"][:2]

    # Ensure Location Node exists
    location_query = """
    MERGE (l:Location {longitude: $longitude, latitude: $latitude})
    ON CREATE SET l.bbox = $bbox
    RETURN l
    """
    graph.run(location_query, longitude=lon, latitude=lat, bbox=str(bbox))

    # Create ClimateRecord Node
    climate_node = Node(
        "ClimateRecord",
        source=source,
        WS10M=str(properties.get("WS10M", {})),
        RH2M=str(properties.get("RH2M", {})),
        T2M=str(properties.get("T2M", {})),
        PRECTOTCORR=str(properties.get("PRECTOTCORR", {}))
    )
    graph.create(climate_node)

    # Create Relationships
    graph.create(Relationship(event_node, "HAS_DATA", climate_node))

    # Relationship between ClimateRecord and Location
    location_match_query = """
    MATCH (l:Location {longitude: $longitude, latitude: $latitude})
    RETURN l
    """
    location_result = graph.run(location_match_query, longitude=lon, latitude=lat).evaluate()

    if location_result:
        graph.create(Relationship(climate_node, "LOCATED_AT", location_result))

print("Data ingestion completed successfully!")
