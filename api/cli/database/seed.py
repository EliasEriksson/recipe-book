from api import schemas
from api.database import Database


async def seed_database() -> None:
    async with Database() as client:
        # Languages
        english = await client.languages.create(
            schemas.language.LanguageCreatable("en")
        )

        # Units
        gram = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Gram", "g")
        )
        hectogram = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Hectogram", "hg")
        )
        kilo = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Kilograms", "kg")
        )
        liter = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Liter", "l")
        )
        deciliter = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Deciliter", "dl")
        )
        centiliter = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Centiliter", "cl")
        )
        milliliter = await client.units.create(
            schemas.unit.UnitCreatable(english.language.id, "Milliliter", "ml")
        )

        # Ingredients
        sugar = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Sugar")
        )
        water = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Water")
        )
        lime_juice = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Lime juice")
        )
        light_rum = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Light rum")
        )
        ice = await client.ingredients.create(
            schemas.ingredient.IngredientCreatable(english.language.id, "Ice")
        )

        # Recipes
        daiquiri = await client.recipes.create(
            schemas.recipe.RecipeCreatable(english.language.id, "Daiquiri")
        )
