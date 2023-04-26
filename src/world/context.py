from uuid import UUID

from pydantic import BaseModel

from ..event.base import EventsManager


class WorldData(BaseModel):
    id: str
    name: str
    current_step: int


class WorldContext(BaseModel):
    world: WorldData
    agents: list[dict]
    locations: list[dict]
    events_manager: EventsManager

    def __init__(
        self,
        agents: dict,
        locations: dict,
        world: WorldData,
    ):
        events_manager = EventsManager(
            current_step=world.current_step, world_id=world.id
        )
        # convert all UUIDs to strings
        for agent in agents:
            agent["id"] = str(agent["id"])
            agent["location_id"] = str(agent["location_id"])

        return super().__init__(
            agents=agents,
            locations=locations,
            world=world,
            events_manager=events_manager,
        )

    def location_context_string(self, agent_id: UUID | str):
        if isinstance(agent_id, UUID):
            agent_id = str(agent_id)

        # get agent
        agent = [agent for agent in self.agents if agent["id"] == agent_id][0]

        # get other agents in this location
        other_agents = [
            a
            for a in self.agents
            if a["location_id"] == agent["location_id"] and a["id"] != agent_id
        ]

        location = [
            loc for loc in self.locations if str(loc["id"]) == str(agent["location_id"])
        ][0]

        return (
            "Current Location: \n"
            + f"{location['name']}: {location['description']}"
            + "\n\nAgents in this location, with whom you can speak: \n- "
            + "- ".join(
                [
                    f"{agent['full_name']}: {agent['public_bio']}\n"
                    for agent in other_agents
                ]
            )
        )

    def get_location_name(self, location_id: UUID | str):
        if isinstance(location_id, UUID):
            location_id = str(location_id)

        # get location
        location = [
            location
            for location in self.locations
            if str(location["id"]) == str(location_id)
        ][0]

        return location["name"]

    def get_channel_id(self, location_id: UUID | str):
        if isinstance(location_id, UUID):
            location_id = str(location_id)

        # get location
        location = [
            location for location in self.locations if location["id"] == location_id
        ][0]

        return location["channel_id"]

    def get_agent_location_id(self, agent_id: UUID | str):
        if isinstance(agent_id, UUID):
            agent_id = str(agent_id)

        # get agent
        agent = [agent for agent in self.agents if agent["id"] == agent_id][0]

        return agent["location_id"]

    def get_agent_full_name(self, agent_id: UUID | str) -> str:
        if isinstance(agent_id, UUID):
            agent_id = str(agent_id)

        # get agent
        agent = [agent for agent in self.agents if agent["id"] == agent_id][0]

        return agent["full_name"]

    def update_agent(self, agent: dict):
        new_agents = [a for a in self.agents if str(a["id"]) != str(agent["id"])]
        agent["location_id"] = str(agent["location_id"])
        new_agents.append(agent)
        self.agents = new_agents

    def update_step(self, step: int):
        self.world.current_step = step