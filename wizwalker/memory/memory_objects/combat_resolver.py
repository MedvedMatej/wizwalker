from typing import List

from wizwalker.memory.memory_object import PropertyClass, DynamicMemoryObject
from .spell_effect import DynamicSpellEffect


class CombatResolver(PropertyClass):
    async def read_base_address(self) -> int:
        raise NotImplementedError()

    async def bool_global_effect(self) -> bool:
        return await self.read_value_from_offset(112, "bool")

    async def write_bool_global_effect(self, bool_global_effect: bool):
        await self.write_value_to_offset(112, bool_global_effect, "bool")

    async def global_effect(self) -> DynamicSpellEffect:
        addr = await self.read_value_from_offset(120, "long long")
        return DynamicSpellEffect(self.hook_handler, addr)

    # async def write_global_effect(self, global_effect: class SharedPointer<class SpellEffect>):
    #     await self.write_value_to_offset(120, global_effect, "class SharedPointer<class SpellEffect>")

    async def battlefield_effects(self) -> List[DynamicSpellEffect]:
        effects = []
        for addr in await self.read_shared_vector(136):
            effects.append(DynamicSpellEffect(self.hook_handler, addr))

        return effects

    # async def write_battlefield_effects(self, battlefield_effects: class SharedPointer<class SpellEffect>):
    #     await self.write_value_to_offset(136, battlefield_effects, "class SharedPointer<class SpellEffect>")


class DynamicCombatResolver(DynamicMemoryObject, CombatResolver):
    pass
